from errors import NotFound

def return_document_by_id(model, query):
    query_set = model.objects(**query).exclude('id','created','valid')
    if not query_set.first():
        raise NotFound
    return query_set.as_pymongo()[0]


def delete_document(model, query):
    document = model.objects(**query).first()
    if not document:
        raise NotFound
    
def get_document(model, query, fields_to_exclude=None):
    query_set = model.objects(**query)
    if not query_set.first():
        raise NotFound
    if fields_to_exclude:
        query_set = query_set.exclude(*fields_to_exclude)
    return query_set.as_pymongo()[0]