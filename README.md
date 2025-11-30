# Python Programming Lab

**Author:** Vinayak (Roll No: 2501730150)  
**Course:** ETCCPP102 - Python Programming  
**Institution:** K.R Mangalam University  
**Program:** B.Tech AI & ML, Semester 1

---

This repository contains comprehensive lab assignments demonstrating Python programming concepts from basic CLI applications to advanced data analysis and visualization.

---

## 📚 Lab Assignments

### Lab 1: Daily Calorie Tracker
**File:** `Lab 1/Calorietracker.py`

A command-line calorie tracking application that helps users monitor daily food intake.

**Features:**
- Set daily calorie limits
- Log multiple meals with calorie amounts
- Calculate total consumption and remaining calories
- Provide personalized feedback (over/under limit)
- Save logs with timestamps to `calorie_log.txt`

**Key Concepts:**
- Input validation with try-except
- List operations and parallel data structures
- String formatting (f-strings)
- File I/O operations
- Working with datetime module

**Usage:**
```bash
python "Lab 1/Calorietracker.py"
```

---

### Lab 2: GradeBook Analyzer
**File:** `Lab 2/Gradebook.py`

A student performance analysis tool that calculates statistics and assigns letter grades.

**Features:**
- Manual data entry for student names and marks
- Statistical analysis (mean, min, max)
- Letter grade assignment (A-F scale)
- Grade distribution visualization
- Identify students needing improvement (<60%)

**Key Concepts:**
- Modular programming (separate functions)
- Statistics module usage
- Dictionary operations for counting
- List comprehensions
- Data filtering and analysis

**Usage:**
```bash
python "Lab 2/Gradebook.py"
```

---

### Lab 3: Library Inventory Manager
**File:** `Lab 3/library_inventory_manager.py`

An object-oriented library management system with JSON persistence.

**Features:**
- Add books (title, author, ISBN)
- Search books by title/author/ISBN
- Display entire catalog
- Issue/return books (status tracking)
- Persistent storage via JSON
- Input validation and error handling
- Logging system (INFO/ERROR)

**Key Concepts:**
- Object-Oriented Programming (Book, LibraryInventory classes)
- JSON serialization/deserialization
- Type hints for documentation
- Pathlib for file management
- Exception handling
- CLI menu-driven interface

**Usage:**
```bash
python "Lab 3/library_inventory_manager.py"
```

**Data Storage:** Creates `library_catalog.json` in the Lab 3 folder.

---

### Lab 4: Weather Data Visualizer
**File:** `Lab 4/weather_data_visualizer.py`

A data analysis and visualization tool for weather datasets.

**Features:**
- Load and clean CSV weather data
- Handle missing values and outliers
- Time-series aggregation (monthly/yearly)
- Generate multiple visualizations:
  - Daily temperature trend (line plot)
  - Monthly average temperatures (bar chart)
  - Monthly statistics combo (avg/min/max)
  - Yearly temperature trends
- Create markdown analysis report
- Export cleaned data

**Key Concepts:**
- Pandas for data manipulation
- Matplotlib for visualization (Agg backend)
- Time-series resampling (.resample())
- Statistical aggregation functions
- Data cleaning and validation
- Non-interactive plotting

**Dependencies:**
```bash
pip install pandas matplotlib
```

**Usage:**
```bash
python "Lab 4/weather_data_visualizer.py"
```

**Input:** `weather_sample.csv` (date, temperature columns)  
**Output:** 
- `cleaned_weather.csv` (cleaned data)
- `daily_trend.png` (visualization)
- `monthly_avg.png` (visualization)
- `combo_chart.png` (visualization)
- `yearly_trend.png` (visualization)
- `weather_report.md` (analysis report)

---

### Capstone Project: Campus Energy-Use Dashboard
**File:** `Capstone/energy_dashboard.py`

A comprehensive energy monitoring system for campus buildings with multi-chart dashboards.

**Features:**
- Load energy meter readings from multiple CSV files
- Object-oriented architecture (MeterReading, Building, BuildingManager classes)
- Time-series analysis (daily/weekly aggregations)
- Statistical analysis (totals, averages, peak detection)
- Multi-chart dashboard generation:
  - Daily consumption trends per building
  - Average weekly usage comparison (bar chart)
  - Hourly consumption distribution (scatter plot)
- Comprehensive reporting:
  - Building summary CSV
  - Text report with insights
  - Combined cleaned data export
- Logging system for operations tracking

**Key Concepts:**
- Advanced Object-Oriented Programming
- Pandas time-series operations
- Matplotlib multi-chart layouts (subplots)
- Data aggregation at multiple levels
- CSV processing from multiple files
- Pathlib for directory operations
- Composition pattern (Manager → Buildings → Readings)

