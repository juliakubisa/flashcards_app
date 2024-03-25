import csv

csv_lines = []


def allowed_file_extension(filename):
    allowed_extensions = {'csv'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def clean_csv(csv_file):
    with open(csv_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if " - " in line:
                line_to_write = []
                line_to_write.append(line.strip().replace("'", ''))
                csv_lines.append(line_to_write)
            else:
                pass
    return csv_lines


def write_csv(data):
    with open('example_csv2.csv', 'w') as f:
        csvwriter = csv.writer(f, delimiter="-")
        csvwriter.writerows(data)


def max_dict_value_len(length, key, d):
    value = d[key]
    max_length = len(value)
    return max_length <= length
