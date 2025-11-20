import random
import sys
import time

from estrutura1 import MatrizEsparsaHash


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
            valor = random.randint(1, 9)  # Usando inteiros de 1 a 9
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
    ESCALAR_TESTE = 5.0  # Escalar que usaremos para o teste
    NOME_ARQUIVO = "resultados_benchmark.csv"

    f = open(NOME_ARQUIVO, "w")

    # Define o cabeçalho para o CSV e para o console
    header = (
        "estrutura,i,n,esparsidade,k,tempo_soma,tempo_mult,tempo_mult_escalar,memoria"
    )

    print(f"Salvando resultados em {NOME_ARQUIVO}\n")

    for i in range(2, 7):  # i=2 até 6
        n = 10**i

        # Define as esparsidades
        if i < 4:
            percentuais = [1, 5, 10, 20]
        else:
            percentuais = [(1 / 10 ** (i + 2)), (1 / 10 ** (i + 1)), (1 / 10**i)]

        for p in percentuais:
            dados_A = gerar_dados_esparsos(n, n, p)
            dados_B = gerar_dados_esparsos(n, n, p)
            k_A = len(dados_A)  # Número de elementos não nulos

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
            print(linha_hash)  # Imprime no console
            f.write(linha_hash + "\n")  # Salva no arquivo

            # Teste: Matriz Tradicional (Bidimensional)
            if i < 4:
                matriz_tradicional_A = criar_matriz_aleatoria(n, n, dados_A)
                matriz_tradicional_B = criar_matriz_aleatoria(n, n, dados_B)

                memoria_tradicional = sys.getsizeof(matriz_tradicional_A)

                inicio = time.perf_counter()
                matriz_tradicional_C = soma_matriz_tradicional(
                    matriz_tradicional_A, matriz_tradicional_B, n, n
                )
                tempo_soma_tradicional = time.perf_counter() - inicio

                inicio = time.perf_counter()
                matriz_tradicional_D = mult_matriz_tradicional(
                    matriz_tradicional_A, matriz_tradicional_B, n, n, n
                )
                tempo_mult_tradicional = time.perf_counter() - inicio

                inicio = time.perf_counter()
                matriz_tradicional_E = mult_escalar_tradicional(
                    matriz_tradicional_A, n, n, ESCALAR_TESTE
                )
                tempo_mult_escalar_tradicional = time.perf_counter() - inicio

                # Formata a linha de dados como string CSV
                linha_tradicional = f"Tradicional,{i},{n},{p:.10f},{k_A},{tempo_soma_tradicional:.10f},{tempo_mult_tradicional:.10f},{tempo_mult_escalar_tradicional:.10f},{memoria_tradicional}"
                print(linha_tradicional)  # Imprime no console
                f.write(linha_tradicional + "\n")  # Salva no arquivo

    f.close()  # Fecha o arquivo
    print(f"\nBenchmarks concluídos. Resultados salvos em '{NOME_ARQUIVO}'")


def main():
    rodar_benchmarks()


if __name__ == "__main__":
    main()
