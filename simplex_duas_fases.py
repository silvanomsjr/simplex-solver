
def printar_tabela_bonitinha(tabela):
    string_lin = ''
    for i in range(len(tabela)):
        primeira_coluna_var = tabela[i][0]
        for j in range(1, len(tabela[0])):
            if i == 0:
                string_lin += ' %s\t'%tabela[i][j-1]
            else:
                string_lin += ' %.2f\t'%tabela[i][j]
        
        if primeira_coluna_var != '-':
            string_lin = '%s\t'%primeira_coluna_var + string_lin

        if i >= len(tabela) - 1:
            string_lin = '-\t' + string_lin

        print(string_lin)
        string_lin = ''



def normalizar(A, c, sinais):
    var_ex_ou_fol = 0
    var_artificiais = 0
    for i in range(len(A)):
        for j in range(len(A)):
            if i == j:
                var_ex_ou_fol += 1
                sinal = sinais[j]
                if sinal == ">=":
                    A[j].append(-1)
                elif sinal == "<=":
                    A[j].append(1)
                else:
                    A[j].append(0)
                c.append(0)
            else:
                A[j].append(0)
    for i in range(len(A)):
        for j in range(len(A)):
            if i == j:
                var_artificiais+= 1
                sinal = sinais[j]
                if sinal == ">=" or sinal == "=":
                    A[j].append(1)
                else:
                    A[j].append(0)
                c.append(0)
            else:
                A[j].append(0)
    return (var_ex_ou_fol, var_artificiais)


def soma_coluna(tabela, coluna):
    soma = 0
    for i in range(1, len(tabela) - 2):
        if tabela[0][coluna][0] == 'a':
            soma = 0
        else:
            soma += tabela[i][coluna]
    return soma


def cria_tabela(A, c, b, variaveis_ja_existentes, variaveis_extras):
    tabela = [
        ['-'],
    ]
    numeroLinhas = len(A) + 1
    numeroColunas = len(c) + 1

    contador_s = 1
    contador_a = 1

    for i in range(1, numeroColunas):
        if i > variaveis_ja_existentes:
            if contador_s <= variaveis_extras[0]:
                tabela[0].append('s%d'%contador_s)
                contador_s += 1
            else:
                tabela[0].append('a%d'%contador_a)
                contador_a += 1
        else:
            tabela[0].append('x%d'%(i))
    tabela[0].append('b')

    contador_a = 1

    for i in range(1, numeroLinhas):
        tabela.append(['a%d'%contador_a])
        contador_a += 1
        for j in range(0, numeroColunas - 1):
            tabela[i].append(A[i-1][j])
            if j == numeroColunas - 2:
                tabela[i].append(b[i-1])
        if i == numeroLinhas - 1:
            tabela.append(['-'])
            for j in range(0, numeroColunas - 1):
                tabela[i+1].append(c[j])
                if j == numeroColunas - 2:
                    tabela[i+1].append(0)
    tabela.append(['-'])
    for i in range(1, numeroColunas+1):
        tabela[-1].append(0-soma_coluna(tabela, i))
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
    print("\n==== PASSO 2 ====")
    col_trabalho = [tabela[i][index_passo1] for i in range(0, len(tabela))][1:-1]
    ult_col = [tabela[i][-1] for i in range(len(tabela))][1:-1]
    if max(col_trabalho) <= 0:
        print("== Nenhum elemento da coluna de trabalho é positivo, problema sem solução! ==")
        return -1
    results = []
    for i in range(len(col_trabalho)):
        if ult_col[i] > 0 and col_trabalho[i] > 0:
            results.append(ult_col[i]/col_trabalho[i])
        else:
            results.append(float('inf'))

    printar_tabela_bonitinha(tabela)

    return results.index(min(results)) + 1

