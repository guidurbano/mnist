n = 20
m = 17
W = []
b = []

for i in range(1, n+1):
    linhaW = []
    for j in range(1, m+1):
        if abs(i-j) <= 4:
            linhaW.append(1/(i+j-1))
        elif abs(i-j) > 4:
            linhaW.append(0)
    W.append(linhaW)
    b.append([i])

print("(W,b) =","(",W,",",b,")")
