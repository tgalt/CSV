#!/usr/bin/env python3
"""
AR Aging vs AR Trial Balance Detail Reconciliation

What it does
- Reads an AR Aging export and an AR Trial Balance Detail export (Excel)
- Normalizes customer/invoice lines
- Reconciles at the invoice level and customer level
- Writes a single Excel workpaper with "All" and "Issues" tabs

Typical use (run from the folder that contains the reports):
    python AR_Aging_ARTB_Recon.py

Optional:
    python AR_Aging_ARTB_Recon.py --aged "AR_AgedInvoiceReport.xlsx" --tb "AR_TrialBalanceDetail.xlsx" --out "AR_Recon_Workpapers.xlsx" --debug
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Reconcile AR Aging vs AR Trial Balance Detail.")
    p.add_argument("--aged", default="AR_AgedInvoiceReport.xlsx", help="Path to AR Aging Excel export.")
    p.add_argument("--tb", default="AR_TrialBalanceDetail.xlsx", help="Path to AR Trial Balance Detail Excel export.")
    p.add_argument("--out", default="", help="Output Excel filename. Default: AR_Recon_Workpapers_YYYYMMDD.xlsx")
    p.add_argument("--debug", action="store_true", help="Print small samples and extra diagnostics.")
    return p.parse_args()


def clean_aging(aged_raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return normalized aging rows and invoice-only rows."""
    aged = aged_raw.rename(columns={
        "Customer/_x000a_Invoice Date": "raw_customer_or_date",
        "Invoice _x000a_Number": "raw_invoice_or_name",
        "_x000a_Balance": "open_amount",
        "Unnamed: 1": "invoice_date",
    }).copy()

    # Customer header rows contain a 7-digit customer number; forward-fill to invoice lines.
    cust_col = aged["raw_customer_or_date"].astype(str)
    mask_code = cust_col.str.match(r"^\d{7}$")

    aged["customer_id"] = np.where(mask_code, cust_col, np.nan)
    aged["customer_name"] = np.where(mask_code, aged["raw_invoice_or_name"], np.nan)

    aged["customer_id"] = aged["customer_id"].ffill()
    aged["customer_name"] = aged["customer_name"].ffill()

    # Invoice lines
    aged["invoice_number"] = aged["raw_invoice_or_name"]
    aged["open_amount"] = pd.to_numeric(aged["open_amount"], errors="coerce")
    aged["invoice_date"] = pd.to_datetime(aged["invoice_date"], errors="coerce")

    aged_inv = aged[
        aged["invoice_number"].notna()
        & aged["open_amount"].notna()
    ].copy()

    return aged, aged_inv


