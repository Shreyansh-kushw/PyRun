import os
import sys
import glob
import traceback

# Ensure src/pyrun is in path to import VirtualMachine
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(project_root, "src", "pyrun")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from vm import VirtualMachine

def run_test_file(test_path):
    print("=" * 60)
    print("Running: {}".format(os.path.basename(test_path)))
    print("=" * 60)

    with open(test_path, "r") as f:
        code_str = f.read()

    try:
        code_obj = compile(code_str, test_path, "exec")
        vm = VirtualMachine()
        vm.run_code(code_obj)
        print("\n>>> Result: PASS\n")
        return True
    except Exception as e:
        print("\n>>> Result: FAIL with exception: {}".format(e))
        traceback.print_exc()
        print()
        return False

def main():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_files = sorted(glob.glob(os.path.join(test_dir, "test_*.py")))

    passed = 0
    total = len(test_files)

    for test_file in test_files:
        success = run_test_file(test_file)
        if success:
            passed += 1

    print("=" * 60)
    print("TEST SUMMARY: {}/{} tests passed.".format(passed, total))
    print("=" * 60)

    if passed != total:
        sys.exit(1)

if __name__ == "__main__":
    main()
