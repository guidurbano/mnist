"""
MAP3121 – MÉTODOS NUMÉRICOS E APLICAÇÕES

EP 1 - Fatoração de Matrizes para Sistemas
de Classificação de Machine Learning

Turma 10 (2019)
Bruno Alicino Anutto 10335170
Guilherme Donatoni Urbano 9835985

    *** Teste inicial da Tarefa 1 (pela função solve):

    A = [[-1,2,1],[2,-4,1],[1,-1,2]]

    b = [[1],[1],[2.5]]

    Cuja solução exata é x = [ 1 , 0.5 , 1 ]


    *** Teste Fatoração não negativa (fnn(A, p))

    A = [[3/10 ,3/5, 0], [1/2, 0, 1], [4/10, 4/5, 0]]

    Na qual:

    W = [[3/5, 0], [0, 1], [4/5, 0]]
    H = [[1/2, 1, 0], [1/2, 0, 1]]

    """

import numpy as np
import time

########################################################################

def rotgivens(W, n, m, i, j, c, s):
    '''
    Matrix -> Matrix
    Aplica a rotação de Givens nas linhas i e j
    '''
    i = int(i)
    j = int(j)
    m = int(m)
    n = int(n)
    c = float(c)
    s = float(s)

    for r in range(m):
        aux = c*W[i][r] - s*W[j][r]
        W[j][r] = s*W[i][r] + c*W[j][r]
        W[i][r] = aux
    return W

########################################################################

def inner_fatoracao(k,W,b):
    '''
    Processo de aplicação da rotação de Givens
    até obtenção de matrizes fatoradas. Usada
    no loop principal da função "fatoracao"
    '''

    n = len(W)
    m = len(W[0])
    mb = len(b[0])
    for j in range(n-1, k, -1):
         i = j - 1
         if W[j][k] != 0:
             if abs(W[i][k]) > abs(W[j][k]):
                 t = -(W[j][k]/ W[i][k])
                 c = 1/((1 + (t**2))**(1/2)) # cosseno
                 s = c*t                     # seno
             else:
                 t = -(W[i][k]/W[j][k])
                 s = 1/((1 + (t**2))**(1/2)) # cosseno
                 c = s*t                     # seno
    
             # as condições acima dizem o valor de
             # c e s para cada coluna
    
             W = rotgivens(W, n, m, i, j, c, s)
             b = rotgivens(b, n, mb, i, j, c, s)
    
         else:
             continue

########################################################################

def fatoracao(W, b):
    '''
    Matrix -> Matrix

    Aplica a rotação de Givens na matriz W e b, resultando
    numa matriz triangular superior (R) na primeira, e uma
    modificada na segunda. Executa a função inner_fatoracao
    '''

    m = len(W[0])
    L = list(map(lambda k : inner_fatoracao(k,W,b), range(0,m)))
    # lambda é um loop que executa bem mais rapido um processo computacionalmente
    # ex: lambda <elemento>: <o que eu vou fazer>, <lista que eu vou percorrer>

    return (W, b)

########################################################################

def solve(W, b):
    '''
    (Matrix, Matrix) -> Matrix

    Calcula a solução de um sistema linear por meio da
    fatoração QR. W é a matriz dos coeficientes e  b a
    dos termos independentes.
    '''

    (R, btio) = fatoracao(W, b)
    
    #cria matriz x preenchida com n zeros      
    x = np.zeros([len(R[0]),len(btio[0])])
    x = x.tolist()

    # troca o ultimo termo de x por btio(m)/R(m,m)   
    for i in range(len(b[0])):
        x[len(R[0])-1][i] = btio[len(R[0])-1][i]/R[len(R[0])-1][len(R[0])-1]

    # resolve o sistema linear
    for k in range(len(b[0])): # para cada sistema simultâneo
        for i in range(len(R[0])-2, -1, -1): # da penultima linha à primeira
            m = 0
            for j in range(len(R[0])-1, i, -1): # da ultima coluna à i+1
                m = m + R[i][j]*x[j][k]
            xi = (btio[i][k] - m)/R[i][i]
            x[i][k] = xi
            
    return x

