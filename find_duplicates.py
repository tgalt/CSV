#!/usr/bin/env python3
"""
Simple script to find duplicate rows in a CSV file, ignoring the invoice column.
"""

import csv
import sys
from pathlib import Path

def find_duplicates(filename, invoice_column='InvNo'):
    """
    Find duplicate rows in a CSV file, ignoring the invoice column.
    
    Args:
        filename: Path to the CSV file
        invoice_column: Name of the invoice column to ignore (default: 'InvNo')
    """
    duplicates = []
    seen_rows = {}
    all_rows = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Get all column names
            if not reader.fieldnames:
                print("Error: Could not read column headers from CSV file.")
                return
            
            fieldnames = reader.fieldnames
            columns_to_check = [col for col in fieldnames if col != invoice_column]
            
            # Process each row
            for row_num, row in enumerate(reader, start=2):  # start=2 because row 1 is header
                all_rows.append((row_num, row))
                
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
                        'duplicate_group': seen_rows[row_key]['group_id'],
                        'row_data': row,
                        'data': {col: row.get(col, '') for col in columns_to_check[:3]}  # Show first 3 columns
                    })
                else:
                    # Store this row for future comparison
                    group_id = len(seen_rows) + 1
                    seen_rows[row_key] = {
                        'row_num': row_num,
                        'invoice': row.get(invoice_column, ''),
                        'group_id': group_id
                    }
        
        # Report results
        print(f"\n{'='*70}")
        print(f"Duplicate Analysis for: {filename}")
        print(f"{'='*70}")
        print(f"Total unique row patterns: {len(seen_rows)}")
        print(f"Total duplicates found: {len(duplicates)}")
        print(f"{'='*70}\n")
        
        if duplicates:
            # Write duplicates to CSV file
            output_filename = f"duplicates_{Path(filename).stem}.csv"
            
            # Collect all duplicate rows including the first occurrence
            duplicate_rows_to_write = []
            duplicate_groups = {}
            
            # Group duplicates
            for dup in duplicates:
                group_id = dup['duplicate_group']
                if group_id not in duplicate_groups:
                    duplicate_groups[group_id] = {
                        'first_row': dup['first_row'],
                        'rows': []
                    }
                duplicate_groups[group_id]['rows'].append({
                    'row_num': dup['current_row'],
                    'data': dup['row_data']
                })
            
            # Build output rows with group information
            for group_id, group_info in duplicate_groups.items():
                # Find the first occurrence
                first_row_num = group_info['first_row']
                first_row_data = None
                for row_num, row in all_rows:
                    if row_num == first_row_num:
                        first_row_data = row
                        break
                
                if first_row_data:
                    duplicate_rows_to_write.append({
                        'DuplicateGroup': group_id,
                        'OriginalRow': first_row_num,
                        **first_row_data
                    })
                
                # Add all duplicate occurrences
                for dup_row in group_info['rows']:
                    duplicate_rows_to_write.append({
                        'DuplicateGroup': group_id,
                        'OriginalRow': first_row_num,
                        **dup_row['data']
                    })
            
            # Write to CSV
            if duplicate_rows_to_write:
                output_fieldnames = ['DuplicateGroup', 'OriginalRow'] + list(fieldnames)
                with open(output_filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=output_fieldnames)
                    writer.writeheader()
                    writer.writerows(duplicate_rows_to_write)
                
                print(f"✓ Duplicate rows written to: {output_filename}")
                print(f"  Total rows in output file: {len(duplicate_rows_to_write)}\n")
            
            # Print summary
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
