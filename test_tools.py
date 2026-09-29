from pathlib import Path
import subprocess
import sys
BASE_DIR=Path(__file__).resolve().parent.parent

PROJECT_WORKSPACE= BASE_DIR/"projectworkspace"

def run_tests(test_path: str="") -> dict: 
    
    # running pytest inside the workspace and return the test results.
    
    try:
        command=[sys.executable,"-m","pytest"]
        if test_path:
            command.append(test_path)
        result=subprocess.run(
            command,
            cwd=str(PROJECT_WORKSPACE),
            capture_output=True,
            text=True,
            timeout=180,  
        )
        return{
            "success":result.returncode ==0,
            "exit_code":result.returncode,
            "stdout":result.stdout,
            "stderr":result.stderr,  
        }
        
    except subprocess.TimeoutExpired:
         return{
            "success":False,
            "exit_code":None,
            "stdout":"",
            "stderr":"Test execution excedded the 180 second timeout.",
             
    }
    except Exception as e:
        return{
            "success":False,
            "exit_code":None,
            "stdout":"",
            "stderr":str(e)
        }