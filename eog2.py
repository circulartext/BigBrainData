import csv

def convert_scientific_to_real(number_str):
    try:
        number = float(number_str)
        # Check if the number is in scientific notation
        if 'e' in number_str.lower():
            return '{:.12f}'.format(number)
        else:
            return number_str  # Return unchanged if not in scientific notation
    except ValueError:
        return number_str  # Return unchanged if not convertible to float

def convert_csv_to_real_numbers(input_csv, output_csv):
    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            converted_row = [convert_scientific_to_real(cell) for cell in row]
            writer.writerow(converted_row)

# Example usage:
input_csv = 'y9_10_2one.csv'  # Change this to the name of your input CSV file
output_csv = 'y9_10_2twoa.csv'  # Change this to the name of the output CSV file
convert_csv_to_real_numbers(input_csv, output_csv)
