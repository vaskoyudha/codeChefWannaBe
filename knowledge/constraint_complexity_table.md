# Constraint–Complexity Mapping Table

> **Purpose:** This reference maps input constraint sizes to the maximum acceptable time complexity, typical techniques that fit each bracket, and the reasoning behind the mappings. Problem-setting agents use this to ensure constraints and intended solutions are mutually consistent.

---

## 1. The Core Mapping Table

| Constraint (N) | Required Complexity | Operations Budget | Typical Techniques |
|---|---|---|---|
| N ≤ 10–20 | O(N!) or O(2^N) | ~10⁶ – 10⁷ | Backtracking, Bitmask DP, brute-force permutations, exhaustive search |
| N ≤ 100 | O(N³) or O(N⁴) | ~10⁶ – 10⁸ | Floyd-Warshall, standard 3D DP, Matrix Chain Multiplication, Gaussian Elimination |
| N ≤ 500 | O(N³) | ~1.25 × 10⁸ | Dense graph APSP, Interval DP, 3D DP with tight inner loop |
| N ≤ 2 000 | O(N²) | ~4 × 10⁶ | Standard 2D DP, Dijkstra (dense), 2D Prefix Sums, O(N²) string algorithms |
| N ≤ 10⁵ | O(N log N) or O(N√N) | ~1.7 × 10⁶ | Sorting-based, Segment Trees, Fenwick Trees, Merge Sort Tree, Divide & Conquer, Sqrt Decomposition |
| N ≤ 10⁶ | O(N) or O(N log log N) | ~10⁶ – 1.5 × 10⁶ | Linear Sieve (Eratosthenes), Counting Sort / Radix Sort, BFS/DFS on trees, two-pointer, sliding window |
| N ≤ 10⁹ | O(√N) or O(log N) | ~3 × 10⁴ – 30 | Number Theory (modular arithmetic, GCD), Binary Search on answer, Sqrt Decomposition, Meet-in-the-middle |
| N ≤ 10¹⁸ | O(log N) or O(log² N) | ~60 – 3 600 | Matrix Exponentiation, Binary Lifting, closed-form math, fast exponentiation, digit DP |

### Quick-Reference: Reverse Look-up

Given an intended solution complexity, what constraints should you set?

| Intended Complexity | Set N to at most |
|---|---|
| O(N!) | 10–12 |
| O(2^N) | 20–22 |
| O(N³) | 300–500 |
| O(N² log N) | 1 000–2 000 |
| O(N²) | 2 000–5 000 |
| O(N log N) | 10⁵ – 5 × 10⁵ |
| O(N √N) | 10⁵ |
| O(N) | 10⁶ – 10⁷ |
| O(√N) | 10⁹ – 10¹² |
| O(log N) | 10⁹ – 10¹⁸ |

---

## 2. Why These Mappings Exist

### 2.1 The CPU Budget

Competitive programming judges typically execute **~10⁸ simple operations per second** (this varies by platform, but 10⁸ is the widely accepted rule of thumb). Most contests allow **1–2 seconds** of execution time.

This means:
- **Time budget** ≈ 10⁸ operations (1-second limit) or 2 × 10⁸ (2-second limit).
- A solution doing 10⁸ additions will pass; a solution doing 10⁸ map lookups might not (constant factor matters).

### 2.2 Constant Factors Matter

Not all operations are equal. The "real" budget depends on the constant factor:

| Operation | Approximate Throughput/sec |
|---|---|
| Simple arithmetic (add, multiply) | ~10⁹ |
| Array access (sequential) | ~10⁹ |
| Array access (random / cache miss) | ~10⁸ |
| HashMap / std::map lookup | ~10⁷ |
| Function call + recursion overhead | ~10⁷ – 10⁸ |
| I/O (cin/cout without sync) | ~10⁶ |

**Practical implication:** An O(N log N) solution with heavy constant factors (e.g., `std::map` inside a loop) may TLE when N = 10⁵, while an O(N²) solution with a trivial inner loop (simple array additions) may pass when N = 5 000.

### 2.3 Memory Constraints

