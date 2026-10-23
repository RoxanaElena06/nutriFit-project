# NutriFit Data Project specifications

## What this project does
The idea of this project is to learn PySpark and Databricks, based on real data. I have 3 files generated with a script with Python. Based on the file mentioned, I want to organize the data in structured tables and generate reports.
- 'daily_activity.csv' with information about user activity in terms of steps, distance, active status, distance status and calories;
- 'daily_nutrition.csv' with users meals by type: breakfast, snack, lunch and dinner on 3 months;
- 'users_profiles.json' with information related to users, like id, name, age, weight, height, daily calorie goal, and daily step goal.
For example: 
```
Raw data (Python generator) -> Databricks (ingest -> clean -> grouping by architecture layers) -> Reports & dashboards
```

## Data is organized in Medallion Architecture. In Databricks, processing is done in 3 steps: 
| Layer | Purpose | What happens |
|---|---|---|
| Bronze | Raw data | Saving exact data as received; nothing is deleted |
| Silver | Clean data | Duplicates removed, invalid calorie values filtered, users without a name removed, orphan records removed, column names standardized |
| Gold | Reporting data | Calculating daily averages and totals; structuring data into reporting tables |

## Components: 
| Component | Status |
|---|---|
| Data generator (Python) | Done |
| Bronze layer (PySpark, batch) | Done |
| Silver layer (PySpark, batch) | Done |
| Gold layer (star schema: fact_daily_summary, fact_meals, dim_users, dim_foods) | Done |
| Automated ingestion with Auto Loader | Planned |
| Data quality with Lakeflow Spark Declarative Pipelines (expectations) | Planned |
| Governance with Unity Catalog (Data Analyst access to Gold only) | Planned |
| Daily orchestration with Lakeflow Jobs | Planned |

## GitHub Project Structure 
```
nutrifit-data-platform/
├── README.md               # Project overview (purpose & workflow)
├── data_generator/         # Python script generating data
├── databricks_notebooks/   # step 1(Bronze), Step 2 Silver) and Step 3(Gold)
└── security_and_jobs/      # Unity Catalog and job configuration
```
## Notes
- I have 48 days with meals but no activity, so in 'Fact table' I keep all days with nutrition data (left join). I add has_activit column with true for metrics that need activity data, such as calorie balance.