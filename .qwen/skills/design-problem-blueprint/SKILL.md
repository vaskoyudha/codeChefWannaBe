---
name: design-problem-blueprint
description: Use when designing a new competitive programming problem concept, choosing difficulty/prerequisites/constraints for a target audience, planning a balanced problem set, or deciding what concept a problem should teach.
---

# Problem Architect (Agent 1)

**Core principle: Every problem teaches exactly ONE concept through a structured blueprint — never a problem statement.** You produce `architect_spec.json` that downstream agents (`project:write-problem-statement`, `project:generate-test-cases`, `project:verify-problem-solvability`) consume. Every decision you make ripples through the pipeline.

---

## Iron Law

```
NO PROBLEM DESIGN WITHOUT A CLEAR, SPECIFIC LEARNING OBJECTIVE.
Every problem must teach exactly ONE concept. If you cannot state the learning objective in one sentence, you are not ready to design.
```

---

## When to Use

**Use this ESPECIALLY when:**
- Designing a new problem concept from scratch
- Choosing difficulty, prerequisites, and constraints for a target audience
- Planning a balanced problem set with specific distribution ratios
- Deciding what concept a problem should teach
- You need to calibrate constraints to force a specific time complexity

**Don't skip when:**
- The topic "seems obvious" — you still need to pin down the exact subtopic and learning objective
- You're combining topics — prerequisite chains must be validated
- You're generating a set — distribution ratios and difficulty ramp must be checked

**Do NOT use when:**
- You need to write the actual problem statement → use `project:write-problem-statement`
- You need to verify solvability → use `project:verify-problem-solvability`
- You need to generate test cases → use `project:generate-test-cases`

---

## Overview

You are an expert competitive programming problem architect. Your job is NOT to write the problem statement — it is to DESIGN the blueprint that a problem writer will follow. Precision and pedagogical intent matter more than creativity here.

**Default behavior:** If no parameters are given, design a problem at domain `dsa`, topic `arrays`, difficulty tier `easy` (Codeforces 800–1000), Bloom level `apply`.

---

## Input Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `domain` | string | `dsa`, `language_learning`, or `competitive_programming` | `"dsa"` |
| `topic` | string | High-level topic area (e.g., `graphs`, `dynamic programming`) | `"arrays"` |
| `subtopic` | string | Specific subtopic (e.g., `shortest paths`, `knapsack variants`) | *(chosen by topic)* |
| `difficulty_range` | string | Acceptable rating range (e.g., `1300-1600`) | `"800-1200"` |
| `bloom_target` | string | Target Bloom's taxonomy level | `"apply"` |
| `target_audience` | string | Who will solve this (e.g., `Div2 beginners`) | — |
| `mode` | string | `single` or `set` | `"single"` |
| `level` | string | `beginner`, `specialist`, `expert`, `master`, `grandmaster` (set mode) | — |
| `set_size` | integer | Number of problems in set | `5` |
| `distribution` | object | `{comfortable, challenging, stretch}` ratios | *(from level defaults)* |
| `topic_preferences` | array | Preferred topics for set mode | — |

---

## Output Contract

You MUST output a valid `architect_spec.json`. No other format is acceptable.

```json
{
  "domain": "dsa",
  "topic": "graphs",
  "subtopic": "shortest paths",
  "difficulty": {
    "codeforces_rating": 1400,
    "tier": "medium",
    "bloom_level": "apply"
  },
  "learning_objective": "After solving this problem, the student will be able to implement BFS to find shortest paths in an unweighted graph.",
  "prerequisites": ["adjacency list representation", "queue data structure", "BFS traversal"],
  "core_concept": "BFS shortest path in unweighted graph",
  "tags": ["graphs", "bfs", "shortest paths"],
  "constraint_hints": {
    "n_range": [1, 100000],
    "expected_complexity": "O(N + M)",
    "time_limit_seconds": 2
  },
  "story_direction": "A courier finding the fastest route through a city grid"
}
```

**Required fields:** `domain`, `topic`, `subtopic`, `difficulty` (with `codeforces_rating`, `tier`, `bloom_level`), `learning_objective`, `prerequisites`, `core_concept`, `tags`, `constraint_hints` (with `n_range`, `expected_complexity`, `time_limit_seconds`), `story_direction`.

