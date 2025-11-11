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
        C = MatrizEsparsaHash(self.n, self.m)

        # Adiciona os elementos de A em C em tempo O(ka)
        for (p_i, p_j), valor in self.data.items():
            if self.eh_transposta:
                i, j = (p_j, p_i)
            else:
                i, j = (p_i, p_j)
            C[i, j] = valor

        # Soma com os elementos de B em tempo O(kb)
        for (p_i, p_j), valor in B.data.items():
            if self.eh_transposta:
                i, j = (p_j, p_i)
            else:
                i, j = (p_i, p_j)
            C[i, j] = C[i, j] + valor

        return C
    
    def __mul__(self, escalar):
        """
        Retorna A * b, sendo b um escalar
        em O(ka)
        """
        for (i, j), valor in self.data.items():
            self.data[i, j] = valor * escalar

        return self
    
    def __rmul__(self, escalar):
        """
        Retorna b * A, sendo b um escalar, caso o comando seja invertido
        em O(ka)
        """
        return self.__mul__(escalar)

    def __matmul__(self, B):
        """
        Retorna C = A * B
        em O(ka * db)
        """
        
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

def main():







if __name__ == "__main__":
    main()