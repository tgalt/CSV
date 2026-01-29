#!/usr/bin/env python3
"""Generate an amortization table CSV for a fixed-rate loan.

Usage example:
    python scripts/amortization_table.py --principal 300000 --apr 6.5 --years 30 \
        --start-date 2025-01-01 --output amortization.csv
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class LoanInputs:
    principal: float
    annual_rate: float
    term_months: int
    start_date: Optional[dt.date]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an amortization table CSV for a fixed-rate loan."
    )
    parser.add_argument("--principal", type=float, required=True, help="Loan principal")
    parser.add_argument(
        "--apr",
        type=float,
        required=True,
        help="Annual percentage rate (e.g., 6.5 for 6.5%%)",
    )
    term_group = parser.add_mutually_exclusive_group(required=True)
    term_group.add_argument("--months", type=int, help="Loan term in months")
    term_group.add_argument("--years", type=float, help="Loan term in years")
    parser.add_argument(
        "--start-date",
        type=str,
        help="Optional start date in YYYY-MM-DD (first payment date)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="amortization.csv",
        help="Output CSV path (default: amortization.csv)",
    )
    return parser.parse_args()


def to_loan_inputs(args: argparse.Namespace) -> LoanInputs:
    if args.months is not None:
        term_months = args.months
    else:
        term_months = int(round(args.years * 12))

    if term_months <= 0:
        raise ValueError("Loan term must be positive")
    if args.principal <= 0:
        raise ValueError("Principal must be positive")

    start_date = None
    if args.start_date:
        start_date = dt.date.fromisoformat(args.start_date)

    return LoanInputs(
        principal=args.principal,
        annual_rate=args.apr,
        term_months=term_months,
        start_date=start_date,
    )


def monthly_payment(principal: float, annual_rate: float, term_months: int) -> float:
    monthly_rate = annual_rate / 100 / 12
    if monthly_rate == 0:
        return principal / term_months
    factor = (1 + monthly_rate) ** term_months
    return principal * monthly_rate * factor / (factor - 1)


def add_months(date: dt.date, months: int) -> dt.date:
    month = date.month - 1 + months
    year = date.year + month // 12
    month = month % 12 + 1
    day = min(date.day, _days_in_month(year, month))
    return dt.date(year, month, day)


def _days_in_month(year: int, month: int) -> int:
    next_month = dt.date(year, month, 28) + dt.timedelta(days=4)
    return (next_month - dt.timedelta(days=next_month.day)).day


def amortization_schedule(inputs: LoanInputs) -> Iterable[dict[str, str]]:
    balance = inputs.principal
    payment_amount = monthly_payment(balance, inputs.annual_rate, inputs.term_months)
    monthly_rate = inputs.annual_rate / 100 / 12

    for payment_number in range(1, inputs.term_months + 1):
        interest_paid = balance * monthly_rate
        principal_paid = payment_amount - interest_paid
        if principal_paid > balance:
            principal_paid = balance
            payment_amount = principal_paid + interest_paid
        balance = balance - principal_paid

        payment_date = ""
        if inputs.start_date:
            payment_date = add_months(inputs.start_date, payment_number - 1).isoformat()

        yield {
            "payment_number": f"{payment_number}",
            "payment_date": payment_date,
            "payment_amount": f"{payment_amount:.2f}",
            "principal_paid": f"{principal_paid:.2f}",
            "interest_paid": f"{interest_paid:.2f}",
            "remaining_balance": f"{max(balance, 0.0):.2f}",
        }


def write_csv(rows: Iterable[dict[str, str]], output_path: str) -> None:
    fieldnames = [
        "payment_number",
        "payment_date",
        "payment_amount",
        "principal_paid",
        "interest_paid",
        "remaining_balance",
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    args = parse_args()
    inputs = to_loan_inputs(args)
    rows = amortization_schedule(inputs)
    write_csv(rows, args.output)


if __name__ == "__main__":
    main()
