#!/usr/bin/env python3
"""
PostToolUse hook: controleert Python code-blokken in markdown bestanden op syntaxfouten.
Wordt automatisch uitgevoerd na Write en Edit tool-aanroepen.
"""
import sys
import json
import ast
import re
import os


def extract_python_blocks(content: str) -> list[tuple[int, str]]:
    """Geeft lijst van (bloknummer, code) tuples terug."""
    blocks = []
    # Zoek ```python ... ``` blokken (niet-greedy)
    pattern = re.compile(r'```python\n(.*?)```', re.DOTALL)
    for i, match in enumerate(pattern.finditer(content), 1):
        blocks.append((i, match.group(1)))
    return blocks


def is_partial_block(code: str) -> bool:
    """
    Partiële code-blokken zijn opzettelijk onvolledig. Herkent:
    - Code die start met inspringing (methodbody buiten klasse)
    - Code die begint met except/elif/else/finally (fragment van control flow)
    - Code die alleen een decorator toont zonder functiedefinitie
    """
    non_empty_lines = [l for l in code.splitlines() if l.strip() and not l.strip().startswith("#")]
    if not non_empty_lines:
        return False

    first = non_empty_lines[0]

    # Ingesprongen eerste regel = onderdeel van een groter blok
    if first[0] in (" ", "\t"):
        return True

    # Fragment van control flow
    if first.strip().startswith(("except ", "except:", "elif ", "else:", "else ", "finally:")):
        return True

    # Alleen een decorator, geen functiedefinitie erna
    if all(l.strip().startswith("@") for l in non_empty_lines):
        return True

    return False


def check_block(block_num: int, code: str) -> str | None:
    """
    Controleert een code-blok op syntaxfouten.
    Geeft foutmelding terug, of None als de code ok is of opzettelijk partieel is.
    """
    if is_partial_block(code):
        return None
    try:
        ast.parse(code)
        return None
    except SyntaxError as e:
        # "expected an indented block" op de laatste regel = bewust afgekapt voorbeeld
        if "expected an indented block" in str(e.msg):
            lines = [l for l in code.splitlines() if l.strip()]
            if e.lineno and e.lineno >= len(lines):
                return None
        lines = code.splitlines()
        offending_line = lines[e.lineno - 1].strip() if e.lineno and e.lineno <= len(lines) else ""
        return f"Blok {block_num}, regel {e.lineno}: {e.msg}\n      → {offending_line}"


def check_file(filepath: str) -> None:
    if not filepath.endswith(".md"):
        return

    if not os.path.isfile(filepath):
        return

    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    blocks = extract_python_blocks(content)
    if not blocks:
        return

    errors = []
    for block_num, code in blocks:
        error = check_block(block_num, code)
        if error:
            errors.append(error)

    filename = os.path.basename(filepath)
    if errors:
        print(f"SYNTAXCONTROLE {filename}: {len(errors)} fout(en) gevonden in Python code-blokken:")
        for err in errors:
            print(f"  - {err}")
        print("  Corrigeer deze fouten voordat je verder gaat.")
    else:
        checked = len(blocks)
        print(f"SYNTAXCONTROLE {filename}: {checked} code-blok(ken) gecontroleerd, geen syntaxfouten.")


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    tool_input = data.get("tool_input", {})
    filepath = tool_input.get("file_path", "")
    if filepath:
        check_file(filepath)


if __name__ == "__main__":
    main()
