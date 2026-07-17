# Edge Case Taxonomy

> **Purpose:** A comprehensive taxonomy of edge cases organized by problem type. Problem-setting agents use this to ensure test suites cover critical boundary conditions. Test generation agents use this to construct adversarial test cases.

---

## General Principles

Before diving into type-specific edge cases, these universal categories apply to **all** problems:

1. **Minimum input size** — N = 0, N = 1, or the smallest valid input
2. **Maximum input size** — N at the constraint boundary (stress test)
3. **All elements identical** — removes variety, tests uniformity handling
4. **Already sorted** — tests if algorithm exploits or breaks on sorted input
5. **Reverse sorted** — tests if algorithm handles worst-case ordering
6. **Extreme values** — elements at INT_MAX, INT_MIN, or constraint boundaries
7. **All zeros** — tests zero-handling, division-by-zero guards
8. **Negative values** — tests signed arithmetic, comparison assumptions
9. **Single-element result** — output is trivially small despite large input
10. **Maximum output** — output at the largest possible value (overflow check)

---

## 1. Array Problems

### Size-Based Edge Cases
| Case | Description | What It Tests |
|---|---|---|
| N = 1 | Single element | Off-by-one in loops, base case handling |
| N = 2 | Two elements | Minimum case for pairwise comparisons, two-pointer |
| N = 3 | Three elements | Minimum for "three distinct" or "triangle" problems |
| All same elements | [5, 5, 5, 5, 5] | Duplicate handling, partition stability |
| Strictly increasing | [1, 2, 3, ..., N] | Sorted-input assumptions, binary search correctness |
| Strictly decreasing | [N, N-1, ..., 1] | Worst case for some sorting algorithms, reverse-sorted assumptions |

### Value-Based Edge Cases
| Case | Description | What It Tests |
|---|---|---|
| All zeros | [0, 0, ..., 0] | Division by zero, zero-sum subarrays |
| All negative | [-5, -3, -1, -7] | Sign handling, max subarray with all negatives |
| Mixed signs | [-100, 0, 100] | Overflow in intermediate calculations |
| Max values | [10⁹, 10⁹, ..., 10⁹] | Integer overflow (sum of two 10⁹ > INT_MAX for 32-bit) |
| Min values | [-10⁹, -10⁹, ..., -10⁹] | Underflow, negative overflow |
| Single large, rest small | [1, 1, 1, ..., 10⁹] | Max/min dominated by one element |
| Alternating | [1, -1, 1, -1, ...] | Pattern-dependent algorithms, prefix sum oscillation |

### Structural Edge Cases
| Case | Description | What It Tests |
|---|---|---|
| All elements form answer | Every element is part of the optimal solution | Greedy correctness |
| No valid subarray/subsequence | Answer is empty or 0 | Empty-result handling |
| Answer is the entire array | Full range is the solution | Boundary inclusion |
| Answer is a single element | Trivial solution exists | Over-complication trap |
| Multiple optimal answers | Many subarrays give the same max/min | Output format (any vs. all) |

### Example: Maximum Subarray Sum (Kadane's)
```
Must-test cases:
- All negative: [-3, -5, -1, -9] → answer is -1 (single element)
- All same: [5, 5, 5, 5] → answer is 20 (entire array)
- Single element: [42] → answer is 42
- Alternating: [1, -2, 3, -4, 5] → tests running sum reset
- Max values: [10⁹, 10⁹, 10⁹] → overflow check (need 64-bit)
```

---

## 2. Graph Problems

### Structural Edge Cases
| Case | Description | What It Tests |
|---|---|---|
| Single node (N=1) | Graph with one vertex, no edges | Base case, loop handling |
| Two nodes, one edge | Minimum connected graph | Simplest path/cut |
| Disconnected graph | Multiple components | Component traversal, "impossible" paths |
| Complete graph | Every pair connected (N(N-1)/2 edges) | Dense graph performance, O(N²) edge iteration |
| Tree | N-1 edges, connected, no cycles | Tree-specific algorithms, parent-child relationships |
| Cycle | Graph contains a cycle | Cycle detection, infinite loop prevention |
| Self-loop | Edge from node to itself | Dijkstra correctness, DFS visited handling |
| Multi-edges | Multiple edges between same pair | Edge counting, minimum selection |
| Star graph | One center connected to all others | Center-biased algorithms, degree-based logic |
| Linear chain | 1-2-3-...-N | Path graph, DFS stack depth (recursion limit) |
| Bipartite graph | Two-colorable | 2-coloring, matching algorithms |
| Directed vs. undirected | Edge direction matters | Strongly connected components, reachability |

