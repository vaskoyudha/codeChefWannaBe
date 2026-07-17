# Anti-Patterns Checklist for Problem Setting

> **Purpose:** A comprehensive catalog of common anti-patterns in competitive programming problem design. Problem-setting agents use this as a validation checklist before finalizing problems. Review agents use this to critique and reject flawed problems.

---

## How to Use This Checklist

Each anti-pattern includes:
- **Description:** What the anti-pattern looks like
- **Impact:** How it harms the contest/problem quality
- **Detection:** How to identify it (automated checks where possible)
- **Fix:** How to resolve or prevent it

Before finalizing any problem, scan it against all 7 anti-patterns below. A problem with **any** unresolved anti-pattern should be revised or rejected.

---

## Anti-Pattern 1: Ambiguous Problem Statement

### Description
The problem statement has undefined terms, multiple valid interpretations, or hidden assumptions that the solver must guess.

### Symptoms
- Terms used without definition (e.g., "subsequence" without clarifying contiguous vs. non-contiguous)
- Multiple valid readings of the same sentence
- Assumptions buried in examples rather than stated in the problem
- Input format doesn't specify edge cases (e.g., "are the elements distinct?")
- Output format unclear (e.g., "print the answer" — modulo what?)

### Impact
- **High severity:** Solvers waste time guessing the intended interpretation
- Leads to "wrong answer" on correct solutions due to misinterpretation
- Post-contest clarification requests and rejudging
- Erodes trust in problem quality
- In educational contexts: teaches bad problem-reading habits

### Detection
- [ ] Read the statement without looking at examples — can you implement directly?
- [ ] Ask: "Is every term defined on first use?"
- [ ] Ask: "Could this statement be interpreted in two ways?"
- [ ] Check: Are constraints on every input variable explicitly stated?
- [ ] Check: Is the output format unambiguous (modulo, precision, "any" vs. "all")?
- [ ] Verify: Do the examples cover only the stated interpretation?

### Fix
- Define every non-standard term explicitly
- State all assumptions in the problem body (not just in examples)
- Use "It is guaranteed that..." for implicit constraints
- Specify output format precisely: "print the answer modulo 10⁹+7" not "print the answer"
- If multiple interpretations exist, choose one and state it clearly
- Add a "Note" section for clarifications that don't fit in the main statement

### Example
```
BAD:  "Find the number of subsequences with sum S."
      → Is subsequence contiguous or not? Is sum exactly S or at most S?

GOOD: "Find the number of non-contiguous subsequences (subsets of elements
       maintaining their relative order) whose elements sum to exactly S.
       Print the answer modulo 10⁹+7."
```

---

## Anti-Pattern 2: Weak Test Cases

### Description
The test suite fails to distinguish correct solutions from incorrect ones. Trivial or random tests only, no adversarial or edge-case coverage.

### Symptoms
- A brute-force O(2^N) solution passes when O(N log N) is required
- Solutions with known bugs (e.g., not handling N=1) still get AC
- Only randomly generated tests, no structured edge cases
- No stress testing against a verified brute-force solution
- All test cases have N near the middle of the constraint range

### Impact
- **Critical severity:** Incorrect solutions are accepted (false positives)
- Correct solutions with minor edge-case bugs get WA unfairly (false negatives)
- Defeats the purpose of constraints — if brute force passes, the problem tests nothing
- Undermines contest integrity and ranking

