#!/usr/bin/env python3
"""
Fetch boatrace information from BoatraceCSV
"""

import argparse
import csv
import sys
from datetime import datetime, timedelta
from io import StringIO
from urllib.request import urlopen
from urllib.error import URLError

# Stadium name to ID mapping
STADIUM_NAMES = {
    "桐生": "01", "戸田": "02", "江戸川": "03", "平和島": "04",
    "多摩川": "05", "浜名湖": "06", "蒲郡": "07", "常滑": "08",
    "津": "09", "三国": "10", "びわこ": "11", "住之江": "12",
    "尼崎": "13", "鳴門": "14", "丸亀": "15", "児島": "16",
    "宮島": "17", "徳山": "18", "下関": "19", "若松": "20",
    "芦屋": "21", "福岡": "22", "唐津": "23", "大村": "24",
}

def parse_date(date_str):
    """
    Parse date string to datetime object
    Supports: 'today', 'tomorrow', or 'YYYY-MM-DD'
    """
    today = datetime.now().date()
    
    if date_str.lower() == 'today':
        return today
    elif date_str.lower() == 'tomorrow':
        return today + timedelta(days=1)
    else:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}. Use 'today', 'tomorrow', or 'YYYY-MM-DD'")

def stadium_name_to_id(stadium_name):
    """
    Convert stadium name to ID
    """
    if stadium_name not in STADIUM_NAMES:
        available = ', '.join(STADIUM_NAMES.keys())
        raise ValueError(f"Unknown stadium: {stadium_name}. Available: {available}")
    return STADIUM_NAMES[stadium_name]

def build_url(data_type, date_obj):
    """
    Build BoatraceCSV URL
    """
    year = date_obj.strftime('%Y')
    month = date_obj.strftime('%m')
    day = date_obj.strftime('%d')
    
    base_url = "https://boatracecsv.github.io/data"
    
    if data_type == 'programs':
        return f"{base_url}/programs/{year}/{month}/{day}.csv"
    elif data_type == 'previews':
        return f"{base_url}/previews/{year}/{month}/{day}.csv"
    elif data_type == 'results':
        return f"{base_url}/results/{year}/{month}/{day}.csv"
    elif data_type == 'estimates':
        return f"{base_url}/estimate/{year}/{month}/{day}.csv"
    elif data_type == 'confirms':
        return f"{base_url}/confirm/{year}/{month}/{day}.csv"
    else:
        raise ValueError(f"Unknown data type: {data_type}")

def fetch_csv(url):
    """
    Fetch CSV from URL
    """
    try:
        with urlopen(url) as response:
            content = response.read().decode('utf-8')
            return content
    except URLError as e:
        raise Exception(f"Failed to fetch from {url}: {e}")

def filter_data(csv_content, stadium_name=None, race_number=None):
    """
    Filter CSV data by stadium and race number
    Returns list of dicts with filtered rows
    """
    reader = csv.DictReader(StringIO(csv_content))
    rows = list(reader)

    if not rows:
        return []

    # Filter by stadium name
    if stadium_name:
        # Convert stadium name to full name (e.g., "平和島" -> "ボートレース平和島")
        full_stadium_name = f"ボートレース{stadium_name}"
        rows = [r for r in rows if r.get("レース場") == full_stadium_name]

    # Filter by race number
    if race_number:
        # Convert race number to full format (e.g., 10 -> "10R")
        race_format = f"{race_number}R"
        rows = [r for r in rows if r.get("レース回") == race_format]

    return rows

def main():
    parser = argparse.ArgumentParser(description='Fetch boatrace information from BoatraceCSV')
    parser.add_argument('--date', required=True, help="Date: 'today', 'tomorrow', or 'YYYY-MM-DD'")
    parser.add_argument('--data-type', required=True, 
                       choices=['programs', 'previews', 'results', 'estimates', 'confirms'],
                       help='Type of data to fetch')
    parser.add_argument('--stadium', help='Stadium name (e.g., 平和島, 戸田)')
    parser.add_argument('--race', type=int, help='Race number (1-12)')
    parser.add_argument('--output-format', choices=['csv', 'json'], default='csv',
                       help='Output format')
    
    args = parser.parse_args()
    
    try:
        # Parse date
        date_obj = parse_date(args.date)

        # Validate stadium name if provided
        if args.stadium:
            stadium_name_to_id(args.stadium)  # This will raise if invalid

        # Build URL and fetch data
        url = build_url(args.data_type, date_obj)
        csv_content = fetch_csv(url)

        # Filter data
        rows = filter_data(csv_content, args.stadium, args.race)
        
        if not rows:
            print("No data found matching the criteria", file=sys.stderr)
            sys.exit(1)
        
        # Output results
        if args.output_format == 'json':
            import json
            print(json.dumps(rows, ensure_ascii=False, indent=2))
        else:
            # CSV output
            if rows:
                writer = csv.DictWriter(sys.stdout, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
