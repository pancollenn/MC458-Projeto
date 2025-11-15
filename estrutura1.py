import time
import sys
import random

class MatrizEsparsaHash():
    def __init__(self, n, m):
        self.n = n
        self.m = m 
        self.data = {}
        self.eh_transposta = False

    def _get_pos(self, i, j):
        """
        Retorna a posição real na matriz (se quisermos a transposta devemos inverter (i, j))
        em O(1)
        """
        if self.eh_transposta:
            return (j, i)
        else:
            return (i, j)
    
    def __getitem__(self, tupla_pos):
        """
        Retorna o valor de A[i, j]
        em O(1)
        """
        i, j = tupla_pos
        chave = self._get_pos(i, j)
        return self.data.get(chave, 0)
    
    def __setitem__(self, tupla_pos, valor):
        """
        Insere ou atualiza o valor de A[i, j] para algum valor
        em O(1)
        """
        i, j = tupla_pos
        chave = self._get_pos(i, j)
        if valor != 0:
            self.data[chave] = valor
        else:
            if chave in self.data:
                del self.data[chave]

    def __add__(self, B):
        """
        Retorna C = A + B
        em O(ka + kb)
        """
        C = MatrizEsparsaHash(self.n, B.m)

        # Adiciona os elementos de A em C em tempo O(ka)
        for (p_i, p_j), valor in self.data.items():
            if self.eh_transposta:
                i, j = (p_j, p_i)
            else:
                i, j = (p_i, p_j)
            C[i, j] = valor

        # Soma com os elementos de B em tempo O(kb)
        for (p_i, p_j), valor in B.data.items():
            if B.eh_transposta:
                i, j = (p_j, p_i)
            else:
                i, j = (p_i, p_j)
            C[i, j] = C[i, j] + valor

        return C
    
    def __mul__(self, escalar):
        """
        Retorna C = A * b, sendo b um escalar
        em O(ka)
        """
        C = MatrizEsparsaHash(self.n, self.m)
        C.eh_transposta = self.eh_transposta
        for (i, j), valor in self.data.items():
            C.data[i, j] = valor * escalar

        return C
    
    def __rmul__(self, escalar):
        """
        Retorna b * A, sendo b um escalar, caso o comando seja invertido
        em O(ka)
        """
        return self.__mul__(escalar)

    def __matmul__(self, B):
        """
        Retorna C = A @ B
        em O(kb + ka * db)
        """
        if self.m != B.n:
            raise ValueError(f"Dimensões incompatíveis para multiplicação")
        
        # C é a matriz de resultado
        C = MatrizEsparsaHash(self.n, B.m)

        # Criamos um dicionário para acesso rápido às linhas de B
        # em O(kb) esperado
        # Estrutura: {indice_linha -> {indice_coluna: valor, ...}}
        B_por_linha = {}
        for (p_i_B, p_j_B), val_B in B.data.items():
            if B.eh_transposta:
                b_i, b_j = p_j_B, p_i_B
            else:
                b_i, b_j = p_i_B, p_j_B
            
            # Adiciona ao dicionário de linhas
            if b_i not in B_por_linha:
                B_por_linha[b_i] = {}
            B_por_linha[b_i][b_j] = val_B

        # Itera sobre A e usa o dicionário de linhas de B
        # em O(ka * db) esperado
        
        for (p_i_A, p_j_A), val_A in self.data.items():
            if self.eh_transposta:
                a_i, a_j = p_j_A, p_i_A
            else:
                a_i, a_j = p_i_A, p_j_A
            
            # Agora, A[i, j] é multiplicado por todos os elementos da linha 'a_j' de B.
            # Usamos nosso mapa para pegar a linha 'a_j' de B em O(1) esperado
            if a_j in B_por_linha:
                
                # coluna_B_j contém {k: B[j, k], ...}
                coluna_B_j = B_por_linha[a_j]
                
                # Itera apenas pelos dB elementos dessa linha
                for b_k, val_B_k in coluna_B_j.items():
                    # C[i, k] = C[i, k] + A[i, j] * B[j, k]
                    C[a_i, b_k] = C[a_i, b_k] + (val_A * val_B_k)
        
        return C
            
    def transpor(self):
        """
        Retorna a matriz A "transposta"
        em O(1)
        """
        # Cria uma cópia com as instâncias invertidas
        transposta = MatrizEsparsaHash(self. m, self.n)
        transposta.data = self.data
        transposta.eh_transposta = not self.eh_transposta
        return transposta
    
    def imprimir_matriz_hash(self):
        """
        Imprime o estado interno real da matriz
        """
        print("Representação Hash:")
        print(self.data)
        print(f"Está Transposta: {self.eh_transposta}")
    
def criar_matriz_aleatoria(n, m, dados_esparsos):
    """
    Cria uma matriz esparsa em sua representação tradicional 
    (arranjo bidimensional) 
    """
    # Inicializa a matriz n x m preenchida com zeros
    matriz = [[0] * m for _ in range(n)]
    
    # Insere os elementos não nulos
    for i, j, valor in dados_esparsos:
        if 0 <= i < n and 0 <= j < m:
            matriz[i][j] = valor
        else:
            print(f"Aviso: Índice ({i}, {j}) fora dos limites. Ignorando.")
            
    return matriz

