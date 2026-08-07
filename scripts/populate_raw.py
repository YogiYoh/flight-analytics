import duckdb
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WAREHOUSE = ROOT / "warehouse" / "airline_weather.duckdb"
DATA_DIR = ROOT / "data"

con = duckdb.connect(WAREHOUSE)

con.execute(
    """
    CREATE SCHEMA IF NOT EXISTS RAW
    """
)


con.execute(
    f"""
    CREATE OR REPLACE TABLE raw.on_time_performance AS
    SELECT *
    FROM read_csv_auto(
        '{DATA_DIR}/On_Time_Reporting_Carrier_On_Time_Performance_*.csv',
        union_by_name = true,
        filename = true
    );
    """  
)

con.execute(
    f"""
    CREATE OR REPLACE TABLE raw.noaa_ghcnh_hourly AS
    SELECT *
    FROM read_parquet(
        '{DATA_DIR}/GHCNh_*.parquet',
        union_by_name = true,
        filename = true
    );
    """  
)

rows, months = con.execute("""
    SELECT count(*), count(DISTINCT Month) FROM raw.on_time_performance
""").fetchone()
print(f"raw.on_time_performance: {rows:,} rows across {months} months")

rows, stations = con.execute("""
    SELECT count(*), count(DISTINCT STATION) FROM raw.noaa_ghcnh_hourly
""").fetchone()
print(f"raw.noaa_ghcnh_hourly: {rows:,} rows across {stations} stations")


con.close()
