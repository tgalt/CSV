from datetime import date, timedelta
import calendar
from pathlib import Path

# =============== CONFIG ===============
TIMEZONE_LABEL = "MDT"
SYSTEM_NAMES = {"erp": "DM2", "statements": "NorthStar"}
WAREHOUSES = "lube, agronomy, and feeds"
HOLIDAYS = set()

# =============== CORE LOGIC ===============
def month_end_close_email_md(year: int, month: int) -> str:
    """Generate markdown formatted month-end close email."""
    month_name = calendar.month_name[month]
    last_day_num = calendar.monthrange(year, month)[1]
    last_day = date(year, month, last_day_num)

    # Find last workday of the month
    last_workday = last_day
    while last_workday.weekday() >= 5:
        last_workday -= timedelta(days=1)

    # Get next month/year
    next_year, next_month = (year + 1, 1) if month == 12 else (year, month + 1)

    # Collect first 7 business days of next month
    business_days = []
    d = date(next_year, next_month, 1)
    while len(business_days) < 7:
        if d.weekday() < 5 and d not in HOLIDAYS:
            business_days.append(d)
        d += timedelta(days=1)

    def fmt_long(d: date) -> str:
        return f"{calendar.day_name[d.weekday()]}, {calendar.month_name[d.month]} {d.day}"

    def fmt_month_day(d: date) -> str:
        return f"{calendar.month_name[d.month]} {d.day}"

    d0 = last_workday
    bd1, bd2, bd3, bd4, bd5, bd6, bd7 = business_days

    return f"""# __**Month-end close schedule for {month_name} {year}**__

Good morning,

Below is the month-end close schedule for {month_name} {year}. Please review the schedule below and plan accordingly.

## **{fmt_long(d0)}**

- __Freeze inventory__ for {WAREHOUSES} – 12Noon {TIMEZONE_LABEL} – all users exit **{SYSTEM_NAMES['erp']}** for 15 mins.
- Physical Inventory Counts – {WAREHOUSES.capitalize()} entered in **{SYSTEM_NAMES['erp']}**.
- All deposits/cash receipts posted in **{SYSTEM_NAMES['erp']}** before end of day.

## **{fmt_long(bd1)} (Business Day 1)**

- All remaining inventory counts completed first thing ({fmt_month_day(bd1)}).
- Adjust any counts from {fmt_month_day(d0)} to reflect end-of-day balances.
- Review variances in the morning.
- Process customer finance charges – 4pm {TIMEZONE_LABEL}.

## **{fmt_long(bd2)} (Business Day 2)**

- All sales orders with a {month_name} ship date posted/changed by 3pm {TIMEZONE_LABEL}.
- All invoice batches posted by 4pm {TIMEZONE_LABEL}.
- __Freeze remaining inventory__ – 4pm {TIMEZONE_LABEL} (all users exit **{SYSTEM_NAMES['erp']}**).
- Process monthly customer statements.
- All remaining cash receipts posted before 6pm {TIMEZONE_LABEL}.
- Perform month-end close procedures – 6pm {TIMEZONE_LABEL} until release.

## **{fmt_long(bd3)} (Business Day 3)**
- Mail customer statements.

## **{fmt_long(bd4)} (Business Day 4)**
- A/P closed for {month_name} – all invoices approved by 6pm {TIMEZONE_LABEL}.

## **{fmt_long(bd5)} (Business Day 5)**
- Review month-end financial balances.
- Preliminary BULOC Trend Report.

## **{fmt_long(bd6)} (Business Day 6)**
- Upload trial balances to **{SYSTEM_NAMES['statements']}**.

## **{fmt_long(bd7)} (Business Day 7)**
- Issue financial statements.

Thank you,

Travis Pickens

Accounting Manager | CityServiceValcon, LLC
"""


if __name__ == "__main__":
    today = date.today()
    md_text = month_end_close_email_md(today.year, today.month)
    Path("month_end_close.md").write_text(md_text, encoding="utf-8")
    print("Markdown file created: month_end_close.md")
