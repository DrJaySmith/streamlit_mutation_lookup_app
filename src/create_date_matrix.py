# %% [markdown]
# # Create Date Matrix
# 
# This script creates a date matrix from the strain mutations data.
# 
# The date matrix is a matrix of dates and the number of times each set of mutations occurs on that date.
# 
# The strain mutations data is not stored in the github due to size constraints.
# %% [markdown]

# %% 
import pandas as pd
import numpy as np
from datetime import datetime
import os

# Define the protein and data sources
proteins = ["mpro", "plpro", "rbd"]  # Change this if needed
data_sources = ["gisaid", "genbank"]

for protein in proteins:
    for data_source in data_sources:
        print(f"\nProcessing {data_source} data...")
        
        # Load the data
        input_file = f"../data/{data_source}/{protein}/{data_source}_{protein}_strain_mutations.csv"
        df = pd.read_csv(input_file)
        print(f"Loaded {len(df)} rows from {input_file}")
        
        # Get all unique dates
        all_dates = set()
        for dates_str in df['dates']:
            try:
                dates = eval(dates_str)
                for d in dates:
                    date = datetime.fromordinal(int(d))
                    all_dates.add(date)
            except:
                continue
        
        all_dates = sorted(list(all_dates))
        print(f"Found {len(all_dates)} unique dates")
        
        # Create a dictionary to store the date counts for each strain
        strain_date_counts = {}
        
        # Process each row
        for _, row in df.iterrows():
            strain = row['mutations']
            
            try:
                dates = eval(row['dates'])
                for d in dates:
                    date = datetime.fromordinal(int(d))
                    if strain not in strain_date_counts:
                        strain_date_counts[strain] = {}
                    
                    # Only store non-zero counts
                    if date not in strain_date_counts[strain]:
                        strain_date_counts[strain][date] = 1
                    else:
                        strain_date_counts[strain][date] += 1
            except:
                continue
        
        # Convert to DataFrame with sparse representation
        print("Converting to DataFrame...")
        date_columns = [date.strftime('%Y-%m-%d') for date in all_dates]
        rows = []
        
        for strain, date_counts in strain_date_counts.items():
            row = {'strain': strain}
            for date in date_counts:
                row[date.strftime('%Y-%m-%d')] = date_counts[date]
            rows.append(row)
        
        date_matrix_df = pd.DataFrame(rows)
        date_matrix_df.set_index('strain', inplace=True)
        
        # Ensure all date columns exist (with NaN for missing values)
        for col in date_columns:
            if col not in date_matrix_df.columns:
                date_matrix_df[col] = np.nan
        
        # Sort columns by date
        date_matrix_df = date_matrix_df[date_columns]
        
        # Save to CSV
        output_file = f"../data/{data_source}/{protein}/{data_source}_{protein}_date_matrix.csv"
        date_matrix_df.to_csv(output_file)
        
        # Get file size
        size_mb = os.path.getsize(output_file) / (1024 * 1024)
        print(f"Saved to {output_file}")
        print(f"File size: {size_mb:.2f} MB")
        print(f"Matrix shape: {date_matrix_df.shape}") 
# %%
