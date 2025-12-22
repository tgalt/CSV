#!/usr/bin/env python3
"""Find duplicate rows in a CSV file, ignoring the invoice column."""

import csv
import sys
from pathlib import Path


def find_duplicates(filename, invoice_column='InvNo'):
    """Find duplicate rows in a CSV file, ignoring the invoice column."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            if not reader.fieldnames:
                print("Error: Could not read column headers from CSV file.")
                return
            
            fieldnames = list(reader.fieldnames)
            columns_to_check = [col for col in fieldnames if col != invoice_column]
            
            # Track seen rows and all rows
            seen = {}
            all_rows = []
            duplicates = []
            
            for row_num, row in enumerate(reader, start=2):
                all_rows.append((row_num, row))
                
                # Create key from all columns except invoice
                key = tuple(row.get(col, '').strip() for col in columns_to_check)
                
                if key in seen:
                    duplicates.append((row_num, seen[key], row))
                else:
                    seen[key] = row_num
        
        # Print summary
        print(f"\n{'='*70}")
        print(f"Duplicate Analysis for: {filename}")
        print(f"{'='*70}")
        print(f"Total unique row patterns: {len(seen)}")
        print(f"Total duplicates found: {len(duplicates)}")
        print(f"{'='*70}\n")
        
        if duplicates:
            # Write duplicates to CSV
            output_filename = f"duplicates_{Path(filename).stem}.csv"
            output_rows = []
            
            # Group duplicates by original row
            groups = {}
            for dup_row_num, orig_row_num, row_data in duplicates:
                if orig_row_num not in groups:
                    groups[orig_row_num] = []
                groups[orig_row_num].append((dup_row_num, row_data))
            
            # Build output with original and duplicate rows
            for group_id, (orig_row_num, group_dups) in enumerate(groups.items(), start=1):
                # Find original row
                orig_row = next(row for num, row in all_rows if num == orig_row_num)
                output_rows.append({'DuplicateGroup': group_id, 'OriginalRow': orig_row_num, **orig_row})
                
                # Add duplicate rows
                for dup_row_num, dup_row in group_dups:
                    output_rows.append({'DuplicateGroup': group_id, 'OriginalRow': orig_row_num, **dup_row})
            
            # Write output file
            with open(output_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['DuplicateGroup', 'OriginalRow'] + fieldnames)
                writer.writeheader()
                writer.writerows(output_rows)
            
            print(f"✓ Duplicate rows written to: {output_filename}")
            print(f"  Total rows in output file: {len(output_rows)}\n")
            
            # Print duplicate details
            print("Duplicate rows found:\n")
            for i, (dup_row, orig_row, row_data) in enumerate(duplicates, 1):
                sample = {col: row_data.get(col, '') for col in columns_to_check[:3]}
                print(f"Duplicate #{i}:")
                print(f"  Row {dup_row} (Invoice: {row_data.get(invoice_column, '')})")
                print(f"  matches Row {orig_row}")
                print(f"  Sample data: {sample}\n")
        else:
            print("✓ No duplicate rows found (ignoring invoice column)!")
            
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.csv'
    find_duplicates(filename)
