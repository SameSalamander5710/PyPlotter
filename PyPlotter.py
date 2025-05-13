import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk

# Map user selection to actual functions/values
agg_func_map = {"Mean": pd.Series.mean, "Median": pd.Series.median}
error_type_map = {"SEM": "se", "SD": "sd"}

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

def generate_plot_from_table(tree, columns, agg_func, error_type, y_scale, log_base):
    # Extract column headers (group titles) dynamically from the Treeview
    edited_columns = [tree.heading(f"#{i+1}", "text") for i in range(len(columns))]

    # Extract data from the Treeview
    table_data = []
    for item in tree.get_children():
        table_data.append(tree.item(item, "values"))

    # Convert the data back to a DataFrame
    table_df = pd.DataFrame(table_data, columns=edited_columns)

    # Ensure numeric columns are properly converted
    for col in table_df.columns:
        table_df[col] = pd.to_numeric(table_df[col], errors='coerce')  # Coerce invalid values to NaN

    # Drop rows with NaN values to clean the data
    table_df = table_df.dropna()

    # Melt the DataFrame to long format for seaborn
    table_df_long = table_df.melt(var_name='Group', value_name='Value')

    # Ensure the 'Value' column is numeric
    table_df_long['Value'] = pd.to_numeric(table_df_long['Value'], errors='coerce')

    # Drop rows with NaN values again after melting
    table_df_long = table_df_long.dropna()

    # Generate the plot
    plt.clf()
    fig = plt.gcf()
    fig.set_size_inches(8, 6)

    sns.barplot(
        data=table_df_long,
        x='Group',
        y='Value',
        estimator=agg_func,
        errorbar=error_type,
        capsize=0.2,
        color='lightblue',
        edgecolor='black'
    )

    sns.stripplot(
        data=table_df_long,
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
    plt.draw()
    plt.pause(0.001)

def make_table_editable(tree):
    """Make the Treeview table and column headers editable."""
    def on_double_click(event):
        # Identify the region clicked (cell or heading)
        region = tree.identify("region", event.x, event.y)

        if region == "cell":
            # Edit cell values
            row_id = tree.identify_row(event.y)
            column_id = tree.identify_column(event.x)

            # Get the current value of the cell
            current_value = tree.item(row_id, "values")[int(column_id[1:]) - 1]

            # Create an Entry widget for editing
            entry = tk.Entry(tree)
            entry.insert(0, current_value)
            entry.place(x=event.x, y=event.y, width=tree.column(column_id, "width"))

            # Function to save the new value
            def save_edit(event=None):
                new_value = entry.get()
                values = list(tree.item(row_id, "values"))
                values[int(column_id[1:]) - 1] = new_value
                tree.item(row_id, values=values)
                entry.destroy()

            # Bind Enter key and focus-out event to save the edit
            entry.bind("<Return>", save_edit)
            entry.bind("<FocusOut>", lambda e: entry.destroy())
            entry.focus()

        elif region == "heading":
            # Edit column headers
            column_id = tree.identify_column(event.x)
            column_index = int(column_id[1:]) - 1
            current_header = tree.heading(column_id, "text")

            # Create an Entry widget for editing the header
            entry = tk.Entry(tree)
            entry.insert(0, current_header)
            entry.place(x=event.x, y=0, width=tree.column(column_id, "width"))

            # Function to save the new header
            def save_header(event=None):
                new_header = entry.get()
                tree.heading(column_id, text=new_header)
                entry.destroy()

            # Bind Enter key and focus-out event to save the header
            entry.bind("<Return>", save_header)
            entry.bind("<FocusOut>", lambda e: entry.destroy())
            entry.focus()

    # Bind the double-click event to the Treeview
    tree.bind("<Double-1>", on_double_click)

# Function to display the clipboard data in a popup window
def show_table_popup(agg_func, error_type, y_scale, log_base):
    # Read wide-format data from clipboard
    df = pd.read_clipboard()

    # Check if the popup window already exists
    if hasattr(show_table_popup, "popup") and show_table_popup.popup.winfo_exists():
        # Clear the existing Treeview widget
        for item in show_table_popup.tree.get_children():
            show_table_popup.tree.delete(item)

        # Clear existing column configurations
        for col in show_table_popup.tree["columns"]:
            show_table_popup.tree.heading(col, text="")  # Clear column headers
            show_table_popup.tree.column(col, width=0)  # Reset column width

        # Reset column headers to match the new data
        show_table_popup.tree["columns"] = list(df.columns)
        for i, col in enumerate(df.columns):
            show_table_popup.tree.heading(f"#{i+1}", text=col)
            show_table_popup.tree.column(f"#{i+1}", width=100, anchor="center")
    else:
        # Create a new popup window
        show_table_popup.popup = tk.Toplevel()
        show_table_popup.popup.title("Clipboard Data Table")

        # Create a Treeview widget to display the data
        show_table_popup.tree = ttk.Treeview(show_table_popup.popup, columns=list(df.columns), show="headings")
        for col in df.columns:
            show_table_popup.tree.heading(col, text=col)
            show_table_popup.tree.column(col, width=100, anchor="center")
        show_table_popup.tree.pack(fill="both", expand=True)

        # Make the table editable
        make_table_editable(show_table_popup.tree)

        # Add a button to generate a plot from the table data
        ttk.Button(
            show_table_popup.popup,
            text="Generate Plot from Table",
            command=lambda: generate_plot_from_table(
                show_table_popup.tree,
                df.columns,
                agg_func_map[mean_var.get()],  # Fetch current aggregation function
                error_type_map[error_var.get()],  # Fetch current error type
                y_scale_var.get(),  # Fetch current y-axis scale
                log_base_var.get()  # Fetch current log base
            )
        ).pack(pady=10)

    # Insert new data into the Treeview
    for _, row in df.iterrows():
        show_table_popup.tree.insert("", "end", values=list(row))

# Function to handle GUI button click
def on_plot_button_click():
    agg_func = mean_var.get()
    error_type = error_var.get()
    y_scale = y_scale_var.get()
    log_base = log_base_var.get()

    # Generate the default plot from clipboard data
    create_plot(agg_func_map[agg_func], error_type_map[error_type], y_scale, log_base)

    # Show the popup window with the table
    show_table_popup(agg_func_map[agg_func], error_type_map[error_type], y_scale, log_base)

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
