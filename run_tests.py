import subprocess
import sys


def run(command):
    print(f"\nRunning: {' '.join(command)}")
    result = subprocess.run(command)
    if result.returncode != 0:
        sys.exit(result.returncode)


if __name__ == "__main__":
    compile_targets = [
        "app.py",
        "about_page.py",
        "core/empirical.py",
        "core/protocol.py",
        "protocol.py",
        "core_empirical.py",
        "core/simulation.py",
        "core/scoring.py",
        "core/parser.py",
    ]
    for target in compile_targets:
        run([sys.executable, "-m", "py_compile", target])
    run([sys.executable, "-m", "pytest", "-q"])
    print("\nAll automated tests passed.")
