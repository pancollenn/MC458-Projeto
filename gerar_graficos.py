import matplotlib.pyplot as plt
import pandas as pd

def gerar_graficos_completos():
    # 1. Carregar os dados
    colunas = ["estrutura", "i", "n", "esparsidade", "k", 
               "tempo_soma", "tempo_mult", "tempo_mult_escalar", "memoria"]
    
    try:
        df = pd.read_csv('resultados_benchmark.csv', names=colunas, header=None)
    except FileNotFoundError:
        print("Arquivo 'resultados_benchmark.csv' não encontrado.")
        return

    # 2. Configurar a área de plotagem (3 linhas x 2 colunas)
    fig, axes = plt.subplots(3, 2, figsize=(14, 16))
    plt.subplots_adjust(hspace=0.4, wspace=0.3)

    # Definições de estilo
    colors = {'Hash': 'green', 'Arvore': 'blue', 'Tradicional': 'red'}
    markers = {'Hash': 'o', 'Arvore': '^', 'Tradicional': 's'}
    estruturas = df['estrutura'].unique()

    # =================================================================
    # LINHA 1: Memória e Soma (vs N, fixando Esparsidade = 1%)
    # =================================================================
    df_1pct = df[df['esparsidade'] == 1.0]

    # --- Gráfico 1: Memória vs N ---
    ax = axes[0, 0]
    for est in estruturas:
        subset = df_1pct[df_1pct['estrutura'] == est].sort_values('n')
        if not subset.empty:
            ax.plot(subset['n'], subset['memoria'], marker=markers[est], 
                    color=colors.get(est, 'gray'), label=est)
    ax.set_title('Memória vs Dimensão N (Esparsidade 1%)')
    ax.set_xlabel('Dimensão N')
    ax.set_ylabel('Memória (bytes)')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend()
    ax.grid(True, which="both", ls="--")

    # --- Gráfico 2: Tempo de Soma vs N ---
    ax = axes[0, 1]
    for est in estruturas:
        subset = df_1pct[df_1pct['estrutura'] == est].sort_values('n')
        if not subset.empty:
            ax.plot(subset['n'], subset['tempo_soma'], marker=markers[est], 
                    color=colors.get(est, 'gray'), label=est)
    ax.set_title('Tempo Soma vs Dimensão N (Esparsidade 1%)')
    ax.set_xlabel('Dimensão N')
    ax.set_ylabel('Tempo (s)')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend()
    ax.grid(True, which="both", ls="--")

    # =================================================================
    # LINHA 2: Mult. Escalar e Mult. Matriz (vs N, fixando Esparsidade = 1%)
    # =================================================================

    # --- Gráfico 3: Tempo Mult. Escalar vs N ---
    ax = axes[1, 0]
    for est in estruturas:
        subset = df_1pct[df_1pct['estrutura'] == est].sort_values('n')
        if not subset.empty:
            ax.plot(subset['n'], subset['tempo_mult_escalar'], marker=markers[est], 
                    color=colors.get(est, 'gray'), label=est)
    ax.set_title('Tempo Mult. Escalar vs Dimensão N (Esparsidade 1%)')
    ax.set_xlabel('Dimensão N')
    ax.set_ylabel('Tempo (s)')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend()
    ax.grid(True, which="both", ls="--")

    # --- Gráfico 4: Tempo Mult. Matriz vs N ---
    ax = axes[1, 1]
    for est in estruturas:
        subset = df_1pct[df_1pct['estrutura'] == est].sort_values('n')
        if not subset.empty:
            ax.plot(subset['n'], subset['tempo_mult'], marker=markers[est], 
                    color=colors.get(est, 'gray'), label=est)
    ax.set_title('Tempo Mult. Matriz vs Dimensão N (Esparsidade 1%)')
    ax.set_xlabel('Dimensão N')
    ax.set_ylabel('Tempo (s)')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend()
    ax.grid(True, which="both", ls="--")

    # =================================================================
    # LINHA 3: Impacto da Esparsidade (N fixo)
    # =================================================================

    # --- Gráfico 5: Tempo Mult vs Esparsidade (N = 1.000) ---
    ax = axes[2, 0]
    df_n1000 = df[df['n'] == 1000]
    
    # CORREÇÃO AQUI: Definimos a lista diretamente no loop
    for est in ['Hash', 'Arvore', 'Tradicional']: 
        if est in df_n1000['estrutura'].unique():
            subset = df_n1000[df_n1000['estrutura'] == est].sort_values('esparsidade')
            ax.plot(subset['esparsidade'], subset['tempo_mult'], marker=markers[est], 
                    color=colors.get(est, 'gray'), label=est)
            
    ax.set_title('Tempo Mult. vs Esparsidade (N = 1.000)')
    ax.set_xlabel('Esparsidade (%)')
    ax.set_ylabel('Tempo (s)')
    ax.set_xscale('log') 
    ax.set_yscale('log')
    ax.legend()
    ax.grid(True, which="both", ls="--")

    # --- Gráfico 6: Tempo Mult vs Esparsidade (N = 1.000.000) ---
    # Apenas Hash e Árvore
    ax = axes[2, 1]
    df_n1M = df[(df['n'] == 1000000) & (df['estrutura'].isin(['Hash', 'Arvore']))]
    
    for est in ['Hash', 'Arvore']:
        if est in df_n1M['estrutura'].unique():
            subset = df_n1M[df_n1M['estrutura'] == est].sort_values('esparsidade')
            ax.plot(subset['esparsidade'], subset['tempo_mult'], marker=markers[est], 
                    color=colors.get(est, 'gray'), label=est)

    ax.set_title('Tempo Mult. vs Esparsidade (N = 1.000.000)')
    ax.set_xlabel('Esparsidade (%)')
    ax.set_ylabel('Tempo (s)')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend()
    ax.grid(True, which="both", ls="--")

    # Salvar
    plt.savefig('graficos_comparativos_completo.png')
    print("Gráficos gerados e salvos em 'graficos_comparativos_completo.png'")
    plt.show()

if __name__ == "__main__":
    gerar_graficos_completos()