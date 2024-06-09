import numpy as np
import mne
from mne.io import read_raw_edf
import pandas as pd  # Import pandas for CSV handling

# Load EDF file
edf_file = '9_10_2.edf'
raw = read_raw_edf(edf_file, preload=True)

# Pick the horizontal EOG channel
eog_data, times = raw.copy().pick_channels(['EEGFp2CPz']).get_data(return_times=True)

# Save EOG data to CSV
eog_df = pd.DataFrame(data={'Time': times, 'C4': eog_data[0, :]})
eog_df.to_csv('y9_10_2one.csv', index=False)

print("Horizontal EOG data saved to 'Fp2data.csv'")
