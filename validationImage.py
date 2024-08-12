import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
train_df = pd.read_csv('samples/mnist_train.csv')
test_df = pd.read_csv('samples/mnist_test.csv')
mnist_df = pd.concat([train_df, test_df], ignore_index=True)

# Define the list of row indices you are interested in
row_indices = [
    12306, 12461, 12928, 14670, 16712, 25371, 25416, 2874, 30708, 31182,
    3493, 35732, 37990, 40341, 43948, 43960, 59956, 45769, 45973, 47356, 47375,
    48033, 59366, 59956, 6094, 64303, 67001, 67512, 69543, 7745
]

# Filter the dataset based on the row indices
filtered_data = mnist_df.iloc[row_indices]

# Create a mapping of row index to labels
# Assuming 'label' column contains the labels
index_to_label_mapping = filtered_data[['label']].copy()

# Add a column for row index to keep track
index_to_label_mapping['row_index'] = filtered_data.index

# Reorder columns to have row_index first
index_to_label_mapping = index_to_label_mapping[['row_index', 'label']]

# Sort the DataFrame by the 'label' column
sorted_index_to_label_mapping = index_to_label_mapping.sort_values(by='label')

# Display the sorted mapping
print(sorted_index_to_label_mapping)
