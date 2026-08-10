import duckdb
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WAREHOUSE = ROOT / "warehouse" / "airline_weather.duckdb"


con = duckdb.connect(WAREHOUSE)

con.execute("CALL start_ui();")


print("DuckDB UI: http://localhost:4213")
input("Press Enter to stop the UI...")