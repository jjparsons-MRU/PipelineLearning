"""
Run Full Pipeline Demo
----------------------
Executes the completed Medallion Architecture pipeline from start to finish.
"""
import os
from pathlib import Path
import subprocess
import sys


def run_pipeline():
    print("========================================")
    print(">>> PIPELINE DEMO INITIATED")
    print("========================================")

    scripts = [
        "ex1_bronze_ingest_completed.py",
        "ex2_silver_cleanse_completed.py",
        "ex3_silver_model_completed.py",
        "ex4_gold_analytics_completed.py",
        "ex5_gold_publish_completed.py",
    ]

    base_dir = Path(__file__).resolve().parent
    exercises_dir = base_dir / "exercises"

    base_dir_str = str(base_dir)
    base_dir_posix = base_dir.as_posix()

    for script in scripts:
        print(f"\n---> Executing {script}...")
        result = subprocess.run(
            [sys.executable, str(exercises_dir / script)],
            cwd=str(exercises_dir),
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"[!] Error in {script}:\n{result.stderr}")
            return
        else:
            output = result.stdout.strip()
            # Ensure any absolute base directory paths are formatted as relative paths
            output = output.replace(base_dir_str + os.sep, f".{os.sep}")
            output = output.replace(base_dir_posix + "/", f".{os.sep}")
            output = output.replace(base_dir_str, f".{os.sep}")
            output = output.replace(base_dir_posix, f".{os.sep}")
            print(output)

    print("\n========================================")
    print(">>> PIPELINE DEMO COMPLETED SUCCESSFULLY")
    print("========================================")


if __name__ == "__main__":
    run_pipeline()
