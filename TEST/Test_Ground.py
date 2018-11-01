import io, sys
sys.stdin = io.StringIO("line 1\nline 2\nline 3")
for line in sys.stdin:
    print(line)