### Detection
- [ ] Does an O(2^N) brute force pass? (It shouldn't, unless N is tiny)
- [ ] Does a solution that ignores edge cases (N=1, all same, etc.) pass?
- [ ] Is there a stress test comparing the intended solution against brute force?
- [ ] Are there tests at the constraint boundaries (N = min, N = max)?
- [ ] Are there adversarial tests designed to break common wrong approaches?

### Fix
- Generate structured edge cases (see `edge_case_taxonomy.md`)
- Include tests at every constraint boundary
- Write a brute-force solution and stress-test against it (≥10⁵ random cases)
- Add adversarial tests targeting common wrong approaches
- Verify: removing any single test — would a known-wrong solution still fail on the rest?
- Use a test-case generation strategy:
  1. Hand-crafted edge cases (30%)
  2. Adversarial cases targeting wrong approaches (30%)
  3. Random cases within constraints (30%)
  4. Maximum-size stress tests (10%)

### Example
```
Problem: Maximum subarray sum, N ≤ 10⁵

WEAK TESTS:
- [1, 2, 3, 4, 5] → 15
- [5, 3, 1, 4, 2] → 15
- Random arrays of size 100

PROBLEM: All-negative arrays fail (answer should be max single element, not 0)
A solution returning max(0, kadane()) would pass all weak tests but fail on [-3, -5, -1]

STRONG TESTS (additions):
- [-1000000000] → -1000000000 (single negative element)
- [-1, -2, -3, -4, -5] → -1 (all negative)
- [1000000000, 1000000000, ...] (10⁵ times) → overflow test, need 64-bit
- [1] → single element
- Array of size 10⁵ with all same elements → stress test
```

---

## Anti-Pattern 3: Constraint–Solution Mismatch

### Description
The constraints don't match the intended solution — they're too loose (simpler solutions pass), too tight (intended solution barely passes or fails), or contradictory.

### Symptoms
- **Too loose:** N ≤ 10⁵ but O(N²) passes comfortably
- **Too tight:** N ≤ 10⁵ with O(N log N) intended, but constant factor makes it TLE
- **Contradictory:** Statement says "solve for each query independently" but constraints require offline processing
- **Misleading:** N ≤ 10⁹ suggests O(log N) but intended solution is O(√N)
- **Memory trap:** Constraints allow O(N²) memory but 256 MB limit doesn't

### Impact
- **High severity:** Wrong solutions pass, or correct solutions TLE
- Contestants who find the intended solution are penalized
- Post-contest disputes and rejudging
- The problem fails to test what it's supposed to test

### Detection
- [ ] Calculate the intended solution's worst-case operations — does it fit in the time budget?
- [ ] Calculate the next-slower approach's operations — does it exceed the budget?
- [ ] Check memory: does the intended solution's memory usage fit in 256 MB?
- [ ] Verify: are there multiple valid approaches at different complexities? If so, do the constraints allow all of them?
- [ ] Cross-reference with `constraint_complexity_table.md`

### Fix
- Use the constraint–complexity table to set constraints that:
  - Allow the intended solution with comfortable margin (≤ 50% of time budget)
  - Exclude the next-slower approach (must exceed time budget)
- Account for constant factors (segment tree has ~20× constant vs. simple array)
- If multiple approaches should be valid, set constraints to allow all of them
- Verify memory: N × N × 4 bytes ≤ 256 MB for 2D arrays
- Test with both the intended solution and a known-wrong approach

### Example
```
Intended: O(N log N) with segment tree, N ≤ 10⁵

MISMATCH (too loose): N ≤ 2000
  → O(N²) = 4 × 10⁶ passes easily, defeating the purpose

MISMATCH (too tight): N ≤ 10⁶ with segment tree
  → 4 × 10⁶ nodes × 20 (constant factor) ≈ 8 × 10⁷ operations — tight
  → Memory: 4 × 10⁶ × 4 bytes = 16 MB per array — OK for one, not for five

CORRECT: N ≤ 2 × 10⁵
  → O(N log N) ≈ 3.4 × 10⁶ × 20 ≈ 6.8 × 10⁷ — comfortable
  → O(N²) = 4 × 10¹⁰ — way too slow ✓
  → Memory: 8 × 10⁵ × 4 = 3.2 MB per array — fine ✓
```

---

## Anti-Pattern 4: Implementation-Heavy Problems (Code Monkey)

### Description
A problem that requires 300+ lines of code with no algorithmic insight. The challenge is purely in implementing a complex simulation or data structure, not in choosing the right approach.

### Symptoms
- Solution requires implementing 3+ data structures with no conceptual insight
- The "trick" is just "implement everything carefully"
- No mathematical or algorithmic insight needed — just careful coding
- Problem is essentially a specification document
- Experienced contestants solve it slowly due to code length, not insight

### Impact
- **Medium severity:** Tests typing speed and debugging endurance, not problem-solving
- Disproportionately favors contestants with pre-written templates
- Boring to solve and boring to read editorials for
- Doesn't discriminate based on algorithmic understanding
- Frustrating when a simple bug causes hours of debugging with no learning value

### Detection
- [ ] Is the intended solution > 200 lines?
- [ ] Can the problem be described as "just implement X, Y, and Z"?
- [ ] Is there a moment of insight required, or is it purely mechanical?
- [ ] Does the editorial say "implement these three things and combine them"?

### Fix
- Simplify the problem to require fewer components
- Add a constraint that forces an insight (e.g., "you can only use O(N) memory")
- Split into multiple subtasks with increasing complexity
- Replace simulation with a mathematical insight that shortens the solution
- Ask: "What concept am I testing?" — if the answer is "careful implementation," redesign

### Example
```
BAD: "Simulate a database with INSERT, DELETE, UPDATE, SELECT, JOIN, INDEX,
      TRANSACTION, ROLLBACK, and VIEW operations." (500 lines, no insight)

GOOD: "Given a sequence of database operations, determine if two operations
       conflict." (Requires understanding of conflict detection — insight +
       clean implementation, ~80 lines)
```

---

## Anti-Pattern 5: "Guess the Output" Problems

### Description
Complex simulation problems where the solver must trace through many steps to determine the output. The challenge is in simulating correctly, not in finding an efficient approach.

### Symptoms
- Problem describes a multi-step process with many rules
- The only approach is careful simulation
- No shortcut or mathematical insight exists
- The problem is essentially "run this algorithm and print the result"
- Examples are large and hard to trace by hand

### Impact
- **Medium severity:** Tests simulation accuracy, not algorithmic thinking
- Boring — no "aha!" moment
- Prone to implementation bugs that don't reflect understanding
- Hard to create good test cases (the output is just "whatever the simulation gives")
- Doesn't teach useful skills

### Detection
- [ ] Is the intended solution a direct simulation with no optimization?
- [ ] Could the problem be solved by a non-programmer following rules on paper?
- [ ] Is there no shorter path to the answer than simulating everything?
- [ ] Does the editorial say "just simulate carefully"?

### Fix
- Add a constraint (large N) that forces finding a pattern or mathematical shortcut
- Ask for a property of the final state rather than the full state
- Reduce the number of rules/steps so the simulation is tractable
- Transform into a "find the pattern" problem: "After 10¹⁸ steps, what is the state?"
- If simulation is the point, make it a subtask, not the whole problem

### Example
```
BAD: "Simulate a cellular automaton with these 12 rules for 1000 steps on a
      100×100 grid. Print the final grid." (Pure simulation, no insight)

GOOD: "A cellular automaton evolves by these rules. After 10¹⁸ steps, how many
       cells are alive?" (Requires finding a cycle or closed-form — insight)
```

---

## Anti-Pattern 6: Insufficient Edge Case Coverage

### Description
The problem statement and test cases don't adequately cover edge cases, allowing solutions that handle only the "happy path" to pass.

### Symptoms
- No test with N = 1 or N = minimum constraint
- No test with all elements identical
- No test with extreme values (max, min, zero)
- No test where the answer is 0 or empty
- No test where the answer overflows 32-bit integers
- Problem statement doesn't mention edge case behavior

### Impact
- **High severity:** Incorrect solutions pass (false positives)
- Solutions with off-by-one errors or missing base cases get AC
- Undermines educational value — contestants don't learn to handle edge cases
- Inconsistent scoring: some contestants' bugs happen to be caught, others' aren't

### Detection
- [ ] Check test suite against `edge_case_taxonomy.md` for the problem type
- [ ] Is there a test with minimum input size?
- [ ] Is there a test with maximum input size?
- [ ] Is there a test where the answer is 0 or empty?
- [ ] Is there a test with extreme values?
- [ ] Is there a test that requires 64-bit integers?

### Fix
- Use the edge case taxonomy to generate type-specific edge cases
- Minimum test suite: sample (2-3) + boundaries (3-5) + structural (3-5) + stress (2-3)
- For each edge case, verify that a known-buggy solution fails on it
- State edge case behavior in the problem: "If no valid answer exists, print -1"
- Add a note: "It is guaranteed that the answer fits in a 64-bit integer" (or not, if overflow is part of the challenge)

---

## Anti-Pattern 7: "Anti-Academic" Problems (Obscure Algorithms)

### Description
Problems that require knowledge of an obscure algorithm not found in standard competitive programming curriculum. The problem tests memorization of a niche technique, not problem-solving ability.

### Symptoms
- Solution requires a research-paper algorithm not in standard references
- The technique is known by fewer than 5% of active contestants
- The problem cannot be solved with any combination of standard techniques
- The editorial references a specific paper or advanced textbook chapter
- The technique has no educational value for the target audience

### What Counts as "Obscure"

| Standard (fair game) | Borderline | Obscure (avoid) |
|---|---|---|
| Segment tree, Fenwick tree | Link-Cut tree | Top tree |
| Dijkstra, Bellman-Ford | Min-cost max-flow | Flow with lower bounds + circulation |
| KMP, Z-algorithm | Suffix automaton | Suffix tree with complex applications |
| DSU, Kruskal | Heavy-light decomposition | Euler tour tree with link/cut |
| DP (standard variants) | DP optimization (alien's trick) | Berlekamp-Massey |
| Convex hull, sweep line | Delaunay triangulation | arrangements of curves |
| Matrix exponentiation | FFT/NTT | Multidimensional NTT with applications |

**Note:** The borderline category is acceptable for **advanced contests** (Div1 only, rating 2000+) if the problem provides enough context. It becomes an anti-pattern when used in beginner contests or when the technique is truly necessary with no alternative approach.

### Impact
- **Medium severity (high for beginners):** Rewards memorization over understanding
- Frustrating for contestants who don't know the technique but could solve with insight
- Narrows the skill set that competitive programming develops
- Creates "gatekeeping" problems that exclude self-taught contestants

### Detection
- [ ] Is the required technique in a standard algorithms textbook (CLRS, competitive programming handbooks)?
- [ ] Could a strong contestant who has never seen this technique solve it with insight?
- [ ] Is the technique teachable in a 5-minute editorial, or does it require a chapter?
- [ ] Would >90% of Grandmasters know this technique offhand?

### Fix
- Replace the obscure technique with a combination of standard techniques
- Provide enough context in the problem statement that the technique can be derived
- If the technique is the point, make it an educational problem with a clear tutorial
- Ensure an alternative solution exists using only standard techniques
- Target the right audience: obscure techniques are fine for expert contests if properly flagged

### Example
```
BAD (for Div2): "Given a string of length 10⁵, answer Q queries about the
      lexicographic rank of substrings." → Requires suffix array + advanced
      data structures. Most Div2 contestants haven't learned suffix arrays.

GOOD: Same problem, but with constraints that allow hashing + binary search
      (standard techniques), or move to Div1 with educational context.
```

---

## Quick Validation Checklist

Before finalizing any problem, verify ALL of the following:

### Statement Quality (Anti-Pattern 1)
- [ ] Every term is defined on first use
- [ ] Only one valid interpretation of the problem
- [ ] All input constraints explicitly stated
- [ ] Output format is unambiguous (modulo, precision, format)
- [ ] Examples are consistent with the statement

### Test Case Quality (Anti-Patterns 2 & 6)
- [ ] Brute force does NOT pass (unless intended)
- [ ] Edge cases covered: N=1, all same, sorted, extreme values
- [ ] Adversarial tests targeting common wrong approaches
- [ ] Stress tested against brute force (≥10⁵ random cases)
- [ ] At least one test requires 64-bit integers (if applicable)

### Constraint Consistency (Anti-Pattern 3)
- [ ] Intended solution passes within time limit with comfortable margin
- [ ] Next-slower approach does NOT pass
- [ ] Memory usage fits within limit
- [ ] Constraints match the `constraint_complexity_table.md`

### Insight vs. Implementation (Anti-Patterns 4 & 5)
- [ ] Problem requires at least one moment of insight
- [ ] Solution is < 200 lines (excluding I/O)
- [ ] Not purely a simulation or "guess the output"
- [ ] Editorial describes an insight, not just "implement carefully"

### Accessibility (Anti-Pattern 7)
- [ ] Required technique is standard for the target difficulty
- [ ] Strong contestants can solve with insight even without knowing the specific technique
- [ ] Alternative approaches using standard techniques exist

---

## Severity Summary

| Anti-Pattern | Severity | Frequency | Priority to Fix |
|---|---|---|---|
| 1. Ambiguous statement | High | Common | **Critical** — fix before anything else |
| 2. Weak test cases | Critical | Common | **Critical** — undermines all scoring |
| 3. Constraint mismatch | High | Moderate | **High** — breaks difficulty calibration |
| 4. Implementation-heavy | Medium | Moderate | **Medium** — reduces problem quality |
| 5. Guess the output | Medium | Rare | **Medium** — boring and uneducational |
| 6. Insufficient edge cases | High | Common | **High** — false positives in scoring |
| 7. Anti-academic | Medium | Rare | **Medium** — depends on target audience |

---

*This document is referenced by the Problem Reviewer and Quality Gate agents. Use it as a mandatory checklist before approving any generated problem. A problem failing any Critical or High severity check must be revised.*
