#!/usr/bin/env python3
"""
Agent Skills Problem Gen — Practice Tool
Reads final_problem.json files and lets you solve them interactively.

Usage:
    python practice.py <problem.json>                  # View the problem
    python practice.py <problem.json> --test <sol.py>  # Test your solution
    python practice.py <problem.json> --hints          # Show progressive hints
    python practice.py <problem.json> --editorial      # Show the editorial
    python practice.py <problem.json> --all            # Show everything
"""

import json
import sys
import os
import subprocess
import tempfile
import argparse
import time
from pathlib import Path


# ─── Terminal Colors ───────────────────────────────────────────────────────────

class Colors:
    """ANSI color codes for terminal output."""
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    
    BG_GREEN = "\033[42m"
    BG_RED = "\033[41m"
    BG_YELLOW = "\033[43m"
    
    RESET = "\033[0m"


def c(text, color):
    """Colorize text."""
    return f"{color}{text}{Colors.RESET}"


def bold(text):
    return c(text, Colors.BOLD)


def dim(text):
    return c(text, Colors.DIM)


def header(text):
    return c(text, Colors.BOLD + Colors.CYAN)


def success(text):
    return c(text, Colors.GREEN)


def error(text):
    return c(text, Colors.RED)


def warning(text):
    return c(text, Colors.YELLOW)


# ─── Problem Loader ────────────────────────────────────────────────────────────

def load_problem(path):
    """Load and validate a final_problem.json file."""
    try:
        with open(path) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(error(f"File not found: {path}"))
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(error(f"Invalid JSON: {e}"))
        sys.exit(1)
    
    # Validate required sections
    required = ["metadata", "problem", "solution", "test_suite", "editorial"]
    missing = [s for s in required if s not in data]
    if missing:
        print(error(f"Missing sections: {', '.join(missing)}"))
        sys.exit(1)
    
    return data


def load_problem_set(path):
    """Load and validate a final_problem_set.json file."""
    try:
        with open(path) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(error(f"File not found: {path}"))
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(error(f"Invalid JSON: {e}"))
        sys.exit(1)
    
    # Validate required sections
    if "set_metadata" not in data or "problems" not in data:
        print(error("Not a valid problem set file (missing set_metadata or problems)"))
        sys.exit(1)
    
    return data


# ─── Display Functions ─────────────────────────────────────────────────────────

