import sys

if __name__ == "__main__":
    a=sys.argv[1]
    l=sys.argv[2:]
    tups = [(tuple(a.index(c) for c in w), w) for w in l]
    print(" ".join(t[1] for t in sorted(tups)))