def clean_tb(tb_raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return normalized TB rows and invoice-only rows (headers/totals removed)."""
    tb = tb_raw.rename(columns={
        "CityServiceValcon, LLC (CSV)": "raw_invoice_or_cust",
        "Unnamed: 1": "invoice_date",
        "Unnamed: 6": "open_amount",
    }).copy()

    cust = tb["raw_invoice_or_cust"].astype(str)

    # Customer header rows look like: "0000003 Kalispell 3rd Ave..."
    cust_match = cust.str.extract(r"^(?P<customer_id>\d{7})\s+(?P<customer_name>.+)$")

    tb["customer_id"] = cust_match["customer_id"]
    tb["customer_name"] = cust_match["customer_name"]

    tb["customer_id"] = tb["customer_id"].ffill()
    tb["customer_name"] = tb["customer_name"].ffill()

    tb["invoice_number"] = tb["raw_invoice_or_cust"]
    tb["open_amount"] = pd.to_numeric(tb["open_amount"], errors="coerce")
    tb["invoice_date"] = pd.to_datetime(tb["invoice_date"], errors="coerce")

    tb_inv = tb[tb["open_amount"].notna()].copy()

    # Remove non-invoice lines
    tb_inv = tb_inv[~tb_inv["invoice_number"].astype(str).str.startswith("Customer")]
    tb_inv = tb_inv[~tb_inv["invoice_number"].astype(str).str.match(r"^\d{7}\s+")]
    tb_inv = tb_inv[~tb_inv["invoice_number"].astype(str).str.contains("Report Totals:", na=False)]

    return tb, tb_inv


def build_recons(aged_inv: pd.DataFrame, tb_inv: pd.DataFrame) -> dict[str, pd.DataFrame]:
    # Invoice-level recon
    inv_recon = aged_inv.merge(
        tb_inv[["customer_id", "invoice_number", "open_amount"]],
        on=["customer_id", "invoice_number"],
        how="outer",
        suffixes=("_aged", "_tb"),
    )

    inv_recon["open_amount_aged"] = inv_recon["open_amount_aged"].fillna(0)
    inv_recon["open_amount_tb"] = inv_recon["open_amount_tb"].fillna(0)
    inv_recon["variance"] = inv_recon["open_amount_aged"] - inv_recon["open_amount_tb"]

    inv_issues = inv_recon[inv_recon["variance"].round(2) != 0].copy()
    inv_issues = inv_issues.sort_values(["customer_id", "invoice_number"], kind="mergesort")

    # Customer-level recon
    aged_cust = (
        aged_inv
        .groupby(["customer_id", "customer_name"], as_index=False)["open_amount"]
        .sum()
        .rename(columns={"open_amount": "aged_open_amount"})
    )

    tb_cust = (
        tb_inv
        .groupby(["customer_id", "customer_name"], as_index=False)["open_amount"]
        .sum()
        .rename(columns={"open_amount": "tb_open_amount"})
    )

    cust_recon = aged_cust.merge(
        tb_cust,
        on=["customer_id", "customer_name"],
        how="outer",
    )

    cust_recon[["aged_open_amount", "tb_open_amount"]] = cust_recon[["aged_open_amount", "tb_open_amount"]].fillna(0)
    cust_recon["variance"] = cust_recon["aged_open_amount"] - cust_recon["tb_open_amount"]

    cust_issues = cust_recon[cust_recon["variance"].round(2) != 0].copy()
    cust_issues = cust_issues.sort_values("variance", kind="mergesort")

    return {
        "inv_recon": inv_recon,
        "inv_issues": inv_issues,
        "cust_recon": cust_recon,
        "cust_issues": cust_issues,
    }


def write_workpaper(
    out_path: Path,
    aged_path: Path,
    tb_path: Path,
    aged_inv: pd.DataFrame,
    tb_inv: pd.DataFrame,
    inv_recon: pd.DataFrame,
    inv_issues: pd.DataFrame,
    cust_recon: pd.DataFrame,
    cust_issues: pd.DataFrame,
) -> None:
    aged_total = float(aged_inv["open_amount"].sum())
    tb_total = float(tb_inv["open_amount"].sum())
    diff = aged_total - tb_total

    summary = pd.DataFrame([{
        "run_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "aged_file": str(aged_path),
        "tb_file": str(tb_path),
        "aged_total_open": aged_total,
        "tb_total_open": tb_total,
        "total_variance": diff,
        "invoice_issue_count": int(len(inv_issues)),
        "customer_issue_count": int(len(cust_issues)),
    }])

    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="Summary", index=False)
        inv_recon.to_excel(writer, sheet_name="Invoice_Recon_All", index=False)
        inv_issues.to_excel(writer, sheet_name="Invoice_Issues", index=False)
        cust_recon.to_excel(writer, sheet_name="Customer_Recon_All", index=False)
        cust_issues.to_excel(writer, sheet_name="Customer_Issues", index=False)


def main() -> int:
    args = parse_args()

    aged_path = Path(args.aged).expanduser().resolve()
    tb_path = Path(args.tb).expanduser().resolve()

    if not aged_path.exists():
        raise FileNotFoundError(f"AR Aging file not found: {aged_path}")
    if not tb_path.exists():
        raise FileNotFoundError(f"AR Trial Balance Detail file not found: {tb_path}")

    out_path = Path(args.out) if args.out else Path(f"AR_Recon_Workpapers_{datetime.now():%Y%m%d}.xlsx")
    out_path = out_path.expanduser().resolve()

    # Read
    aged_raw = pd.read_excel(aged_path)
    tb_raw = pd.read_excel(tb_path)

    if args.debug:
        print("Aging raw shape:", aged_raw.shape)
        print("TB raw shape:", tb_raw.shape)
        print("\nAging raw head:\n", aged_raw.head(5))
        print("\nTB raw head:\n", tb_raw.head(5))

    # Clean
    _, aged_inv = clean_aging(aged_raw)
    _, tb_inv = clean_tb(tb_raw)

    # Totals quick-check
    aged_total = float(aged_inv["open_amount"].sum())
    tb_total = float(tb_inv["open_amount"].sum())
    diff = aged_total - tb_total
    print(f"Aging total open: {aged_total:,.2f}")
    print(f"TB total open:    {tb_total:,.2f}")
    print(f"Total variance:   {diff:,.2f}")

    recons = build_recons(aged_inv, tb_inv)

    print(f"Invoice issues:  {len(recons['inv_issues'])}")
    print(f"Customer issues: {len(recons['cust_issues'])}")

    write_workpaper(
        out_path=out_path,
        aged_path=aged_path,
        tb_path=tb_path,
        aged_inv=aged_inv,
        tb_inv=tb_inv,
        inv_recon=recons["inv_recon"],
        inv_issues=recons["inv_issues"],
        cust_recon=recons["cust_recon"],
        cust_issues=recons["cust_issues"],
    )

    print(f"Wrote workpaper: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
