#!/usr/bin/env python3
ROWS = [
    ("unit q", "site facing + spin sheet"),
    ("q and -q", "two sheets, one facing"),
    ("conjugate", "mirror gate"),
    ("multiply", "parent writes on child"),
    ("real w", "hold / ground rest"),
    ("i j k", "three HEX-SPLIT midlines"),
    ("4pi trip", "C-308 closure"),
]
def main():
    print("POINT-SPIN")
    for a, b in ROWS:
        print(f"{a:<16}  {b}")
if __name__ == "__main__":
    main()
