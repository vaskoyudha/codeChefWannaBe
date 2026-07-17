# Bloom's Taxonomy Mapping for Programming Problems

> **Purpose:** Maps Bloom's cognitive taxonomy levels to competitive programming problem types. Problem-setting agents use this to target specific cognitive skills and ensure a problem set exercises a range of thinking levels.

---

## Overview

Bloom's taxonomy classifies cognitive skills from simple recall to creative synthesis. In competitive programming, each level corresponds to distinct problem types and solver behaviors.

```
                    ┌─────────────────┐
Level 6 (Revised)   │    CREATE       │  Design novel algorithms
                    ├─────────────────┤
Level 5             │    EVALUATE     │  Compare & justify solutions
                    ├─────────────────┤
Level 4             │    ANALYZE      │  Decompose problems, choose approaches
                    ├─────────────────┤
Level 3             │    APPLY        │  Implement known algorithms
                    ├─────────────────┤
Level 2             │    UNDERSTAND   │  Explain & trace code
                    ├─────────────────┤
Level 1             │    REMEMBER     │  Recall facts & syntax
                    └─────────────────┘
```

---

## Level 1: Remember — Recall Facts & Syntax

### Cognitive Action
Retrieve relevant knowledge from memory. Recognize or recall facts, terms, basic concepts.

### Programming Manifestations
- Syntax recall: "What does `std::sort` do?"
- API knowledge: "Which function computes GCD in C++?"
- Definition recall: "What is a prime number?"
- Formula recall: "What is the time complexity of binary search?"

### Problem Types

| Type | Description | Example |
|---|---|---|
| **MCQ (Syntax)** | Choose correct output of a code snippet | "What does this loop print?" |
| **Fill-in-the-blank** | Complete a code statement | "The time complexity of merge sort is O(___)" |
| **Definition match** | Match term to definition | "Which data structure uses LIFO?" |
| **API identification** | Name the function/method | "Which C++ function finds the lower bound?" |
| **Complexity recall** | State complexity of standard algorithm | "What is the space complexity of BFS?" |

### Example Problem
```
What is the output of the following code?

int a = 5;
int b = a++ + ++a;
cout << b << endl;

A) 10  B) 11  C) 12  D) Undefined behavior
```
**Answer:** D (Undefined behavior in C++)

### Agent Guidance
- **Use for:** Warm-up problems, quizzes, screening rounds
- **Difficulty:** Level 0 in DSA progression
- **Not suitable for:** Main contest problems (too simple)
- **Tip:** Combine with Level 2 for "understand the code, then predict output" problems

---

## Level 2: Understand — Explain & Trace

### Cognitive Action
Construct meaning from messages. Interpret, exemplify, classify, summarize, infer, compare, explain.

### Programming Manifestations
- Trace execution: "What is the value of x after line 15?"
- Explain behavior: "Why does this code give wrong answer?"
- Summarize algorithm: "In one sentence, what does this function compute?"
- Compare approaches: "What's the difference between BFS and DFS?"
- Predict output: "Given this input, what does the program output?"

### Problem Types

| Type | Description | Example |
|---|---|---|
| **Code tracing** | Determine output by mentally executing code | "What does this recursive function return for N=5?" |
| **Bug identification** | Find the error in a given solution | "This Dijkstra implementation fails on which input?" |
| **Algorithm explanation** | Explain why an algorithm works | "Why does greedy fail for the knapsack problem?" |
| **Complexity analysis** | Determine complexity of given code | "What is the time complexity of this nested loop?" |
| **Input-output prediction** | Given algorithm + input, predict output | "What does this sorting algorithm's array look like after pass 3?" |

### Example Problem
```
The following code is supposed to find the maximum element in an array:

int findMax(int arr[], int n) {
    int max = 0;
    for (int i = 0; i < n; i++) {
        if (arr[i] > max) max = arr[i];
    }
    return max;
}

For which input does this function return an incorrect result?

A) [1, 2, 3, 4, 5]
B) [5, 4, 3, 2, 1]
C) [-1, -2, -3]
D) [0, 0, 0]
```
**Answer:** C (initializes max to 0, but all elements are negative)

### Agent Guidance
- **Use for:** Educational problems, debugging exercises, code review simulations
- **Difficulty:** Level 0–1 in DSA progression
- **Not suitable for:** Competitive contests (tests reading comprehension, not problem-solving)
- **Tip:** Good for "what's wrong with this solution?" format — tests understanding without requiring implementation

---

## Level 3: Apply — Implement Known Algorithms

### Cognitive Action
Carry out or use a procedure in a given situation. Execute or implement a known method.

### Programming Manifestations
- Implement a standard algorithm on a new input
- Apply a known technique to a straightforward problem
- Use a data structure to solve a direct application problem
- Follow a described algorithm and code it

### Problem Types

