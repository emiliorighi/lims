from io import StringIO
import csv


def generate_tsv_reader(report):
    report_data = StringIO(report.read().decode('utf-8'))
    lines = report_data.readlines()
    # Return each line as a string, removing any trailing newlines
    return [line.strip().split('\t') for line in lines]

def generate_tsv_dict_reader(report):
    tsv_data = StringIO(report.read().decode('utf-8'))
    tsvreader = csv.DictReader(tsv_data, delimiter='\t')
    return tsvreader

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

def get_nested_value(dictionary, keys):
    keys_list = keys.split('.')
    value = dictionary
    try:
        for key in keys_list:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return None
    
