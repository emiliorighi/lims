from db.models import Sample,Project
from errors import NotFound
from datetime import datetime
from mongoengine.queryset.visitor import Q


def get_samples(offset=0,limit=20,
                    filter=None,
                    start_date=None, end_date=datetime.utcnow,
                    sort_column=None, sort_order=None):
    if filter:
        projects= Sample.objects((Q(name__icontains=filter) | Q(name__iexact=filter))).exclude('id','created')
    else:
        filter_query = None
    if start_date:
        date_query = (Q(metadata__collection_date__gte=start_date) & Q(metadata__collection_date__lte=end_date))
    else:
        date_query = None
    if filter_query and date_query:
        samples = BioSample.objects(filter_query & date_query).exclude('id','created')
    elif filter_query:
        samples = BioSample.objects(filter_query).exclude('id','created')
    elif date_query:
        samples = BioSample.objects(date_query).exclude('id','created')
    else:
        samples = BioSample.objects().exclude('id','created')
    if sort_column:
        if sort_column == 'collection_date':
            sort_column = 'metadata.collection_date'
        sort = '-'+sort_column if sort_order == 'desc' else sort_column
        samples = samples.order_by(sort)
    return samples.count(), samples[int(offset):int(offset)+int(limit)]


def get_samples(project_id, offset=0,limit=20,
                    filter=None,filter_field=None,
                    start_date=None, end_date=datetime.utcnow,
                    sort_column=None, sort_order=None):
    project = Project.objects(project_id=project_id).first()
    if not project:
        raise NotFound
    samples = Sample.objects(project=project_id)
    filter_query = None
    if filter_field and filter:
        key = f"{filter_query}__icontains"
        query = dict()
        query[key]=filter
        filter_query = (Q(query))
    date_query = None
    if start_date:
        date_query = (Q(created__gte=start_date) & Q(created__lte=end_date))
    if filter_query and date_query:
        samples = samples.filter(filter_query & date_query)
    elif filter_query:
        samples = samples.filter(filter_query)
    elif date_query:
        samples = samples.filter(date_query)
    samples = samples.exclude('id', 'created')
    if sort_column:
        sort = '-'+sort_column if sort_order == 'desc' else sort_column
        samples = samples.order_by(sort)
    return samples.count(), samples[int(offset):int(offset)+int(limit)]

def get_sample(id):
    samples = Sample.objects(sample_id=id).exclude('id','created')
    if not samples.first():
        raise NotFound
    return samples.as_pymongo()[0]
    

def create_sample(project_id, data):
    project = Project.objects(project_id=project_id).first()
    if not project:
        raise NotFound
    samples = Sample.objects(project=project_id)
    required_fields = [f for f in project.sample['fields'] if f['required']]
    id_fields = project.sample['id_fields']
    sample_id = [attr for attr in data.keys() if attr in id_fields].join('_')
    if sample_id:
        sample = samples.filter(sample_id=sample_id).first()
    # VALIDATION STEPS:
    # 1) VALIDATE ID
    # 2) VALIDATE REQUIRED FIELDS
    # 3) VALIDATE FIELDS
    # 4) SAVE DOCUMENT
def update_sample(id,data):
    sample = Sample.objects(sample_id=id)
    if not sample.first():
        raise NotFound
    sample.update(**data)
    return f"Sample {id} successfully updated", 201

def delete_sample(id):
    sample = Sample.objects(sample_id=id).first()
    if not sample:
        raise NotFound
    sample.delete()
    return f"Sample {id} successfully deleted",201

def get_filter(filter, option):
    if option == 'taxid':
        return (Q(taxid__iexact=filter) | Q(taxid__icontains=filter))
    elif option == 'habitat':
        return (Q(metadata__habitat__iexact=filter) | Q(metadata__habitat__icontains=filter))
    elif option == 'gal':
        return (Q(metadata__GAL__iexact=filter) | Q(metadata__GAL__icontains=filter))
    elif option == 'accession':
        return (Q(accession__iexact=filter) | Q(accession__icontains=filter))
    else:
        return (Q(scientific_name__iexact=filter) | Q(scientific_name__icontains=filter))

def create_related_biosample(accession):
    biosample_obj = BioSample.objects(accession=accession).first()
    if biosample_obj:
        return biosample_obj
    biosample_response = ena_client.get_sample_from_samples(accession)
    if not biosample_response:
        return
    biosample_obj = create_biosample_from_ebi_data(biosample_response)
    return biosample_obj