### Weight-Based Edge Cases (Weighted Graphs)
| Case | Description | What It Tests |
|---|---|---|
| All weights zero | Every edge has weight 0 | Dijkstra vs. BFS, zero-weight cycles |
| Negative weights | Some edges have negative weight | Bellman-Ford necessity, negative cycle detection |
| Negative cycle | Cycle with total negative weight | Detection requirement, "shortest path undefined" |
| Very large weights | Weights near 10⁹ | Path sum overflow |
| All same weights | Reduces to unweighted | BFS should give same result as Dijkstra |

### Path/Connectivity Edge Cases
| Case | Description | What It Tests |
|---|---|---|
| Source = destination | Path from node to itself | Zero-length path handling |
| No path exists | Source and destination in different components | "Impossible" output handling |
| Unique path | Only one path between source and destination | Tree-like structure in general graph |
| All paths same length | Multiple shortest paths | Counting paths vs. finding one |
| Bridge edge | Removing it disconnects the graph | Bridge-finding, articulation points |

### Example: Shortest Path (Dijkstra)
```
Must-test cases:
- Disconnected: source and destination in different components → -1
- Source = destination → 0
- Self-loop on source → should be ignored
- Negative edge → Dijkstra fails (need Bellman-Ford)
- Linear chain → longest path, tests relaxation order
- Star graph → all paths go through center
- Large weights → overflow in distance array
```

---

## 3. String Problems

### Size-Based Edge Cases
| Case | Description | What It Tests |
|---|---|---|
| Empty string | Length 0 | Null/empty handling, loop boundary |
| Single character | "a" | Minimum non-empty input |
| Two characters | "ab" or "aa" | Minimum for pairwise comparison |
| Maximum length | N at constraint boundary | Performance, memory |

### Pattern-Based Edge Cases
| Case | Description | What It Tests |
|---|---|---|
| All same characters | "aaaa...a" | Run-length, repeated pattern handling |
| All distinct characters | "abcdef...z" | No repetition, uniqueness assumptions |
| Palindrome | "racecar", "abba" | Symmetry exploitation |
| Near-palindrome | "abcddcba" vs "abcdeba" | Off-by-one in palindrome detection |
| Repeated pattern | "abcabcabc" | Period detection, KMP failure function |
| No match | Pattern doesn't occur in text | Empty result handling |
| Match at start | Pattern at index 0 | Boundary inclusion |
| Match at end | Pattern at last valid position | Off-by-one in end conditions |
| Overlapping matches | "aa" in "aaa" → 2 matches | Non-overlapping vs. overlapping counting |
| Pattern = text | Exact match | Full-string comparison |
| Pattern longer than text | Impossible match | Early termination |

### Case-Sensitivity and Character Set
| Case | Description | What It Tests |
|---|---|---|
| Mixed case | "aAbBcC" | Case-sensitivity assumptions |
| Non-alphabetic | Digits, special characters | ASCII/Unicode assumptions |
| Unicode / multi-byte | Emojis, CJK characters | Character vs. byte handling |
| Spaces and newlines | "hello world" | Whitespace handling in input parsing |

### Example: Pattern Matching (KMP)
```
Must-test cases:
- Pattern not in text → -1 or 0 occurrences
- Pattern = text → 1 match at position 0
- Pattern at very end of text → boundary
- Overlapping: pattern "aa" in "aaaa" → 3 (overlapping) or 2 (non-overlapping)
- All same: pattern "aaa" in "aaaaaa" → stress test failure function
- Single char pattern → degenerate case
- Pattern longer than text → no match possible
```

---

## 4. DP Problems

### Base Case Edge Cases
| Case | Description | What It Tests |
|---|---|---|
| N = 0 | Empty input | Base case of recursion, empty collection |
| N = 1 | Single item | Trivially solvable, first non-base case |
| Capacity = 0 | Knapsack with zero capacity | Zero-capacity handling, answer is 0 |
| Target = 0 | Sum/product target is 0 | Zero-target handling |
| All weights same | Every item has identical weight | Symmetry, counting distinct subsets |
| All values same | Every item has identical value | Greedy works when values are equal |

