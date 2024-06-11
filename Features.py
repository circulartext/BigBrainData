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
        first_digits = '-' + mantissa[1:4]
    else:
        first_digits = mantissa[:3]
    return first_digits, exponent

def euclidean_distance(pair1, pair2):
    mantissa1, exponent1 = pair1
    mantissa2, exponent2 = pair2
    mantissa_diff = float(mantissa1) - float(mantissa2)
    exponent_diff = float(exponent1[2:]) - float(exponent2[2:])
    return math.sqrt(mantissa_diff ** 2 + exponent_diff ** 2)

def find_matching_pairs_with_times(csv_file, output_file1, output_file2, threshold=1000):
    pairs = []
    times = []
    occurrences = {}
    matched_indices = set()

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            value = row['EOG Horizontal_Modified']
            time = row['Time']
            first_digits, exponent = extract_first_and_exponent(value)
            if first_digits is not None and exponent is not None:
                pairs.append((first_digits, exponent))
                times.append(time)

    for i in range(len(pairs) - 5):
        if i not in matched_indices:
            window = pairs[i:i + 6]
            if len(set(x[0] for x in window)) >= 4:
                pattern = tuple(window)
                occurrences.setdefault(pattern, []).append(times[i])
                matched_indices.update(range(i, i + 4))

    sorted_occurrences = {k: v for k, v in sorted(occurrences.items(), key=lambda item: len(item[1]), reverse=True)}

    with open(output_file1, 'w', newline='') as outfile1:
        writer1 = csv.writer(outfile1)
        for match, start_times in sorted_occurrences.items():
            if len(start_times) > 1:
                matching_pairs = ', '.join(str(p) for p in match)
                rounded_start_times = [int(float(time)) for time in start_times]
                writer1.writerow(["Matching Pairs:", matching_pairs])
                writer1.writerow(["Occurrences:", len(start_times)])
                writer1.writerow(["Start Times:", ', '.join(map(str, rounded_start_times))])
                writer1.writerow([])

            # Associate single occurrences with closest match
            elif len(start_times) == 1:
                min_distance = float('inf')
                closest_matches = []
                for other_match, other_times in sorted_occurrences.items():
                    if len(other_times) > 1:
                        distance = min(euclidean_distance(match[0], other_pair) for other_pair in other_match)
                        if distance < min_distance:
                            min_distance = distance
                            closest_matches = [(other_match, other_times)]
                        elif distance == min_distance:
                            closest_matches.append((other_match, other_times))
                if min_distance < threshold:
                    for closest_match, closest_times in closest_matches:
                        occurrences[closest_match] = closest_times + start_times

    sorted_occurrences = {k: v for k, v in sorted(occurrences.items(), key=lambda item: len(item[1]), reverse=True)}

    for match, start_times in sorted_occurrences.items():
        matching_pairs = ', '.join(str(p) for p in match)
        rounded_start_times = [int(float(time)) for time in start_times]
        writer1.writerow(["Matching Pairs:", matching_pairs])
        writer1.writerow(["Occurrences:", len(start_times)])
        writer1.writerow(["Start Times:", ', '.join(map(str, rounded_start_times))])
        writer1.writerow([])

    print("Matching pairs with times written to output file:", output_file1)

    with open(output_file2, 'w', newline='') as outfile2:
        writer2 = csv.writer(outfile2)
        writer2.writerow(['Matching Pairs', 'Occurrences'])
        for match, count in sorted_occurrences.items():
            matching_pairs = ', '.join(str(p) for p in match)
            writer2.writerow([matching_pairs, len(count)])
    print("Matching pairs with occurrence count written to output file:", output_file2)

# Example usage:
input_csv = 'y9_10_2three.csv'  # Replace with the path to your input CSV file
output_csv1 = 'y9_10_2threeFeat.csv'  # Specify the path for the output CSV file with times
output_csv2 = 'y9_10_2threeFeat.csv'  # Specify the path for the output CSV file with occurrence count
find_matching_pairs_with_times(input_csv, output_csv1, output_csv2)
