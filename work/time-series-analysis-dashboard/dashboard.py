import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import tkinter as tk
from tkinter import filedialog

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def plot_time_series(data, time_column, columns):
    fig = make_subplots(rows=5, cols=1, shared_xaxes=True, vertical_spacing=0.02)
    
    for i, column in enumerate(columns):
        fig.add_trace(go.Scatter(x=data[time_column], y=data[column], mode='lines', name=column), row=i+1, col=1)
    
    fig.update_layout(height=1500, width=1000, title_text="Time Series Visualizations")
    
    # Add cursors
    for i in range(5):
        fig.add_vline(x=data[time_column].iloc[0], line_width=3, line_dash="dash", line_color="red", row=i+1, col=1)

    fig.show()

def main():
    # Step 1: Select the file
    file_path = select_file()
    
    # Step 2: Read the file into a DataFrame
    data = pd.read_csv(file_path)
    
    # Step 3: Ensure the time column is in timedelta format
    time_column = 'Time'  # Adjust this to the correct column name for time
    data[time_column] = data[time_column] - data[time_column].min()
    data[time_column] = pd.to_timedelta(data[time_column])
    
    # Step 4: Select columns for visualization
    columns = data.columns.difference([time_column]).tolist()[:5]
    
    # Step 5: Plot time series visualizations
    plot_time_series(data, time_column, columns)

if __name__ == "__main__":
    main()
