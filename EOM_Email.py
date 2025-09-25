from datetime import date, timedelta
import calendar

# =============== CONFIG ===============
# Customize these as needed
TIMEZONE_LABEL = "MDT"  # e.g., "MDT", "MST"
SYSTEM_NAMES = {
    "erp": "DM2",
    "statements": "NorthStar",
}
WAREHOUSES = "lube, agronomy, and feeds"

# Optional: list company holidays to skip (only affects "Business Day N" dates)
# Example format: {date(2025, 8, 4), date(2025, 9, 1)}
HOLIDAYS = set()

# =============== CORE LOGIC ===============
def month_end_close_email(year: int, month: int) -> str:
    """
    Build the month-end close email for a given month/year.
    - Uses the last working day of the month for the initial freeze/counts.
    - Then schedules Business Day 1..7 on the first seven business days of the next month,
      skipping weekends and any dates listed in HOLIDAYS.
    """
    # Names
    month_name = calendar.month_name[month]
    # Compute last day of the month
    last_day_num = calendar.monthrange(year, month)[1]
    last_day = date(year, month, last_day_num)

    # Find the LAST WORKDAY on or before the last calendar day
    last_workday = last_day
    while last_workday.weekday() >= 5:  # 5=Sat, 6=Sun
        last_workday -= timedelta(days=1)

    # Next month/year
    next_year, next_month = (year + 1, 1) if month == 12 else (year, month + 1)

    # Collect first 7 business days of next month (skip weekends + holidays)
    business_days = []
    d = date(next_year, next_month, 1)
    # If the 1st is weekend/holiday, advance until first business day
    while len(business_days) < 7:
        if d.weekday() < 5 and d not in HOLIDAYS:
            business_days.append(d)
        d += timedelta(days=1)

    # Convenience accessors
    def fmt_long(d: date) -> str:
        return f"{calendar.day_name[d.weekday()]}, {calendar.month_name[d.month]} {d.day}"

    def fmt_month_day(d: date) -> str:
        return f"{calendar.month_name[d.month]} {d.day}"

    # Day aliases used in body text
    d0 = last_workday  # Final workday of target month
    bd1, bd2, bd3, bd4, bd5, bd6, bd7 = business_days

    # Build the email text
    lines = []
    lines.append(f"Month-end close schedule for {month_name} {year}")
    lines.append("")
    lines.append("")
    lines.append("Good morning,")
    lines.append("")
    lines.append("")
    lines.append(f"Below is the month-end close schedule for {month_name} {year}. Please review the schedule below and plan accordingly for resources and timing.")
    lines.append("")
    lines.append("If anyone will be out during any of the dates listed below, it is critical that you make sure there is a plan in place for coverage of any month-end responsibilities, to ensure all tasks are completed during your absence.")
    lines.append("")
    lines.append(f"{fmt_long(d0)}")
    lines.append("")
    lines.append(f"Freeze inventory for {WAREHOUSES} warehouses – 12Noon {TIMEZONE_LABEL} – All users exit {SYSTEM_NAMES['erp']} for 15 mins.")
    lines.append("")
    lines.append(f"Physical Inventory Counts – {WAREHOUSES.capitalize()} inventory counted and entered in {SYSTEM_NAMES['erp']}.")
    lines.append("")
    lines.append(f"All bank deposits made in the bank and all cash receipts posted in {SYSTEM_NAMES['erp']} before end of day.")
    lines.append("")
    lines.append("")
    lines.append(f"{fmt_long(bd1)} (Business Day 1)")
    lines.append("")
    lines.append(f"Very first thing ({calendar.day_name[bd1.weekday()]} morning, {fmt_month_day(bd1)}) – All remaining physical inventory counts completed.")
    lines.append("")
    lines.append(
        f"Any inventory counts for {fmt_month_day(d0)} completed on the morning of {fmt_month_day(bd1)}, "
        f"MUST be adjusted for any changes in inventory that may have occurred after {fmt_month_day(d0)}. "
        f"Physical counts must accurately reflect actual on-hand inventory quantities at the close of business on {fmt_long(d0)}."
    )
    lines.append("")
    lines.append("Review inventory counts and resolve any variances – First thing in the morning.")
    lines.append("")
    lines.append(f"Process customer finance charges – 4pm {TIMEZONE_LABEL}.")
    lines.append("")
    lines.append("")
    lines.append(f"{fmt_long(bd2)} (Business Day 2)")
    lines.append("")
    lines.append(f"All sales orders with a {month_name} ship date must be posted, deleted, or changed to a {month_name} ship date (as applicable) by 3pm {TIMEZONE_LABEL}.")
    lines.append("")
    lines.append(f"All invoice data entry batches posted – before 4pm {TIMEZONE_LABEL}.")
    lines.append("")
    lines.append(f"Freeze remaining inventory – 4pm {TIMEZONE_LABEL} – All users exit {SYSTEM_NAMES['erp']} for 15 mins.")
    lines.append("")
    lines.append("Process monthly customer statements.")
    lines.append("")
    lines.append(f"All remaining cash receipts batches posted before 6pm {TIMEZONE_LABEL}.")
    lines.append("")
    lines.append(f"Perform month-end close procedures 6pm {TIMEZONE_LABEL} – everyone must exit {SYSTEM_NAMES['erp']} until notification that {SYSTEM_NAMES['erp']} is available again.")
    lines.append("")
    lines.append("")
    lines.append(f"{fmt_long(bd3)} (Business Day 3)")
    lines.append("")
    lines.append("Mail customer statements.")
    lines.append("")
    lines.append("")
    lines.append(f"{fmt_long(bd4)} (Business Day 4)")
    lines.append("")
    lines.append(f"A/P closed for {month_name}. All remaining {month_name} invoices must be approved AND submitted to A/P prior to 6pm {TIMEZONE_LABEL}.")
    lines.append("")
    lines.append("")
    lines.append(f"{fmt_long(bd5)} (Business Day 5)")
    lines.append("")
    lines.append("Review month-end financial balances.")
    lines.append("")
    lines.append("Preliminary BULOC Trend Report.")
    lines.append("")
    lines.append("")
    lines.append(f"{fmt_long(bd6)} (Business Day 6)")
    lines.append("")
    lines.append(f"Upload trial balances to {SYSTEM_NAMES['statements']}.")
    lines.append("")
    lines.append("")
    lines.append(f"{fmt_long(bd7)} (Business Day 7)")
    lines.append("")
    lines.append("Issue financial statements.")
    lines.append("")
    lines.append("")
    lines.append("Thank you,")
    return "\n".join(lines)


if __name__ == "__main__":
    # EXAMPLES:
    # 1) Generate for July 2025 (matches your example, but auto-calculated)
    # print(month_end_close_email(2025, 7))

    # 2) Generate for the CURRENT month automatically:
    today = date.today()
    print(month_end_close_email(today.year, today.month))

    # 3) Add a holiday (e.g., skip Labor Day 2025 for Business Day counting):
    # HOLIDAYS.add(date(2025, 9, 1))
    # print(month_end_close_email(2025, 8))