Most platforms enforce a **256 MB memory limit** (some use 512 MB or 64 MB).

Memory implications per constraint size:

| N | 1D array (int) | 2D array (int) | 3D array (int) |
|---|---|---|---|
| 10³ | 4 KB | 4 MB | 4 GB ❌ |
| 2 × 10³ | 8 KB | 16 MB | 32 GB ❌ |
| 5 × 10³ | 20 KB | 100 MB | — |
| 10⁴ | 40 KB | 400 MB ❌ | — |
| 10⁵ | 400 KB | 40 GB ❌ | — |
| 10⁶ | 4 MB | — | — |

**Key rules:**
- A 2D `int` array of size N × N is viable only up to N ≈ 5 000 (100 MB).
- A 3D `int` array of size N × N × N is viable only up to N ≈ 500 (500 MB — tight).
- For N = 10⁵, you cannot store pairwise distances (O(N²) memory = 40 GB).

### 2.4 The Hidden Multiplier: Test Cases

Many problems have **T test cases** per file. The total work is T × (work per test case). If the sum of N across test cases is bounded (e.g., "ΣN ≤ 10⁵"), the budget applies to the sum. If not, each test case must independently fit the budget.

**Watch out:** A problem with T = 100 and N = 10⁴ per test case requires O(N log N) per case, giving 100 × 10⁴ × 14 ≈ 1.4 × 10⁷ — well within budget. But T = 100 with N = 10⁵ gives 100 × 10⁵ × 17 ≈ 1.7 × 10⁸ — tight.

---

## 3. Reverse-Engineering Constraints from Intended Solution

When designing a problem, start from the solution and work backward:

### Step-by-step process:

1. **Identify the core algorithm** you want contestants to use.
   - Example: "I want this to require a Segment Tree with lazy propagation."

2. **Determine the algorithm's complexity.**
   - Segment Tree with lazy propagation: O(N log N) per query, or O((N + Q) log N) total.

3. **Calculate the maximum N that fits the time budget.**
   - (N + Q) × log₂(N) ≤ 10⁸
   - If Q ≈ N, then 2N × log₂(N) ≤ 10⁸
   - N = 10⁵ → 2 × 10⁵ × 17 ≈ 3.4 × 10⁶ ✓
   - N = 10⁶ → 2 × 10⁶ × 20 ≈ 4 × 10⁷ ✓ (but constant factor of Segment Tree is ~10–20×, so real ops ≈ 4 × 10⁸ — tight)
   - Set N ≤ 2 × 10⁵ to be safe.

4. **Verify memory is feasible.**
   - Segment Tree needs 4N nodes → 4 × 2 × 10⁵ = 8 × 10⁵ ints ≈ 3.2 MB ✓

