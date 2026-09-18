import os
import sqlite3

print("--- CHECKING PROJECT FILES ---")
required_files = [
    'data/raw/vendors.csv', 'data/processed/vendors.csv', 'procureflow.db',
    'database/schema.sql', 'database/indexes.sql',
    'sql/01_data_quality.sql', 'sql/02_procurement_kpis.sql', 'sql/03_vendor_analysis.sql',
    'sql/04_delivery_analysis.sql', 'sql/05_cost_analysis.sql', 'sql/06_pareto_analysis.sql',
    'sql/07_process_analysis.sql', 'sql/08_advanced_analysis.sql',
    'python/generate_data.py', 'python/clean_data.py', 'python/exploratory_analysis.py',
    'dashboard/app.py', 'documentation/business_problem.md', 'documentation/data_dictionary.md',
    'documentation/kpi_definitions.md', 'documentation/data_quality_report.md',
    'documentation/root_cause_analysis.md', 'documentation/recommendations.md',
    'documentation/consulting_case_study.md', 'interview_prep/interview_questions.md',
    'requirements.txt', 'README.md', '.gitignore'
]

missing = [f for f in required_files if not os.path.exists(f)]
if missing:
    print("MISSING FILES:", missing)
else:
    print("ALL 28 PROJECT FILES PRESENT AND VERIFIED!")

conn = sqlite3.connect('procureflow.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("DATABASE TABLES:", [t[0] for t in tables])

cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
views = cursor.fetchall()
print("DATABASE VIEWS:", [v[0] for v in views])
conn.close()