def custom_index(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

def passo3(tabela, linha, col):
    print("==== PASSO 3 ====")
    var_linha = tabela[linha][0]
    var_col = tabela[0][col]

    if var_linha[0] == 'a' and custom_index(tabela[0], var_linha) != -1:
       #Pega index da coluna a ser excluida
        col_excluida_index = tabela[0].index(tabela[linha][0])
        for i in range(0, len(tabela)):
            tabela[i].pop(col_excluida_index)


    #Fazendo a troca de variáveis
    tabela[linha][0] = var_col
    tabela[0][col] = var_linha
    printar_tabela_bonitinha(tabela)

def passo4(tabela, linha, col, pivo):
    print("==== PASSO 4 ====")
    nova_linha_pivo = [tabela[linha][j]/pivo if tabela[linha][j] != 0 and pivo != 0 else 0 for j in range(1, len(tabela[linha]))]
    nova_linha_pivo.insert(0, tabela[linha][0])
    tabela[linha] = nova_linha_pivo

    for i in range(1, len(tabela)):
        if(i != linha):
            nova_linha = [] 
            for j in range(1, len(nova_linha_pivo)):
                nova_linha.append(round(tabela[i][j]-tabela[i][col] * nova_linha_pivo[j], 5))

            nova_linha.insert(0, tabela[i][0])
            tabela[i] = nova_linha

    printar_tabela_bonitinha(tabela)

def passo5(tabela):
    ultima_linha = tabela[-1][1:-1]
    contador = 0
    for i in range(len(ultima_linha)):
        if ultima_linha[i] >= 0:
            contador += 1
    
    if contador == len(ultima_linha):
        tabela.pop(-1)



def checa_artificiais_primeira_coluna(tabela):
    for i in range(1, len(tabela)-1):
        if tabela[i][0][0] == 'a':
            return True
    return False

def pega_valor_final_variaveis(tabela):
    result = []
    for i in range(1, len(tabela)-1):
        if tabela[i][0][0] == 'x':
            result.append((tabela[i][0], i))
    return result

'''
    A = Matriz das restrições
    c = Função objetivo
    b = Coef das restrições
'''

def simplex_duas_fases(A, c, b, sinais, maximizacao= True):

    variaveis_ja_existentes = len(c)
    vars = normalizar(A, c, sinais)
    tabela = cria_tabela(A, c, b, variaveis_ja_existentes, vars)
    index_passo1 = passo1(tabela)

    contador = 1
    
    
    tabela_len = len(tabela)
    while(index_passo1 != -1):
        contador+=1
        print("\n\n============ %d iteração ============\n\n"%contador)
        linha_pivo = passo2(tabela, index_passo1)
        if linha_pivo == -1: return
        pivo = tabela[linha_pivo][index_passo1]
        passo3(tabela, linha_pivo, index_passo1)
        passo4(tabela, linha_pivo, index_passo1, pivo)
        if len(tabela) == tabela_len:
            passo5(tabela)
        index_passo1 = passo1(tabela)
    z = tabela[-1][-1] if maximizacao == True else -tabela[-1][-1]

    tem_artificial = checa_artificiais_primeira_coluna(tabela)
    if tem_artificial:
        print("\n\n == ENCONTRADA VARIÁVEIS ARTIFICIAIS NA PRIMEIRA COLUNA, SOLUÇÃO INVIÁVEL!! ==\n\n")
        return -1
    
    variaveis_finais = pega_valor_final_variaveis(tabela)

    print("\n\n == RESULTADO FINAL ==")
    print("Z = ", round(z,2))
    for i in range(len(variaveis_finais)):
        print("%s = %s"%(variaveis_finais[i][0], round(tabela[variaveis_finais[i][1]][len(tabela[0])-1], 2)))


    return z


real_A = [
    [0.1, 0],
    [0, 0.1],
    [0.1, 0.2],
    [0.2, 0.1]
]

sinais = [">=", ">=", ">=", ">="]


real_c = [80, 32]


real_b = [0.4,0.6,2.0,1.7]

simplex_duas_fases(real_A, real_c, real_b, sinais, False)