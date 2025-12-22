from datetime import date, timedelta
import calendar

# =============== CONFIG ===============
TIMEZONE_LABEL = "MDT"
SYSTEM_NAMES = {"erp": "DM2", "statements": "NorthStar"}
WAREHOUSES = "lube, agronomy, and feeds"
HOLIDAYS = set()

# =============== CORE LOGIC ===============
def month_end_close_email(year: int, month: int) -> str:
    """Build the month-end close email for a given month/year."""
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

    # Build email using f-string
    return f"""Month-end close schedule for {month_name} {year}


Good morning,


Below is the month-end close schedule for {month_name} {year}. Please review the schedule below and plan accordingly for resources and timing.

If anyone will be out during any of the dates listed below, it is critical that you make sure there is a plan in place for coverage of any month-end responsibilities, to ensure all tasks are completed during your absence.

{fmt_long(d0)}

Freeze inventory for {WAREHOUSES} warehouses – 12Noon {TIMEZONE_LABEL} – All users exit {SYSTEM_NAMES['erp']} for 15 mins.

Physical Inventory Counts – {WAREHOUSES.capitalize()} inventory counted and entered in {SYSTEM_NAMES['erp']}.

All bank deposits made in the bank and all cash receipts posted in {SYSTEM_NAMES['erp']} before end of day.


{fmt_long(bd1)} (Business Day 1)

Very first thing ({calendar.day_name[bd1.weekday()]} morning, {fmt_month_day(bd1)}) – All remaining physical inventory counts completed.

Any inventory counts for {fmt_month_day(d0)} completed on the morning of {fmt_month_day(bd1)}, MUST be adjusted for any changes in inventory that may have occurred after {fmt_month_day(d0)}. Physical counts must accurately reflect actual on-hand inventory quantities at the close of business on {fmt_long(d0)}.

Review inventory counts and resolve any variances – First thing in the morning.

Process customer finance charges – 4pm {TIMEZONE_LABEL}.


{fmt_long(bd2)} (Business Day 2)

All sales orders with a {month_name} ship date must be posted, deleted, or changed to a {month_name} ship date (as applicable) by 3pm {TIMEZONE_LABEL}.

All invoice data entry batches posted – before 4pm {TIMEZONE_LABEL}.

Freeze remaining inventory – 4pm {TIMEZONE_LABEL} – All users exit {SYSTEM_NAMES['erp']} for 15 mins.

Process monthly customer statements.

All remaining cash receipts batches posted before 6pm {TIMEZONE_LABEL}.

Perform month-end close procedures 6pm {TIMEZONE_LABEL} – everyone must exit {SYSTEM_NAMES['erp']} until notification that {SYSTEM_NAMES['erp']} is available again.


{fmt_long(bd3)} (Business Day 3)

Mail customer statements.


{fmt_long(bd4)} (Business Day 4)

A/P closed for {month_name}. All remaining {month_name} invoices must be approved AND submitted to A/P prior to 6pm {TIMEZONE_LABEL}.


{fmt_long(bd5)} (Business Day 5)

Review month-end financial balances.

Preliminary BULOC Trend Report.


{fmt_long(bd6)} (Business Day 6)

Upload trial balances to {SYSTEM_NAMES['statements']}.


{fmt_long(bd7)} (Business Day 7)

Issue financial statements.


Thank you,"""


if __name__ == "__main__":
    today = date.today()
    print(month_end_close_email(today.year, today.month))
