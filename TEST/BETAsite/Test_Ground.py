import io, sys
sys.stdin = io.StringIO("line 1\nline 2\nline 3")
for line in sys.stdin:
    print(line)

def g():
    yield 'hola'
    for x in range(7):
        yield x
    
G = g()
print(next(G))
for i,x in enumerate(G):
    print(x)
print(next(G))


