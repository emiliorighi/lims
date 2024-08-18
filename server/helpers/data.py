import csv
from io import StringIO
from bson.json_util import dumps, JSONOptions, DatetimeRepresentation
from mongoengine.queryset.visitor import Q
from . import filter

def dump_json(response_dict):
    json_options = JSONOptions()
    json_options.datetime_representation = DatetimeRepresentation.ISO8601
    return dumps(response_dict, indent=4, sort_keys=True, json_options=json_options)

def create_tsv(items, fields):
    writer_file = StringIO()
    tsv = csv.writer(writer_file, delimiter='\t')
    header = []
    for f in fields:
        if 'metadata.' in f:
            header.append(f.split('.')[1])
        else:
            header.append(f)
    tsv.writerow(header)
    for item in items:
        new_row = []

        for k in fields:
            if 'metadata.' in k:
                value = get_nested_value(item, k)
            else:
                value = item.get(k)

            if type(value) is list:
                value = ', '.join(value)

            new_row.append(value)
        tsv.writerow(new_row)
    return writer_file.getvalue()

def get_pagination(args):
    return int(args.get('limit', 10)),  int(args.get('offset', 0))

def get_sort(args):
    return args.get('sort_column'), args.get('sort_order', 'desc')

def get_items(args, model, fieldToExclude, q_query, tsv_fields, project_id=None):
    mimetype = "application/json"
    ##parse args
    format = args.get('format', 'json')
    limit, offset = get_pagination(args)     
    sort_column, sort_order = get_sort(args)
    query, q_query =create_query(args, q_query)
    if project_id:
        query['project'] = project_id
    items = model.objects(**query).exclude(*fieldToExclude)

    if q_query:
        items = items.filter(q_query)

    if sort_column:
        sort =f"-metadata.{sort_column}" if sort_order == 'desc' else  f"metadata.{sort_column}"
        items = items.order_by(sort)

    total = items.count()
    if format == 'tsv':
        assemblies = create_tsv(items.as_pymongo(), tsv_fields).encode('utf-8')
        mimetype="text/tab-separated-values"
        return assemblies, mimetype, 200

    response = dict(total=total, data=list(items.skip(offset).limit(limit).as_pymongo()))
    return dump_json(response), mimetype, 200

def create_query(args, q_query):
    query={}
    
    for k, v in args.items():

        if not v:
            continue

            #TODO: add multi select field query

        if "__gte" in k or "__lte" in k:
            if filter.validate_number(v):
                query_visitor = {f"metadata__{k.replace('.', '__')}":float(v)}
            q_query = Q(**query_visitor) & q_query if q_query else Q(**query_visitor)
        elif k in ("limit", "offset", "sort_order", "sort_column", "filter", "format", "fields[]"):
            continue
        else:
            query[f"metadata__{k.replace('.', '__')}"] = v
    return query, q_query

def get_nested_value(dictionary, keys):
    keys_list = keys.split('.')
    value = dictionary
    try:
        for key in keys_list:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return None
    