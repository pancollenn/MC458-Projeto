import time

class No:
    def __init__(self, chave: tuple[int, int], valor: int | float) -> None:
        self.chave: tuple[int, int] = chave
        self.valor: int | float = valor
        self.esquerda: No | None = None
        self.direita: No | None = None
        self.altura: int = 1


class Arvore:
    def __init__(self) -> None:
        self.raiz: No | None = None
        self.tamanho: int = 0

    def _altura(self, no: No | None) -> int:
        if no is None:
            return 0
        return no.altura

    def _balanceamento(self, no: No | None) -> int:
        if no is None:
            return 0
        return self._altura(no.esquerda) - self._altura(no.direita)

    def _atualizar_altura(self, no: No | None) -> None:
        if no is not None:
            no.altura = 1 + max(self._altura(no.esquerda), self._altura(no.direita))

    def _rotacao_direita(self, y: No) -> No:
        x: No = y.esquerda  # type: ignore
        B: No | None = x.direita
        x.direita = y
        y.esquerda = B
        self._atualizar_altura(y)
        self._atualizar_altura(x)
        return x

    def _rotacao_esquerda(self, x: No) -> No:
        y: No = x.direita  # type: ignore
        B: No | None = y.esquerda
        y.esquerda = x
        x.direita = B
        self._atualizar_altura(x)
        self._atualizar_altura(y)
        return y

    def _balancear(self, no: No) -> No:
        self._atualizar_altura(no)
        bal: int = self._balanceamento(no)

        if bal > 1 and self._balanceamento(no.esquerda) >= 0:
            return self._rotacao_direita(no)

        if bal < -1 and self._balanceamento(no.direita) <= 0:
            return self._rotacao_esquerda(no)

        if bal > 1 and self._balanceamento(no.esquerda) < 0:
            no.esquerda = self._rotacao_esquerda(no.esquerda)  # type: ignore
            return self._rotacao_direita(no)

        if bal < -1 and self._balanceamento(no.direita) > 0:
            no.direita = self._rotacao_direita(no.direita)  # type: ignore
            return self._rotacao_esquerda(no)

        return no

    def _inserir_recursivo(self, no: No | None, chave: tuple[int, int], 
                          valor: int | float) -> No:
        if no is None:
            self.tamanho += 1
            return No(chave, valor)

        if chave < no.chave:
            no.esquerda = self._inserir_recursivo(no.esquerda, chave, valor)
        elif chave > no.chave:
            no.direita = self._inserir_recursivo(no.direita, chave, valor)
        else:
            no.valor = valor
            return no

        return self._balancear(no)

    def inserir(self, chave: tuple[int, int], valor: int | float) -> None:
        self.raiz = self._inserir_recursivo(self.raiz, chave, valor)

    def _buscar_recursivo(self, no: No | None, 
                         chave: tuple[int, int]) -> No | None:
        if no is None:
            return None

        if chave < no.chave:
            return self._buscar_recursivo(no.esquerda, chave)
        elif chave > no.chave:
            return self._buscar_recursivo(no.direita, chave)
        else:
            return no

    def buscar(self, chave: tuple[int, int]) -> int | float | None:
        no: No | None = self._buscar_recursivo(self.raiz, chave)
        return no.valor if no else None

    def contem(self, chave: tuple[int, int]) -> bool:
        return self._buscar_recursivo(self.raiz, chave) is not None

    def _no_minimo(self, no: No) -> No:
        atual: No = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def _remover_recursivo(self, no: No | None, 
                          chave: tuple[int, int]) -> No | None:
        if no is None:
            return no

        if chave < no.chave:
            no.esquerda = self._remover_recursivo(no.esquerda, chave)
        elif chave > no.chave:
            no.direita = self._remover_recursivo(no.direita, chave)
        else:
            self.tamanho -= 1

            if no.esquerda is None:
                return no.direita
            elif no.direita is None:
                return no.esquerda

            sucessor: No = self._no_minimo(no.direita)
            no.chave = sucessor.chave
            no.valor = sucessor.valor
            no.direita = self._remover_recursivo(no.direita, sucessor.chave)

        return self._balancear(no)

    def remover(self, chave: tuple[int, int]) -> None:
        self.raiz = self._remover_recursivo(self.raiz, chave)

    def _iterar_inordem(self, no: No | None):
        if no is not None:
            yield from self._iterar_inordem(no.esquerda)
            yield (no.chave, no.valor)
            yield from self._iterar_inordem(no.direita)

    def items(self):
        return self._iterar_inordem(self.raiz)

    def __len__(self) -> int:
        return self.tamanho


