## AK tie-out (YE 12/31/2025): why the reports don’t “tie”

### Files reviewed

- `ak-tie-out-2025/K01 - PPE Rollforward YE 2025.1.xlsx` (sheet `1. PPE Rollforward Template`)
- `ak-tie-out-2025/K02 - PPE Additions Detail - CSV_AK_Activity_By_Year_Report Additions Detail YE 12.31.2025.xlsx` (sheet `Sheet1`)
- `ak-tie-out-2025/K02 - PPE Disposals Detail - CityServiceValcon_Activity_By_Year_Report Disposals Detail YE 12.31.2025.xlsx` (sheet `Sheet1`)
- `ak-tie-out-2025/K03 - PPE Subledger - CSV_Monthly_Abbreviated_Report_ AK All Assets Summary YTD 12.31.2025.xlsx` (sheet `Sheet1`)

### Executive summary

- **K01 (rollforward) *does* tie to K03 (subledger)** for YE balances (Cost and Accumulated Depreciation), with only de minimis rounding noise.
- The perceived “doesn’t tie” problem is **K01 activity columns vs K02 detail reports**:
  - **K01 uses a mix of “Additions”, “Transfers”, and a separate “CIP” line** to explain cost movement.
  - **K02 “Additions Detail” is a gross acquisitions listing** (by Date Acq and Asset A/C#), and **doesn’t have a CIP bucket**.
  - **K02 “Disposals Detail” shows positive disposal costs**, while **K01 records cost disposals as negative values**.
- When you reconcile with consistent definitions (and sign conventions), **only two asset accounts materially drive the differences**: **Vehicles (15070)** and **Propane Tanks (15130)**.

### What ties cleanly (K01 vs K03)

All amounts below are totals across the asset A/C# totals shown in K03 (and matching cost / A/D lines in K01).

- **Total cost @ 12/31/2025**
  - **K01 ending cost**: 73,438,782.09
  - **K03 cost**: 73,438,782.09 (K03 carries more decimals; the difference is ~0.00 after rounding)
  - **Difference**: ~0.00

- **Total accumulated depreciation @ 12/31/2025**
  - **K01 ending A/D**: (26,186,502.32)
  - **K03 “To Date” depreciation**: 26,186,502.13
  - **Difference**: ~0.19 (rounding)

### Why K01 doesn’t “tie” to K02 (definitions mismatch)

#### 1) K01 has a CIP line that K02 does not

K01 includes a **separate “CIP” row** (no GL account populated) with significant movement:

- **CIP** (K01)
  - Beginning: 1,543,285.46
  - Additions: 5,994,680.29
  - Disposals: (193,581.44)
  - Transfers: (4,645,414.13)
  - Ending: 2,698,970.18

This means a large portion of “acquisitions” for the year **may first land in CIP and later transfer into a depreciable asset A/C#**. A K02 “Additions Detail” report by Asset A/C# will not present CIP as its own bucket, so **gross acquisitions won’t line up to K01 “Additions” without considering K01 “Transfers” and CIP movement.**

#### 2) Sign convention differences (especially for disposals)

- **K01 “Disposals” are entered as negative amounts** on cost lines (e.g., (35,200.00)).
- **K02 “Disposals Detail” shows disposal costs as positive amounts** (e.g., 35,200.00).

So tie-outs should compare **K02 disposals** to **ABS(K01 disposals)** (or to \(-1 \times\) K01 disposals).

#### 3) K02 is “gross activity”; K01 is a rollforward split across columns

K02 reports:
- “Additions Detail” is **gross acquisitions** by Asset A/C# (682 assets; year total 6,245,808.33).
- “Disposals Detail” is **gross disposals** by Asset A/C# (568 assets; year total 2,459,135.24).

K01 splits movement across:
- **Additions** (some purchases)
- **Transfers** (often large, including CIP placed-in-service / reclasses)
- **Disposals** (negative, cost removed)

### Differences (K01 vs K02), by account

#### A) Additions / acquisitions (K02 acquisitions vs K01 (Additions + Transfers))

K02 “Totals for Year: 2025” acquisitions: **6,245,808.33**  
K01 sum across asset A/C# lines of (Additions + Transfers): **5,951,318.72**  
**Difference**: **294,489.61**

Only two accounts drive this net difference:

| Asset A/C# | Description | K02 Acquisitions | K01 Additions | K01 Transfers | K01 (Add+Xfer) | Variance (K02 - K01) |
|---:|---|---:|---:|---:|---:|---:|
| 15070 | Vehicles | 4,129,044.84 | 447,761.52 | 3,884,515.37 | 4,332,276.89 | (203,232.05) |
| 15130 | Propane Tanks | 1,034,666.85 | 38,470.04 | 498,475.15 | 536,945.19 | 497,721.66 |

**Interpretation (most likely):**
- **Vehicles (15070)**: K01 includes **transfer-in cost** that is **not treated as a 2025 “acquisition”** in the Activity-by-Year “Additions” definition (e.g., a reclass / transfer-in of previously-acquired assets). Net effect: **K01 higher** than K02 by 203,232.05.
- **Propane Tanks (15130)**: K02 shows a large volume of small “Leased ___” acquisitions (607 assets), but K01’s cost movement for 15130 is largely sitting in **Transfers (498,475.15)** and **does not reflect the same gross acquisition total**. Net effect: **K01 lower** than K02 by 497,721.66.

#### B) Disposals (K02 disposals vs ABS(K01 disposals))

K02 “Totals for Year: 2025” disposals: **2,459,135.24**  
K01 sum across asset A/C# lines of ABS(Disposals): **1,967,819.78**  
**Difference**: **491,315.46**

Again, only two accounts drive the difference:

| Asset A/C# | Description | K02 Disposals | K01 Disposals (signed) | ABS(K01 Disposals) | Variance (K02 - ABS(K01)) |
|---:|---|---:|---:|---:|---:|
| 15070 | Vehicles | 1,650,013.88 | (1,673,969.78) | 1,673,969.78 | (23,955.90) |
| 15130 | Propane Tanks | 515,271.36 | 0.00 | 0.00 | 515,271.36 |

**Interpretation (most likely):**
- **Vehicles (15070)**: K01 is **higher** than K02 by 23,955.90, consistent with **a disposal-like reduction recorded in K01** that does **not meet the K02 report’s “Disposals *” criteria** (often a reclass/transfer-out that isn’t a “Disposed” status).
- **Propane Tanks (15130)**: K02 shows **479 disposed assets totaling 515,271.36**, but **K01 shows 0.00 cost disposals** on the 15130 line. This is the single biggest “why isn’t it tying” item.

### Key takeaways / likely root causes

- **The rollforward (K01) itself is internally coherent and ties to the subledger (K03).**
- The “not tying” is due to **using K02 gross activity reports as if they map 1:1 to K01’s column definitions**, which they do not (especially with a material **CIP** bucket).
- **Vehicles (15070)** and **Propane Tanks (15130)** are where the column-definition mismatch is most visible:
  - Vehicles: K01 includes additional transfer-type movements not counted as K02 acquisitions/disposals.
  - Propane Tanks: K02 indicates material cost disposals (515k) that are not shown as cost disposals on the K01 15130 cost line (even though the A/D rollforward does show disposed depreciation on 16130).

### Recommended next steps to make the workpapers “tie” the way you expect

- **Decide the intended definition of K01 columns** (esp. “Transfers” vs “Additions”, and whether CIP is meant to be included/excluded from the rollforward you’re comparing).
- For a clean tie-out to K02:
  - **Compare K02 disposals to ABS(K01 disposals)**.
  - **Either include CIP as its own reconciliation bucket** or **reclass CIP transfers into the same definition K02 uses**.
- For **Propane Tanks (15130)** specifically:
  - Confirm whether the 515,271.36 of disposed tank cost should be reflected as a cost disposal in K01 (15130 “Disposals”), or whether those events are being treated as a different transaction type in the rollforward logic (e.g., “Transfers” / “Other Adjustments”).
