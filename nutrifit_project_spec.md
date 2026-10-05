NutriFit Data Project specifications

1. The idea of this project is to learn PySpark and Databricks, based on real data. I have 3 files generate with a script with Python:
- daily_activity.csv with information about user activity in terms of steps, distance, active status, distance status and calories;
- daily_nutrition.csv with users meals by type: breakfast, snack, lunch and dinner on 3 months;
- users_profile.json with information related to users, like id, name, age, weight, height, daily calorie goal, and daily step goal.
	Based on the file mentioned, I want to organized the data in structured tables and generate reports. For example:
[ 1. Raw data ] > Simulating fitness and nutrition data         
[ 2. Processing in Databricks ] > Ingest data -> Cleaning data -> Grouping by arhitecture layers        
[ 3. Output ] > Reports and Dashboards 

2. Data is organized in Medallion Architecture. In Databricks, processing is done in 3 steps:
┌──────────────────────────────────────────────────────────────────────────────────┐
│                              MEDALLION ARCHITECTURE                              │
├──────────────────────────┬──────────────────────────┬────────────────────────────┤
│ 🥉 BRONZE Layer          │ 🥈 SILVER Layer          │ 🥇 GOLD Layer             │
│ (Raw Data)               │ (Clean Data)             │ (Final Reporting Data)     │
├──────────────────────────┼──────────────────────────┼────────────────────────────┤
│ • Saving exact data as   │ • Removing errors and    │ • Calculating daily        │
│   received from the app/ │   duplicates.            │   averages and totals.     │
│   watch.                 │ • Validating calorie     │ • Structuring data into    │
│ • Nothing is deleted.    │   values.                │   reporting tables.        │
└──────────────────────────┴──────────────────────────┴────────────────────────────┘
3. Components:
a. Data Generator (Source):
	- Python script that creates fake users, their meals and daily steps counts.

b. Automated Ingestion (Auto Loader):
	- Ingests new files directly into the Bronze Layer.

c. Data Cleaning & Quality Control (Delta Live Tables):
	- Automated rules that eliminate invalid records (e.g., negative calorie values or missing user names);
	- Saves validated data into the Silver Layer.

d. Data Modeling for Analytics (Star Schema):
	- Building the final tables in the Gold Layer:
		- Fact Table: Daily summary (total steps, total calories burned and consumed);
		- Dimension Tables: User and food items lists.

e. Governance & Security (Unity Catalog):
	- Organizing everything under a central catalog (nutrifit_catalog) and defining access control policies (Data Analysts only have access to the final Gold Layer).

f. Workflow Automation (Databricks Workflows):
	- Scheduling an automated pipeline that runs once a day without manual intervention.

4. GitHub Project Structure (File Organization)
nutrifit-data-platform/
│
├── README.md                # Project overview (purpose & workflow)
│
├── generate_date/           # Python script generating data
│
├── databricks_notebooks/    # tep 1(Bronze), Step 2 Silver) and Step 3(Gold)
│
└── securitate_si_joburi/    # Databricks security and workflow automation settings