5. **Set constraints that exclude simpler solutions.**
   - If N ≤ 2 000, an O(N²) brute force would pass → set N = 2 × 10⁵ to force O(N log N).
   - If you want to exclude O(N √N) (Mo's algorithm), ensure queries are online (require forced online with encryption).

### Example: Designing a DP problem

- **Intended solution:** O(N²) DP.
- **Set N ≤ 5 000** (5 000² = 2.5 × 10⁷ — comfortable).
- **Exclude O(N³):** N = 5 000 makes O(N³) = 1.25 × 10¹¹ — way too slow. ✓
- **Exclude O(2^N):** Obviously too slow. ✓
- **Allow O(N² log N)?** 2.5 × 10⁷ × 13 ≈ 3.25 × 10⁸ — might pass. If you want to strictly require O(N²), set N = 3 000 so O(N² log N) ≈ 10⁷ — fine, but O(N³) = 2.7 × 10¹⁰ — still too slow.

---

## 4. Common Constraint Patterns in Competitive Programming

### 4.1 Classic Constraint Signatures

These patterns appear so often they serve as "hints" to experienced contestants:

| Constraint Pattern | Likely Intended Approach |
|---|---|
| N ≤ 20, sum of subsets / permutations | Bitmask DP or backtracking |
| N ≤ 100, grid/path | O(N³) DP or Floyd-Warshall |
| N ≤ 2 000, pairs | O(N²) DP or two-pointer after sorting |
| N ≤ 10⁵, range queries | Segment Tree / Fenwick Tree / Sparse Table |
| N ≤ 10⁵, subarray with property | Two-pointer / Sliding Window / Prefix sums |
| N ≤ 10⁶, counting / frequency | Linear scan, prefix sums, or sieve |
| N ≤ 10⁹, "find the K-th" | Binary search on answer |
| N ≤ 10⁹, modular arithmetic | Number theory (GCD, modular inverse, Euler's theorem) |
| N ≤ 10¹⁸, "after K steps" | Matrix exponentiation or binary lifting |
| String of length ≤ 10⁵, pattern matching | KMP, Z-algorithm, or hashing |
| Tree with N ≤ 2 × 10⁵, path queries | Heavy-Light Decomposition or Centroid Decomposition |

### 4.2 Multi-dimensional Constraints

When multiple variables are involved, the complexity must account for all of them:

| Constraints | Typical Complexity | Notes |
|---|---|---|
| N, M ≤ 1 000 | O(N × M) | 2D grid problems, bipartite matching |
| N ≤ 10⁵, K ≤ 100 | O(N × K) | Knapsack with small capacity, DP with limited states |
| N ≤ 1 000, K ≤ 10 | O(N² × K) or O(N × 2^K) | Choose based on which is smaller |
| N ≤ 10⁵, Q ≤ 10⁵ | O((N + Q) log N) | Offline query processing |

---

## 5. Validation Checklist for Problem Setters

Before finalizing constraints, verify:

- [ ] **Does the intended solution pass?** Calculate worst-case operations and confirm ≤ 10⁸ (or 2 × 10⁸).
- [ ] **Are simpler solutions excluded?** Check if O(N²) brute force passes when you intend O(N log N). If yes, tighten constraints.
- [ ] **Is memory feasible?** Check 2D/3D array sizes against 256 MB limit.
- [ ] **Are test cases accounted for?** If T test cases, verify T × (per-case work) ≤ budget.
- [ ] **Is the constraint "natural"?** Powers of 10 (10⁵, 10⁶) or common values (2 000, 5 000) look natural. Arbitrary values like 13 337 look contrived.
- [ ] **Does the constraint hint too obviously?** N ≤ 20 screams "bitmask" — consider if you want that hint. Sometimes slightly larger constraints (N ≤ 25) can misdirect brute force while still allowing bitmask.

---

## 6. Edge Cases in Constraint Design

### 6.1 When Constraints Lie

Sometimes the constraint doesn't reflect the true complexity:
- **Sparse graphs:** N = 10⁵ nodes but M = 10⁵ edges → O(N + M) algorithms work, even though a dense-graph O(N²) approach wouldn't.
- **Small alphabet:** String of length 10⁵ over alphabet {a, b} → O(N × |Σ|) = O(2N) effectively.
- **Bounded values:** Array of N = 10⁵ elements where each A[i] ≤ 100 → counting sort in O(N + max_A).

### 6.2 The "Sum of N" Pattern

Modern problems often state "the sum of N over all test cases does not exceed X." This means:
- Your solution's total work across all test cases must be O(X × f(X)).
- You cannot have O(N²) per test case if a single test case can have N = X.
- But you CAN have O(N log N) per test case, since Σ(Nᵢ log Nᵢ) ≤ X log X.

---

## 7. Quick Decision Flowchart

```
Given N, what complexity do I need?

N ≤ 20     → Can try exponential: O(2^N), O(N!)
N ≤ 100    → Need cubic or better: O(N³), O(N²)
N ≤ 2000   → Need quadratic or better: O(N²)
N ≤ 10^5   → Need O(N log N) — sorting, trees, divide & conquer
N ≤ 10^6   → Need linear or near-linear: O(N), O(N log log N)
N ≤ 10^9   → Need sublinear: O(√N), O(log N)
N ≤ 10^18  → Need O(log N) or O(1) — math, matrix expo
```

---

*This document is referenced by the Problem Architect and Constraint Validator agents. Use it to verify that every generated problem has consistent constraints and intended solution complexity.*