class MatrizEsparsaArvore:
    """
    Estrutura 2: Usa Árvore AVL balanceada para armazenar elementos não-nulos
    Complexidades GARANTIDAS:
    - Memória: O(k)
    - Acesso A[i,j]: O(log k)
    - Inserção: O(log k)
    - Transposta: O(1)
    - Soma: O((ka + kb) log k)
    - Multiplicação escalar: O(k)
    - Multiplicação matricial: O(ka * db * log kc)
    """

    def __init__(self, n: int, m: int) -> None:
        self.n: int = n
        self.m: int = m
        self.data: Arvore = Arvore()  
        self.eh_transposta: bool = False

    def _get_pos(self, i: int, j: int) -> tuple[int, int]:
        if self.eh_transposta:
            return (j, i)
        else:
            return (i, j)

    def __getitem__(self, tupla_pos: tuple[int, int]) -> int | float:
        inicio = time.perf_counter()
        i, j = tupla_pos
        chave: tuple[int, int] = self._get_pos(i, j)
        valor: int | float | None = self.data.buscar(chave)
        fim = time.perf_counter()
        print(f"Tempo de execução Getitem - Arvore: {fim - inicio}")
        return valor if valor is not None else 0

    def __setitem__(self, tupla_pos: tuple[int, int], 
                    valor: int | float) -> None:
        inicio = time.perf_counter()
        i, j = tupla_pos
        chave: tuple[int, int] = self._get_pos(i, j)
        if valor != 0:
            self.data.inserir(chave, valor)
        else:
            if self.data.contem(chave):
                self.data.remover(chave)
        fim = time.perf_counter()
        print(f"Tempo de execução Setitem - Arvore: {fim - inicio}")

    def __add__(self, B: 'MatrizEsparsaArvore') -> 'MatrizEsparsaArvore':
        inicio = time.perf_counter()
        if self.n != B.n or self.m != B.m:
            raise ValueError("Matrizes devem ter mesmas dimensões")

        C: MatrizEsparsaArvore = MatrizEsparsaArvore(self.n, self.m)

        for (p_i, p_j), valor in self.data.items():
            if self.eh_transposta:
                i, j = (p_j, p_i)
            else:
                i, j = (p_i, p_j)
            C[i, j] = valor

        for (p_i, p_j), valor in B.data.items():
            if B.eh_transposta:
                i, j = (p_j, p_i)
            else:
                i, j = (p_i, p_j)
            C[i, j] = C[i, j] + valor  
        fim = time.perf_counter()
        print(f"Tempo de execução Add - Arvore: {fim - inicio}")
        return C

    def __mul__(self, escalar: int | float) -> 'MatrizEsparsaArvore':
        inicio = time.perf_counter()
        C: MatrizEsparsaArvore = MatrizEsparsaArvore(self.n, self.m)
        C.eh_transposta = self.eh_transposta

        elementos: list = list(self.data.items())
        for chave, valor in elementos:
            C.data.inserir(chave, valor * escalar)
        fim = time.perf_counter()
        print(f"Tempo de execução Mul - Arvore: {fim - inicio}")
        return C

    def __rmul__(self, escalar: int | float) -> 'MatrizEsparsaArvore':
        inicio = time.perf_counter()
        result = self.__mul__(escalar)
        fim = time.perf_counter()
        print(f"Tempo de execução Rmul - Arvore: {fim - inicio}")
        return result

    def __matmul__(self, B: 'MatrizEsparsaArvore') -> 'MatrizEsparsaArvore':
        inicio = time.perf_counter()
        if self.m != B.n:
            raise ValueError(
                f"Dimensões incompatíveis: ({self.n}x{self.m}) @ ({B.n}x{B.m})"
            )

        C: MatrizEsparsaArvore = MatrizEsparsaArvore(self.n, B.m)

        for (p_i, p_k), valor_a in self.data.items():
            if self.eh_transposta:
                i, k = (p_k, p_i)
            else:
                i, k = (p_i, p_k)

            for (p_k2, p_j), valor_b in B.data.items():
                if B.eh_transposta:
                    k2, j = (p_j, p_k2)
                else:
                    k2, j = (p_k2, p_j)

                if k == k2:
                    C[i, j] = C[i, j] + valor_a * valor_b
        fim = time.perf_counter()
        print(f"Tempo de execução Matmul - Arvore: {fim - inicio}")
        return C

    def transpor(self) -> 'MatrizEsparsaArvore':
        inicio = time.perf_counter()
        transposta: MatrizEsparsaArvore = MatrizEsparsaArvore(self.m, self.n)
        transposta.data = self.data
        transposta.eh_transposta = not self.eh_transposta
        fim = time.perf_counter()
        print(f"Tempo de execução Transpor - Arvore: {fim - inicio}")
        return transposta

    def k(self) -> int:
        inicio = time.perf_counter()
        result = len(self.data)
        fim = time.perf_counter()
        print(f"Tempo de execução NumeroElementos - Arvore: {fim - inicio}")
        return result