def create_biosample_from_accession(accession):
    resp_obj = dict()
    biosample_obj = BioSample.objects(accession=accession).first()
    if biosample_obj:
        resp_obj['message'] = f"{accession} already exists"
        resp_obj['status'] = 400
        return resp_obj
    biosample_response = ena_client.get_sample_from_samples(accession)
    if not biosample_response:
        resp_obj['message'] = f"{accession} not found in INSDC"
        resp_obj['status'] = 400
        return resp_obj
    biosample_obj = create_biosample_from_ebi_data(biosample_response)
    if biosample_obj:
        resp_obj['message'] = f'{biosample_obj.accession} correctly saved'
        resp_obj['status'] = 201
        return resp_obj
    resp_obj['message'] = 'Unhandled error'
    resp_obj['status'] = 500
    return resp_obj

def create_biosample_from_ncbi_data(accession, ncbi_response, organism):
    biosample_obj = BioSample.objects(accession=accession).first()
    if biosample_obj:
        return biosample_obj
    required_metadata = dict(accession=accession,taxid=organism.taxid,scientific_name=organism.scientific_name)
    biosample_metadata = dict()
    ##format to biosample response model
    for attr in ncbi_response['biosample']['attributes']:
        biosample_metadata[attr['name']] = [dict(text=attr['value'])] 
    extra_metadata = parse_sample_metadata(biosample_metadata)
    new_biosample = BioSample(metadata=extra_metadata,**required_metadata).save()
    sample_locations_service.save_coordinates(new_biosample)
    sample_locations_service.update_countries_from_biosample(new_biosample)
    organism.modify(add_to_set__samples=new_biosample.accession)
    organism.save()
    return new_biosample

def create_biosample_from_ebi_data(sample):
    existing_biosample = BioSample.objects(accession=sample['accession']).first()
    if existing_biosample:
        return existing_biosample
    required_metadata=dict(accession=sample['accession'],taxid=str(sample['taxId']))
    organism = organisms_service.get_or_create_organism(required_metadata['taxid'])
    if organism:
        required_metadata['scientific_name'] = organism.scientific_name
    else:
        print(f'Unable to save sample, taxid not found in {sample}')
        return
    extra_metadata = parse_sample_metadata({k:sample['characteristics'][k] for k in sample['characteristics'].keys() if k not in ['taxId','scientificName','accession','organism']})
    new_biosample = BioSample(metadata=extra_metadata,**required_metadata).save()
    sample_locations_service.save_coordinates(new_biosample)
    sample_locations_service.update_countries_from_biosample(new_biosample)
    sample_derived_from = extra_metadata.get('sample derived from', None)
    if sample_derived_from:
        print(f'creating father sample {sample_derived_from}')
        father_biosample = create_related_biosample(sample_derived_from)
        if father_biosample:
            print(f'father sample {father_biosample.accession} created')
            father_biosample.modify(add_to_set__sub_samples=new_biosample.accession)
            organism.modify(add_to_set__samples=sample_derived_from)
    else:
        print(f'appending sample {new_biosample.accession} to {organism.scientific_name}')
        organism.modify(add_to_set__samples=new_biosample.accession)
        organism.save()
    return new_biosample
    

def delete_biosample(accession):
    biosample_to_delete = BioSample.objects(accession=accession).first()
    if not biosample_to_delete:
        raise NotFound
    Assembly.objects((Q(sample_accession=biosample_to_delete.accession) | Q(metadata__sample_accession=biosample_to_delete.accession))).delete()
    Experiment.objects(metadata__sample_accession=biosample_to_delete.accession).delete()
    SampleCoordinates.objects(sample_accession=accession).delete()
    organism = Organism.objects(taxid=biosample_to_delete.taxid).first()
    organism.modify(pull__samples=biosample_to_delete.accession)
    organism.save()
    biosample_to_delete.delete()
    return accession

def parse_sample_metadata(metadata):
    sample_metadata = dict()
    for k in metadata.keys():
        sample_metadata[k] = metadata[k][0]['text']
    return sample_metadata

def map_samples_by_relationship(samples):
    samples_derived_from = {}
    for biosample in samples:
        if biosample.metadata and 'sample derived from' in biosample.metadata.keys():
            parent_accession = biosample.metadata['sample derived from']
            if not parent_accession in samples_derived_from.keys():
                samples_derived_from[parent_accession]=[]
            samples_derived_from[parent_accession].append(biosample)
    return samples_derived_from