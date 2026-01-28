# How to Create an Amortization Table in Excel

An amortization table (or amortization schedule) is a detailed breakdown of loan payments over time, showing how much of each payment goes toward principal versus interest. This guide explains the math behind amortization and provides step-by-step instructions for building an amortization table in Excel.

---

## Table of Contents

1. [What is Amortization?](#what-is-amortization)
2. [The Math Behind Amortization](#the-math-behind-amortization)
3. [Key Excel Functions](#key-excel-functions)
4. [Step-by-Step: Building an Amortization Table](#step-by-step-building-an-amortization-table)
5. [Complete Example](#complete-example)
6. [Advanced Tips](#advanced-tips)

---

## What is Amortization?

Amortization is the process of spreading a loan into a series of fixed payments over time. Each payment consists of two parts:

- **Principal**: The portion that reduces the loan balance
- **Interest**: The cost of borrowing, calculated on the remaining balance

In a standard amortizing loan (like a mortgage or car loan), early payments are interest-heavy, while later payments are principal-heavy.

---

## The Math Behind Amortization

### Monthly Payment Formula

The fixed monthly payment for an amortizing loan is calculated using this formula:

$$
PMT = P \times \frac{r(1+r)^n}{(1+r)^n - 1}
$$

Where:
- **PMT** = Monthly payment
- **P** = Principal (loan amount)
- **r** = Monthly interest rate (annual rate ÷ 12)
- **n** = Total number of payments (loan term in months)

### Interest Payment Formula

For each period, the interest portion is:

$$
\text{Interest Payment} = \text{Beginning Balance} \times r
$$

### Principal Payment Formula

The principal portion is the difference between the total payment and interest:

$$
\text{Principal Payment} = PMT - \text{Interest Payment}
$$

### Ending Balance Formula

The new balance after each payment:

$$
\text{Ending Balance} = \text{Beginning Balance} - \text{Principal Payment}
$$

---

## Key Excel Functions

| Function | Purpose | Syntax |
|----------|---------|--------|
| `PMT` | Calculate fixed periodic payment | `=PMT(rate, nper, pv)` |
| `IPMT` | Calculate interest portion of a payment | `=IPMT(rate, per, nper, pv)` |
| `PPMT` | Calculate principal portion of a payment | `=PPMT(rate, per, nper, pv)` |
| `CUMIPMT` | Calculate cumulative interest over a range | `=CUMIPMT(rate, nper, pv, start, end, type)` |
| `CUMPRINC` | Calculate cumulative principal over a range | `=CUMPRINC(rate, nper, pv, start, end, type)` |

### Function Parameter Definitions

- **rate**: Interest rate per period (annual rate / 12 for monthly)
- **nper**: Total number of payment periods
- **pv**: Present value (loan amount) - enter as negative for positive payment results
- **per**: Specific period number for IPMT/PPMT
- **start/end**: Range of periods for cumulative functions
- **type**: 0 = end of period, 1 = beginning of period

---

## Step-by-Step: Building an Amortization Table

### Step 1: Set Up Your Loan Parameters

Create an input section at the top of your spreadsheet:

| Cell | Label | Value | Notes |
|------|-------|-------|-------|
| A1 | Loan Amount | $250,000 | Principal |
| A2 | Annual Interest Rate | 6.5% | Enter as decimal or percentage |
| A3 | Loan Term (Years) | 30 | |
| A4 | Payments Per Year | 12 | Monthly payments |

In the adjacent cells (B1:B4), enter your values.

### Step 2: Calculate Derived Values

| Cell | Label | Formula |
|------|-------|---------|
| B5 | Monthly Rate | `=B2/B4` |
| B6 | Total Payments | `=B3*B4` |
| B7 | Monthly Payment | `=PMT(B5,B6,-B1)` |

> **Note**: The loan amount is negative in PMT because Excel treats cash outflows as negative. Using `-B1` gives a positive payment result.

### Step 3: Create the Table Headers

Starting in row 10, create these column headers:

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| Payment # | Beginning Balance | Payment | Interest | Principal | Ending Balance |

### Step 4: Enter the First Row Formulas

For row 11 (first payment):

| Cell | Formula | Description |
|------|---------|-------------|
| A11 | `1` | Payment number |
| B11 | `=$B$1` | Beginning balance = original loan amount |
| C11 | `=$B$7` | Fixed monthly payment |
| D11 | `=B11*$B$5` | Interest = balance × monthly rate |
| E11 | `=C11-D11` | Principal = payment - interest |
| F11 | `=B11-E11` | Ending balance = beginning - principal |

### Step 5: Enter Subsequent Row Formulas

For row 12 (and all subsequent payments):

| Cell | Formula |
|------|---------|
| A12 | `=A11+1` |
| B12 | `=F11` | Beginning balance = previous ending balance |
| C12 | `=$B$7` |
| D12 | `=B12*$B$5` |
| E12 | `=C12-D12` |
| F12 | `=B12-E12` |

### Step 6: Copy Down to Complete the Table

1. Select row 12 (cells A12:F12)
2. Copy the formulas down to row 370 (for a 30-year loan with 360 payments)
3. You can use `Ctrl+Shift+End` to select through the last row, or drag the fill handle

---

## Complete Example

### Loan Parameters

- **Loan Amount**: $250,000
- **Annual Interest Rate**: 6.5%
- **Loan Term**: 30 years (360 monthly payments)

### Calculated Values

**Monthly Payment**:
$$
PMT = 250,000 \times \frac{0.005417(1.005417)^{360}}{(1.005417)^{360} - 1} = \$1,580.17
$$

Where monthly rate = 6.5% ÷ 12 = 0.5417% = 0.005417

### Sample Amortization Schedule (First 12 Months)

| Payment # | Beginning Balance | Payment | Interest | Principal | Ending Balance |
|-----------|-------------------|---------|----------|-----------|----------------|
| 1 | $250,000.00 | $1,580.17 | $1,354.17 | $225.99 | $249,774.01 |
| 2 | $249,774.01 | $1,580.17 | $1,352.94 | $227.22 | $249,546.78 |
| 3 | $249,546.78 | $1,580.17 | $1,351.71 | $228.45 | $249,318.33 |
| 4 | $249,318.33 | $1,580.17 | $1,350.47 | $229.70 | $249,088.64 |
| 5 | $249,088.64 | $1,580.17 | $1,349.23 | $230.94 | $248,857.70 |
| 6 | $248,857.70 | $1,580.17 | $1,347.98 | $232.19 | $248,625.51 |
| 7 | $248,625.51 | $1,580.17 | $1,346.72 | $233.45 | $248,392.06 |
| 8 | $248,392.06 | $1,580.17 | $1,345.46 | $234.71 | $248,157.35 |
| 9 | $248,157.35 | $1,580.17 | $1,344.19 | $235.98 | $247,921.37 |
| 10 | $247,921.37 | $1,580.17 | $1,342.91 | $237.26 | $247,684.11 |
| 11 | $247,684.11 | $1,580.17 | $1,341.62 | $238.54 | $247,445.57 |
| 12 | $247,445.57 | $1,580.17 | $1,340.33 | $239.84 | $247,205.73 |

### Sample Amortization Schedule (Last 6 Months)

| Payment # | Beginning Balance | Payment | Interest | Principal | Ending Balance |
|-----------|-------------------|---------|----------|-----------|----------------|
| 355 | $9,313.67 | $1,580.17 | $50.45 | $1,529.72 | $7,783.95 |
| 356 | $7,783.95 | $1,580.17 | $42.16 | $1,538.01 | $6,245.95 |
| 357 | $6,245.95 | $1,580.17 | $33.83 | $1,546.34 | $4,699.61 |
| 358 | $4,699.61 | $1,580.17 | $25.46 | $1,554.71 | $3,144.90 |
| 359 | $3,144.90 | $1,580.17 | $17.03 | $1,563.13 | $1,581.77 |
| 360 | $1,581.77 | $1,580.17 | $8.57 | $1,571.60 | $10.17* |

> *Note: Small rounding differences may result in a final balance that isn't exactly zero. This is normal and can be adjusted in the final payment.

### Summary Statistics

| Metric | Value |
|--------|-------|
| Total Payments | $568,861.03 |
| Total Interest Paid | $318,861.03 |
| Total Principal Paid | $250,000.00 |
| Interest-to-Principal Ratio | 1.28:1 |

**Excel Formula for Total Interest**:
```
=CUMIPMT(B5,B6,B1,1,B6,0)
```

---

## Advanced Tips

### 1. Add Extra Principal Payments

To model extra payments, add a column for "Extra Principal":

| G | Extra Principal |
|---|-----------------|
| G11 | (enter extra amount or 0) |

Then modify your formulas:

- **Total Principal (E11)**: `=C11-D11+G11`
- **Ending Balance (F11)**: `=MAX(B11-E11,0)` (prevents negative balance)

### 2. Handle the Final Payment

The last payment often needs adjustment due to rounding. Use this formula for the payment column:

```
=IF(B11+B11*$B$5<$B$7, B11+B11*$B$5, $B$7)
```

This ensures the final payment doesn't exceed the remaining balance plus interest.

### 3. Create a Dynamic Table with IF Statements

To handle variable loan terms, wrap your formulas in IF statements:

```
=IF(A11<=$B$6, F10, "")
```

This hides rows beyond the loan term.

### 4. Bi-Weekly Payment Schedule

For bi-weekly payments (26 per year):
- Divide annual rate by 26: `=B2/26`
- Multiply years by 26: `=B3*26`

Bi-weekly payments can save significant interest over the life of a loan.

### 5. Add Conditional Formatting

Highlight when principal exceeds interest (the "crossover point"):
1. Select the Principal and Interest columns
2. Apply conditional formatting rule: `=$E11>$D11`
3. Format with green fill to visualize the shift

---

## Quick Reference: Excel Formulas Summary

```
Monthly Payment:        =PMT(annual_rate/12, years*12, -loan_amount)
Interest Payment:       =IPMT(annual_rate/12, period, years*12, -loan_amount)
Principal Payment:      =PPMT(annual_rate/12, period, years*12, -loan_amount)
Cumulative Interest:    =CUMIPMT(annual_rate/12, years*12, loan_amount, 1, period, 0)
Cumulative Principal:   =CUMPRINC(annual_rate/12, years*12, loan_amount, 1, period, 0)
Remaining Balance:      =loan_amount + CUMPRINC(annual_rate/12, years*12, loan_amount, 1, period, 0)
```

---

## Troubleshooting Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Payment shows as negative | PV is positive | Use `-loan_amount` in PMT formula |
| Final balance isn't zero | Rounding errors | Normal; adjust final payment manually |
| #NUM! error | Invalid inputs | Check that rate > 0 and nper > 0 |
| Interest seems too high | Using annual rate instead of monthly | Divide annual rate by 12 |

---

## Conclusion

Building an amortization table in Excel helps you understand exactly how your loan payments work and how much you'll pay in interest over time. The key formulas are straightforward once you understand the underlying math, and Excel's built-in financial functions make the calculations easy.

For additional analysis, consider:
- Creating charts to visualize the principal vs. interest breakdown over time
- Building scenarios to compare different loan terms or interest rates
- Adding extra payment columns to see how prepayments affect total interest

---

*Last updated: January 2026*