| Type | Description | Example |
|---|---|---|
| **Direct implementation** | Implement a well-known algorithm | "Implement Dijkstra's algorithm for the given graph" |
| **Standard application** | Apply a technique to a new but clear scenario | "Use a segment tree to answer range minimum queries" |
| **Template adaptation** | Modify a standard algorithm slightly | "Modify BFS to find the shortest path with at most K edges" |
| **Recipe following** | Problem statement essentially describes the algorithm | "Simulate the process described, output the final state" |
| **Data structure drill** | Use a specific data structure to solve a problem | "Use a priority queue to merge K sorted arrays" |

### Example Problem
```
Given an array of N integers and Q queries, each query gives L and R.
For each query, find the sum of elements from index L to R (1-indexed).

Constraints: N ≤ 10⁵, Q ≤ 10⁵

Intended solution: Prefix sums — O(N) preprocessing, O(1) per query.
```

### Agent Guidance
- **Use for:** Div2 A/B/C problems, educational rounds, beginner contests
- **Difficulty:** Level 1–2 in DSA progression
- **This is the "bread and butter"** of competitive programming — most problems at the Apply level
- **Tip:** The problem statement should make the approach relatively clear. The challenge is in correct implementation, not in figuring out what to do.

---

## Level 4: Analyze — Decompose & Choose

### Cognitive Action
Break material into constituent parts. Determine how parts relate to each other and to an overall structure. Detect underlying patterns, identify relevant vs. irrelevant information.

### Programming Manifestations
- Decompose a complex problem into subproblems
- Choose the right algorithm/data structure from multiple candidates
- Identify the relevant structure hidden in a problem description
- Debug a broken solution by analyzing why it fails
- Determine which constraints are binding

### Problem Types

| Type | Description | Example |
|---|---|---|
| **Problem decomposition** | Break a complex problem into manageable parts | "Find the number of paths in a grid that pass through exactly K obstacles" → decompose into subproblems |
| **Approach selection** | Multiple valid approaches; choose the best | "Should I use DP or greedy here?" — problem requires analysis to determine |
| **Hidden structure** | Problem looks like X but is actually Y | "This looks like a graph problem but is actually a DP problem on the sequence of choices" |
| **Debugging** | Given a wrong solution, identify the flaw | "This solution gives WA on test 3. What edge case does it miss?" |
| **Constraint analysis** | Determine what the constraints imply about the solution | "N ≤ 10⁵ means I need O(N log N) — what technique fits?" |
| **Counterexample construction** | Disprove a conjecture by finding a counterexample | "Is this greedy always optimal? If not, provide a counterexample." |

### Example Problem
```
You are given a tree with N nodes. Each node has a color. Find the number of
paths (u, v) such that all nodes on the path have distinct colors.

Analysis required:
- It's a tree problem (given)
- "All distinct colors" → need to track color frequency on paths
- Naive: check all O(N²) paths → too slow for N = 10⁵
- Better: use centroid decomposition or DSU on tree to count efficiently
- Key insight: reformulate from "count valid paths" to "count invalid paths" or
  use inclusion-exclusion on color groups
```

### Agent Guidance
- **Use for:** Div2 D/E, Div1 B/C — the "thinking" problems
- **Difficulty:** Level 2–4 in DSA progression
- **The key differentiator** between average and strong contestants
- **Tip:** The problem statement should NOT reveal the approach. The challenge is in analysis, not implementation.

---

## Level 5: Evaluate — Judge & Justify

### Cognitive Action
Make judgments based on criteria and standards. Check, critique, justify, prove, evaluate efficiency.

### Programming Manifestations
- Compare two solutions and justify which is better
- Prove that a greedy approach is correct (or provide a counterexample)
- Evaluate whether a solution meets the required complexity
- Determine if a problem formulation is well-defined
- Judge the optimality of a given answer

### Problem Types

| Type | Description | Example |
|---|---|---|
| **Solution comparison** | Compare two approaches and justify the better one | "Alice uses approach A, Bob uses approach B. Which is faster for N = 10⁵?" |
| **Proof of correctness** | Prove or disprove a greedy strategy | "Prove that the earliest-deadline-first greedy gives optimal scheduling" |
| **Optimality verification** | Determine if a given solution is optimal | "Is this assignment of tasks to machines optimal? Prove it or provide a better one." |
| **Complexity justification** | Justify why a solution is O(f(N)) | "Explain why this algorithm with nested loops is actually O(N log N), not O(N²)" |
| **Lower bound argument** | Prove no algorithm can do better | "Prove that any comparison-based sort requires Ω(N log N) comparisons" |
| **Problem critique** | Identify ambiguity or issues in a problem statement | "This problem statement has two valid interpretations. Identify them." |

### Example Problem
```
Alice claims the following greedy solves the activity selection problem:
"Sort activities by START time. Pick the first activity. Then pick the next
activity whose start time is ≥ the end time of the last picked activity."

1. Is this greedy correct? If yes, prove it. If no, provide a counterexample.
2. If incorrect, what modification makes it correct?
3. Prove that the corrected version is optimal.
```