### Feasibility Edge Cases
| Case | Description | What It Tests |
|---|---|---|
| Impossible case | No valid selection meets the target | -1 or "impossible" output |
| Exactly one way | Unique solution | Counting vs. existence |
| All ways valid | Every selection works | Answer is 2^N or C(N,K) |
| Maximum answer | Answer exceeds 32-bit integer | Need for modular arithmetic or 64-bit |
| Answer is 0 | Valid input but result is 0 | Zero vs. impossible distinction |

### DP-Specific Structural Cases
| Case | Description | What It Tests |
|---|---|---|
| All items fit | Total weight < capacity | Greedy vs. DP distinction |
| No items fit | Smallest item > capacity | Answer is 0 |
| Single item exactly fills | One item = capacity | Boundary of feasibility |
| Increasing weights | [1, 2, 4, 8, ...] | Exponential growth, subset sum uniqueness |
| Decreasing values | Higher weight = lower value | Trade-off optimization |
| Ties in DP table | Multiple states give same optimal value | Counting distinct optimal solutions |

### Example: 0/1 Knapsack
```
Must-test cases:
- N=1, item fits → take it
- N=1, item doesn't fit → 0
- Capacity = 0 → 0
- All items same weight and value → count how many fit
- All items fit → sum of all values
- No items fit → 0
- Exact subset sums to capacity → tests precision
- Answer requires 64-bit → large values
- Answer modulo 10⁹+7 → counting variant
```

---

## 5. Tree Problems

### Structural Edge Cases
| Case | Description | What It Tests |
|---|---|---|
| Single node | N = 1, no edges | Base case, empty path |
| Two nodes | N = 2, one edge | Minimum tree |
| Linear chain (caterpillar) | 1-2-3-...-N | Recursion depth, path-based algorithms |
| Star graph | One center, N-1 leaves | Center-biased logic, degree-based algorithms |
| Complete binary tree | Perfectly balanced | Balanced-tree assumptions, height = log N |
| Degenerate binary tree | Each node has only one child (becomes a chain) | BST worst case, recursion depth |
| Binary tree with all left children | Skewed left | Mirror of degenerate case |

### Property-Based Edge Cases
| Case | Description | What It Tests |
|---|---|---|
| All nodes same value | Uniform values | Equality handling, max/min on equal elements |
| Leaf-only query | Query targets only leaves | Leaf identification, parent access |
| Root-only path | Path from root to root | Single-node path |
| Deepest leaf | Maximum depth node | Depth tracking, stack overflow in DFS |
| Diameter path | Longest path in tree | Two-DFS or rerooting technique |
| Centroid is root | Centroid coincides with root | Centroid decomposition base case |

### LCA / Path Edge Cases
| Case | Description | What It Tests |
|---|---|---|
| LCA of node with itself | Should return the node | Identity case |
| LCA of parent and child | Should return parent | Ancestor check |
| LCA of nodes in different subtrees | Standard case | Correctness of jump pointers |
| Path from node to ancestor | Upward path only | Direction handling |
| Path covering root | Path crosses the root | Subtree decomposition |

### Example: Tree Diameter
```
Must-test cases:
- N=1 → diameter is 0
- N=2 → diameter is 1
- Star graph → diameter is 2 (leaf to leaf through center)
- Linear chain → diameter is N-1 (end to end)
- Complete binary tree → diameter passes through root
- Diameter has even length → center is an edge
- Diameter has odd length → center is a node
```

---

## 6. Math / Number Theory Problems

### Input Value Edge Cases
| Case | Description | What It Tests |
|---|---|---|
| N = 0 | Zero input | Division by zero, 0! = 1, empty product = 1 |
| N = 1 | Unit input | Identity elements, trivial factorization |
| N = 2 | Smallest prime | Edge of prime/composite boundary |
| Negative N | Negative input | Signed arithmetic, absolute value |
| N = INT_MAX | 2³¹ - 1 = 2147483647 | 32-bit overflow, prime check on large value |
| N = 10⁹ | Common constraint boundary | √N = 31623, fits in int |
| N = 10¹⁸ | Large constraint | Need for 64-bit, √N = 10⁹ |

### Number Property Edge Cases
| Case | Description | What It Tests |
|---|---|---|
| N is prime | Has exactly 2 divisors | Factorization, primality testing |
| N is a perfect square | √N is integer | Square root precision (floating point issues) |
| N is a perfect power | N = a^b for some a, b > 1 | Root extraction, logarithm precision |
| N is highly composite | Many divisors (e.g., 720720) | Divisor enumeration performance |
| N is a power of 2 | N = 2^k | Bit manipulation, binary representation |
| N = p × q (semiprime) | Product of two large primes | Factorization difficulty |
| Coprime inputs | GCD(a, b) = 1 | Modular inverse existence |
| One divides the other | a | b or b | a | Divisibility edge |