########################################################################

def normaliza(W):
    '''
    Normaliza uma matriz (W)
    '''

    W = np.array(W)
    s = np.sqrt((W**2).sum(axis=0))
    for j in range(len(W[0])):
        for i in range(len(W)):
            W[i][j] = W[i][j]/s[j]

    W = W.tolist()
    return W

########################################################################

def transposta(A):
    '''
    Retorna a matriz transposta de A  
    '''

    At = np.transpose(A)
    At = At.tolist()
    
    return At

########################################################################
    
def prodmatriz(A, B):
    '''
    Multiplica duas matrizes
    '''
    C = np.dot(A,B)
    C = C.tolist()

    return C

########################################################################

def geramatriz(n, p):
    '''
    Gera uma matriz randomica com n linhas e p colunas
    '''
    
    W = np.random.random([n,p])
    W = W.tolist()

    return W

########################################################################

def removenegativos(H):
    '''
    Troca os elementos negativos
    de H por zero.
    '''
    
    for i in range(len(H)):
        for j in range(len(H[0])):
            H[i][j] = max(0, H[i][j])   #retira os elementos negativos

    return H

########################################################################
    
def copia(A):
    '''
    Armazena uma cópia de A.
    '''
    A = np.array(A)
    copyA = A.copy()
    A = A.tolist()
    copyA = copyA.tolist()

    return copyA

########################################################################

def fnn(A, p):
    '''
    Faz a fatoração não negativa de uma matriz (A) dado o valor de p
    '''
    
    it = 0      #iteração
    aux = 0     #será usado no cálculo do erro    
    A2 = copia(A)
    derro = 1

#   loop principal
    W = geramatriz(len(A2), p)

#   enquanto as iterações forem menores que 100
#   ou a diferença de erro menor que 10e-5 
    while it <= 100 and derro > 10e-5:    
        print("Progress {:2.1%} ".format(it / 100), end= "\r") # mostra a porcentagem de conclusão
        W = normaliza(W)
        H = solve(W,A2)
        H = removenegativos(H)
        Ht = transposta(H)
        A2 = copia(A)
        A2t = transposta(A2)
        Wt = solve(Ht, A2t)
        W = transposta(Wt)
        W = removenegativos(W)
        A2 = copia(A)
        P = prodmatriz(W, H)
        
#   cálculo do erro
        erro = 0
        for i in range(len(A2)):
            for j in range(len(A2[0])):
                erro = erro + (A[i][j] - (P[i][j]))**2
        derro = abs(erro - aux)
        aux = erro
        it += 1

    return (W, H)

########################################################################

def ler_arquivo(file):
    '''
    Lê o arquivo .txt e retorna uma matriz
    em formato de lista
    '''
    arquivo = open(file, "r")
    matriz = []
    for linha in arquivo:
        l = linha.strip()
        if len(l) > 0:
            a = l.split(" ")    # retir os espaços
            matriz.append(a)
    arquivo.close()

    return matriz

########################################################################

def treino(ndig_treino, p, d):
    '''
    Calcula a matriz Wd com p componentes para o 
    dígito d a partir de ndig_treino imagens
    '''
    L = []
    A = ler_arquivo('train_dig%d.txt' %(d))
    print("Aprendendo o dígito "+str(d))
    for i in range(len(A)):
        linha = []
        for j in range(ndig_treino):
            linha.append(int(A[i][j])/255)  # normaliza dividindo por 255
        L.append(linha)
    (Wd,H) = fnn(L,p)   # estamos interessados em Wd
    return Wd

########################################################################

