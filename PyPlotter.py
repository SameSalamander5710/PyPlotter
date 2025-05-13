import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk

# Function to create the plot
def create_plot(agg_func, error_type, y_scale, log_base):
    # Clear the current figure
    plt.clf()

    # Read wide-format data from clipboard (copied from Excel)
    df = pd.read_clipboard()

    # Melt to long format for seaborn
    df_long = df.melt(var_name='Group', value_name='Value')

    # Create the plot
    fig = plt.gcf()
    fig.set_size_inches(8, 6)

    # Bar plot with selected aggregation function and error type
    sns.barplot(
        data=df_long,
        x='Group',
        y='Value',
        estimator=agg_func,
        errorbar=error_type,
        capsize=0.2,
        color='lightblue',
        edgecolor='black'
    )

    # Overlay individual data points
    sns.stripplot(
        data=df_long,
        x='Group',
        y='Value',
        color='black',
        alpha=0.7,
        jitter=True,
        dodge=True
    )

    # Set y-axis scale
    if y_scale == "Logarithmic":
        plt.yscale("log", base=float(log_base))

    # Customize
    plt.title(f"Bar Plot with Individual Data Points ({agg_func.__name__.capitalize()} ± {error_type.upper()})")
    plt.ylabel("Value")
    plt.xlabel("Group")
    plt.tight_layout()

    # Draw the updated plot
    plt.draw()
    plt.pause(0.001)  # Allow the plot to update dynamically

# Function to handle GUI button click
def on_plot_button_click():
    agg_func = mean_var.get()
    error_type = error_var.get()
    y_scale = y_scale_var.get()
    log_base = log_base_var.get()

    # Map user selection to actual functions/values
    agg_func_map = {"Mean": pd.Series.mean, "Median": pd.Series.median}
    error_type_map = {"SEM": "se", "SD": "sd"}

    create_plot(agg_func_map[agg_func], error_type_map[error_type], y_scale, log_base)

# Create the GUI window
root = tk.Tk()
root.title("Plot Customization")

# Dropdown for aggregation function
mean_var = tk.StringVar(value="Mean")
ttk.Label(root, text="Aggregation Function:").grid(row=0, column=0, padx=10, pady=5)
ttk.OptionMenu(root, mean_var, "Mean", "Mean", "Median").grid(row=0, column=1, padx=10, pady=5)

# Dropdown for error type
error_var = tk.StringVar(value="SEM")
ttk.Label(root, text="Error Type:").grid(row=1, column=0, padx=10, pady=5)
ttk.OptionMenu(root, error_var, "SEM", "SEM", "SD").grid(row=1, column=1, padx=10, pady=5)

# Dropdown for y-axis scale
y_scale_var = tk.StringVar(value="Linear")
ttk.Label(root, text="Y-Axis Scale:").grid(row=2, column=0, padx=10, pady=5)
ttk.OptionMenu(root, y_scale_var, "Linear", "Linear", "Logarithmic").grid(row=2, column=1, padx=10, pady=5)

# Entry for log base
log_base_var = tk.StringVar(value="10")
ttk.Label(root, text="Log Base:").grid(row=3, column=0, padx=10, pady=5)
ttk.Entry(root, textvariable=log_base_var).grid(row=3, column=1, padx=10, pady=5)

# Plot button
ttk.Button(root, text="Generate Plot", command=on_plot_button_click).grid(row=4, column=0, columnspan=2, pady=10)

# Run the GUI event loop
root.mainloop()
