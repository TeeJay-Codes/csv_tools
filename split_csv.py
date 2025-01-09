import csv
import os
import argparse

def split_csv(file_path, max_entries):
    # Ensure the file exists
    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return

    # Create the output directory
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.join(os.path.dirname(file_path), base_name)
    os.makedirs(output_dir, exist_ok=True)

    # Open the input CSV file
    with open(file_path, 'r') as input_file:
        reader = csv.reader(input_file)
        header = next(reader)  # Read the header row

        batch_number = 1
        batch_entries = []
        for row in reader:
            batch_entries.append(row)
            if len(batch_entries) == max_entries:
                write_batch(output_dir, batch_number, header, batch_entries)
                batch_number += 1
                batch_entries = []

        # Write the remaining entries if any
        if batch_entries:
            write_batch(output_dir, batch_number, header, batch_entries)

def write_batch(output_dir, batch_number, header, entries):
    # Determine the output file name
    output_file = os.path.join(output_dir, f"batch{batch_number}.csv")

    # Write the batch to a new CSV file
    with open(output_file, 'w', newline='') as output_csv:
        writer = csv.writer(output_csv)
        writer.writerow(header)  # Write the header
        writer.writerows(entries)  # Write the entries

    print(f"Written {len(entries)} entries to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split a CSV file into smaller files.')
    parser.add_argument('file_path', type=str, help='Path to the CSV file to split')
    parser.add_argument('max_entries', type=int, help='Maximum number of entries per split file')

    args = parser.parse_args()
    split_csv(args.file_path, args.max_entries)