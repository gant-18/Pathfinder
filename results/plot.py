import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style for better aesthetics
sns.set(style="whitegrid")

# Load the CSV file
df = pd.read_csv("simulation_metrics.csv")

# Function to map original Mode to standardized Prefetcher names
def map_prefetcher(mode):
    if mode == "from_file":
        return "pathfinder"
    elif mode == "from_file_IF":
        return "modified pathfinder"
    elif "sisb_bo" in mode:
        return "sisb_bo"
    elif "sisb" in mode:
        return "sisb"
    elif "bo" in mode:
        return "bo"
    elif "no" in mode:
        return "no"
    else:
        return mode  # Retain original if no match

# Apply the mapping to create a new column
df["Prefetcher"] = df["Mode"].apply(map_prefetcher)

# Drop the original 'Mode' column
df.drop(columns=["Mode"], inplace=True)

# Reorder columns for clarity
df = df[["Trace", "Prefetcher", "IPC", "Accuracy", "Coverage"]]

# Sort the DataFrame by 'Trace' and 'Prefetcher'
df.sort_values(by=["Trace", "Prefetcher"], inplace=True)

# Save the cleaned and sorted DataFrame to a new CSV file
df.to_csv("simulation_metrics_cleaned.csv", index=False)

# Define the metrics to plot
metrics = ["IPC", "Accuracy", "Coverage"]

# Define a color palette for the prefetcher modes
prefetcher_colors = {
    "pathfinder": "tab:blue",
    "modified pathfinder": "tab:orange",
    "sisb_bo": "tab:green",
    "sisb": "tab:red",
    "bo": "tab:purple",
    "no": "tab:brown"
}

# Create the output directory if it doesn't exist
output_dir = "simulation_plots"
os.makedirs(output_dir, exist_ok=True)

# Iterate over each metric to create individual plots
for metric in metrics:
    # For 'Accuracy' and 'Coverage', exclude 'no' prefetcher
    if metric in ["Accuracy", "Coverage"]:
        plot_df = df[df["Prefetcher"] != "no"]
    else:
        plot_df = df.copy()

    plt.figure(figsize=(12, 6))
    ax = sns.barplot(
        data=plot_df,
        x="Trace",
        y=metric,
        hue="Prefetcher",
        palette=prefetcher_colors
    )
    plt.title(f"{metric} by Trace and Prefetcher")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    # Place the legend outside the plot
    plt.legend(title="Prefetcher", bbox_to_anchor=(1.05, 1), loc='upper left')
    # Save each plot as a PNG file in the specified directory
    plt.savefig(os.path.join(output_dir, f"{metric.lower()}_by_trace_prefetcher.png"), bbox_inches='tight')
    plt.close()
