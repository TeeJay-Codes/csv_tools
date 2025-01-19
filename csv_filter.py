import csv
import re
import sys
import os

def convert_to_regex(pattern_description):
    # Convert plain text description to regex pattern
    # Example: "123__1234" -> r'^\d{3}__\d{4}$'
    regex_pattern = re.sub(r'\d+', lambda x: r'\d{' + str(len(x.group())) + '}', pattern_description)
    return f'^{regex_pattern}$'

def filter_csv(input_file, column_name, pattern_description):
    if not os.path.isfile(input_file):
        print(f"Error: The file {input_file} does not exist.")
        sys.exit(1)

    # pattern = convert_to_regex(pattern_description)
    pattern = r'^\d{5}_\d{10}$'

    with open(input_file, mode='r', newline='') as infile:
        reader = csv.DictReader(infile)
        filtered_rows = [row for row in reader if re.match(pattern, row[column_name])]
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, 'filtered.csv')

    with open(output_file, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)
    
    print(f"{len(filtered_rows)} lines written into filtered.csv")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python csv_filter.py <input_file> <column_name> <pattern_description>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    column_name = sys.argv[2]
    pattern_description = sys.argv[3]
    
    filter_csv(input_file, column_name, pattern_description)