def teste(n_test, ndig_treino, p):
    '''
    Retorna uma matriz com os erros correspondentes
    a cada uma das n_test imagens para um dígito d,
    considerando Wd com p componentes a partir de 
    ndig_treino imagens
    
    '''
    A= []
    L = ler_arquivo("test_images.txt")
    A = np.array(L,dtype="int16")
    A = A/255     # normaliza dividindo por 255
    A = A[:,0:n_test]
    A = A.tolist()

    C = []  # matriz que armazena cada Wd
    for d in range(0,10):
        Wd = treino(ndig_treino, p, d)
        C.append(Wd)

#   Cálculo do erro para cada dígito para cada imagem
    E = []
    for k in range(0,10):
        print("Calculando erro para o digito %d" %(k))
        A2 = copia(A)
        H = solve(C[k], A2)
        P = prodmatriz(C[k], H)
        D = np.subtract(A,P)
        e = []    #armazena o erro de cada imagem     
        e = np.sqrt(np.sum((D**2),axis=0))
        e = e.tolist()
        E.append(e)
    
    return E

########################################################################

def provavel(E, n_test):
    '''
    Retorna os dígitos mais prováveis
    para os n_test  dados  os erros E
    
    '''
    p = np.zeros(n_test)    # supomos que seja o dígito 0 aquele mais provável
    p = p.tolist()

    for j in range(n_test):
            M = E[0][j]
            for i in range(1, 10):
                if E[i][j] > M:
                    k = i
                    M = E[i][j]
                    p[j] = k     # novo dígito mais provável armazenado
                else:
                    continue
    return p

########################################################################

def main():
    s = time.time()
    '''
    Calcula o percentual total de acertos e quantas classificações foram 
    corretas para cada dígito e o percentual de acertos para cada dígito
    '''
    print("+-----------------------------------------------------+")
    print("|         CLASSIFICADOR DE DÍGITO MANUSCRITO          |")
    print("+-----------------------------------------------------+", end = "\n")
    print("Init Main...")
    n_test = int(input("n_test (10000): "))
    ndig_treino = int(input("ndigtreino (100, 1000, 4000): "))
    p = int(input("p (5, 10, 15): "))
       
    print("Reading Test File")

    index = np.loadtxt("test_index.txt") # matriz com digítos verdadeiros

    print("Initializing Solution...", end = "\n")

    E = teste(n_test, ndig_treino, p)   # erros para cada imagem para cada dígito
    p = provavel(E, n_test)   # dígitos mais prováveis

    print("+--- Checking results ---+")
    
#   Calculando porcentagens
    acertosd = []   # armazena o numero de acertos para cada um dos digitos de 0 a 9
    ocorrenciad = [] # armazena o numero de ocorrencias para cada um dos digitos de 0 a 9
    for d in range(10):
        a = 0
        o = 0
        for j in range(n_test):
            if p[j] == d:
                o += 1    # ocorrência identificada
                if p[j] == index[j]:
                    a += 1    #acerto identificado
            else:
                continue
        acertosd.append(a)
        ocorrenciad.append(o)

    print("Calculating Metrics...")
    
#   Porcentagem de acertos geral
    acertos = sum(acertosd)
    pacertos = (100*acertos)/n_test

#   Porcentagem de acertos por dígito
    pcorretasd = []
    for i in range(10):
        if ocorrenciad[i] != 0:     # condição apenas para testar com n_teste pequeno (nem todo dígito aparece)
            pcorretasd.append((100*acertosd[i])/(ocorrenciad[i]))
        else:
            pcorretasd.append(0)
             
    print("* Porcentagem de acertos = "+str(pacertos)+"%",end = "\n")
    print("* Acertos para cada dígito = "+str(acertosd),end = "\n")
    print("* Ocorrências para cada dígito = "+str(ocorrenciad),end = "\n")
    print("* Porcentagem de acertos para cada dígito = "+str(pcorretasd),end = "\n")
    f = time.time() 
    print("Tempo de execucção (min): "+str(((f-s)/60)))
main()
