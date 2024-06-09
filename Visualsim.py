import csv
import matplotlib.pyplot as plt
import ast
import numpy as np
from matplotlib.animation import FuncAnimation

# Function to parse the CSV file and organize the data
def parse_csv(filename):
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        current_pairs = None
        current_occurrences = None
        current_start_times = None

        for row in reader:
            if not row:
                continue  # Skip empty rows
            if "Matching Pairs:" in row[0]:
                current_pairs = ast.literal_eval(row[1])
            elif "Occurrences:" in row[0]:
                current_occurrences = int(row[1])
            elif "Start Times:" in row[0]:
                current_start_times = list(map(int, row[1].split(',')))
                data.append((current_pairs, current_occurrences, current_start_times))

    return data

# Function to generate a color palette for plotting
def generate_color_palette(num_colors):
    cmap = plt.get_cmap('tab10')  # Choose a color map (tab10 provides 10 distinct colors)
    colors = cmap(np.linspace(0, 1, num_colors))  # Generate a set of colors
    return colors

# Function to update the plot at each frame of the animation
def update(frame, data, ax):
    ax.clear()  # Clear the previous plot
    colors = generate_color_palette(len(data))  # Generate colors for each combination
    markers = ['o', 's', '^', 'v', '*', 'D', 'X', 'P']  # Define marker shapes
    num_markers = len(markers)

    for i, (pair, occurrences, start_times) in enumerate(data):
        if frame in start_times:
            if pair:  # Check if the combination has data
                x_values = list(range(len(pair)))
                y_values = [float(coord[0]) * 10**float(coord[1].split('e')[1]) for coord in pair]  # Convert coordinates
                label = f"Combination {i} (Occurrences: {occurrences})"  # Construct label using combination index and occurrences number
                marker_index = i % num_markers  # Get marker index ensuring it doesn't go out of bounds
                ax.plot(x_values, y_values, label=label, color=colors[i], marker=markers[marker_index])  # Plot markers for each combination with a unique color and shape

    ax.set_xlabel('Index within the Row')
    ax.set_ylabel('Coordinate Value')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))  # Place legend outside the plot area

def main():
    try:
        data = parse_csv('all.csv')
    except Exception as e:
        print("Error parsing CSV:", e)
        return

    fig, ax = plt.subplots(figsize=(8, 6))
    ani = FuncAnimation(fig, update, frames=range(30001), fargs=(data, ax), interval= 1000, repeat=False)  # Animate the plot with a slower interval
    plt.show()

if __name__ == "__main__":
    main()