**Dependencies:**
```bash
pip install pandas matplotlib
```

**Usage:**
```bash
python "Capstone/energy_dashboard.py"
```

**Input:** CSV files in `Capstone/data/` with columns: `timestamp`, `kwh`  
**Output (in `Capstone/output/`):**
- `building_summary.csv` - Statistics per building
- `cleaned_energy_data.csv` - Combined dataset
- `summary.txt` - Key findings report
- `dashboard.png` - Three-chart visualization

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+** (3.11 recommended)
- **pip** (Python package manager)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/codeREDxbt/Python-programming-Lab.git
cd Python-programming-Lab
```

2. **Install dependencies (for Lab 4 and Capstone):**
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install pandas matplotlib
```

### Running the Labs

**Labs 1-3 (No dependencies):**
```bash
python "Lab 1/Calorietracker.py"
python "Lab 2/Gradebook.py"
python "Lab 3/library_inventory_manager.py"
```

**Lab 4 (Requires pandas, matplotlib):**
```bash
cd "Lab 4"
python weather_data_visualizer.py
```

**Capstone (Requires pandas, matplotlib):**
```bash
cd Capstone
python energy_dashboard.py
```

---

## 📦 Repository Structure

```
Python-programming-Lab/
├── README.md
├── requirements.txt
├── Lab 1/
│   ├── Calorietracker.py
│   └── Lab1_Report.md
├── Lab 2/
│   ├── Gradebook.py
│   └── Lab2_Report.md
├── Lab 3/
│   ├── library_inventory_manager.py
│   ├── library_catalog.json (generated)
│   └── Lab3_Report.md
├── Lab 4/
│   ├── weather_data_visualizer.py
│   ├── weather_sample.csv
│   ├── cleaned_weather.csv (generated)
│   ├── *.png (generated visualizations)
│   ├── weather_report.md (generated)
│   └── Lab4_Report.md
└── Capstone/
    ├── energy_dashboard.py
    ├── data/
    │   ├── Building_A.csv
    │   └── Building_B.csv
    ├── output/ (generated)
    │   ├── building_summary.csv
    │   ├── cleaned_energy_data.csv
    │   ├── summary.txt
    │   └── dashboard.png
    └── Capstone_Report.md
```

---

## 🎯 Learning Objectives

### Programming Fundamentals (Labs 1-2)
- Variables, data types, operators
- Control flow (if/else, loops)
- Functions and modular programming
- User input and validation
- File I/O operations
- Error handling (try-except)

### Object-Oriented Programming (Lab 3)
- Classes and objects
- Methods and attributes
- Encapsulation
- JSON serialization
- Type hints
- Logging systems

### Data Analysis & Visualization (Lab 4, Capstone)
- Pandas DataFrames
- Data cleaning and validation
- Time-series operations
- Statistical aggregation
- Matplotlib plotting
- Multi-chart dashboards
- Report generation

### Software Engineering Practices
- Modular design
- Code documentation
- Error handling
- Logging for debugging
- Single-file deployments
- Version control (Git)

---

## 💡 Key Technologies

| Technology | Usage | Labs |
|------------|-------|------|
| **Python 3.11** | Core language | All |
| **Pandas** | Data manipulation | Lab 4, Capstone |
| **Matplotlib** | Data visualization | Lab 4, Capstone |
| **JSON** | Data persistence | Lab 3 |
| **Logging** | Operation tracking | Lab 3, Capstone |
| **Pathlib** | File management | Lab 3, Lab 4, Capstone |
| **Datetime** | Timestamp handling | Lab 1 |
| **Statistics** | Statistical analysis | Lab 2 |

---

## 📝 Notes

- All code is original and follows assignment guidelines
- Labs 1-3 are self-contained with no external dependencies
- Lab 4 and Capstone require pandas and matplotlib
- Each lab includes comprehensive inline documentation
- Generated files (JSON, CSV, PNG, TXT) are created in respective lab folders
- Non-interactive matplotlib backend (Agg) used for server-safe plotting

---

## 👤 Author Information

**Name:** Vinayak  
**Roll Number:** 2501730150  
**Section:** C  
**Program:** B.Tech in Artificial Intelligence & Machine Learning  
**Semester:** 1  
**Course:** ETCCPP102 - Python Programming  
**Faculty:** Dr. Sameer Farooq  
**Institution:** K.R Mangalam University - School of Engineering & Technology

---

## 📧 Contact

For questions or issues, please contact:  
📩 sameer.farooq@krmangalam.edu.in

---

## 📄 License

This repository contains academic coursework for K.R Mangalam University.  
All rights reserved © 2025 Vinayak

---

**Last Updated:** December 1, 2025
