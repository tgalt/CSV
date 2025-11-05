#!/usr/bin/env python3
"""
Simple script to import data from input.csv into a SQLite database.
"""

import sqlite3
import csv

def import_csv_to_sqlite(csv_file='input.csv', db_file='database.db', table_name='invoices'):
    """
    Import CSV data into SQLite database.
    
    Args:
        csv_file: Path to the CSV file
        db_file: Path to the SQLite database file
        table_name: Name of the table to create
    """
    print(f"Reading data from {csv_file}...")
    
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Read CSV file
    with open(csv_file, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        
        # Get headers from first row
        headers = next(csv_reader)
        
        # Clean up header names (remove special characters, spaces, etc.)
        clean_headers = []
        for header in headers:
            # Replace spaces and special characters with underscores
            clean_header = header.strip().replace(' ', '_').replace('?', '').replace('/', '_').replace(',', '').replace(':', '').replace('.', '').replace('-', '_')
            # Remove any remaining problematic characters
            clean_header = ''.join(c if c.isalnum() or c == '_' else '_' for c in clean_header)
            clean_headers.append(clean_header or f'column_{len(clean_headers)}')
        
        print(f"Found {len(clean_headers)} columns: {', '.join(clean_headers[:5])}...")
        
        # Drop table if it exists
        cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
        
        # Create table with all columns as TEXT type
        columns_def = ', '.join([f'"{header}" TEXT' for header in clean_headers])
        create_table_sql = f'CREATE TABLE {table_name} ({columns_def})'
        cursor.execute(create_table_sql)
        print(f"Created table: {table_name}")
        
        # Prepare INSERT statement
        placeholders = ', '.join(['?' for _ in clean_headers])
        insert_sql = f'INSERT INTO {table_name} VALUES ({placeholders})'
        
        # Insert data
        row_count = 0
        for row in csv_reader:
            # Pad row with empty strings if it has fewer columns than headers
            while len(row) < len(clean_headers):
                row.append('')
            # Truncate row if it has more columns than headers
            row = row[:len(clean_headers)]
            
            cursor.execute(insert_sql, row)
            row_count += 1
            
            # Print progress every 1000 rows
            if row_count % 1000 == 0:
                print(f"Inserted {row_count} rows...")
        
        # Commit changes
        conn.commit()
        print(f"\nSuccessfully imported {row_count} rows into {db_file}")
        
        # Show some statistics
        cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
        total_rows = cursor.fetchone()[0]
        print(f"Total rows in database: {total_rows}")
    
    # Close connection
    conn.close()
    print(f"Database connection closed. Data saved to {db_file}")

if __name__ == '__main__':
    import_csv_to_sqlite()
