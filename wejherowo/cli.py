import argparse
from .core import run

def main():
    parser = argparse.ArgumentParser(description="Wejherowo CLI tool.")
    parser.add_argument("--param1", type=str, help="Description for param1")
    parser.add_argument("--param2", type=str, help="Description for param2")
    args = parser.parse_args()
    run(args.param1, args.param2)

if __name__ == "__main__":
    main()
