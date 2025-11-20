class MatrizEsparsaHash:
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
            raise ValueError("Dimensões incompatíveis para multiplicação")

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
        transposta = MatrizEsparsaHash(self.m, self.n)
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
