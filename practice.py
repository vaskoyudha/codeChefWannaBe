#!/usr/bin/env python3
"""
CodeChefWannaBe — Practice Tool
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
        description="CodeChefWannaBe Practice Tool — Solve AI-generated programming problems",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python practice.py problem.json                  # View the problem
  python practice.py problem.json --test sol.py    # Test your Python solution
  python practice.py problem.json --test sol.cpp   # Test your C++ solution
  python practice.py problem.json --hints          # Show progressive hints
  python practice.py problem.json --editorial      # Show the editorial
  python practice.py problem.json --all            # Show everything
        """
    )
    
    parser.add_argument("problem", help="Path to final_problem.json")
    parser.add_argument("--test", "-t", metavar="SOLUTION", help="Path to your solution file (.py, .cpp, .java, etc.)")
    parser.add_argument("--hints", action="store_true", help="Show progressive hints")
    parser.add_argument("--editorial", "-e", action="store_true", help="Show the editorial")
    parser.add_argument("--all", "-a", action="store_true", help="Show problem + hints + editorial")
    parser.add_argument("--json", action="store_true", help="Output raw JSON (for piping)")
    
    args = parser.parse_args()
    
    # Load problem
    data = load_problem(args.problem)
    
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
