# DSA Learning Progression

> **Purpose:** A structured 7-level progression for Data Structures & Algorithms mastery, from absolute beginner to competitive programming expert. Problem-setting agents use this to tag problems by difficulty level and ensure prerequisite chains are respected.

---

## Overview

| Level | Name | Typical Solver | Example Milestone |
|---|---|---|---|
| 0 | Foundations | Absolute beginner | Can write loops, conditionals, basic I/O |
| 1 | Basic Data Structures | Novice competitor | Can solve Div2 A/B problems |
| 2 | Core Algorithms | Regular Div2 solver | Can solve Div2 C / Div1 A consistently |
| 3 | Intermediate Techniques | Strong Div2 / weak Div1 | Can solve Div2 D / Div1 B |
| 4 | Advanced Techniques | Regular Div1 solver | Can solve Div1 C consistently |
| 5 | Expert Methods | Strong Div1 / Grandmaster path | Can solve Div1 D/E |
| 6 | Research / Creative | Candidate Master+ | Creates novel combinations, solves Div1 F |

---

## Level 0 — Foundations

### Topics
- Variables, data types, type casting
- Control flow: if/else, loops (for, while), nested loops
- Functions, recursion basics (factorial, Fibonacci)
- Basic I/O (reading input, printing output)
- Time complexity awareness (O(1), O(N), O(N²) — conceptual)
- Basic math: GCD, LCM, modular arithmetic (a + b) % m

### Must-Master Concepts
- Can trace a simple loop and determine its iteration count
- Can write a brute-force solution to a simple problem
- Understands that O(N²) with N = 10⁵ will TLE

### Gate Criteria (advance when)
- Can solve 3+ problems rated 800–1000 on Codeforces consistently
- Comfortable writing 30–50 line programs without syntax errors
- Can identify the brute-force approach for any simple problem

---

## Level 1 — Basic Data Structures

### Topics
- **Arrays:** 1D, 2D, prefix sums, difference arrays
- **Strings:** Basic manipulation, reversal, substring search (naive)
- **Sorting:** Built-in sort, custom comparators, stability
- **Searching:** Linear search, binary search (on sorted arrays)
- **Stack & Queue:** Implementation, basic applications (balanced parentheses, next greater element)
- **Hashing:** Hash maps / sets for frequency counting, two-sum style problems
- **Two Pointers:** Opposite-direction, same-direction
- **Sliding Window:** Fixed-size and variable-size windows
- **Greedy basics:** Activity selection, fractional knapsack
- **Number theory basics:** Prime checking (O(√N)), Sieve of Eratosthenes, prime factorization

### Must-Master Concepts
- Prefix sums for O(1) range sum queries
- Binary search: both `lower_bound` / `upper_bound` semantics and custom binary search on answer
- Hash map for O(1) lookups vs. sorted array for O(log N) lookups
- When to sort first, then apply two-pointer

### Gate Criteria
- Can solve 3+ problems rated 1000–1200 consistently
- Can identify when to use prefix sums, binary search, or hashing
- Comfortable with 50–100 line programs

---

## Level 2 — Core Algorithms

### Topics
- **Recursion & Backtracking:** N-Queens, subset generation, permutation generation
- **Divide & Conquer:** Merge sort, quicksort, counting inversions
- **Graphs (Basics):** BFS, DFS, connected components, cycle detection
- **Trees (Basics):** Traversal (in/pre/post-order), diameter, LCA (binary lifting)
- **DP (Intro):** 1D DP (climbing stairs, house robber), 2D DP (grid paths, LCS)
- **Greedy (Intermediate):** Interval scheduling, Huffman coding, job sequencing
- **Number Theory:** Modular exponentiation, Fermat's little theorem, extended GCD
- **Bit Manipulation:** Bitmask basics, subset enumeration, bit tricks
- **Disjoint Set Union (DSU):** Path compression, union by rank, applications

### Must-Master Concepts
- BFS gives shortest path in unweighted graphs
- DP requires identifying overlapping subproblems and optimal substructure
- DSU with path compression is nearly O(1) per operation
- Can distinguish greedy-solvable problems from those requiring DP

### Gate Criteria
- Can solve 3+ problems rated 1300–1500 consistently
- Can recognize standard graph traversals and DP patterns
- Can implement BFS/DFS/DP without reference

---

## Level 3 — Intermediate Techniques

