import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(
        main()
    )  # exit() is not available when run python -S, use sys.exit() explicitly
    # raise SystemExit(main()) # another alternative
