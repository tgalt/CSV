#!/usr/bin/env python3
"""
pdf_to_csv.py — Extract tables from a PDF and save as CSV.

Engines supported:
  - camelot   (pip install camelot-py; requires Ghostscript)
  - tabula    (pip install tabula-py; requires Java)
  - plumber   (pip install pdfplumber; pure Python fallback)

Examples:
  python pdf_to_csv.py input.pdf -o out.csv
  python pdf_to_csv.py input.pdf -o out.csv --engine camelot --flavor lattice --pages 1-3
  python pdf_to_csv.py input.pdf --engine tabula --pages all --per-table
  python pdf_to_csv.py input.pdf --engine plumber --pages 2

Notes:
  - For scanned PDFs (images), run OCR first (e.g., `ocrmypdf input.pdf ocr.pdf`) or
    use Tesseract-based pipelines—table extractors need text.
"""

import argparse
import os
import sys

def parse_args():
    p = argparse.ArgumentParser(description="Convert PDF tables to CSV.")
    p.add_argument("pdf", help="Path to input PDF")
    p.add_argument("-o", "--output", help="Output CSV path (combined). If omitted with --per-table, files are numbered next to the PDF.")
    p.add_argument("--engine", choices=["camelot", "tabula", "plumber"], default="camelot",
                   help="Extraction engine to use (default: camelot).")
    p.add_argument("--pages", default="all", help="Pages spec (e.g., 'all', '1', '1-3', '1,3,5')")
    p.add_argument("--flavor", choices=["lattice", "stream"], default="lattice",
                   help="Table detection flavor (camelot/tabula). lattice needs ruling lines; stream uses text alignment.")
    p.add_argument("--area", nargs="+", default=None,
                   help="Table area(s) as top,left,bottom,right in PDF points (multiple allowed).")
    p.add_argument("--password", default=None, help="PDF password if encrypted.")
    p.add_argument("--per-table", action="store_true",
                   help="Write one CSV per detected table instead of combining.")
    p.add_argument("--encoding", default="utf-8", help="CSV encoding (default: utf-8)")
    p.add_argument("--delimiter", default=",", help="CSV delimiter (default: ,)")
    return p.parse_args()

def pages_to_str(pages):
    return str(pages)

def out_base_paths(pdf_path, output, per_table):
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    if per_table:
        outdir = os.path.dirname(output) if output else os.path.dirname(pdf_path)
        return os.path.join(outdir, base + "_table")
    else:
        return output or os.path.join(os.path.dirname(pdf_path), base + ".csv")

def write_combined_csv(dfs, out_path, encoding="utf-8", delimiter=","):
    import pandas as pd
    if not dfs:
        raise RuntimeError("No tables found.")
    # Normalize columns to max width
    max_cols = max(df.shape[1] for df in dfs)
    normed = []
    for df in dfs:
        if df.shape[1] < max_cols:
            # pad with empty columns
            for i in range(max_cols - df.shape[1]):
                df[f"_pad{i}"] = ""
        normed.append(df)
    combined = pd.concat(normed, ignore_index=True)
    combined.to_csv(out_path, index=False, encoding=encoding, sep=delimiter)

def write_per_table_csv(dfs, base_path, encoding="utf-8", delimiter=","):
    paths = []
    for i, df in enumerate(dfs, 1):
        path = f"{base_path}_{i}.csv"
        df.to_csv(path, index=False, encoding=encoding, sep=delimiter)
        paths.append(path)
    return paths

def extract_with_camelot(args):
    try:
        import camelot
    except ImportError:
        raise RuntimeError("camelot not installed. Try: pip install camelot-py")
    kw = {
        "pages": pages_to_str(args.pages),
        "flavor": args.flavor,
    }
    if args.password:
        kw["password"] = args.password
    if args.area:
        # camelot expects list of strings like "top,left,bottom,right"
        kw["table_areas"] = args.area
    tables = camelot.read_pdf(args.pdf, **kw)
    dfs = [t.df for t in tables]
    return dfs

def extract_with_tabula(args):
    try:
        import tabula
    except ImportError:
        raise RuntimeError("tabula-py not installed. Try: pip install tabula-py (requires Java)")
    # area can be a list of lists of floats
    area = None
    if args.area:
        area = []
        for a in args.area:
            parts = [float(x) for x in a.split(",")]
            if len(parts) != 4:
                raise RuntimeError(f"Bad --area '{a}', use top,left,bottom,right")
            area.append(parts)
    dfs = tabula.read_pdf(
        args.pdf,
        pages=pages_to_str(args.pages),
        stream=(args.flavor == "stream"),
        lattice=(args.flavor == "lattice"),
        guess=(args.flavor == "stream"),
        area=area,
        password=args.password,
        multiple_tables=True,
        pandas_options={"dtype": str},
    )
    return dfs

def extract_with_plumber(args):
    try:
        import pdfplumber
        import pandas as pd
    except ImportError:
        raise RuntimeError("pdfplumber not installed. Try: pip install pdfplumber pandas")
    dfs = []
    page_idxs = None
    if args.pages == "all":
        page_idxs = None  # handle after opening
    else:
        # parse simple specs like '1', '1-3', '1,3,5'
        target = []
        for token in args.pages.split(","):
            token = token.strip()
            if "-" in token:
                a, b = token.split("-", 1)
                target.extend(range(int(a), int(b) + 1))
            else:
                target.append(int(token))
        # convert to zero-based later
        page_idxs = sorted(set(target))
    with pdfplumber.open(args.pdf, password=args.password) as pdf:
        chosen = range(1, len(pdf.pages) + 1) if page_idxs is None else page_idxs
        # default table settings—tweak as needed
        table_settings = {
            "vertical_strategy": "lines",
            "horizontal_strategy": "lines",
            "intersection_x_tolerance": 5,
            "intersection_y_tolerance": 5,
            "snap_tolerance": 3,
            "join_tolerance": 3,
            "edge_min_length": 3,
            "min_words_vertical": 1,
            "min_words_horizontal": 1,
            "keep_blank_chars": True,
            "text_x_tolerance": 2,
            "text_y_tolerance": 2,
        }
        for pno in chosen:
            page = pdf.pages[pno - 1]
            # pdfplumber uses extract_tables; returns list of 2D lists
            tables = page.extract_tables(table_settings=table_settings)
            for tbl in tables:
                # normalize to DataFrame
                dfs.append(pd.DataFrame(tbl))
    return dfs

def main():
    args = parse_args()
    if not os.path.isfile(args.pdf):
        print(f"Input not found: {args.pdf}", file=sys.stderr)
        sys.exit(1)

    if args.engine == "camelot":
        extractor = extract_with_camelot
    elif args.engine == "tabula":
        extractor = extract_with_tabula
    else:
        extractor = extract_with_plumber

    try:
        dfs = extractor(args)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(2)

    if not dfs:
        print("No tables found.", file=sys.stderr)
        sys.exit(3)

    base = out_base_paths(args.pdf, args.output, args.per_table)
    try:
        if args.per_table:
            paths = write_per_table_csv(dfs, base, encoding=args.encoding, delimiter=args.delimiter)
            print("\n".join(paths))
        else:
            out_path = base
            write_combined_csv(dfs, out_path, encoding=args.encoding, delimiter=args.delimiter)
            print(out_path)
    except Exception as e:
        print(f"[ERROR writing CSV] {e}", file=sys.stderr)
        sys.exit(4)

if __name__ == "__main__":
    main()
