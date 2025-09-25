from datetime import date, timedelta
import calendar
from pathlib import Path

# =============== CONFIG ===============
TIMEZONE_LABEL = "MDT"
SYSTEM_NAMES = {
    "erp": "DM2",
    "statements": "NorthStar",
}
WAREHOUSES = "lube, agronomy, and feeds"
HOLIDAYS = set()

# =============== CORE LOGIC ===============
def month_end_close_email_md(year: int, month: int) -> str:
    month_name = calendar.month_name[month]
    last_day_num = calendar.monthrange(year, month)[1]
    last_day = date(year, month, last_day_num)

    last_workday = last_day
    while last_workday.weekday() >= 5:
        last_workday -= timedelta(days=1)

    next_year, next_month = (year + 1, 1) if month == 12 else (year, month + 1)

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

    md = []
    md.append(f"# __**Month-end close schedule for {month_name} {year}**__\n")
    md.append("Good morning,\n")
    md.append(f"Below is the month-end close schedule for {month_name} {year}. "
              "Please review the schedule below and plan accordingly.\n")

    md.append(f"## **{fmt_long(d0)}**\n")
    md.append(f"- __Freeze inventory__ for {WAREHOUSES} – 12Noon {TIMEZONE_LABEL} – all users exit **{SYSTEM_NAMES['erp']}** for 15 mins.")
    md.append(f"- Physical Inventory Counts – {WAREHOUSES.capitalize()} entered in **{SYSTEM_NAMES['erp']}**.")
    md.append(f"- All deposits/cash receipts posted in **{SYSTEM_NAMES['erp']}** before end of day.\n")

    md.append(f"## **{fmt_long(bd1)} (Business Day 1)**\n")
    md.append(f"- All remaining inventory counts completed first thing ({fmt_month_day(bd1)}).")
    md.append(f"- Adjust any counts from {fmt_month_day(d0)} to reflect end-of-day balances.")
    md.append("- Review variances in the morning.")
    md.append(f"- Process customer finance charges – 4pm {TIMEZONE_LABEL}.\n")

    md.append(f"## **{fmt_long(bd2)} (Business Day 2)**\n")
    md.append(f"- All sales orders with a {month_name} ship date posted/changed by 3pm {TIMEZONE_LABEL}.")
    md.append(f"- All invoice batches posted by 4pm {TIMEZONE_LABEL}.")
    md.append(f"- __Freeze remaining inventory__ – 4pm {TIMEZONE_LABEL} (all users exit **{SYSTEM_NAMES['erp']}**).")
    md.append("- Process monthly customer statements.")
    md.append(f"- All remaining cash receipts posted before 6pm {TIMEZONE_LABEL}.")
    md.append(f"- Perform month-end close procedures – 6pm {TIMEZONE_LABEL} until release.\n")

    md.append(f"## **{fmt_long(bd3)} (Business Day 3)**\n- Mail customer statements.\n")
    md.append(f"## **{fmt_long(bd4)} (Business Day 4)**\n- A/P closed for {month_name} – all invoices approved by 6pm {TIMEZONE_LABEL}.\n")
    md.append(f"## **{fmt_long(bd5)} (Business Day 5)**\n- Review month-end financial balances.\n- Preliminary BULOC Trend Report.\n")
    md.append(f"## **{fmt_long(bd6)} (Business Day 6)**\n- Upload trial balances to **{SYSTEM_NAMES['statements']}**.\n")
    md.append(f"## **{fmt_long(bd7)} (Business Day 7)**\n- Issue financial statements.\n")

    md.append("Thank you,\n")
    md.append("Travis Pickens\n")
    md.append("Accounting Manager | CityServiceValcon\n")

    return "\n".join(md)


if __name__ == "__main__":
    today = date.today()
    md_text = month_end_close_email_md(today.year, today.month)

    # Write to file
    Path("month_end_close.md").write_text(md_text, encoding="utf-8")
    print("Markdown file created: month_end_close.md")
