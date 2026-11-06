$ErrorActionPreference = "Stop"

Write-Host "1/5 Starting Postgres..."
docker compose up -d

Write-Host "2/5 Extracting data..."
python src\extract.py

Write-Host "3/5 Loading raw data..."
python src\load.py

Write-Host "4/5 Running dbt models..."
Push-Location dbt_project
dbt run
Write-Host "5/5 Running dbt tests..."
dbt test
Pop-Location

Write-Host "Done. Start the dashboard with: streamlit run dashboard\app.py"