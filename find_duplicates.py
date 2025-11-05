#!/usr/bin/env python3
"""
Simple script to find duplicate rows in a CSV file, ignoring the invoice column.
"""

import csv
import sys

def find_duplicates(filename, invoice_column='InvNo'):
    """
    Find duplicate rows in a CSV file, ignoring the invoice column.
    
    Args:
        filename: Path to the CSV file
        invoice_column: Name of the invoice column to ignore (default: 'InvNo')
    """
    duplicates = []
    seen_rows = {}
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Get all column names except the invoice column
            if reader.fieldnames:
                columns_to_check = [col for col in reader.fieldnames if col != invoice_column]
            else:
                print("Error: Could not read column headers from CSV file.")
                return
            
            # Process each row
            for row_num, row in enumerate(reader, start=2):  # start=2 because row 1 is header
                # Create a tuple of values (excluding invoice column) to use as a key
                row_key = tuple(row.get(col, '').strip() for col in columns_to_check)
                
                # Check if we've seen this combination before
                if row_key in seen_rows:
                    # This is a duplicate
                    duplicates.append({
                        'current_row': row_num,
                        'current_invoice': row.get(invoice_column, ''),
                        'first_row': seen_rows[row_key]['row_num'],
                        'first_invoice': seen_rows[row_key]['invoice'],
                        'data': {col: row.get(col, '') for col in columns_to_check[:3]}  # Show first 3 columns
                    })
                else:
                    # Store this row for future comparison
                    seen_rows[row_key] = {
                        'row_num': row_num,
                        'invoice': row.get(invoice_column, '')
                    }
        
        # Report results
        print(f"\n{'='*70}")
        print(f"Duplicate Analysis for: {filename}")
        print(f"{'='*70}")
        print(f"Total unique row patterns: {len(seen_rows)}")
        print(f"Total duplicates found: {len(duplicates)}")
        print(f"{'='*70}\n")
        
        if duplicates:
            print("Duplicate rows found:\n")
            for i, dup in enumerate(duplicates, 1):
                print(f"Duplicate #{i}:")
                print(f"  Row {dup['current_row']} (Invoice: {dup['current_invoice']})")
                print(f"  matches Row {dup['first_row']} (Invoice: {dup['first_invoice']})")
                print(f"  Sample data: {dup['data']}")
                print()
        else:
            print("✓ No duplicate rows found (ignoring invoice column)!")
            
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    # Default to input.csv
    filename = 'input.csv'
    
    # Allow user to specify a different file via command line
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    find_duplicates(filename)