### Agent Guidance
- **Use for:** Advanced educational problems, proof-based contests, oral examinations
- **Difficulty:** Level 3–5 in DSA progression
- **Rare in standard competitive programming** but valuable for learning
- **Tip:** Interactive format works well — "here's a proposed solution, evaluate it"

---

## Level 6: Create — Design & Synthesize

### Cognitive Action
Put elements together to form a coherent whole. Generate, plan, produce, design novel solutions.

### Programming Manifestations
- Design a novel algorithm for a problem with no standard approach
- Combine multiple techniques in an innovative way
- Create an efficient solution where no known template applies
- Formulate a problem mathematically from a vague description
- Invent a new data structure or algorithm variant

### Problem Types

| Type | Description | Example |
|---|---|---|
| **Novel algorithm design** | Solve a problem with no known standard approach | "Design an algorithm for this new problem type" |
| **Technique fusion** | Combine unrelated techniques creatively | "Combine FFT with centroid decomposition to solve this counting problem" |
| **Open-ended optimization** | Find the best solution to an under-specified problem | "Design a system that handles these constraints optimally" |
| **Problem invention** | Create a new problem given constraints | "Design a graph problem that requires both flow and DP" |
| **Ad-hoc insight** | Problem requires a creative "aha!" moment | "Find the pattern / invariant that makes this problem tractable" |

### Example Problem
```
You are given N points on a plane. You need to partition them into two groups
such that the convex hulls of the two groups don't intersect. Minimize the
difference in sizes of the two groups.

This requires:
- Geometric insight (separating lines)
- Creative formulation (not a standard problem)
- Combining convex hull with partition/optimization
- Novel approach — no textbook algorithm directly applies
```

### Agent Guidance
- **Use for:** Final rounds, olympiad problems, research-inspired challenges
- **Difficulty:** Level 4–6 in DSA progression
- **The hallmark of great contests** — memorable problems that require genuine insight
- **Tip:** These problems are hard to generate automatically. The agent should focus on combining known techniques in new ways rather than pure invention.

---

## Targeting Specific Levels: Agent Guidelines

### For Beginner-Focused Problems (Levels 1–3)
- State the approach clearly or give strong hints
- Use familiar problem structures
- Focus on correct implementation
- Provide examples that illustrate the algorithm
- Constraints should be generous

### For Intermediate Problems (Levels 3–4)
- Don't reveal the approach in the statement
- Require analysis to identify the right technique
- Include red herrings (plausible but wrong approaches)
- Constraints should guide toward the intended complexity
- Test edge cases that distinguish correct from almost-correct solutions

### For Advanced Problems (Levels 4–6)
- Require deep structural insight
- May combine techniques from different domains
- The "trick" is non-obvious and may require mathematical insight
- Constraints may be unusual to prevent standard approaches
- Multiple solution paths may exist with different trade-offs

### Mapping to DSA Learning Progression

| Bloom's Level | Typical DSA Level | Contest Division |
|---|---|---|
| Remember | Level 0 | — |
| Understand | Level 0–1 | — |
| Apply | Level 1–2 | Div2 A/B/C |
| Analyze | Level 2–4 | Div2 D/E, Div1 B/C |
| Evaluate | Level 3–5 | Div1 C/D |
| Create | Level 4–6 | Div1 D/E/F |

### Multi-Level Problems

Most good problems span **2–3 Bloom levels**:
- **Apply + Analyze:** Implement a known technique, but figure out which one (most Div2 C/D)
- **Analyze + Create:** Decompose the problem, then design a novel combination (most Div1 D/E)
- **Understand + Apply:** Trace why a given approach works, then implement an improved version (educational problems)

### Anti-Patterns in Bloom Level Targeting

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Targeting Remember for a contest | Too easy, insults contestants' intelligence | Move to warm-up round or educational section |
| Targeting Create for beginners | Frustrating, no clear entry point | Reduce to Analyze level by hinting at the technique |
| Pure Evaluate in a standard contest | Hard to auto-judge, requires human evaluation | Convert to "find the counterexample" (constructive = auto-judgeable) |
| All problems at same Bloom level | Contest lacks differentiation | Mix Apply (40%), Analyze (40%), Create (20%) |

---

## Quick Reference: Problem → Bloom Level

| If the problem asks the solver to... | Bloom Level |
|---|---|
| Recall a definition or syntax | Remember |
| Explain why code works or trace execution | Understand |
| Implement a standard algorithm | Apply |
| Figure out which algorithm to use | Analyze |
| Prove correctness or compare solutions | Evaluate |
| Design a novel approach | Create |

---

*This document is referenced by the Problem Architect and Difficulty Calibrator agents. Use it to assign cognitive levels to problems and ensure problem sets exercise a balanced range of thinking skills.*