### Topics
- **Segment Trees:** Point update + range query, lazy propagation
- **Fenwick Trees (BIT):** Point update + prefix query, range update variants
- **DP (Intermediate):** Knapsack variants, LIS, digit DP, bitmask DP, DP on trees
- **Graphs (Intermediate):** Dijkstra, Bellman-Ford, Floyd-Warshall, topological sort, MST (Kruskal, Prim)
- **Trees (Intermediate):** Centroid, heavy-light decomposition (intro), Euler tour technique
- **String Algorithms:** KMP, Z-algorithm, string hashing (single and double)
- **Math:** Combinatorics (nCr mod p), inclusion-exclusion, pigeonhole principle
- **Square Root Decomposition:** Block decomposition, Mo's algorithm (basic)
- **Binary Search on Answer:** Parametric search, binary search on real values

### Must-Master Concepts
- Segment tree with lazy propagation for range update + range query
- Difference between Dijkstra (non-negative weights) and Bellman-Ford (handles negative)
- When to use bitmask DP vs. regular DP
- String hashing: collision probability and double hashing

### Gate Criteria
- Can solve 3+ problems rated 1600–1800 consistently
- Can implement a segment tree with lazy propagation from scratch
- Can identify DP state transitions for non-trivial problems

---

## Level 4 — Advanced Techniques

