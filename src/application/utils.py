import csv
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

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


def test_algorithm():
    # Define the number of rows
    num_rows = 100

    # Generate initial data within specified ranges
    data = {
        'last_answer_correct': np.random.choice([-1, 1], num_rows),
        'number_correct_answers': np.random.randint(0, 11, num_rows),
        'answer_time': np.random.uniform(0.1, 60, num_rows)
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Standardize columns 'number_correct_answers' and 'answer_time'
    scaler = StandardScaler()
    df[['number_correct_answers', 'answer_time']] = scaler.fit_transform(df[['number_correct_answers', 'answer_time']])

    # Print initial DataFrame
    print("Initial DataFrame:")
    print(df.head())

    # Add more rows if needed
    while len(df) < num_rows:
        new_data = {
            'last_answer_correct': np.random.choice([-1, 1]),
            'number_correct_answers': scaler.transform([[np.random.randint(0, 11)]])[0][0],
            'answer_time': scaler.transform([[np.random.uniform(0.1, 60)]])[0][0]
        }
        df = df.append(new_data, ignore_index=True)

    # Print final DataFrame
    print("\nFinal DataFrame:")
    print(df)

    last_answer_correct_weight = 0.5
    number_correct_answers_weight = 0.25
    answer_time_weight = -0.25

    df['easiness'] = (last_answer_correct_weight * df['last_answer_correct']
                      + number_correct_answers_weight * df['number_correct_answers']
                      + answer_time_weight * df['answer_time'])

    print(df['easiness'].min())
