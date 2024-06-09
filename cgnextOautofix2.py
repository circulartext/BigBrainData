import csv
from collections import Counter
import math

def extract_first_and_exponent(value):
    parts = value.split('e+')
    if len(parts) < 2:
        return None, None
    mantissa = parts[0]
    exponent = 'e+' + parts[1]
    if mantissa[0] == '-':
        first_digits = '-' + mantissa[1:5]  # Changed to [1:6] to include 5 characters
    else:
        first_digits = mantissa[:5]  # Changed to [:6] to include 5 characters
    return first_digits, exponent

def euclidean_distance(pair1, pair2):
    mantissa1, exponent1 = pair1
    mantissa2, exponent2 = pair2
    mantissa_diff = float(mantissa1) - float(mantissa2)
    exponent_diff = float(exponent1[2:]) - float(exponent2[2:])
    return math.sqrt(mantissa_diff ** 2 + exponent_diff ** 2)

def find_matching_pairs_with_times(csv_file, output_file_template, threshold=1000):
    pairs = []
    times = []
    occurrences = {}

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            value = row['EOG Horizontal_Modified']
            time = row['Time']
            first_digits, exponent = extract_first_and_exponent(value)
            if first_digits is not None and exponent is not None:
                pairs.append((first_digits, exponent))
                times.append(time)

    window_sizes = [4, 5, 6, 7, 8, 9, 10]
    min_diff_digits = [1, 2, 3, 4, 5, 6, 7]

    for i, (window_size, min_digits) in enumerate(zip(window_sizes, min_diff_digits)):
        occurrences.clear()

        for j in range(len(pairs) - window_size + 1):
            window = pairs[j:j + window_size]
            if len(set(x[0] for x in window)) >= min_digits:
                pattern = tuple(window)
                occurrences.setdefault(pattern, []).append(times[j])

        sorted_occurrences = {k: v for k, v in sorted(occurrences.items(), key=lambda item: len(item[1]), reverse=True)}

        output_file = output_file_template.format(i)

        with open(output_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            for match, start_times in sorted_occurrences.items():
                if len(start_times) > 1:
                    matching_pairs = ', '.join(str(p) for p in match)
                    rounded_start_times = [int(float(time)) for time in start_times]
                    writer.writerow(["Matching Pairs:", matching_pairs])
                    writer.writerow(["Occurrences:", len(start_times)])
                    writer.writerow(["Start Times:", ', '.join(map(str, rounded_start_times))])
                    writer.writerow([])

                elif len(start_times) == 1:
                    min_distance = float('inf')
                    closest_match = None
                    for other_match, other_times in occurrences.items():
                        if len(other_times) > 1:
                            distance = min(euclidean_distance(match[0], other_pair) for other_pair in other_match)
                            if distance < min_distance:
                                min_distance = distance
                                closest_match = other_match
                    if min_distance < threshold and closest_match is not None:
                        occurrences[closest_match].extend(start_times)

        print(f"Matching pairs with times written to output file: {output_file}")

# Example usage:
input_csv = 'y9_10_2three.csv'  # Replace with the path to your input CSV file
output_csv_template = '9_10_2threeFeat{}.csv'  # Specify the template for the output CSV files

find_matching_pairs_with_times(input_csv, output_csv_template)
