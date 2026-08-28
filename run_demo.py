"""
Run Full Pipeline Demo
----------------------
Executes the completed Medallion Architecture pipeline from start to finish.
"""
import subprocess
from pathlib import Path
import os

def run_pipeline():
    print("========================================")
    print(">>> PIPELINE DEMO INITIATED")
    print("========================================")
    
    scripts = [
        "ex1_bronze_ingest_completed.py",
        "ex2_silver_cleanse_completed.py",
        "ex3_silver_model_completed.py",
        "ex4_gold_analytics_completed.py",
        "ex5_gold_publish_completed.py"
    ]
    
    base_dir = Path(__file__).resolve().parent
    exercises_dir = base_dir / "exercises"
    
    # Get the string representation of the base directory to mask it
    base_dir_str = str(base_dir)
    
    for script in scripts:
        print(f"\n---> Executing {script}...")
        result = subprocess.run(
            ["python", str(exercises_dir / script)],
            cwd=str(exercises_dir),
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"[!] Error in {script}:\n{result.stderr}")
            return
        else:
            output = result.stdout.strip()
            # MASK THE DIRECTORY: replace the absolute path with a relative path (.\)
            output = output.replace(base_dir_str + os.sep, ".\\")
            print(output)
            
    print("\n========================================")
    print(">>> PIPELINE DEMO COMPLETED SUCCESSFULLY")
    print("========================================")

if __name__ == "__main__":
    run_pipeline()
