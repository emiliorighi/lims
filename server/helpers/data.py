from bson.json_util import dumps, JSONOptions, DatetimeRepresentation
from mongoengine.queryset.visitor import Q
import csv
from io import StringIO

def dump_json(response_dict):
    json_options = JSONOptions()
    json_options.datetime_representation = DatetimeRepresentation.ISO8601
    return dumps(response_dict, indent=4, sort_keys=True, json_options=json_options)

def project_model_query(project_id, model_name):
    return dict(project_id=project_id,model_name=model_name)

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
    return int(args.pop('limit', 10)),  int(args.pop('offset', 0))

def get_sort(args):
    return args.pop('sort_column',None), args.pop('sort_order',None)

def create_query(args, q_query):
    query = {}

    for key, value in args.items():
        # Skip keys with empty values
        if not value:
            continue
        
        if value == 'false':
            value = False

        if value == 'true':
            value = True

        if value == 'No Entry' or ( '__exists' in key and value == False):
            value = None

        # Handle greater than/less than conditions
        if any(op in key for op in ['__gte', '__lte', '__gt', '__lt', '__size']):
            q_query = add_range_filter(key, value, q_query)

        #handle potential lists
        elif '__in' in key:
            if isinstance(value, str):
                result = [
                    None if part.strip() == "No Entry" else part.strip()
                    for part in value.split(",")
                ] 
            elif isinstance(value, list):
                result = value
            else:
                result = [value]
            query[key] = result
        else:
            query[key] = value

    return query, q_query

def add_range_filter(key, value, q_query):
    """Add range filtering to the query (e.g., __gte and __lte), and attempt to convert the value to a number or date."""
    # Attempt to convert value to a number (int or float)

    if validate_number(value):
        value = float(value.replace(',', '.')) if '.' in value or ',' in value else int(value)
    # Create the filter for the query
    query_visitor = {f"{key}": value}
    if q_query:
        return Q(**query_visitor) & q_query
    return Q(**query_visitor)

def validate_number(number):
    try:
        float(number)
        return True
    except ValueError:
        return False   

def generate_response(format, fields, items, limit, offset):
    if format == 'tsv':
        return create_tsv(items.as_pymongo(), fields).encode('utf-8'), "text/tab-separated-values"
    elif format == 'jsonl':
        return generate_jsonlines(items.as_pymongo()), "application/jsonlines"
    else:
        total = items.count()
        response = dict(total=total, data=list(items.skip(offset).limit(limit).as_pymongo()))
        return dump_json(response), "application/json"

def create_tsv(items, fields):
    writer_file = StringIO()
    tsv = csv.writer(writer_file, delimiter='\t')
    tsv.writerow(fields)
    for item in items:
        new_row = []
        for k in fields:
            new_row.append(item.get(k))
        tsv.writerow(new_row)
    return writer_file.getvalue()

def generate_jsonlines(pymongo_data):
    for item in pymongo_data:
        yield dump_json(item) + "\n"

def apply_sorting(cursor, sort_column: str, sort_order: str):
    sort = f"-{sort_column}" if sort_order == 'desc' else sort_column
    return cursor.order_by(sort)