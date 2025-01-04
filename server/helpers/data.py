from bson.json_util import dumps, JSONOptions, DatetimeRepresentation
from mongoengine.queryset.visitor import Q
from . import filter

def dump_json(response_dict):
    json_options = JSONOptions()
    json_options.datetime_representation = DatetimeRepresentation.ISO8601
    return dumps(response_dict, indent=4, sort_keys=True, json_options=json_options)

def generate_tsv(cursor, fields, batch_size=1000):
    """
    Generates a TSV string from a MongoDB cursor with the specified fields.
    
    Args:
    - cursor: MongoDB cursor object.
    - fields: List of fields to extract from each document.
    - batch_size: Number of rows to yield at once to minimize frequent yielding.
    """

    yield '\t'.join(fields) + '\n'
    
    buffer = []
    for doc in cursor:
        doc_dict = doc.to_mongo().to_dict()
        
        new_row = []

        for k in fields:
            value = doc_dict.get(k, " ")

            if isinstance(value, list):
                value = ', '.join(value)

            new_row.append(value)
        
        buffer.append('\t'.join(map(str, new_row)) + '\n')
        
        # Yield in batches to improve performance
        if len(buffer) >= batch_size:
            yield ''.join(buffer)
            buffer.clear()

    # Yield any remaining rows
    if buffer:
        yield ''.join(buffer)

def get_pagination(args):
    return int(args.get('limit', 10)),  int(args.get('offset', 0))

def get_sort(args):
    return args.get('sort_column'), args.get('sort_order')

def build_query(filters, args, query):
    for f in filters:

        key = f.get('key')
        if not key in args:
            continue
        
        filter_type = f.get('filter')
        value = args.get(key)

        if value == 'No Value':
            value = None

        if filter_type.get('choices') or filter_type.get('min'):
            query &= Q(**{f"{key}" : value})

        else:
            query &= (Q(**{f"{key}__icontains":value}) | Q(**{f"{key}__iexact":value})) 
            print('HERE')
            print(query)

    for key, value in args.items():

        if any(op in key for op in ['__gte', '__lte', '__gt', '__lt']):
            query &= Q(**{f"{key}":value})
            
    return query


def apply_sorting(cursor, sort_column: str, sort_order: str):
    sort = f"-{sort_column}" if sort_order == 'desc' else sort_column
    return cursor.order_by(sort)