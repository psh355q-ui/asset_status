
import subprocess
import sys

with open("test_output.log", "w", encoding="utf-8") as f:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "backend/tests/integration/test_transactions.py", "-v"],
        stdout=f,
        stderr=f,
        cwd=r"D:\code\ai-trading-system\Asset_Status-phase2-transaction-be"
    )
print(f"Done. Exit code: {result.returncode}")
