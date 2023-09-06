import pandas as pd
import numpy as np
import argparse
import os

# Define the time points and replicates
time_points = ["0h", "2h", "3h", "12h", "24h", "48h"]
replicates = ["1", "2", "3"]

# Initialize an empty DataFrame to store the results
result_df = None

# Create an argument parser for console input
parser = argparse.ArgumentParser(description="Process RNA abundance data and generate a combined output file.")
parser.add_argument("output_file", type=str, help="Output file name (TSV format)")

args = parser.parse_args()

# Iterate through time points and replicates
for time_point in time_points:
    for replicate in replicates:
        file_path = f"{time_point}_rna_{replicate}/plain/abundance.tsv"

        # Read the data, selecting only columns 1 and 5
        df = pd.read_csv(file_path, sep='\t', usecols=[0, 4])

        # Offset "tpm" values by 1 and then log2 transform them
        df[f"{time_point}_rna_{replicate}"] = np.log2(df.iloc[:, 1] + 1)

        # Drop the original "tpm" column
        df = df.drop(columns=df.columns[1])

        # Rename columns
        df.columns = ["target_id", f"{time_point}_rna_{replicate}"]

        # Merge or concatenate the results
        if result_df is None:
            result_df = df
        else:
            result_df = pd.merge(result_df, df, on="target_id")

# Save the final DataFrame to the specified output file
output_filename = args.output_file
result_df.to_csv(output_filename, sep='\t', index=False)

print(f"Data processed and saved to {output_filename}")
