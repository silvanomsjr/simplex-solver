
def printar_tabela_bonitinha(tabela):
    for i in range(len(tabela)):
        print(tabela[i])
        print('\n')


def normalizar(A, c):
    for i in range(len(A)):
        for j in range(len(A)):
            if i == j:
                A[j].append(1)
                c.append(0)
            else:
                A[j].append(0)


def cria_tabela(A, c, b, variaveis_ja_existentes):
    tabela = [
        ['-'],
    ]
    numeroLinhas = len(A) + 1
    numeroColunas = len(c) + 1

    contador_s = 1

    for i in range(1, numeroColunas):
        if i > variaveis_ja_existentes:
            tabela[0].append('s%d'%contador_s)
            contador_s += 1
        else:
            tabela[0].append('x%d'%(i))
    tabela[0].append('-')

    contador_s = 1

    for i in range(1, numeroLinhas):
        tabela.append(['s%d'%contador_s])
        contador_s += 1
        for j in range(0, numeroColunas - 1):
            tabela[i].append(A[i-1][j])
            if j == numeroColunas - 2:
                tabela[i].append(b[i-1])
        if i == numeroLinhas - 1:
            tabela.append(['-'])
            for j in range(0, numeroColunas - 1):
                tabela[i+1].append(0 - c[j])
                if j == numeroColunas - 2:
                    tabela[i+1].append(0)
    return tabela


def passo1(tabela):
    #Pega a ultima linha
    ultima_linha = tabela[-1:]
    
    #Retira a primeira coluna (apenas texto auxiliar) e também retira a ultima coluna, como pedido no passo 1
    numeros_validos = ultima_linha[0][1:-1]

    if min(numeros_validos) >= 0:
        return -1

    return numeros_validos.index(min(numeros_validos)) + 1
    

def passo2(tabela, index_passo1):
    col_trabalho = [tabela[i][index_passo1] for i in range(0, len(tabela))][1:-1]
    ult_col = [tabela[i][-1] for i in range(len(tabela))][1:-1]
    results = [ult_col[i]/col_trabalho[i] for i in range(len(col_trabalho))]

    return results.index(min(results)) + 1

def passo3(tabela, linha, col):
    var_linha = tabela[linha][0]
    var_col = tabela[0][col]
    #Fazendo a troca de variáveis
    tabela[linha][0] = var_col
    tabela[0][col] = var_linha


def passo4(tabela, linha, col, pivo):
    nova_linha_pivo = [tabela[linha][j]/pivo for j in range(1, len(tabela[linha]))]
    nova_linha_pivo.insert(0, tabela[linha][0])
    tabela[linha] = nova_linha_pivo

    for i in range(1, len(tabela)):
        if(i != linha):
            nova_linha = [(nova_linha_pivo[j] * (0 -tabela[i][col]) + tabela[i][j]) for j in range(1,len(nova_linha_pivo))]
            nova_linha.insert(0, tabela[i][0])
            tabela[i] = nova_linha


def simplex_uma_fase(A, c, b, maximizacao = True):
    '''
    A = Matriz das restrições
    c = Função objetivo
    b = Coef das restrições

    •Passo 1: Localize o número mais negativo da última linha do quadro simplex, excluída a última coluna,
        e chame a coluna em que este número aparece de coluna de trabalho.
        Se existir mais de um candidato a número mais negativo, escolha um.
    •Passo 2: Para cada elemento da coluna de trabalho, forme quocientes entre a divisão do elemento da última
        coluna pelo elemento da linha correspondente na coluna de trabalho
        (exclua deste processo a última linha do quadro).
        Designe por pivô o elemento da coluna de trabalho que conduza o menor quociente.
        Se mais de um elemento conduzir ao menor quociente, escolha um.
        Se nenhum elemento da coluna de trabalho for positivo, o problema não terá solução.
    •Passo 3: Substitua a variável x existente na linha pivô e primeira coluna pela variável x da primeira linha e coluna pivô.
        Esta nova primeira coluna é o novo conjunto de variáveis básicas.
    •Passo 4: Use operações elementares sobre as linhas a fim de converter o elemento pivô em 1 e, em seguida, reduzir a zero
        todos os outros elementos da coluna de trabalho.
    •Passo 5: Repita os passos de 1 a 4 até a inexistência de números negativos na última linha, excluindo-se desta a preciação
        a última coluna.
    •Passo 6: A solução ótima é obtida atribuindo-se a cada variável da primeira coluna o valor da linha correspondente, na última coluna
        .Às demais variáveis é atribuído o valor zero. O valor ótimo da função objetivo, associado a z, é o número resultante na última linha,
        última coluna, nos problemas de maximização ou o negativo deste número, nos problemas de minização.
    '''

    variaveis_ja_existentes = len(c)


    normalizar(A, c)

    tabela = cria_tabela(A, c, b, variaveis_ja_existentes)



    # tabela_inicial = [
    #     ['-', 'x1', 'x2', 's1', 's2', '-'],
    #     ['s1', 4,    9,     1,   0,   400],
    #     ['s2', 10,   6,     0,   1,   600],
    #     ['-',  -6,  -8,     0,   0,     0],
    # ]

    index_passo1 = passo1(tabela)
    contador = 1

    print('-- Tabela inicial --')
    printar_tabela_bonitinha(tabela)

    while(index_passo1 != -1):
        linha_pivo = passo2(tabela, index_passo1)
        pivo = tabela[linha_pivo][index_passo1]
        passo3(tabela, linha_pivo, index_passo1)
        passo4(tabela, linha_pivo, index_passo1, pivo)
        print('--%d iteração--'%contador)
        printar_tabela_bonitinha(tabela)
        contador+=1
        index_passo1 = passo1(tabela)

    print('===== tabela final =======')

    z = tabela[-1][-1] if maximizacao else 0-tabela[-1][-1]


    printar_tabela_bonitinha(tabela)

    print('\n-O valor final da função Z = ', z)
    print(z)
    print('\n')

    return z


real_A = [
    [4,9],
    [10,6]
]


real_c = [6,8]

real_b = [400,600]

simplex_uma_fase(real_A, real_c, real_b)


