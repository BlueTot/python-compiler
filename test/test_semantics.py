from pathlib import Path
import pytest
from compiler.main import compile


CASES_DIR = Path(__file__).parent / "cases"


def normalise_output(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


def run_compile(program: str) -> str:
    try:
        compile(program)
        return "All Ok"
    except Exception as exc:
        message = str(exc).strip()
        if message:
            return f"{type(exc).__name__}: {message}"
        return type(exc).__name__


def load_cases():
    src_files = sorted(CASES_DIR.glob("*.src"))

    if not src_files:
        raise AssertionError(f"No .src files found in {CASES_DIR}")

    cases = []

    for src_path in src_files:
        expected_path = src_path.with_suffix(".expected")

        if not expected_path.exists():
            raise AssertionError(f"Missing expected file for {src_path.name}")

        cases.append(pytest.param(src_path, expected_path, id=src_path.stem))

    return cases


@pytest.mark.parametrize("src_path, expected_path", load_cases())
def test_semantic_case(src_path: Path, expected_path: Path):
    program = src_path.read_text(encoding="utf-8")
    expected = normalise_output(expected_path.read_text(encoding="utf-8"))
    actual = normalise_output(run_compile(program))

    assert actual == expected