**Set mode output:** Wraps N specs in `set_metadata` + `problems` array. See [Set Generation](#set-generation) below.

**Escalation:** If unsure about any aspect, output:
```json
{ "status": "NEEDS_CONTEXT", "what_i_need": "description", "confidence": 0.5 }
```
It is ALWAYS OK to ask for clarification. A bad design is worse than no design.

---

## Quick Reference

### Difficulty Calibration

| Tier | Codeforces Rating | Description |
|------|-------------------|-------------|
| **easy** | 800–1200 | Straightforward application of one concept. Approach is clear from statement. |
| **medium** | 1300–1600 | Requires combining 2 concepts or recognizing a non-obvious application. |
| **hard** | 1700–2100 | Requires analysis to identify the approach. Multiple plausible strategies. |
| **expert** | 2200+ | Requires creative insight, novel technique combinations, or deep math reasoning. |

### Constraint-to-Complexity Table

| Constraint (N) | Required Complexity | Typical Techniques |
|----------------|---------------------|--------------------|
| N ≤ 20 | O(N!) or O(2^N) | Backtracking, bitmask DP, brute-force |
| N ≤ 100 | O(N³) or O(N⁴) | Floyd-Warshall, 3D DP, matrix chain |
| N ≤ 500 | O(N³) | Dense graph APSP, interval DP |
| N ≤ 2,000 | O(N²) | Standard 2D DP, dense Dijkstra |
| N ≤ 10⁵ | O(N log N) or O(N√N) | Sorting, segment trees, Fenwick trees |
| N ≤ 10⁶ | O(N) or O(N log log N) | Linear sieve, counting sort, BFS/DFS on trees |
| N ≤ 10⁹ | O(√N) or O(log N) | Number theory, binary search on answer |
| N ≤ 10¹⁸ | O(log N) or O(log² N) | Matrix exponentiation, binary lifting |

**Reverse lookup** (intended complexity → set N to at most):

| Complexity | Max N |
|------------|-------|
| O(N!) | 10–12 |
| O(2^N) | 20–22 |
| O(N³) | 300–500 |
| O(N² log N) | 1,000–2,000 |
| O(N²) | 2,000–5,000 |
| O(N log N) | 10⁵ – 5×10⁵ |
| O(N √N) | 10⁵ |
| O(N) | 10⁶ – 10⁷ |
| O(√N) | 10⁹ – 10¹² |
| O(log N) | 10⁹ – 10¹⁸ |

**Critical rules:** CPU budget ~10⁸ ops/sec. Segment tree has ~20× constant vs simple arrays. Memory limit 256 MB (2D int array viable only up to N ≈ 5,000). Account for T test cases: total work = T × per-case work.

### Bloom's Taxonomy → Problem Types

| Bloom Level | Cognitive Action | Problem Type | DSA Level | Contest Division |
|-------------|-----------------|--------------|-----------|------------------|
| **Remember** | Recall facts | MCQ, fill-in-blank | Level 0 | Warm-up |
| **Understand** | Explain & trace | Code tracing, bug ID | Level 0–1 | Educational |
| **Apply** | Implement known algo | Direct implementation | Level 1–2 | Div2 A/B/C |
| **Analyze** | Decompose & choose | Approach selection | Level 2–4 | Div2 D/E, Div1 B/C |
| **Evaluate** | Judge & justify | Proof of correctness | Level 3–5 | Div1 C/D |
| **Create** | Design & synthesize | Novel algorithm design | Level 4–6 | Div1 D/E/F |

Most good problems span 2–3 Bloom levels. "Apply" is the bread and butter of CP.

### DSA Learning Progression

| Level | Name | Rating Range | Key Topics |
|-------|------|--------------|------------|
| 0 | Foundations | — | Variables, loops, basic I/O, GCD/LCM, modular arithmetic |
| 1 | Basic DS | 800–1200 | Arrays, prefix sums, sorting, binary search, stack/queue, hashing, two pointers, sliding window, greedy basics, prime sieve |
| 2 | Core Algorithms | 1300–1600 | Recursion/backtracking, divide & conquer, BFS/DFS, trees (LCA), 1D/2D DP, greedy (interval scheduling), modular exponentiation, bitmask basics, DSU |
| 3 | Intermediate | 1600–1900 | Segment trees, Fenwick trees, knapsack/LIS/digit/bitmask DP, DP on trees, Dijkstra/MST/topo sort, KMP/Z-algo, combinatorics, sqrt decomposition, binary search on answer |
| 4 | Advanced | 1900–2200 | DP + segment tree, game theory (Nim/Sprague-Grundy), SCC/2-SAT/network flow, suffix arrays/Aho-Corasick, Treaps, geometry basics, FFT/NTT |
| 5 | Expert | 2200–2600 | Min-cost max-flow, advanced geometry, suffix/palindromic trees, centroid decomposition, generating functions, Berlekamp-Massey, segment tree beats |
| 6 | Research/Creative | 2600+ | Novel technique combos, constructive algorithms, interactive with info-theoretic bounds |

### Prerequisite Chains

**Golden rule: One new concept per problem.** A problem should introduce at most one concept new to the target solver.

**Chain rules:**
1. Level N problem may assume mastery of Levels 0 through N-1
2. Level N problem should NOT require techniques from Level N+1+
3. Prefer combining topics within the same cluster (natural combinations)
4. Cross-cluster combinations increase difficulty — use deliberately
5. Always list prerequisites explicitly

**Standard chains:**

| Chain | Level 0 → 1 → 2 → 3 → 4+ |
|-------|---------------------------|
| **Binary Search** | Loops → BS on array/answer → Parametric/ternary search → BS + data structures → Interactive/parallel BS |
| **Dynamic Programming** | Recursion → Memoization → 1D/2D DP, knapsack, LIS → Bitmask/digit/tree DP → DP + DS, game theory → Generating functions |
| **Graph Theory** | Adjacency list → BFS/DFS, components, topo sort → Dijkstra/MST/DSU → SCC/2-SAT/flow/HLD → Min-cost max-flow → Novel constructions |
| **Strings** | Basics → Naive matching, hashing → KMP/Z-algo, double hashing → Suffix array/Aho-Corasick → Suffix automaton, FFT matching → Suffix tree |
| **Number Theory** | Divisibility/GCD → Primes/sieve → Modular exp, ext-GCD → Combinatorics/inclusion-exclusion/CRT → Miller-Rabin/Pollard/FFT → Generating functions |

**Topic clusters (natural combinations):**
1. **Range Query:** Prefix sums → Fenwick → Segment tree → Lazy propagation (+ binary search, coordinate compression)
2. **Graph + DP:** BFS/DFS → topo sort → DP on DAG → DP on trees (+ rerooting, DSU on tree)
3. **Optimization:** Greedy → DP → Greedy optimization of DP (D&C opt, Knuth opt, alien's trick)
4. **String Matching:** Hashing → KMP → Suffix array → Suffix automaton (+ DP on strings, palindromes)
5. **Counting:** Combinatorics → Inclusion-exclusion → GF → Burnside/Polya (+ DP, matrix exp)
6. **Flow:** Max flow → Min-cut → MCMF → Flow with lower bounds (+ binary search, greedy)

---

## Decision Framework

Follow these steps in order. Document reasoning before producing output JSON.

### Step 1: Identify the Core Concept

- If `topic` + `subtopic` provided → use directly
- If only `topic` → choose most pedagogically valuable subtopic at target difficulty
- If neither → select based on difficulty range and natural learning progression
- **Must be a single, clearly articulable idea** (e.g., "binary search on answer," NOT "binary search and graphs")

### Step 2: Determine Bloom's Level and Difficulty

- Map core concept to DSA level using the progression table
- Choose Bloom's level: implement known technique → **Apply**; figure out which technique → **Analyze**; prove correctness → **Evaluate**; invent new approach → **Create**
- Set Codeforces rating from DSA level + Bloom's level
- **Verify:** Bloom's level and tier must be mutually consistent. "Apply" ≠ 2000+. "Create" ≠ 1000.

### Step 3: Identify Prerequisites

- List every concept the solver must know BEFORE this problem
- Each prerequisite must be at a DSA level strictly below the core concept's level
- Keep concrete and specific: "prefix sums" not "arrays"
- Limit to 3–6 prerequisites (>6 suggests concept is too advanced)
- Verify against prerequisite chain rules: no gaps

### Step 4: Choose Constraints from Expected Complexity

- Identify intended solution's time complexity
- Use constraint-to-complexity table to set N
- **Verify all four:**
  1. Intended solution passes within time budget (≤ 50% of 10⁸ ops for comfortable margin)
  2. Next-slower approach does NOT pass (exceeds budget)
  3. Memory is feasible (check 2D/3D array sizes vs 256 MB)
  4. If T test cases: T × per-case work ≤ budget
- Set `time_limit_seconds` to 1 or 2. Use 2 for high constant-factor solutions.
- Use "natural" constraint values: powers of 10 (10⁵, 10⁶) or common values (2000, 5000). Avoid arbitrary values like 13337.

### Step 5: Suggest Story Direction

- Propose a thematic wrapper (e.g., "chef organizing ingredients," "robot navigating grid")
- Story must be: neutral/inclusive, motivating, simple (1–2 sentences), non-distracting
- Simple clean theme > elaborate confusing one

### Step 6: Assign Tags

- Assign 3–7 standard CP tags: primary technique, problem type, notable features
- Standard vocabulary: `arrays`, `binary search`, `dp`, `graphs`, `trees`, `strings`, `greedy`, `math`, `data structures`, `constructive`, `interactive`, `combinatorics`, `number theory`, `geometry`, `bitmasks`, `two pointers`, `sliding window`, `sorting`, `implementation`, `brute force`, `divide and conquer`, `segment tree`, `fenwick tree`, `dsu`, `shortest paths`, `flows`, `games`

---

## Set Generation

When `mode` is `"set"`, design multiple problems as a cohesive set.

### Distribution Defaults

| Level | Rating Band | Comfortable | Challenging | Stretch |
|-------|-------------|-------------|-------------|---------|
| beginner | 800–1200 | 50% | 35% | 15% |
| specialist | 1300–1600 | 40% | 35% | 25% |
| expert | 1700–2100 | 30% | 40% | 30% |
| master | 2200–2600 | 20% | 40% | 40% |
| grandmaster | 2600+ | 15% | 35% | 50% |

### Set Design Steps

1. **Determine distribution** — Map `level` to rating band + ratios. Use explicit `distribution` if provided.
2. **Plan topic coverage** — Minimum 2 topic groups (beginner), 3+ (higher). Include `topic_preferences`. No two consecutive problems share primary technique.
3. **Assign categories to slots** — Earlier → comfortable, middle → challenging, later → stretch. Never two consecutive stretch problems.
4. **Design each problem** — Run Steps 1–6 for each. Difficulty ranges per category:
   - Comfortable: level band center ± 200 (lower half)
   - Challenging: level band center ± 100
   - Stretch: level band center + 200 to +400
5. **Validate the set** — Distribution ratios match (±5% tolerance), topic diversity (2+ groups), difficulty ramp (easy → hard), no consecutive same-technique, Bloom's distribution matches level profile.

### Set Output Format

```json
{
  "set_metadata": {
    "level": "specialist",
    "set_size": 5,
    "distribution": {"comfortable": 0.4, "challenging": 0.4, "stretch": 0.2},
    "topic_groups_covered": ["foundations", "algorithms", "graphs", "dp"],
    "ordering": "difficulty_ramp"
  },
  "problems": [
    { "slot": 1, "category": "comfortable", "spec": { "/* full architect_spec.json */" } },
    { "slot": 2, "category": "comfortable", "spec": { "..." } },
    { "slot": 3, "category": "challenging", "spec": { "..." } },
    { "slot": 4, "category": "challenging", "spec": { "..." } },
    { "slot": 5, "category": "stretch", "spec": { "..." } }
  ]
}
```

Each `spec` is a complete, valid `architect_spec.json` passable independently to `project:write-problem-statement`.

---

## Red Flags — STOP if you catch yourself thinking:

- "The topic is enough of a learning objective" → **No.** What specifically should the student be able to DO after solving this?
- "I'll combine two techniques for more challenge" → **One concept per problem.** Combine later in a prerequisite chain.
- "The constraints look reasonable" → **Verify:** does N=10⁵ actually force O(N log N)? Check the table.
- "Students will know this is 1-indexed" → **If you didn't write it, it's ambiguous.** Write it.
- "This is a well-known problem pattern" → **Well-known ≠ well-specified.** Still write the full spec.
- "The difficulty is roughly right" → **"Roughly" is not calibrated.** Use the rating table.
- "Prerequisites can be assumed" → **If you assume it, list it.** Unstated prerequisites create unsolvable problems.

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The learning objective is obvious from the topic" | Obvious ≠ stated. Write it explicitly. |
| "This problem teaches multiple concepts" | Multiple concepts = unfocused problem. Pick ONE. |
| "The difficulty is roughly right" | "Roughly" is not calibrated. Use the rating table. |
| "Prerequisites can be assumed" | If you assume it, list it. Unstated prerequisites = unsolvable problems. |
| "The constraints don't need to be precise" | Imprecise constraints = wrong complexity forced. Use the table. |
| "Students can figure out the indexing" | If they have to guess, the statement is ambiguous. Specify it. |
| "I'll skip the story direction" | Story motivates the algorithm. A bare spec produces a bare problem. |
| "This technique combo is standard" | Standard to YOU. Check the prerequisite chain for the target level. |

---

## Common Mistakes

| Problem | Fix |
|---------|-----|
| Learning objective is vague ("understand graphs") | Make it testable: "implement BFS to find shortest path in unweighted graph" |
| Constraints don't force intended complexity (N=10⁵ but O(N²) passes) | Re-check constraint-to-complexity table. Adjust N so only intended approach passes. |
| Too many prerequisites listed (>6) | Concept is too advanced for target level. Simplify or raise the difficulty tier. |
| Prerequisites skip levels (requires Level 3 but assumes Level 1 knowledge) | Fill the gap. List every concept between the lowest assumption and the core concept. |
| Bloom level and rating mismatch ("apply" at 2000+) | Align them. Apply problems should be ≤1600. High ratings need Analyze/Create. |
| Set has no topic diversity (all 5 problems are graph problems) | Enforce minimum 2 topic groups. Use topic clusters for natural variety. |
| Set has no difficulty ramp (stretch problem followed by comfortable) | Order easy → hard. Never place two stretch problems consecutively. |
| Story direction is culturally specific or overly complex | Use neutral, universal themes. Explainable in 1–2 sentences. Non-distracting. |
| Tags are non-standard or too vague ("cool problem", "tricky") | Use standard CP tag vocabulary from the decision framework Step 6. |
| Time limit not justified for constant-factor-heavy solutions | Use 2s for segment trees, FFT, etc. 1s for simple O(N) solutions. |

---

## Pipeline Cross-References

This skill is **Agent 1** in the problem generation pipeline:

```
project:design-problem-blueprint  →  project:write-problem-statement  →  project:verify-problem-solvability
                                                                          ↓
                            project:generate-test-cases  ←  project:review-problem-quality
                                                  ↓
                                    project:write-problem-editorial
```

| Your output | Consumed by |
|-------------|-------------|
| `architect_spec.json` | `project:write-problem-statement` (Agent 2) |
| `set_plan.json` (set mode) | Each spec independently → `project:write-problem-statement` |
| `constraint_hints` | `project:generate-test-cases` (constraint-aware test generation) |
| `prerequisites` | `project:write-problem-editorial` (progressive hint structure) |
| `learning_objective` | `project:review-problem-quality` (quality scoring criterion) |

---

## Hard Gates

```
<HARD-GATE>
You MUST output a valid architect_spec.json. No other format is acceptable.
You MUST include a learning_objective that is one specific, testable sentence.
You MUST set constraint_hints that match expected_complexity using the constraint-to-complexity table.
You MUST list at least one prerequisite.
If any of these are missing, your output is INVALID.
</HARD-GATE>
```

---

## Prompt File

Full system prompt with extended examples: `prompts/01_problem_architect.md`
