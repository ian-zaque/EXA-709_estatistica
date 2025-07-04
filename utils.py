import matplotlib.pyplot as plt
import questionario
import numpy as np
import pandas as pd
from scipy.stats import mode, entropy, chi2_contingency, pearsonr, ttest_ind
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

rotulos_questoes = questionario.rotulos_questoes
limites = questionario.limites
de_para = questionario.de_para
plt.rcParams["figure.figsize"] = (12, 8)
TOTAL_NUMBER = 217

# ====== FUNÇÕES PARA VARIÁVEIS QUANTITATIVAS ======
def contagem(df, coluna):
    return df[coluna].count()

def media(df, coluna):
    return df[coluna].mean().round(2)

def mediana(df, coluna):
    return df[coluna].median().round(2)

def moda(df, coluna):
    return df[coluna].mode().iloc[0] if not df[coluna].mode().empty else None

def minimo(df, coluna):
    return df[coluna].min()

def maximo(df, coluna):
    return df[coluna].max()

def intervalo(df, coluna):
    return maximo(df, coluna) - minimo(df, coluna)

def desvio_padrao(df, coluna):
    return df[coluna].std().round(2)

def variancia(df, coluna):
    return df[coluna].var().round(2)

def coef_var(df, coluna):
    media_val = media(df, coluna)
    return (desvio_padrao(df, coluna) / media_val).round(2) if media_val != 0 else np.nan

def quartis(df, coluna):
    return {
        'Q1': df[coluna].quantile(0.25).round(2),
        'Q2': df[coluna].quantile(0.50).round(2),
        'Q3': df[coluna].quantile(0.75).round(2),
        'Q4': df[coluna].quantile(1).round(2)
    }

def iqr(df, coluna):
    q = quartis(df, coluna)
    return q['Q3'] - q['Q1']

def histograma(df, coluna, intervalo):
    # plt.figure(figsize=(10, 6))  # Tamanho maior da figura
    
    # Geração do histograma e captura dos valores
    counts, bins, patches = plt.hist(df[coluna], bins=intervalo, edgecolor='black')

    # Adiciona os valores acima das barras
    for count, bin_left, bin_right in zip(counts, bins[:-1], bins[1:]):
        x = (bin_left + bin_right) / 2  # centro da barra
        y = count
        plt.text(x, y + max(counts)*0.01, f'{int(count)}', ha='center', va='bottom')

    # Títulos e rótulos
    titulo = rotulos_questoes.get(int(coluna[1:]), coluna)
    plt.title(f'Histograma - {titulo}')
    plt.xlabel(titulo)
    plt.ylabel('Frequência')
    plt.grid(False)
    # plt.tight_layout()

    # Salva e fecha
    plt.savefig(f'DB/histograma_{coluna}.png')
    plt.close()



# ====== FUNÇÕES PARA VARIÁVEIS CATEGÓRICAS ======
def freq_absoluta(df, coluna):
    return df[coluna].value_counts().round(2)

def freq_relativa(df, coluna):
    return (df[coluna].value_counts(normalize=True) * 100).round(2)

def moda_categoria(df, coluna):
    return df[coluna].mode().iloc[0] if not df[coluna].mode().empty else None

def format_pizza_labels(pct, allvals):
    absolute = int(round(pct/100. * np.sum(allvals)))
    return f"{absolute} ({pct:.1f}%)"

def grafico_pizza(df, coluna):
    plt.figure()
    titulo = rotulos_questoes.get(int(coluna[1:]), coluna)
    codigos = df[coluna].value_counts()
    
    # Se houver DE/PARA disponível, substituir os valores
    if int(coluna[1:]) in de_para:
        labels = [de_para[int(coluna[1:])].get(int(k), str(k)) for k in codigos.index]
        codigos.index = labels

    # codigos.plot.pie(autopct='%1.1f%%', startangle=90)
    codigos.plot.pie(
        autopct=lambda pct: format_pizza_labels(pct, codigos),
        startangle=90
    )
    plt.title(f'Gráfico de Pizza - {titulo}')
    plt.ylabel('')
    # plt.tight_layout()
    plt.savefig(f'DB/pizza_{coluna}.png')
    plt.close()

def grafico_barras(df, coluna):
    plt.figure()
    titulo = rotulos_questoes.get(int(coluna[1:]), coluna)
    codigos = df[coluna].value_counts().sort_index()

    # Substituir códigos por rótulos DE/PARA, se existirem
    if int(coluna[1:]) in de_para:
        labels = [de_para[int(coluna[1:])].get(int(k), str(k)) for k in codigos.index]
        codigos.index = labels

    codigos.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title(f'Gráfico de Barras - {titulo}')
    plt.xlabel(titulo)
    plt.ylabel('Frequência')
    plt.xticks(rotation=0)
    plt.grid(axis='y')
    
    for i, v in enumerate(codigos.values):
        plt.text(i, v + 0.02, f'{v:.0f}', ha='center', va='bottom')

    # plt.tight_layout()
    plt.savefig(f'DB/barras_{coluna}.png')
    plt.close()

