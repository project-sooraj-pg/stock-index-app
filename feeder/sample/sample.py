import duckdb
import json

data = [
    {"ticker": "A", "name": "Agilent Technologies Inc.", "market": "stocks", "locale": "us", "primary_exchange": "XNYS", "type": "CS", "active": True, "currency_name": "usd", "cik": "0001090872", "composite_figi": "BBG000C2V3D6", "share_class_figi": "BBG001SCTQY4", "last_updated_utc": "2025-12-20T07:06:20.399238389Z"},
    {"ticker": "AA", "name": "Alcoa Corporation", "market": "stocks", "locale": "us", "primary_exchange": "XNYS", "type": "CS", "active": True, "currency_name": "usd", "cik": "0001675149", "composite_figi": "BBG00B3T3HD3", "share_class_figi": "BBG00B3T3HF1", "last_updated_utc": "2025-12-20T07:06:20.39923902Z"},
    {"ticker": "AAM", "name": "AA Mission Acquisition Corp.", "market": "stocks", "locale": "us", "primary_exchange": "XNYS", "type": "CS", "active": True, "currency_name": "usd", "cik": "0002012964", "last_updated_utc": "2025-12-20T07:06:20.399240483Z"},
    {"ticker": "AAM.U", "name": "AA Mission Acquisition Corp. Units, each consisting of one Class A Ordinary Share and one-half of one redeemable warrant", "market": "stocks", "locale": "us", "primary_exchange": "XNYS", "type": "UNIT", "active": True, "currency_name": "usd", "cik": "0002012964", "last_updated_utc": "2025-12-20T07:06:20.399240583Z"},
    {"ticker": "AAM.WS", "name": "AA Mission Acquisition Corp. Warrants, each whole warrant entitles the holder to purchase one Class A ordinary share at a price of $11.50 per share", "market": "stocks", "locale": "us", "primary_exchange": "XNYS", "type": "WARRANT", "active": True, "currency_name": "usd", "cik": "0002012964", "last_updated_utc": "2025-12-20T07:06:20.399240964Z"},
    {"ticker": "AAMI", "name": "Acadian Asset Management Inc.", "market": "stocks", "locale": "us", "primary_exchange": "XNYS", "type": "CS", "active": True, "currency_name": "usd", "cik": "0001748824", "composite_figi": "BBG00P2HLNY3", "share_class_figi": "BBG00P2HLNZ2", "last_updated_utc": "2025-12-20T07:06:20.399241204Z"},
    {"ticker": "AAP", "name": "ADVANCE AUTO PARTS INC", "market": "stocks", "locale": "us", "primary_exchange": "XNYS", "type": "CS", "active": True, "currency_name": "usd", "cik": "0001158449", "composite_figi": "BBG000F7RCJ1", "share_class_figi": "BBG001SD2SB2", "last_updated_utc": "2025-12-20T07:06:20.399241495Z"}
]

# Serialize the data to a JSON string
json_str = json.dumps(data)

# Connect to DuckDB in-memory
con = duckdb.connect(database=':memory:')

# Use DuckDB's read_json_auto to load the JSON string as a table
con.execute("""
    CREATE TABLE raw_data AS
    SELECT * FROM read_json_auto(?)
""", [json_str])

# Create companies table (company_id, company_name)
con.execute('''
    CREATE TABLE companies AS
    SELECT ROW_NUMBER() OVER (ORDER BY name) AS company_id, name AS company_name
    FROM raw_data
    GROUP BY name
''')

# Create listings table (listing_id, company_id, ticker_symbol, exchange_code)
con.execute('''
    CREATE TABLE listings AS
    SELECT
        ROW_NUMBER() OVER (ORDER BY ticker) AS listing_id,
        c.company_id,
        r.ticker AS ticker_symbol,
        r.primary_exchange AS exchange_code
    FROM raw_data r
    JOIN companies c ON r.name = c.company_name
''')

# Print the normalized tables
print("Companies:")
print(con.execute("SELECT * FROM companies").fetchdf())
print("\nListings:")
print(con.execute("SELECT * FROM listings").fetchdf())
