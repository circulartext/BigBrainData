import pandas as pd

# Read the existing CSV file
df = pd.read_csv("y9_10_2two.csv")

def format_value(value):
    
    if value == 0:
        return "0.000"  # Ensure consistent 3 decimal places for zeros
    else:
        abs_value = abs(value)
        # Ensure values slightly below 0.0001 get 8 decimal places
        if abs_value < 0.0001 + 1e-10:
            decimal_places = 8
        else:
            # Determine decimal places based on magnitude (starting from 7)
            if abs_value < 0.001:
                decimal_places = 7
            elif abs_value < 0.01:
                decimal_places = 6
            elif abs_value < 0.1:
                decimal_places = 5
            elif abs_value < 1:
                decimal_places = 4
            else:
                decimal_places = 3
        # Use scientific notation for all values
        formatted_value = f"{value:.{decimal_places}e}"
        return formatted_value.replace(".", "")

# Apply formatting function to "EOG Horizontal" column
df["EOG Horizontal_Modified"] = df["C4"].apply(format_value)

# Select desired columns and save to a new CSV file
df[["Time", "EOG Horizontal_Modified"]].to_csv("y9_10_2three.csv", index=False)

print("Data processed and saved to .csv")
