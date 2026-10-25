# Ride Booking Analytics

**Turning ride-booking data into actionable business insights using SQL, Python, MySQL, and Streamlit.**

## Overview

Ride-booking businesses need to understand booking performance, cancellations, vehicle usage, and customer demand to make better operational decisions.

This project analyzes 150,000 ride-booking records to explore operational patterns and present key metrics through an interactive dashboard. It combines SQL queries, Python-based data analysis, MySQL integration, and data visualization in a single analytics project.

## Business Questions

This analysis explores questions such as:

- What proportion of bookings are completed, cancelled, or assigned other statuses?
- What cancellation reasons are recorded most frequently?
- How does booking activity vary across vehicle types?
- At what times is booking demand highest?
- How do booking trends change over time?
- Which metrics can help monitor ride-booking operations?

## Technology Stack

- **Python:** Data analysis and processing
- **Pandas and NumPy:** Data manipulation
- **SQL and MySQL:** Database management and business analysis
- **Matplotlib and Seaborn:** Data visualization
- **Plotly:** Interactive charts, where used
- **Streamlit:** Interactive dashboard

## Project Structure

```text
44877/
├── data/
│   └── archive/
│       └── ncr_ride_bookings.csv
├── python/
│   ├── 01_inspect_data.py
│   ├── 02_business_insights.py
│   ├── 03_visualizations.py
│   ├── 04_load_data_to_mysql.py
│   └── app.py
├── sql/
│   ├── 01_setup.sql
│   └── 02_business_analysis.sql
├── visualizations/
│   ├── 01_booking_status.png
│   ├── 02_vehicle_performance.png
│   ├── 03_hourly_demand.png
│   ├── 04_cancellation_reasons.png
│   └── 05_monthly_trends.png
├── screenshots/
│   └── dashboard.png
├── .gitignore
├── requirements.txt
└── README.md
```

## Analysis Workflow

### Data Exploration
Inspected the dataset structure and explored booking records to prepare the data for analysis.

### SQL Business Analysis
Used SQL queries to investigate booking statuses, cancellations, vehicle usage, and booking trends.

### Python Analysis
Used Python to examine business metrics, process data, and explore patterns in ride-booking activity.

### Data Visualization
Created charts to make booking performance, cancellation patterns, vehicle comparisons, and demand trends easier to understand.

### Interactive Dashboard
Developed a Streamlit dashboard that brings key metrics and visualizations together in one interface.

## Dashboard Features

- Booking-status filtering
- Vehicle-type filtering
- Date-range selection
- Total bookings and completed rides
- Overall cancellation rate
- Average completed booking value
- Booking-status and vehicle-performance charts
- Daily booking trends and peak-hour analysis
- Business insights based on selected filters
- CSV export of filtered booking records



## Key Metrics

Initial results from the full dataset:

| Metric | Value |
|---|---:|
| Total bookings | 150,000 |
| Completed rides | 93,000 |
| Overall cancellation rate | 25.0% |
| Average completed booking value | 508.18 |

These metrics describe the initial analysis and should match the final project output before publication. The booking value is shown in the dataset's recorded units.

## Business Value

The project demonstrates how operational booking data can be organized and analyzed to support questions about service performance, cancellations, vehicle usage, and demand.

The dashboard allows users to explore selected booking records and compare metrics across filters, while the SQL and Python scripts provide the underlying analytical workflow.

## Dataset

**NCR Ride Bookings**

Source: [Uber Ride Analytics Dashboard — Kaggle](https://www.kaggle.com/datasets/yashdevladdha/uber-ride-analytics-dashboard)

The dataset contains ride-booking records used to analyze booking statuses, vehicle types, booking values, cancellations, and demand patterns.

The application expects the dataset at:

`data/archive/ncr_ride_bookings.csv`

Dataset redistribution is subject to the original source's licensing and terms.

## Run Locally

### Requirements
- Python
- The project dataset
- MySQL Server for database-related functionality

### Install dependencies

```bash
pip install -r requirements.txt
```

### Launch the dashboard

Run the following command from the project root:

```bash
streamlit run python/app.py
```

Open the local URL provided by Streamlit to explore the dashboard.

MySQL-based functionality requires the database to be configured for the local environment. Database credentials should be kept out of version control.

## Skills Demonstrated

- SQL querying and business analysis
- Python-based data analysis
- Data visualization
- MySQL database integration
- Interactive dashboard development
- Translating operational data into business questions

## Author

Narayanamma Reddycharla