### Overflow Boundary Cases
| Case | Description | What It Tests |
|---|---|---|
| a × b > INT_MAX | Two large ints multiplied | Need for long long |
| a + b > INT_MAX | Two large ints added | Need for long long |
| a^b overflows | Exponentiation result too large | Modular exponentiation required |
| N! overflows | Factorial exceeds 64-bit | Need for modular arithmetic |
| C(N, K) overflows | Binomial coefficient too large | Pascal's triangle mod p, or Lucas' theorem |
| Intermediate overflow | Final answer fits but intermediates don't | Careful ordering of operations, modular inverse |

### Example: Counting Divisors
```
Must-test cases:
- N = 1 → 1 divisor
- N = 2 → 2 divisors (1, 2)
- N = prime → 2 divisors
- N = p^k → k+1 divisors
- N = p × q → 4 divisors
- N = perfect square → odd number of divisors
- N = 10⁹ → stress test √N approach
- N = 10¹⁸ → need for O(N^(1/3)) or Pollard's rho
```

---

## 7. Geometry Problems (Supplementary)

### Degenerate Cases
| Case | Description | What It Tests |
|---|---|---|
| All points collinear | No proper polygon | Convex hull degeneracy |
| All points identical | Single location | Distance = 0, area = 0 |
| Two points only | No triangle possible | Minimum for line segment |
| Triangle with zero area | Three collinear points | Cross product = 0 |
| Point on edge boundary | Exactly on the border | Inside/outside test precision |
| Point at vertex | Exactly on a vertex | Vertex inclusion |

### Precision Edge Cases
| Case | Description | What It Tests |
|---|---|---|
| Very small coordinates | Near-zero values | Floating point precision |
| Very large coordinates | Near-max values | Overflow in cross product |
| Nearly collinear points | Cross product ≈ 0 but not exactly | Epsilon comparison |
| Irrational results | √2, π in answers | Output precision (fixed decimal places) |

---

## 8. Combinatorics / Counting Problems

| Case | Description | What It Tests |
|---|---|---|
| Count is 0 | No valid configurations | Empty set handling |
| Count is 1 | Unique configuration | Trivial case |
| Count is N! | All permutations valid | Over-counting check |
| Count exceeds 64-bit | Need modular arithmetic | Modular output |
| K = 0 or K = N | Choosing nothing or everything | C(N,0) = C(N,N) = 1 |
| K > N | Impossible selection | Answer is 0 |
| Repetition allowed vs. not | Stars and bars vs. combinations | Formula selection |

---

## 9. Interactive Problems (Supplementary)

| Case | Description | What It Tests |
|---|---|---|
| Minimum queries | Information-theoretic lower bound | Optimal strategy |
| Maximum queries | Just within query limit | Efficiency |
| Adversarial responses | Hidden input designed to break specific strategies | Robustness |
| Consistent but misleading | Responses consistent with multiple answers | Disambiguation |

---

## 10. Test Suite Construction Guidelines

### Minimum Test Suite Per Problem
Every problem's test suite should include:

1. **Sample tests** (2–3): Illustrate the problem, cover basic cases
2. **Boundary tests** (3–5): Min/max input sizes, extreme values
3. **Structural tests** (3–5): Type-specific edge cases from this taxonomy
4. **Stress tests** (2–3): Maximum input size with adversarial structure
5. **Random tests** (5–10): Randomly generated within constraints

### Adversarial Test Generation Strategy
1. Identify the intended solution's weakness (e.g., quicksort worst case = sorted input)
2. Construct input that triggers that weakness
3. Verify the intended solution still passes (it should — the weakness is in naive approaches)
4. Verify that incorrect solutions fail on this input

### Coverage Checklist
For each problem, verify tests cover:
- [ ] Minimum input size
- [ ] Maximum input size (stress)
- [ ] All-same elements
- [ ] Sorted / reverse-sorted (if applicable)
- [ ] Extreme values (max, min, zero)
- [ ] Type-specific structural edge cases (from relevant section above)
- [ ] At least one case where answer is 0 or empty
- [ ] At least one case where answer is maximum possible

---

*This document is referenced by the Test Suite Generator and Edge Case Validator agents. Use it to ensure comprehensive test coverage for every generated problem.*
