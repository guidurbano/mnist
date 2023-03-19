n = 64 #Caso da matriz tridiagonal
p = 64
W = []
b = [] # Três sistemas simultâneos (m=3)

for i in range(1, n+1):
    linhaW = []
    linhab = []
    for j in range(1, p+1):
        if i == j:
            linhaW.append(2)
        elif abs(i-j) == 1:
            linhaW.append(1)
        elif abs(i-j) > 1:
            linhaW.append(0)
        if j==1:
            linhab.append(1)
        if j==2:
            linhab.append(i)
        if j==3:
            linhab.append(2*i-1)
    W.append(linhaW)
    b.append(linhab)

print("(W,b) =","(",W,",",b,")")   