def display_problem(data):
    """Display the problem statement nicely."""
    meta = data["metadata"]
    prob = data["problem"]
    
    # Title bar
    width = 70
    print()
    print(c("═" * width, Colors.CYAN))
    title = prob.get("title", "Untitled Problem")
    print(c(f"  {title}", Colors.BOLD + Colors.CYAN))
    print(c("═" * width, Colors.CYAN))
    print()
    
    # Metadata badges
    diff = meta.get("difficulty", {})
    tier = diff.get("tier", "unknown").upper()
    rating = diff.get("codeforces_rating", "?")
    tags = ", ".join(meta.get("tags", []))
    bloom = meta.get("bloom_level", "unknown")
    
    tier_color = {"easy": Colors.GREEN, "medium": Colors.YELLOW, "hard": Colors.RED, "expert": Colors.MAGENTA}.get(tier.lower(), Colors.WHITE)
    
    print(f"  {bold('Difficulty:')} {c(tier, tier_color)} (CF {rating})")
    print(f"  {bold('Topic:')} {meta.get('topic', '?')} → {meta.get('subtopic', '?')}")
    print(f"  {bold('Tags:')} {tags}")
    print(f"  {bold('Bloom Level:')} {bloom}")
    print(f"  {bold('Prerequisites:')} {', '.join(meta.get('prerequisites', ['none']))}")
    print()
    
    # Story
    story = prob.get("story", "")
    if story:
        print(c("─" * width, Colors.DIM))
        print(f"  {bold('Story')}")
        print(c("─" * width, Colors.DIM))
        for line in story.strip().split("\n"):
            print(f"  {line}")
        print()
    
    # Statement
    print(c("─" * width, Colors.DIM))
    print(f"  {bold('Problem Statement')}")
    print(c("─" * width, Colors.DIM))
    for line in prob.get("statement", "").strip().split("\n"):
        print(f"  {line}")
    print()
    
    # Input Format
    print(c("─" * width, Colors.DIM))
    print(f"  {bold('Input Format')}")
    print(c("─" * width, Colors.DIM))
    input_fmt = prob.get("input_format", {})
    if isinstance(input_fmt, dict):
        for key, val in input_fmt.items():
            print(f"  {c(key, Colors.YELLOW)}: {val}")
    else:
        print(f"  {input_fmt}")
    print()
    
    # Output Format
    print(f"  {bold('Output Format')}")
    print(f"  {prob.get('output_format', '')}")
    print()
    
    # Constraints
    print(c("─" * width, Colors.DIM))
    print(f"  {bold('Constraints')}")
    print(c("─" * width, Colors.DIM))
    for constraint in prob.get("constraints", []):
        print(f"  {c('•', Colors.CYAN)} {constraint}")
    print()
    
    # Subtasks
    subtasks = prob.get("subtasks", [])
    if subtasks:
        print(f"  {bold('Subtasks')}")
        for st in subtasks:
            pts = st.get("points", "?")
            desc = st.get("description", "")
            constraints = ", ".join(st.get("constraints", []))
            print(f"  {c(f'[{pts} pts]', Colors.MAGENTA)} {desc} ({constraints})")
        print()
    
    # Sample Tests
    print(c("─" * width, Colors.DIM))
    print(f"  {bold('Sample Tests')}")
    print(c("─" * width, Colors.DIM))
    samples = prob.get("sample_tests", [])
    for i, sample in enumerate(samples, 1):
        print(f"\n  {c(f'Sample {i}:', Colors.YELLOW)}")
        print(f"  {bold('Input:')}")
        for line in sample.get("input", "").split("\n"):
            print(f"    {c(line, Colors.WHITE)}")
        print(f"  {bold('Output:')}")
        for line in sample.get("output", "").split("\n"):
            print(f"    {c(line, Colors.GREEN)}")
        explanation = sample.get("explanation", "")
        if explanation:
            print(f"  {bold('Explanation:')} {dim(explanation)}")
    
    # Notes
    notes = prob.get("notes", [])
    if notes:
        print()
        print(f"  {bold('Notes:')}")
        for note in notes:
            print(f"  {c('⚠', Colors.YELLOW)} {note}")
    
    print()
    print(c("═" * width, Colors.CYAN))
    print()


def display_hints(data):
    """Display progressive hints."""
    editorial = data.get("editorial", {})
    hints = editorial.get("hints", [])
    
    if not hints:
        print(warning("No hints available."))
        return
    
    print()
    print(header("💡 Progressive Hints"))
    print(c("─" * 50, Colors.DIM))
    print()
    
    for i, hint in enumerate(hints, 1):
        level = ["🟢 Direction", "🟡 Approach", "🔴 Key Insight"][i - 1] if i <= 3 else f"Hint {i}"
        print(f"  {bold(f'Hint {i} — {level}:')}")
        print(f"  {hint}")
        print()
    
    print(c("─" * 50, Colors.DIM))
    print(dim("  Try to solve before reading the editorial!"))
    print()


def display_editorial(data):
    """Display the full editorial."""
    editorial = data.get("editorial", {})
    
    print()
    print(header("📖 Editorial"))
    print(c("═" * 60, Colors.CYAN))
    print()
    
    # Brute force explanation
    bf = editorial.get("brute_force_explanation", "")
    if bf:
        print(f"  {bold('Brute Force Approach:')}")
        for line in bf.strip().split("\n"):
            print(f"  {line}")
        print()
    
    # Optimal solution walkthrough
    walkthrough = editorial.get("optimal_solution_walkthrough", "")
    if walkthrough:
        print(c("─" * 50, Colors.DIM))
        print(f"  {bold('Optimal Solution:')}")
        print(c("─" * 50, Colors.DIM))
        for line in walkthrough.strip().split("\n"):
            print(f"  {line}")
        print()
    
    # Complexity analysis
    complexity = editorial.get("complexity_analysis", "")
    if complexity:
        print(f"  {bold('Complexity Analysis:')}")
        for line in complexity.strip().split("\n"):
            print(f"  {line}")
        print()
    
    # Alternative approaches
    alts = editorial.get("alternative_approaches", [])
    if alts:
        print(c("─" * 50, Colors.DIM))
        print(f"  {bold('Alternative Approaches:')}")
        for alt in alts:
            print(f"  {c('•', Colors.CYAN)} {alt}")
        print()
    
    # Common mistakes
    mistakes = editorial.get("common_mistakes", [])
    if mistakes:
        print(c("─" * 50, Colors.DIM))
        print(f"  {bold('Common Mistakes:')}")
        for mistake in mistakes:
            print(f"  {c('✗', Colors.RED)} {mistake}")
        print()
    
    print(c("═" * 60, Colors.CYAN))
    print()


