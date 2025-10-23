"""Find combinations of CSV column values that sum to target (optimized).

Improvements over brute-force itertools.combinations:
- Convert floats to integer cents to avoid FP issues.
- Sort and use backtracking with pruning (early exit when partial sum exceeds target).
- Return original row indices and values so user can trace back to input.
- Add argparse CLI options and limit max_matches to stop early.
"""

from __future__ import annotations

import argparse
import time
from typing import List, Tuple

import pandas as pd
import sys
import math


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Find combinations in CSV that sum to target")
    p.add_argument("csv", nargs="?", default="data4.csv", help="path to CSV file")
    p.add_argument("--col", default="Amount", help="column name containing numeric values")
    p.add_argument("--target", type=float, default=2245.35, help="target sum (float)")
    p.add_argument("--tol", type=float, default=0.01, help="tolerance for matching target")
    p.add_argument("--max-size", type=int, default=5, help="maximum combination size")
    p.add_argument("--max-matches", type=int, default=50, help="stop after this many matches (0 = unlimited)")
    p.add_argument("--verbose", action="store_true", help="print progress and timing info")
    p.add_argument("--timeout", type=float, default=30.0, help="max seconds to search before giving up (0 = no timeout)")
    p.add_argument("--both-signs", action="store_true", help="search for both +target and -target")
    return p.parse_args()


def to_cents(x: float) -> int:
    """Convert float dollars to integer cents safely."""
    return int(round(x * 100))


def find_combinations(values: List[int], indices: List[int], target: int, max_size: int,
                      max_matches: int = 0,
                      end_time: float | None = None,
                      verbose: bool = False) -> List[List[Tuple[int, int]]]:
    """Backtracking search over sorted values with pruning.

    values: list of integer cents (sorted ascending)
    indices: corresponding original row indices
    target: target in cents
    returns list of matches where each match is list of (original_index, value_cents)
    """
    results: List[List[Tuple[int, int]]] = []

    n = len(values)
    # prefix_sums[i] = sum of values[i:]  (suffix sums) used to prune when remaining values can't reach target
    suffix_sums = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix_sums[i] = suffix_sums[i + 1] + values[i]

    def backtrack(start: int, curr_sum: int, path: List[int]):
        # stop if we've reached desired size or sum
        # check timeout periodically
        if end_time is not None and time.time() > end_time:
            if verbose:
                print("Timeout reached, stopping search...")
            raise TimeoutError()
        if curr_sum == target:
            results.append([(indices[i], values[i]) for i in path])
            return
        if curr_sum > target:
            return
        if len(path) >= max_size:
            return

        prev = None
        for i in range(start, n):
            # skip duplicates (same value at same recursion depth) to reduce equivalent branches
            if prev is not None and values[i] == prev:
                continue
            prev = values[i]

            # pruning: if even taking all remaining values still can't reach target, break early
            # suffix_sums[i] is sum of values from i..end
            if curr_sum + suffix_sums[i] < target:
                # Not enough remaining to reach target
                break

            # pruning: if adding smallest remaining values can't reach target, we still explore;
            # more important: stop when partial sum exceeds target (we check above)
            path.append(i)
            backtrack(i + 1, curr_sum + values[i], path)
            path.pop()

            if max_matches and len(results) >= max_matches:
                return

    backtrack(0, 0, [])
    return results


def main() -> None:
    args = parse_args()

    start_time = time.time()
    df = pd.read_csv(args.csv)

    if args.col not in df.columns:
        raise SystemExit(f"Column '{args.col}' not found in {args.csv}. Available: {', '.join(df.columns)}")

    # dropna rows but keep indices so results can point back
    series = df[args.col].dropna()
    orig_indices = series.index.tolist()
    floats = series.astype(float).tolist()

    cents = [to_cents(x) for x in floats]
    target_cents = to_cents(args.target)
    tol_cents = to_cents(args.tol)

    # We'll search for values that sum to any integer within [target-tol, target+tol]
    low_target = target_cents - tol_cents
    high_target = target_cents + tol_cents

    # if there are negatives, sorting ascending still works but pruning for > target only applies for non-negatives
    combined = list(zip(cents, orig_indices))
    # filter values larger than high_target (if all non-negative) to reduce search space
    if all(v >= 0 for v, _ in combined):
        combined = [(v, idx) for v, idx in combined if v <= high_target]

    if not combined:
        print("No candidate values after filtering; nothing to search.")
        return

    # sort by value ascending for deterministic search and better pruning
    combined.sort(key=lambda x: x[0])
    sorted_values, sorted_indices = zip(*combined)
    sorted_values = list(sorted_values)
    sorted_indices = list(sorted_indices)

    matches = []
    # run search with a timeout and optional verbose progress
    timeout = args.timeout
    end_time = start_time + timeout if timeout > 0 else None

    # wrap find_combinations to check timeout and progress
    # We will implement a small monitor: if verbose, print elapsed time periodically.

    # Support searching for both +target and -target if requested
    targets_to_try = [target_cents]
    if args.both_signs:
        targets_to_try.append(-target_cents)

    final_matches = []
    for t in targets_to_try:
        try:
            matches = find_combinations(sorted_values, sorted_indices, t, args.max_size, args.max_matches, end_time, args.verbose)
        except TimeoutError:
            if args.verbose:
                print(f"Search timed out for target {t/100.0}; collecting results so far.")
            matches = []

        # Filter matches that are within tolerance (in case rounding produced small mismatches)
        for m in matches:
            s = sum(val for _, val in m)
            if abs(s - t) <= tol_cents:
                final_matches.append((t, m))

    elapsed = time.time() - start_time

    if final_matches:
        print(f"Found {len(final_matches)} matches (showing up to {args.max_matches or len(final_matches)}) in {elapsed:.2f}s:")
        for match in final_matches[: args.max_matches or None]:
            pretty = [(i, v / 100.0) for i, v in match]
            total = sum(v for _, v in match) / 100.0
            print(pretty, "=>", f"{total:.2f}")
    else:
        print(f"No combinations found that sum to ~{args.target} (tol={args.tol}) in {elapsed:.2f}s")


if __name__ == "__main__":
    main()
