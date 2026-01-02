"""
SuperOS Upload Test
Hello World sanity check
"""

import sys
import time
from datetime import datetime


def main():
    print("=" * 40)
    print("🚀 SuperOS Hello World")
    print("=" * 40)

    print(f"Python version : {sys.version.split()[0]}")
    print(f"Executable     : {sys.executable}")
    print(f"Time           : {datetime.now().isoformat()}")

    print("\nCounting:")
    for i in range(1, 6):
        print(f"  {i}")
        time.sleep(0.5)

    print("\n✅ Execution complete.")
    print("=" * 40)


if __name__ == "__main__":
    main()
