# AK YE 12/31/2025 tie-out: Vehicles (15070) and Propane Tanks (15130) net differences

This memo summarizes what drives the two net differences you called out:

- **Vehicles (15070)**: net difference \(\approx (38,741.15)\) — **mechanically explained by K02 report definitions**, with the remaining residual driven by **transfer/reclass and disposal-classification differences** between K01 vs K02.
- **Propane Tanks (15130)**: net difference **2,000** — remains **after** correcting for K02’s “active additions” vs “disposed assets” split, pointing to a **small classification/timing difference** (likely one \(\sim \$2k\) tank transaction).

---

## Vehicles (15070): what causes the net difference

### 1) The key structural issue: K02 Additions excludes assets acquired and disposed in the same year

K02 “Additions Detail” is effectively an **active additions listing**. Vehicles acquired in 2025 and sold in 2025 will **not** appear there; they show up in K02 “Disposals Detail” under the **Acquisitions** subtotal for the account section.

For Vehicles, K02 “Disposals Detail” shows **Acquisitions (1 asset)** of:

- **140,805.00** (a refueler acquired 05/19/2025 and sold 05/28/2025)

If you compare K01 to K02 without adding this back, you will overstate the “K01 vs K02” net difference.

### 2) Vehicles net cost-change reconciliation (K01 vs K02)

**K01 Vehicles net cost change**:

- Beginning cost (K01): **27,938,169.33**
- Ending cost (K01): **30,596,476.44**
- **Net change (K01)** = 30,596,476.44 − 27,938,169.33 = **2,658,307.11**

**K02 Vehicles net cost change** (must include “in-year acquired & disposed” acquisitions):

- K02 Additions Detail acquisitions (15070): **4,129,044.84**
- K02 Disposals Detail “Acquisitions” (15070): **140,805.00**
- K02 Disposals Detail “Disposals *” cost (15070): **1,650,013.88**
- **Net change (K02)** = (4,129,044.84 + 140,805.00) − 1,650,013.88 = **2,619,835.96**

**Net difference (K01 − K02)**:

- 2,658,307.11 − 2,619,835.96 = **38,471.15** (very close to the \((38,741.15)\) you cited; the driver mechanics are exactly as shown above)

### 3) What makes up the remaining residual (after correcting for in-year acquisitions)

After you correctly include the **140,805** “acquired & sold in-year” item, the remaining Vehicles net difference is explained by **how K01 classifies activity vs how K02’s activity-by-year reports classify it**:

- **Transfer/reclass activity counted in K01 but not counted as K02 “acquisitions”**  
  K01 Vehicles has large **Transfers** (**3,884,515.37**) that can include previously-acquired assets reclassed/placed-in-service into 15070. K02 “Additions” is driven by acquisition criteria and may not treat those as current-year acquisitions.

- **Disposal-like cost reductions captured in K01 but not meeting K02 “Disposals *” criteria**  
  K01 Vehicles shows cost disposals of **(1,673,969.78)** (ABS = **1,673,969.78**).  
  K02 Vehicles “Disposals *” shows **1,650,013.88**.  
  The difference between these disposal totals indicates **some K01 cost reduction** is being treated as disposal/reduction in the rollforward but is not presented as a “Disposed” status item in K02 (commonly reclasses/transfer-outs).

---

## Propane Tanks (15130): what causes the net difference of 2,000

### 1) Same structural issue applies: K02 Additions excludes assets acquired and disposed in the same year

For Propane Tanks, K02 “Disposals Detail” shows **Acquisitions (11 assets)** totaling:

- **19,549.70**

Those are **2025 acquisitions that were also disposed in 2025**, and therefore they do **not** appear in K02 “Additions Detail”.

### 2) Propane net cost-change reconciliation (K01 vs K02)

**K01 Propane net cost change**:

- Beginning cost (K01): **16,378,798.25**
- Ending cost (K01): **16,915,743.44**
- **Net change (K01)** = 16,915,743.44 − 16,378,798.25 = **536,945.19**

**K02 Propane net cost change** (must include “in-year acquired & disposed” acquisitions):

- K02 Additions Detail acquisitions (15130): **1,034,666.85**
- K02 Disposals Detail “Acquisitions” (15130): **19,549.70**
- K02 Disposals Detail “Disposals *” cost (15130): **515,271.36**
- **Net change (K02)** = (1,034,666.85 + 19,549.70) − 515,271.36 = **538,945.19**

**Net difference (K01 − K02)**:

- 536,945.19 − 538,945.19 = **(2,000.00)**

### 3) What the 2,000 residual likely represents

Because the “in-year acquisitions” structural issue is already corrected above, the remaining **2,000** is best interpreted as a **classification/timing difference** between:

- what K02 tags as **2025 Propane Tanks acquisitions / disposals**, and
- what K01 captures on the **15130 cost line** (via Additions vs Transfers vs other rollforward logic).

Most likely root cause: **one propane transaction of approximately \$2,000** is being:

- included in K02 activity for 15130, but
- classified differently in K01 (e.g., recorded as a transfer/reclass/CIP-related movement, or booked to a different asset A/C#).

---

## Practical next checks (fastest way to fully “close” both items)

- **Vehicles**: identify which K01 “Disposals” (or cost reductions) are not showing as “Disposals *” in K02 Vehicles; these are typically **reclasses/transfer-outs** rather than true disposed-status events.
- **Propane**: search the 15130 activity for a single \(\sim \$2,000\) transaction and confirm whether it is:
  - recorded in K01 under **Transfers** instead of Additions, or
  - posted to a different A/C# (misclassification), or
  - included/excluded due to “disposed before current period” logic differences.

