import subprocess
import sys
import os

GIT_EXE = r"C:\Users\harva\mingit\cmd\git.exe"
WORKSPACE = r"c:\Users\harva\OneDrive\Documents\DMBS"

def run_git(args):
    cmd = [GIT_EXE] + args
    print(f"\n> git {' '.join(args)}")
    result = subprocess.run(cmd, cwd=WORKSPACE, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print("ERR:", result.stderr.strip())
    return result.returncode

def main():
    run_git(["init"])
    run_git(["config", "user.name", "harva"])
    run_git(["config", "user.email", "harva@users.noreply.github.com"])
    run_git(["branch", "-M", "main"])
    run_git(["add", "."])
    run_git(["status", "--short"])
    run_git(["commit", "-m", "Initial commit: Academic Conference DBMS complete 3-review project"])
    run_git(["log", "--oneline", "-n", "3"])

if __name__ == "__main__":
    main()
