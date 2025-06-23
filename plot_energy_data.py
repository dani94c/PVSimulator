import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def plot_energy_data(csv_file_path):
    """
    Reads a CSV file with energy data and creates a plot with timestamp on X-axis
    and different power measurements as separate lines on Y-axis.
    
    Args:
        csv_file_path (str): Path to the CSV file to read
    """
    
    try:
        # Read the CSV file using pandas
        # pandas is a powerful library for manipulating structured data
        df = pd.read_csv(csv_file_path)
        
        # Verify that the CSV has the required columns
        required_columns = ['timestamp', 'meter_power_kw', 'pv_power_kw', 'net_power_kw']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Error: Missing columns in CSV: {missing_columns}")
            return
        
        # Convert timestamp column to datetime format
        # This step is crucial to allow matplotlib to properly interpret dates
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Sort data by timestamp to ensure the plot is chronologically ordered
        df = df.sort_values('timestamp')
        
        # Create the figure and axes for the plot
        # figsize controls the plot dimensions in inches (width, height)
        plt.figure(figsize=(12, 8))
        
        # Plot the three lines with different colors
        # We use linewidth to make the lines more visible
        # marker='o' adds small circles on data points (optional, useful for few points)
        plt.plot(df['timestamp'], df['meter_power_kw'], 
                color='blue', linewidth=2, label='Meter Power (kW)', marker='o', markersize=3)
        
        plt.plot(df['timestamp'], df['pv_power_kw'], 
                color='green', linewidth=2, label='PV Power (kW)', marker='s', markersize=3)
        
        plt.plot(df['timestamp'], df['net_power_kw'], 
                color='red', linewidth=2, label='Net Power (kW)', marker='^', markersize=3)
        
        # Configure X-axis to display dates in a readable format
        # This is important when working with time series data
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))   #('%Y-%m-%d %H:%M')
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))  # Show every 1 hours
        
        # Rotate X-axis labels to avoid overlapping
        plt.xticks(rotation=45)
        
        # Add labels and title to make the plot more understandable
        plt.xlabel('Timestamp', fontsize=12)
        plt.ylabel('Power (kW)', fontsize=12)
        plt.title('Power Trends Over Time', fontsize=14, fontweight='bold')
        
        # Add a grid to facilitate reading values
        plt.grid(True, alpha=0.3)
        
        # Add legend to identify the different lines
        plt.legend(loc='best', fontsize=10)
        
        # Improve layout to prevent labels from being cut off
        plt.tight_layout()
        
        # Display the plot
        plt.show()
        
        # Print some basic statistics about the data
        print("\n=== DATA STATISTICS ===")
        print(f"Number of data points: {len(df)}")
        print(f"Time period: from {df['timestamp'].min()} to {df['timestamp'].max()}")
        print("\nStatistics by column:")
        for col in ['meter_power_kw', 'pv_power_kw', 'net_power_kw']:
            print(f"{col}:")
            print(f"  Average: {df[col].mean():.2f} kW")
            print(f"  Minimum: {df[col].min():.2f} kW")
            print(f"  Maximum: {df[col].max():.2f} kW")
            print()
        
    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found.")
        print("Make sure the file path is correct.")
    
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
    
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    """
    Main function that asks the user for the CSV file path
    and starts the data visualization.
    """
    
    print("=== ENERGY DATA CSV VISUALIZER ===")
    print("This script reads a CSV file with power data and creates a plot.")
    print()
    
    # Ask the user for the CSV file path
    csv_path = input("Enter the CSV file path: ").strip()
    
    # If the user doesn't enter anything, use a default name
    if not csv_path:
        csv_path = "energy_data.csv"
        print(f"Using default file: {csv_path}")
    
    # Call the function to create the plot
    plot_energy_data(csv_path)

# This block is executed only if the script has been directly launched
# (not when it is imported as module)
if __name__ == "__main__":
    main()