def gerar_dados_esparsos(n, m, percentual_esparsidade):
    total_posicoes = n * m
    k = int(total_posicoes * (percentual_esparsidade / 100.0))
    dados = []
    posicoes_usadas = set()
    while len(dados) < k:
        i = random.randint(0, n - 1)
        j = random.randint(0, m - 1)
        if (i, j) not in posicoes_usadas:
            posicoes_usadas.add((i, j))
            valor = random.randint(1, 9) # Usando inteiros de 1 a 9
            dados.append((i, j, valor))
    return dados

def imprimir_matriz_tradicional(matriz):
    print("Representação Tradicional (Bidimensional):")
    for linha in matriz:
        print(linha)
    
def converter_estrutura_hash(n, m, dados):
    matriz_hash = MatrizEsparsaHash(n, m)
    for i, j, valor in dados:
        matriz_hash[i, j] = valor
    return matriz_hash

def soma_matriz_tradicional(A, B, n, m):
    """
    Soma duas matrizes tradicionais (bidimensional)
    em O(n * m)
    """
    C = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            C[i][j] = A[i][j] + B[i][j]
    return C

def mult_matriz_tradicional(A, B, n, m, p):
    """
    Multiplica duas matrizes tradicionais
    em O(n ** 3)
    """
    C = [[0] * p for _ in range(n)]
    for i in range(n):
        for j in range(p):
            for k in range(m):
                C[i][j] += A[i][k] * B[k][j]
    return C

def mult_escalar_tradicional(A, n, m, escalar):
    """
    Multiplica uma matriz tradicional por um escalar
    em O(n * m)
    """
    C = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            C[i][j] = A[i][j] * escalar
    return C

def rodar_benchmarks():
    ESCALAR_TESTE = 5.0 # Escalar que usaremos para o teste
    NOME_ARQUIVO = "resultados_benchmark.csv"
    
    f = open(NOME_ARQUIVO, "w")
    
    # Define o cabeçalho para o CSV e para o console
    header = "estrutura,i,n,esparsidade,k,tempo_soma,tempo_mult,tempo_mult_escalar,memoria"
    
    print(f"Salvando resultados em {NOME_ARQUIVO}\n")
    
    for i in range(2, 7): # i=2 até 6
        n = 10**i
        
        # Define as esparsidades
        if i < 4:
            percentuais = [1, 5, 10, 20]
        else:
            percentuais = [
                (1 / 10**(i+2)),
                (1 / 10**(i+1)),
                (1 / 10**i)
            ]

        for p in percentuais:
            
            dados_A = gerar_dados_esparsos(n, n, p)
            dados_B = gerar_dados_esparsos(n, n, p)
            k_A = len(dados_A) # Número de elementos não nulos

            # Teste: Estrutura HASH 
            matriz_hash_A = converter_estrutura_hash(n, n, dados_A)
            matriz_hash_B = converter_estrutura_hash(n, n, dados_B)
            
            memoria_hash = sys.getsizeof(matriz_hash_A.data)
            
            inicio = time.perf_counter()
            matriz_hash_C = matriz_hash_A + matriz_hash_B
            tempo_soma_hash = time.perf_counter() - inicio

            inicio = time.perf_counter()
            matriz_hash_D = matriz_hash_A @ matriz_hash_B
            tempo_mult_hash = time.perf_counter() - inicio
            
            inicio = time.perf_counter()
            matriz_hash_E = matriz_hash_A * ESCALAR_TESTE
            tempo_mult_escalar_hash = time.perf_counter() - inicio

            # Formata a linha de dados como string CSV
            linha_hash = f"Hash,{i},{n},{p:.10f},{k_A},{tempo_soma_hash:.10f},{tempo_mult_hash:.10f},{tempo_mult_escalar_hash:.10f},{memoria_hash}"
            print(linha_hash)     # Imprime no console
            f.write(linha_hash + "\n") # Salva no arquivo
            
            # Teste: Matriz Tradicional (Bidimensional)
            if i < 4:
                matriz_tradicional_A = criar_matriz_aleatoria(n, n, dados_A)
                matriz_tradicional_B = criar_matriz_aleatoria(n, n, dados_B)
                
                memoria_tradicional = sys.getsizeof(matriz_tradicional_A)

                inicio = time.perf_counter()
                matriz_tradicional_C = soma_matriz_tradicional(matriz_tradicional_A, matriz_tradicional_B, n, n)
                tempo_soma_tradicional = time.perf_counter() - inicio

                inicio = time.perf_counter()
                matriz_tradicional_D = mult_matriz_tradicional(matriz_tradicional_A, matriz_tradicional_B, n, n, n)
                tempo_mult_tradicional = time.perf_counter() - inicio
                
                inicio = time.perf_counter()
                matriz_tradicional_E = mult_escalar_tradicional(matriz_tradicional_A, n, n, ESCALAR_TESTE)
                tempo_mult_escalar_tradicional = time.perf_counter() - inicio
                
                # Formata a linha de dados como string CSV
                linha_tradicional = f"Tradicional,{i},{n},{p:.10f},{k_A},{tempo_soma_tradicional:.10f},{tempo_mult_tradicional:.10f},{tempo_mult_escalar_tradicional:.10f},{memoria_tradicional}"
                print(linha_tradicional)     # Imprime no console
                f.write(linha_tradicional + "\n") # Salva no arquivo
        
    f.close() # Fecha o arquivo
    print(f"\nBenchmarks concluídos. Resultados salvos em '{NOME_ARQUIVO}'")

def main():
    rodar_benchmarks()


if __name__ == "__main__":
    main()