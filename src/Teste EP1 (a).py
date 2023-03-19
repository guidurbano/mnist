n = 64 #Caso da matriz tridiagonal
m = 64 
W = []
b = []

for i in range(1, n+1):
    linhaW = []
    for j in range(1, m+1):
        if i == j:
            linhaW.append(2)
        elif abs(i-j) == 1:
            linhaW.append(1)
        elif abs(i-j) > 1:
            linhaW.append(0)
    W.append(linhaW)
    b.append([1])
    
print("(W,b) =","(",W,",",b,")")    
