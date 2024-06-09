Project Name: EOG Data Analysis and Visualization
Description
This project involves analyzing and visualizing electrooculography (EOG) data obtained from CSV files. The project consists of several Python scripts that perform various tasks such as data extraction, formatting, analysis, and visualization.

Files:
eog1.py

Purpose: Extracts EOG data from an EDF file and saves it to a CSV file.
eog2.py

Purpose: Processes the CSV file generated by eog1.py if required.
eog3.py

Purpose: Further processes the CSV file if necessary.
Features.py

Purpose: Identifies matching pairs of EOG data and calculates occurrences over time.
Visualsim.py

Purpose: Visualizes the occurrences of different combinations of EOG data pairs over time using an animated plot.
y9_10_2.edf

EDF file containing EOG data.
y9_10_2one.csv

Output CSV file generated by eog1.py.
y9_10_2two.csv

Output CSV file processed by eog2.py.
y9_10_2three.csv

Output CSV file processed by eog3.py.
9_10_2threeFeat{}.csv

Output CSV files generated by Features.py.
all.csv

Combined output CSV file for visualization generated by Features.py.
Usage
Run eog1.py to extract EOG data from the EDF file and save it to a CSV file.
Process the generated CSV file using eog2.py and eog3.py if necessary.
Run Features.py to identify matching pairs of EOG data and calculate occurrences over time. This generates multiple output CSV files.
Combine the output CSV files into a single file (all.csv) for visualization.
Run Visualsim.py to visualize the occurrences of different combinations of EOG data pairs over time using an animated plot.
Requirements
Python 3.x
Required Python packages: numpy, mne, pandas, matplotlib
Author
[CirculartextApps]

License
This project is licensed GNU Affero General Public License Version 3