# ─── Solution Tester ───────────────────────────────────────────────────────────

def detect_language(filepath):
    """Detect programming language from file extension."""
    ext = Path(filepath).suffix.lower()
    lang_map = {
        ".py": "python",
        ".cpp": "cpp",
        ".cc": "cpp",
        ".cxx": "cpp",
        ".c": "c",
        ".java": "java",
        ".js": "javascript",
        ".ts": "typescript",
        ".rb": "ruby",
        ".go": "go",
        ".rs": "rust",
    }
    return lang_map.get(ext)


def compile_solution(filepath, language):
    """Compile the solution if needed. Returns (executable_path, error_msg)."""
    if language == "python":
        return filepath, None
    
    if language == "cpp" or language == "c":
        # Compile C++
        output = tempfile.mktemp(prefix="solution_")
        compiler = "g++" if language == "cpp" else "gcc"
        cmd = [compiler, "-O2", "-o", output, filepath]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                return None, f"Compilation failed:\n{result.stderr}"
            return output, None
        except FileNotFoundError:
            return None, f"{compiler} not found. Install g++ first."
    
    if language == "java":
        # Java needs to be in the right directory with the right class name
        return filepath, None
    
    return None, f"Unsupported language: {language}"


def run_solution(executable, language, input_text, timeout=10):
    """Run the solution with given input. Returns (output, time_seconds, error)."""
    try:
        if language == "python":
            cmd = ["python3", executable]
        elif language in ("cpp", "c"):
            cmd = [executable]
        elif language == "java":
            # Compile first
            dir_path = os.path.dirname(os.path.abspath(executable))
            compile_result = subprocess.run(
                ["javac", executable],
                capture_output=True, text=True, timeout=30, cwd=dir_path
            )
            if compile_result.returncode != 0:
                return None, 0, f"Java compilation failed:\n{compile_result.stderr}"
            # Find class name
            class_name = Path(executable).stem
            cmd = ["java", "-cp", dir_path, class_name]
        elif language == "javascript":
            cmd = ["node", executable]
        elif language == "go":
            cmd = ["go", "run", executable]
        elif language == "ruby":
            cmd = ["ruby", executable]
        elif language == "rust":
            # Compile first
            output = tempfile.mktemp(prefix="solution_")
            compile_result = subprocess.run(
                ["rustc", "-O", "-o", output, executable],
                capture_output=True, text=True, timeout=30
            )
            if compile_result.returncode != 0:
                return None, 0, f"Rust compilation failed:\n{compile_result.stderr}"
            cmd = [output]
        else:
            return None, 0, f"Unsupported language: {language}"
        
        start = time.time()
        result = subprocess.run(
            cmd,
            input=input_text,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        elapsed = time.time() - start
        
        if result.returncode != 0:
            return None, elapsed, f"Runtime error (exit code {result.returncode}):\n{result.stderr}"
        
        return result.stdout.strip(), elapsed, None
    
    except subprocess.TimeoutExpired:
        return None, timeout, "Time Limit Exceeded (TLE)"
    except Exception as e:
        return None, 0, f"Error: {e}"


def display_problem_set(data):
    """Display a problem set overview."""
    meta = data["set_metadata"]
    problems = data["problems"]
    
    width = 70
    print()
    print(c("═" * width, Colors.CYAN))
    print(c(f"  Problem Set — {meta.get('level', 'unknown').upper()}", Colors.BOLD + Colors.CYAN))
    print(c("═" * width, Colors.CYAN))
    print()
    
    # Set metadata
    level = meta.get("level", "unknown").upper()
    set_size = meta.get("set_size", len(problems))
    successful = meta.get("successful_count", sum(1 for p in problems if p.get("status") == "success"))
    
    dist_target = meta.get("distribution_target", {})
    dist_actual = meta.get("distribution_actual", {})
    topics = meta.get("topic_groups_covered", [])
    
    print(f"  {bold('Level:')} {c(level, Colors.YELLOW)}")
    print(f"  {bold('Problems:')} {successful}/{set_size} successful")
    print(f"  {bold('Topics:')} {', '.join(topics) if topics else 'N/A'}")
    print()
    
    # Distribution bar
    print(f"  {bold('Distribution (target → actual):')}")
    for cat in ["comfortable", "challenging", "stretch"]:
        target = dist_target.get(cat, 0)
        actual = dist_actual.get(cat, 0)
        target_pct = f"{target*100:.0f}%"
        actual_pct = f"{actual*100:.0f}%"
        cat_color = {"comfortable": Colors.GREEN, "challenging": Colors.YELLOW, "stretch": Colors.RED}.get(cat, Colors.WHITE)
        bar_len = 30
        filled = int(actual * bar_len)
        bar = c("█" * filled, cat_color) + c("░" * (bar_len - filled), Colors.DIM)
        print(f"    {cat:12s} {bar} {actual_pct} (target: {target_pct})")
    print()
    
    # Problem list
    print(c("─" * width, Colors.DIM))
    print(f"  {bold('Problems:')}")
    print(c("─" * width, Colors.DIM))
    print()
    
    for entry in problems:
        slot = entry.get("slot", "?")
        category = entry.get("category", "?")
        status = entry.get("status", "?")
        
        cat_color = {"comfortable": Colors.GREEN, "challenging": Colors.YELLOW, "stretch": Colors.RED}.get(category, Colors.WHITE)
        status_icon = c("✓", Colors.GREEN) if status == "success" else c("✗", Colors.RED)
        
        if status == "success" and entry.get("problem"):
            prob = entry["problem"]
            prob_meta = prob.get("metadata", {})
            prob_data = prob.get("problem", {})
            title = prob_data.get("title", "Untitled")
            rating = prob_meta.get("difficulty", {}).get("codeforces_rating", "?")
            topic = prob_meta.get("topic", "?")
            bloom = prob_meta.get("bloom_level", "?")
            
            print(f"  {status_icon} {c(f'Problem {slot}', Colors.BOLD)} — {title}")
            print(f"     {c(category, cat_color)} | CF {rating} | {topic} | Bloom: {bloom}")
        else:
            reason = entry.get("failure_reason", "Unknown error")
            print(f"  {status_icon} {c(f'Problem {slot}', Colors.BOLD)} — {c('FAILED', Colors.RED)}")
            print(f"     {dim(reason[:80])}")
        print()
    
    # Warnings
    warnings = data.get("warnings", [])
    if warnings:
        print(c("─" * width, Colors.DIM))
        print(f"  {bold('Warnings:')}")
        for w in warnings:
            print(f"  {c('⚠', Colors.YELLOW)} {w}")
        print()
    
    print(c("═" * width, Colors.CYAN))
    print()
    print(dim("  Use --problem N to view/test a specific problem from the set."))
    print()


def export_to_markdown(data, output_path=None):
    """Convert final_problem.json to a clean Markdown file."""
    meta = data.get("metadata", {})
    prob = data.get("problem", {})
    solution = data.get("solution", {})
    test_suite = data.get("test_suite", {})
    editorial = data.get("editorial", {})

    md = []

    # Title and metadata
    title = prob.get("title", "Untitled Problem")
    md.append(f"# {title}\n")

    diff = meta.get("difficulty", {})
    tier = diff.get("tier", "unknown").upper()
    rating = diff.get("codeforces_rating", "?")
    topic = meta.get("topic", "?")
    subtopic = meta.get("subtopic", "?")
    bloom = meta.get("bloom_level", "?")
    tags = ", ".join(meta.get("tags", []))

    md.append(f"**Difficulty:** {tier} (CF {rating})  ")
    md.append(f"**Topic:** {topic} → {subtopic}  ")
    md.append(f"**Bloom Level:** {bloom}  ")
    md.append(f"**Tags:** {tags}\n")
    md.append("---\n")

    # Story
    story = prob.get("story", "")
    if story:
        md.append("## Story\n")
        md.append(story)
        md.append("")

    # Problem Statement
    statement = prob.get("statement", "")
    if statement:
        md.append("## Problem Statement\n")
        md.append(statement)
        md.append("")

    # Input Format
    input_fmt = prob.get("input_format", {})
    if input_fmt:
        md.append("## Input Format\n")
        if isinstance(input_fmt, dict):
            for key, val in input_fmt.items():
                md.append(f"- **{key}:** {val}")
        else:
            md.append(str(input_fmt))
        md.append("")

    # Output Format
    output_fmt = prob.get("output_format", "")
    if output_fmt:
        md.append("## Output Format\n")
        md.append(output_fmt)
        md.append("")

    # Constraints
    constraints = prob.get("constraints", [])
    if constraints:
        md.append("## Constraints\n")
        for c in constraints:
            md.append(f"- {c}")
        md.append("")

    # Subtasks
    subtasks = prob.get("subtasks", [])
    if subtasks:
        md.append("## Subtasks\n")
        for st in subtasks:
            pts = st.get("points", "?")
            desc = st.get("description", "")
            cons = ", ".join(st.get("constraints", []))
            md.append(f"- **[{pts} pts]** {desc} ({cons})")
        md.append("")

    # Sample Tests
    samples = prob.get("sample_tests", [])
    if samples:
        md.append("## Sample Tests\n")
        for i, sample in enumerate(samples, 1):
            md.append(f"### Sample {i}\n")
            inp = sample.get("input", "")
            out = sample.get("output", "")
            exp = sample.get("explanation", "")

            md.append("**Input:**")
            md.append("```")
            md.append(inp)
            md.append("```\n")

            md.append("**Output:**")
            md.append("```")
            md.append(out)
            md.append("```\n")

            if exp:
                md.append(f"**Explanation:** {exp}\n")

    # Notes
    notes = prob.get("notes", [])
    if notes:
        md.append("## Notes\n")
        for note in notes:
            md.append(f"- ⚠ {note}")
        md.append("")

    md.append("---\n")

    # Hints (collapsible)
    hints = editorial.get("hints", [])
    if hints:
        md.append("## Hints\n")
        hint_labels = ["Direction", "Approach", "Key Insight"]
        for i, hint in enumerate(hints):
            label = hint_labels[i] if i < len(hint_labels) else f"Hint {i+1}"
            md.append(f"<details>")
            md.append(f"<summary>Hint {i+1} ({label})</summary>")
            md.append("")
            md.append(hint)
            md.append("")
            md.append("</details>\n")

    md.append("---\n")

    # Editorial
    md.append("## Editorial\n")

    bf = editorial.get("brute_force_explanation", "")
    if bf:
        md.append("### Brute Force Approach\n")
        md.append(bf)
        md.append("")

    walkthrough = editorial.get("optimal_solution_walkthrough", "")
    if walkthrough:
        md.append("### Optimal Solution\n")
        md.append(walkthrough)
        md.append("")

    complexity = editorial.get("complexity_analysis", "")
    if complexity:
        md.append("### Complexity Analysis\n")
        md.append(complexity)
        md.append("")

    alts = editorial.get("alternative_approaches", [])
    if alts:
        md.append("### Alternative Approaches\n")
        for alt in alts:
            md.append(f"- {alt}")
        md.append("")

    mistakes = editorial.get("common_mistakes", [])
    if mistakes:
        md.append("### Common Mistakes\n")
        for m in mistakes:
            md.append(f"-  {m}")
        md.append("")

    # Write to file
    content = "\n".join(md)

    if output_path is None:
        # Default: same name as input but .md extension
        input_path = args.problem if hasattr(args, 'problem') else "problem"
        output_path = str(Path(input_path).with_suffix('.md'))

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return output_path


def normalize_output(text):
    """Normalize output for comparison (strip whitespace, normalize line endings)."""
    if text is None:
        return ""
    lines = text.strip().split("\n")
    return "\n".join(line.strip() for line in lines)


def test_solution(data, solution_path):
    """Test a solution against all test cases."""
    test_suite = data.get("test_suite", {})
    test_cases = test_suite.get("test_cases", [])
    
    if not test_cases:
        print(warning("No test cases found in the problem file."))
        return
    
    # Detect language
    language = detect_language(solution_path)
    if not language:
        print(error(f"Cannot detect language for: {solution_path}"))
        print(dim("Supported: .py, .cpp, .c, .java, .js, .go, .rb, .rs"))
        return
    
    print()
    print(header(f"🧪 Testing Solution"))
    print(c("─" * 60, Colors.DIM))
    print(f"  {bold('File:')} {solution_path}")
    print(f"  {bold('Language:')} {language}")
    print(f"  {bold('Test cases:')} {len(test_cases)}")
    print()
    
    # Compile if needed
    executable, compile_error = compile_solution(solution_path, language)
    if compile_error:
        print(error(compile_error))
        return
    
    # Get time limit from metadata or default
    time_limit = 10  # generous default
    
    # Run test cases
    passed = 0
    failed = 0
    tle = 0
    results = []
    
    for tc in test_cases:
        tc_id = tc.get("id", "?")
        category = tc.get("category", "?")
        input_text = tc.get("input", "")
        expected = tc.get("expected_output", "")
        purpose = tc.get("purpose", "")
        
        output, elapsed, err = run_solution(executable, language, input_text, time_limit)
        
        if err:
            if "Time Limit" in err:
                status = c("TLE", Colors.YELLOW)
                tle += 1
            else:
                status = c("RTE", Colors.RED)
                failed += 1
            actual = err[:100]
        else:
            if normalize_output(output) == normalize_output(expected):
                status = c("PASS", Colors.GREEN)
                passed += 1
                actual = output[:50] + ("..." if len(output) > 50 else "")
            else:
                status = c("FAIL", Colors.RED)
                failed += 1
                actual = output[:50] if output else "(empty)"
        
        cat_color = {
            "basic": Colors.WHITE,
            "edge_case": Colors.YELLOW,
            "adversarial": Colors.MAGENTA,
            "boundary": Colors.CYAN,
        }.get(category, Colors.WHITE)
        
        time_str = f"{elapsed:.3f}s" if elapsed < 1 else c(f"{elapsed:.3f}s", Colors.YELLOW)
        
        print(f"  [{status}] {c(tc_id, cat_color)} ({category}) {dim(time_str)}")
        if err and "Time Limit" not in err:
            print(f"         {dim(err[:80])}")
        
        results.append({
            "id": tc_id,
            "category": category,
            "status": "PASS" if normalize_output(output) == normalize_output(expected) else "FAIL",
            "time": elapsed,
            "purpose": purpose,
        })
    
    # Summary
    print()
    print(c("─" * 60, Colors.DIM))
    total = len(test_cases)
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    summary_color = Colors.GREEN if passed == total else (Colors.YELLOW if passed > total * 0.5 else Colors.RED)
    print(f"  {c(f'  Results: {passed}/{total} passed ({pass_rate:.0f}%)', summary_color + Colors.BOLD)}")
    print(f"  {success(f'✓ Passed: {passed}')}  {error(f'✗ Failed: {failed}')}  {warning(f'⏱ TLE: {tle}')}")
    
    # Category breakdown
    categories = {}
    for r in results:
        cat = r["category"]
        if cat not in categories:
            categories[cat] = {"pass": 0, "fail": 0}
        if r["status"] == "PASS":
            categories[cat]["pass"] += 1
        else:
            categories[cat]["fail"] += 1
    
    if categories:
        print()
        print(f"  {bold('By category:')}")
        for cat, counts in categories.items():
            total_cat = counts["pass"] + counts["fail"]
            bar_len = 20
            filled = int(counts["pass"] / total_cat * bar_len) if total_cat > 0 else 0
            bar = c("█" * filled, Colors.GREEN) + c("░" * (bar_len - filled), Colors.RED)
            print(f"    {cat:15s} {bar} {counts['pass']}/{total_cat}")
    
    # Failed test details
    failed_tests = [r for r in results if r["status"] != "PASS"]
    if failed_tests:
        print()
        print(f"  {bold('Failed tests:')}")
        for r in failed_tests:
            print(f"    {error('•')} {r['id']} ({r['category']}): {dim(r['purpose'])}")
    
    # Show editorial hint if all passed
    if passed == total:
        print()
        print(success("  🎉 All tests passed! Great job!"))
        print(dim("  Run with --editorial to see the solution explanation."))
    elif passed > 0:
        print()
        print(warning("  💡 Some tests failed. Try --hints for guidance."))
    
    print()
    
    # Cleanup compiled binary
    if language in ("cpp", "c") and executable and os.path.exists(executable):
        try:
            os.unlink(executable)
        except:
            pass


# ─── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Agent Skills Problem Gen Practice Tool — Solve AI-generated programming problems",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python practice.py problem.json                  # View the problem
  python practice.py problem.json --test sol.py    # Test your Python solution
  python practice.py problem.json --test sol.cpp   # Test your C++ solution
  python practice.py problem.json --hints          # Show progressive hints
  python practice.py problem.json --editorial      # Show the editorial
  python practice.py problem.json --all            # Show everything
  python practice.py problem.json --export-md      # Export as Markdown (open in VSCode!)
  python practice.py set.json --set                # View a problem set overview
  python practice.py set.json --set --problem 3    # View problem 3 from a set
  python practice.py set.json --set --problem 3 --test sol.py  # Test solution on problem 3
  python practice.py set.json --set --export-md    # Export entire set as Markdown
        """
    )
    
    parser.add_argument("problem", help="Path to final_problem.json or final_problem_set.json")
    parser.add_argument("--test", "-t", metavar="SOLUTION", help="Path to your solution file (.py, .cpp, .java, etc.)")
    parser.add_argument("--hints", action="store_true", help="Show progressive hints")
    parser.add_argument("--editorial", "-e", action="store_true", help="Show the editorial")
    parser.add_argument("--all", "-a", action="store_true", help="Show problem + hints + editorial")
    parser.add_argument("--json", action="store_true", help="Output raw JSON (for piping)")
    parser.add_argument("--set", "-s", action="store_true", help="Treat input as a problem set file")
    parser.add_argument("--problem-num", "-p", type=int, metavar="N", help="Select problem N from a set (1-indexed)")
    parser.add_argument("--export-md", "-m", action="store_true", help="Export problem as Markdown file")
    
    args = parser.parse_args()
    
    # Set mode
    if args.set:
        data = load_problem_set(args.problem)

        # Export set to Markdown
        if args.export_md:
            output_path = str(Path(args.problem).with_suffix('.md'))
            with open(output_path, 'w', encoding='utf-8') as f:
                meta = data.get("set_metadata", {})
                problems = data.get("problems", [])

                f.write(f"# Problem Set — {meta.get('level', 'unknown').upper()}\n\n")
                f.write(f"**Level:** {meta.get('level', 'unknown').upper()}  \n")
                f.write(f"**Problems:** {meta.get('successful_count', 0)}/{meta.get('set_size', 0)}  \n")
                f.write(f"**Topics:** {', '.join(meta.get('topic_groups_covered', []))}\n\n")
                f.write("---\n\n")

                for entry in problems:
                    slot = entry.get("slot", "?")
                    category = entry.get("category", "?")
                    status = entry.get("status", "?")

                    if status == "success" and entry.get("problem"):
                        prob_data = entry["problem"]
                        prob_meta = prob_data.get("metadata", {})
                        prob = prob_data.get("problem", {})
                        title = prob.get("title", "Untitled")
                        rating = prob_meta.get("difficulty", {}).get("codeforces_rating", "?")
                        topic = prob_meta.get("topic", "?")

                        f.write(f"## Problem {slot}: {title}\n\n")
                        f.write(f"**Category:** {category} | **CF Rating:** {rating} | **Topic:** {topic}\n\n")

                        story = prob.get("story", "")
                        if story:
                            f.write("### Story\n\n")
                            f.write(story + "\n\n")

                        statement = prob.get("statement", "")
                        if statement:
                            f.write("### Problem Statement\n\n")
                            f.write(statement + "\n\n")

                        input_fmt = prob.get("input_format", {})
                        if input_fmt:
                            f.write("### Input Format\n\n")
                            if isinstance(input_fmt, dict):
                                for key, val in input_fmt.items():
                                    f.write(f"- **{key}:** {val}\n")
                            else:
                                f.write(str(input_fmt) + "\n")
                            f.write("\n")

                        output_fmt = prob.get("output_format", "")
                        if output_fmt:
                            f.write("### Output Format\n\n")
                            f.write(output_fmt + "\n\n")

                        constraints = prob.get("constraints", [])
                        if constraints:
                            f.write("### Constraints\n\n")
                            for c in constraints:
                                f.write(f"- {c}\n")
                            f.write("\n")

                        samples = prob.get("sample_tests", [])
                        if samples:
                            f.write("### Sample Tests\n\n")
                            for i, sample in enumerate(samples, 1):
                                f.write(f"#### Sample {i}\n\n")
                                f.write("**Input:**\n```\n")
                                f.write(sample.get("input", "") + "\n```\n\n")
                                f.write("**Output:**\n```\n")
                                f.write(sample.get("output", "") + "\n```\n\n")
                                exp = sample.get("explanation", "")
                                if exp:
                                    f.write(f"**Explanation:** {exp}\n\n")

                        f.write("---\n\n")
                    else:
                        f.write(f"## Problem {slot}: FAILED\n\n")
                        f.write(f"Status: {status}\n\n")
                        reason = entry.get("failure_reason", "Unknown error")
                        f.write(f"Reason: {reason}\n\n")
                        f.write("---\n\n")

            print(success(f"  Exported set to: {output_path}"))
            print(dim("  Open in VSCode: code " + output_path))
            return

        if args.json:
            print(json.dumps(data, indent=2))
            return
        
        # If --problem-num specified, extract that problem and treat as single
        if args.problem_num:
            problems = data["problems"]
            if args.problem_num < 1 or args.problem_num > len(problems):
                print(error(f"Problem {args.problem_num} out of range (1-{len(problems)})"))
                sys.exit(1)
            entry = problems[args.problem_num - 1]
            if entry.get("status") != "success" or not entry.get("problem"):
                print(error(f"Problem {args.problem_num} failed during generation"))
                sys.exit(1)
            single = entry["problem"]
            
            if args.test:
                display_problem(single)
                test_solution(single, args.test)
            elif args.all:
                display_problem(single)
                display_hints(single)
                display_editorial(single)
            elif args.hints:
                display_hints(single)
            elif args.editorial:
                display_editorial(single)
            else:
                display_problem(single)
            return
        
        # Default: show set overview
        display_problem_set(data)
        return
    
    # Single problem mode
    data = load_problem(args.problem)

    # Export to Markdown
    if args.export_md:
        output_path = export_to_markdown(data)
        print(success(f"  Exported to: {output_path}"))
        print(dim("  Open in VSCode: code " + output_path))
        print(dim("  Preview: Ctrl+Shift+V"))
        return

    # Raw JSON mode
    if args.json:
        print(json.dumps(data, indent=2))
        return
    
    # Show all
    if args.all:
        display_problem(data)
        display_hints(data)
        display_editorial(data)
        return
    
    # Test mode
    if args.test:
        display_problem(data)
        test_solution(data, args.test)
        return
    
    # Hints only
    if args.hints:
        display_hints(data)
        return
    
    # Editorial only
    if args.editorial:
        display_editorial(data)
        return
    
    # Default: show problem
    display_problem(data)
    print(dim("  Commands:"))
    print(dim("    --test <solution>   Test your solution against all test cases"))
    print(dim("    --hints             Show progressive hints"))
    print(dim("    --editorial         Show the full editorial"))
    print(dim("    --all               Show problem + hints + editorial"))
    print()


if __name__ == "__main__":
    main()