def medida_entropia(df, coluna):
    probs = df[coluna].value_counts(normalize=True)
    return entropy(probs, base=2).round(2)

def teste_chi2(df, col1, col2):
    cont = pd.crosstab(df[col1], df[col2])
    stat, p, dof, _ = chi2_contingency(cont)
    return {'chi2': stat, 'p': p, 'dof': dof}

def proporcoes(df, coluna):
    return freq_relativa(df, coluna).round(2)

def comparacao_subgrupos(df, cat_col, target_col):
    return df.groupby(cat_col)[target_col].value_counts(normalize=True).unstack().fillna(0)

def matriz_confusao(df, col1, col2):
    return pd.crosstab(df[col1], df[col2]).round(2)

def analise_correspondencia(df, col1, col2):
    cont = pd.crosstab(df[col1], df[col2])
    stat, p, dof, _ = chi2_contingency(cont)
    return {'contingencia': cont.round(2), 'p_valor': p.round(2) }

# === Analise Conjunta ===
def pearson_corr(df, col1, col2):
    r, p = pearsonr(df[col1], df[col2])
    return {"correlação_pearson": r.round(2), "p_valor": p.round(2)}

def qui_quadrado(df, col1, col2):
    tabela = pd.crosstab(df[col1], df[col2])
    chi2, p, dof, _ = chi2_contingency(tabela)
    return {"qui2": chi2.round(2), "p_valor": p.round(2), "graus_liberdade": dof, "tabela": tabela.to_dict()}

def media_por_grupo(df, grupo_col, valor_col):
    grupos = df.groupby(grupo_col)[valor_col].mean().round(2)
    return grupos.to_dict()

def teste_t_por_grupo(df, grupo_col, valor_col):
    grupo1 = df[df[grupo_col] == 1][valor_col]
    grupo2 = df[df[grupo_col] == 2][valor_col]
    t_stat, p_valor = ttest_ind(grupo1, grupo2, equal_var=False)
    return {
        "media_grupo_1": grupo1.mean().astype(int).round(2),
        "media_grupo_2": grupo2.mean().astype(int).round(2),
        "t_stat": t_stat.astype(int).round(2),
        "p_valor": p_valor.astype(int).round(2)
    }

def clusterizar(df, cols, n_clusters=3):
    scaler = StandardScaler()
    X_norm = scaler.fit_transform(df[cols])
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init="auto")
    df['cluster'] = kmeans.fit_predict(X_norm)
    return df['cluster'], df.groupby('cluster')[cols].mean().round(2)

def plot_barras_agrupadas(df, col_base, col_grupo, titulo=None, nome_arquivo=None):
    """
    Gera gráfico de barras agrupadas entre duas colunas categóricas de um DataFrame.

    Parâmetros:
    - df: pandas.DataFrame com os dados
    - col_base: coluna para eixo X (categorias principais)
    - col_grupo: coluna para as barras agrupadas (subcategorias)
    - titulo: título do gráfico (opcional)
    - nome_arquivo: caminho para salvar o gráfico (opcional)
    """
    # Agrupar os dados
    grupo = df.groupby([col_base, col_grupo]).size().unstack(fill_value=0)
    
    # Preparar o gráfico
    categorias_base = grupo.index.astype(str)
    subcategorias = grupo.columns
    x = np.arange(len(categorias_base))  # posições das categorias base
    largura = 0.8 / len(subcategorias)   # largura de cada barra
    cores = plt.cm.Set2.colors

    fig, ax = plt.subplots(figsize=(10, 6))
    for i, subcat in enumerate(subcategorias):
        barras = ax.bar(x + i * largura, grupo[subcat], width=largura,
           label=f'{questionario.de_para[int(col_grupo[1:])][int(subcat)]}', color=cores[i % len(cores)])
        
        # Adicionar a frequência em cima de cada barra
        for barra in barras:
            altura = barra.get_height()
            ax.text(
                barra.get_x() + barra.get_width() / 2,  # posição x do centro da barra
                altura,                                # posição y logo acima da barra
                str(int(altura)),                      # texto a ser exibido
                ha='center', va='bottom', fontsize=9
            )

    labels = [de_para[int(col_base[1:])].get(int(k), str(k)) for k in de_para[int(col_base[1:])]]
    # Configurar eixos e rótulos
    ax.set_xticks(x + largura * (len(subcategorias) - 1) / 2)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Frequência")
    ax.set_title(titulo or f"Distribuição de {col_base} por {col_grupo}")
    ax.legend()
    plt.tight_layout()

    if nome_arquivo:
        plt.savefig("DB/"+nome_arquivo)