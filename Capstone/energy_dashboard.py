"""
Capstone Project: Campus Energy-Use Dashboard
Author: Vinayak [2501730150]
Course: Programming for Problem Solving using Python

Features:
- Ingests multiple CSVs from /data/ directory
- OOP Design: Building, MeterReading, BuildingManager
- Aggregates daily/weekly consumption
- Visualizes trends (Line, Bar, Scatter) in a dashboard
- Exports cleaned data and summary report
"""

import os
import glob
import logging
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MeterReading:
    """Represents a single energy reading."""
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh

class Building:
    """Represents a campus building with energy readings."""
    def __init__(self, name):
        self.name = name
        self.readings = []  # List of MeterReading objects
        self.df = pd.DataFrame()

    def add_reading(self, reading):
        self.readings.append(reading)

    def process_readings(self):
        """Converts readings list to DataFrame for analysis."""
        if not self.readings:
            return
        data = [{'timestamp': r.timestamp, 'kwh': r.kwh} for r in self.readings]
        self.df = pd.DataFrame(data)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df.set_index('timestamp', inplace=True)
        self.df.sort_index(inplace=True)

    def calculate_daily_totals(self):
        if self.df.empty:
            return pd.Series()
        return self.df['kwh'].resample('D').sum()

    def calculate_weekly_aggregates(self):
        if self.df.empty:
            return pd.DataFrame()
        return self.df['kwh'].resample('W').agg(['mean', 'min', 'max', 'sum'])

class BuildingManager:
    """Manages multiple buildings and orchestrates data loading/analysis."""
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.buildings = {}  # name -> Building object
        self.combined_df = pd.DataFrame()

    def load_data(self):
        """Reads all CSV files in data_dir and populates buildings."""
        csv_files = list(self.data_dir.glob("*.csv"))
        if not csv_files:
            logging.warning(f"No CSV files found in {self.data_dir}")
            return

        all_data = []
        for file_path in csv_files:
            try:
                # Assume filename is BuildingName.csv or similar
                building_name = file_path.stem
                logging.info(f"Loading {building_name} from {file_path}")
                
                df = pd.read_csv(file_path)
                
                # Validation: Check required columns
                if 'timestamp' not in df.columns or 'kwh' not in df.columns:
                    logging.error(f"Skipping {file_path}: Missing 'timestamp' or 'kwh' columns")
                    continue

                # Create Building object if not exists
                if building_name not in self.buildings:
                    self.buildings[building_name] = Building(building_name)

                # Add readings to Building object
                for _, row in df.iterrows():
                    reading = MeterReading(row['timestamp'], row['kwh'])
                    self.buildings[building_name].add_reading(reading)
                
                # Process building data
                self.buildings[building_name].process_readings()

                # Prepare for combined DataFrame
                df['building'] = building_name
                all_data.append(df)

            except Exception as e:
                logging.error(f"Error reading {file_path}: {e}")

        if all_data:
            self.combined_df = pd.concat(all_data, ignore_index=True)
            self.combined_df['timestamp'] = pd.to_datetime(self.combined_df['timestamp'])
            logging.info(f"Combined data loaded. Total rows: {len(self.combined_df)}")

    def generate_summary_report(self, output_dir):
        """Generates summary CSV and text report."""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        summary_lines = ["Campus Energy Summary Report", "============================"]
        
        # Total Campus Consumption
        total_consumption = self.combined_df['kwh'].sum() if not self.combined_df.empty else 0
        summary_lines.append(f"Total Campus Consumption: {total_consumption:.2f} kWh")

        # Building-wise Summary
        building_stats = []
        highest_consumer = (None, 0)

        for name, building in self.buildings.items():
            if building.df.empty:
                continue
            total = building.df['kwh'].sum()
            avg = building.df['kwh'].mean()
            max_kwh = building.df['kwh'].max()
            
            building_stats.append({
                'Building': name,
                'Total (kWh)': total,
                'Average (kWh)': avg,
                'Max (kWh)': max_kwh
            })

            if total > highest_consumer[1]:
                highest_consumer = (name, total)

        summary_df = pd.DataFrame(building_stats)
        summary_csv_path = output_dir / "building_summary.csv"
        summary_df.to_csv(summary_csv_path, index=False)
        logging.info(f"Building summary saved to {summary_csv_path}")

        summary_lines.append(f"Highest Consuming Building: {highest_consumer[0]} ({highest_consumer[1]:.2f} kWh)")
        
        # Peak Load Time
        if not self.combined_df.empty:
            peak_row = self.combined_df.loc[self.combined_df['kwh'].idxmax()]
            summary_lines.append(f"Peak Load Time: {peak_row['timestamp']} ({peak_row['kwh']} kWh by {peak_row['building']})")

        # Write text report
        report_path = output_dir / "summary.txt"
        with open(report_path, "w") as f:
            f.write("\n".join(summary_lines))
        logging.info(f"Summary report saved to {report_path}")
        
        # Export cleaned combined data
        cleaned_path = output_dir / "cleaned_energy_data.csv"
        self.combined_df.to_csv(cleaned_path, index=False)
        logging.info(f"Cleaned data exported to {cleaned_path}")

        # Print summary to console
        print("\n" + "\n".join(summary_lines))

    def create_dashboard(self, output_dir):
        """Generates the multi-chart dashboard."""
        if self.combined_df.empty:
            logging.warning("No data to visualize.")
            return

        output_dir = Path(output_dir)
        fig, axes = plt.subplots(3, 1, figsize=(12, 18))
        fig.suptitle('Campus Energy-Use Dashboard', fontsize=16)

        # 1. Trend Line: Daily Consumption per Building
        ax1 = axes[0]
        for name, building in self.buildings.items():
            daily = building.calculate_daily_totals()
            if not daily.empty:
                ax1.plot(daily.index, daily.values, label=name, marker='o')
        ax1.set_title('Daily Energy Consumption Trend')
        ax1.set_ylabel('kWh')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 2. Bar Chart: Average Weekly Usage
        ax2 = axes[1]
        avg_weekly = {}
        for name, building in self.buildings.items():
            weekly = building.calculate_weekly_aggregates()
            if not weekly.empty:
                avg_weekly[name] = weekly['mean'].mean() # Average of weekly means
        
        if avg_weekly:
            ax2.bar(avg_weekly.keys(), avg_weekly.values(), color='skyblue')
            ax2.set_title('Average Weekly Energy Usage')
            ax2.set_ylabel('Average kWh')
        
        # 3. Scatter Plot: Consumption vs Time (Peak Hour Analysis)
        ax3 = axes[2]
        for name, building in self.buildings.items():
            if not building.df.empty:
                # Extract hour for x-axis
                hours = building.df.index.hour
                ax3.scatter(hours, building.df['kwh'], label=name, alpha=0.6)
        ax3.set_title('Hourly Consumption Distribution (Peak Analysis)')
        ax3.set_xlabel('Hour of Day (0-23)')
        ax3.set_ylabel('kWh')
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        dashboard_path = output_dir / "dashboard.png"
        plt.savefig(dashboard_path)
        logging.info(f"Dashboard saved to {dashboard_path}")
        plt.close()

def main():
    # Setup paths
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"
    output_dir = base_dir / "output"

    # Initialize Manager
    manager = BuildingManager(data_dir)
    
    # 1. Ingest Data
    manager.load_data()
    
    # 2. Generate Reports & Export Data
    manager.generate_summary_report(output_dir)
    
    # 3. Create Visualizations
    manager.create_dashboard(output_dir)

if __name__ == "__main__":
    main()