### Topics
- **Advanced DP:** DP with data structures (DP + segment tree), broken profile DP, game theory (Nim, Sprague-Grundy)
- **Advanced Graphs:** Strongly connected components (Tarjan, Kosaraju), 2-SAT, network flow (max-flow min-cut, Dinic's)
- **Advanced Trees:** Link-Cut trees, persistent segment trees, heavy-light decomposition (advanced)
- **Advanced Strings:** Suffix arrays, suffix automata, Aho-Corasick
- **Advanced Data Structures:** Treaps, Splay trees, persistent data structures
- **Geometry (Basics):** Convex hull, line intersection, point-in-polygon, sweep line
- **Number Theory (Advanced):** Chinese Remainder Theorem, Miller-Rabin, Pollard's rho, discrete logarithm
- **FFT/NTT:** Polynomial multiplication, applications to counting problems

### Must-Master Concepts
- Max-flow formulation: how to model real problems as flow networks
- Suffix array construction in O(N log N) and its applications
- When to use persistent data structures vs. offline processing
- FFT for polynomial multiplication and its applications to string/counting problems

### Gate Criteria
- Can solve 3+ problems rated 1900–2100 consistently
- Can model complex problems as flow networks or DP
- Comfortable implementing advanced data structures under time pressure

---

## Level 5 — Expert Methods

### Topics
- **Advanced Flow:** Min-cost max-flow, flow with lower bounds, circulation
- **Advanced Geometry:** Half-plane intersection, rotating calipers, Minkowski sum, Delaunay triangulation
- **String (Expert):** Suffix tree, palindromic tree (Eertree), suffix automaton applications
- **Decomposition Techniques:** Centroid decomposition (advanced), long path decomposition, DSU on tree
- **Advanced Math:** Generating functions, Burnside's lemma, Polya enumeration, linear recurrences (Berlekamp-Massey)
- **Data Structure Combinatorics:** Segment tree beats, Li Chao tree, kinetic segment tree
- **Randomized Algorithms:** Randomized hashing, simulated annealing, randomized divide & conquer
- **Online Algorithms:** Link-Cut tree applications, top tree (conceptual)

### Must-Master Concepts
- Can combine 2+ advanced techniques in a single problem
- Understands when randomized algorithms are appropriate
- Can derive generating functions for counting problems
- Can implement min-cost max-flow and flow with lower bounds

### Gate Criteria
- Can solve 3+ problems rated 2200–2400 consistently
- Can recognize when to combine advanced techniques
- Regularly solves Div1 C/D problems

---

## Level 6 — Research / Creative

### Topics
- Novel combinations of known techniques
- Problems requiring mathematical insight beyond standard curriculum
- Constructive algorithms with no standard template
- Interactive problems with information-theoretic lower bounds
- Problems requiring deep understanding of computational complexity
- Ad-hoc problems that resist classification

### Characteristics
- No fixed syllabus — solver creates new approaches
- Often involves proving properties of the problem structure before coding
- May require adapting research-paper algorithms
- Creative insight is more important than technique memorization

### Gate Criteria
- Can solve Div1 E/F problems
- Can create original problem ideas that combine techniques in novel ways
- Contributes to problem-setting or competitive programming community

---

## Prerequisite Chains

### Binary Search Chain
```
Level 0: Loops, conditionals
  ↓
Level 1: Binary search on sorted array, binary search on answer
  ↓
Level 2: Parametric search, ternary search
  ↓
Level 3: Binary search + data structures (e.g., binary search on segment tree)
  ↓
Level 4+: Binary search in interactive problems, parallel binary search
```

### Dynamic Programming Chain
```
Level 0: Recursion basics
  ↓
Level 1: Memoization concept (overlapping subproblems)
  ↓
Level 2: 1D DP, 2D DP, basic knapsack, LIS
  ↓
Level 3: Bitmask DP, digit DP, DP on trees, broken profile
  ↓
Level 4: DP + data structures, game theory, broken profile DP
  ↓
Level 5: Generating functions, Berlekamp-Massey, linear recurrence solving
```

### Graph Theory Chain
```
Level 0: Adjacency list representation
  ↓
Level 1: (No graph topics at this level)
  ↓
Level 2: BFS, DFS, connected components, topological sort, basic trees
  ↓
Level 3: Dijkstra, MST, Bellman-Ford, Floyd-Warshall, DSU
  ↓
Level 4: SCC, 2-SAT, network flow, HLD
  ↓
Level 5: Min-cost max-flow, flow with lower bounds, centroid decomposition
  ↓
Level 6: Novel graph constructions, ad-hoc graph problems
```

### String Algorithms Chain
```
Level 0: String basics (character arrays, length, comparison)
  ↓
Level 1: Naive pattern matching, string hashing (single)
  ↓
Level 2: KMP, Z-algorithm, double hashing
  ↓
Level 3: Suffix array, Aho-Corasick
  ↓
Level 4: Suffix automaton, FFT-based string matching
  ↓
Level 5: Suffix tree, palindromic tree, advanced suffix automaton
```

### Number Theory Chain
```
Level 0: Basic divisibility, GCD
  ↓
Level 1: Prime checking, Sieve of Eratosthenes
  ↓
Level 2: Modular exponentiation, extended GCD, Fermat's little theorem
  ↓
Level 3: Combinatorics, inclusion-exclusion, CRT
  ↓
Level 4: Miller-Rabin, Pollard's rho, discrete log, FFT/NTT
  ↓
Level 5: Generating functions, Burnside/Polya, linear recurrences
```

---

## Topic Clusters (Natural Combinations)

These technique groups appear together frequently in problems:

### Cluster 1: "Range Query" Cluster
- Prefix sums → Fenwick tree → Segment tree → Segment tree with lazy propagation
- Often combined with: binary search, coordinate compression

### Cluster 2: "Graph Traversal + DP" Cluster
- BFS/DFS → topological sort → DP on DAG → DP on trees
- Often combined with: rerooting technique, DSU on tree

### Cluster 3: "Optimization" Cluster
- Greedy → DP → greedy optimization of DP (divide & conquer optimization, Knuth optimization, alien's trick / lambda optimization)

### Cluster 4: "String Matching" Cluster
- Hashing → KMP → Suffix array → Suffix automaton
- Often combined with: DP on strings, palindrome detection

### Cluster 5: "Counting" Cluster
- Combinatorics → inclusion-exclusion → generating functions → Burnside/Polya
- Often combined with: DP, matrix exponentiation

### Cluster 6: "Flow" Cluster
- Max flow → min-cut → max-flow min-cut theorem → min-cost max-flow → flow with lower bounds
- Often combined with: binary search, greedy

---

## Usage Notes for Problem Setting

1. **Tag every problem with a level** (0–6) based on the primary technique required.
2. **Respect prerequisite chains** — a Level 3 problem should not require Level 4 techniques.
3. **Combine topics within clusters** for natural difficulty progression.
4. **Cross-cluster combinations** increase difficulty — a problem combining segment trees (Cluster 1) with game theory (Cluster 2/DP) is harder than either alone.
5. **The level refers to the solution technique, not the problem statement complexity.** A problem with a simple statement but requiring suffix automaton is Level 4+.

---

*This document is referenced by the Problem Architect and Difficulty Calibrator agents. Use it to assign appropriate difficulty levels and ensure problems in a set follow a logical progression.*
