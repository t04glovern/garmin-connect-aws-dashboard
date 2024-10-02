# Evidence Garmin

## Create DuckDB Database

Run the [app.py](../duckdb/app.py) script to create the DuckDB database.

```bash
cd ../duckdb
python app.py
```

Copy the DuckDB database to the evidence directory.

```bash
cp garmin.duckdb ../evidence/sources/garmin/garmin.duckdb
```

## Run Evidence

```bash
npm install
npm run sources
npm run dev -- --host 0.0.0.0
```
