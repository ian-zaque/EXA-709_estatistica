import random
import pandas as pd
import json
import numpy as np
from scipy.stats import mode, entropy, chi2_contingency, pearsonr, ttest_ind
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Número de dados a serem gerados
N = 10  # Altere conforme necessário

rotulos_questoes = {
    1: "Idade (anos)",
    2: "Sexo",
    3: "Semestre que está cursando",
    4: "Renda familiar",
    5: "Período (1-Diurno / 2-Noturno)",
    6: "Você trabalha?",
    7: "Tempo de estudo diário (horas)",
    8: "Mora com quem?",
    9: "Há quanto tempo utiliza computador?",
    10: "Você costuma acessar a Internet?",
    11: "Quanto tempo estuda na internet (horas)",
    12: "Dispositivo móvel mais acessado",
    13: "Tempo conectado por dia (horas)",
    14: "Você utiliza a internet para trabalho?",
    15: "Você utiliza a internet para conversar com amigos?",
    16: "Você utiliza a internet para conversar com desconhecidos?",
    17: "Você utiliza a internet para acessar e-mail?",
    18: "Você utiliza a internet para pesquisas acadêmicas?",
    19: "Você utiliza a internet para acessar notícias?",
    20: "Você utiliza a internet para fazer compras online?",
    21: "Você utiliza a internet para assistir a vídeos online?",
    22: "Você utiliza a internet para participar de jogos online?",
    23: "Você acredita que a internet atrapalha sua formação?",
    24: "Você considera as redes sociais um ambiente tóxico?",
    25: "Você utiliza a internet para fazer download de conteúdo?",
    26: "O que o computador representa para você?",
    27: "Como você se sente em relação à informática?"
}

# Limites e tipos de respostas
limites = {
    1: lambda: random.randint(17, 27),
    2: lambda: random.choice([1, 2]),
    3: lambda: random.randint(1, 12),
    4: lambda: random.randint(1, 8),
    5: lambda: random.choice([1, 2]),
    6: lambda: random.choice([1, 2]),
    7: lambda: random.randint(0, 8),
    8: lambda: random.choice([1, 2, 3]),
    9: lambda: random.randint(3, 25),
    10: lambda: random.choice([1, 2]),
    11: lambda: random.randint(0, 8),
    12: lambda: random.choice([1, 2, 3]),
    13: lambda: random.randint(1, 10),
    14: lambda: random.choice([1, 2]),
    15: lambda: random.choice([1, 2]),
    16: lambda: random.choice([1, 2]),
    17: lambda: random.choice([1, 2]),
    18: lambda: random.choice([1, 2]),
    19: lambda: random.choice([1, 2]),
    20: lambda: random.choice([1, 2]),
    21: lambda: random.choice([1, 2]),
    22: lambda: random.choice([1, 2]),
    23: lambda: random.choice([1, 2]),
    24: lambda: random.choice([1, 2]),
    25: lambda: random.choice([1, 2]),
    26: lambda: random.choice([1, 2, 3]),
    27: lambda: random.choice([1, 2, 3]),
}

# Mapeamento DE/PARA baseado nas alternativas do questionário
de_para = {
    2: {1: "Masculino", 2: "Feminino"},
    5: {1: "Diurno", 2: "Noturno"},
    6: {1: "Sim", 2: "Não"},
    8: {1: "Só", 2: "Amigos", 3: "Família"},
    10: {1: "Sim", 2: "Não"},
    12: {1: "Celular", 2: "Tablet", 3: "Computador/Notebook"},
    14: {1: "Sim", 2: "Não"},
    15: {1: "Sim", 2: "Não"},
    16: {1: "Sim", 2: "Não"},
    17: {1: "Sim", 2: "Não"},
    18: {1: "Sim", 2: "Não"},
    19: {1: "Sim", 2: "Não"},
    20: {1: "Sim", 2: "Não"},
    21: {1: "Sim", 2: "Não"},
    22: {1: "Sim", 2: "Não"},
    23: {1: "Sim", 2: "Não"},
    24: {1: "Sim", 2: "Não"},
    25: {1: "Sim", 2: "Não"},
    26: {1: "Avanço tecnológico que melhora a vida", 2: "Forma rápida de se comunicar", 3: "Atrapalha, exige mais conhecimento" },
    27: {1: "Entusiasmado, quer saber mais", 2: "Obrigada a aprender", 3: "Acho difícil e complicado"}
}

# Geração dos dados
dados_numericos = []
dados_textuais = []

print("Gerando dados aleatórios... \n")

for _ in range(N):
    entrada_numerica = {f"Q{q}": limites[q]() for q in range(1, 28)}
    entrada_textual = {
        f"Q{q}": de_para[q][entrada_numerica[f"Q{q}"]] if q in de_para else entrada_numerica[f"Q{q}"]
        for q in range(1, 28)
    }
    # print(f"Dados Numericos: {entrada_numerica}")
    # print(f"Dados Textuais: {entrada_textual}\n \n")
    dados_numericos.append(entrada_numerica)
    dados_textuais.append(entrada_textual)

# Criação de DataFrames
df_numerico = pd.DataFrame(dados_numericos)
df_textual = pd.DataFrame(dados_textuais)

# Salvando arquivos
print("Salvando arquivos XLS... \n")
df_numerico.to_excel("dados_numericos.xlsx", index=False)
df_textual.to_excel("dados_textuais.xlsx", index=False)

# with open("dados_numericos.json", "w", encoding="utf-8") as f:
#     json.dump(dados_numericos, f, ensure_ascii=False, indent=4)

# with open("dados_textuais.json", "w", encoding="utf-8") as f:
#     json.dump(dados_textuais, f, ensure_ascii=False, indent=4)


# ====== FUNÇÕES PARA VARIÁVEIS QUANTITATIVAS ======
def contagem(df, coluna):
    return df[coluna].count()

def media(df, coluna):
    return df[coluna].mean()

def mediana(df, coluna):
    return df[coluna].median()

def moda(df, coluna):
    return df[coluna].mode().iloc[0] if not df[coluna].mode().empty else None

def minimo(df, coluna):
    return df[coluna].min()

def maximo(df, coluna):
    return df[coluna].max()

def intervalo(df, coluna):
    return maximo(df, coluna) - minimo(df, coluna)

def desvio_padrao(df, coluna):
    return df[coluna].std()

def variancia(df, coluna):
    return df[coluna].var()

def coef_var(df, coluna):
    media_val = media(df, coluna)
    return desvio_padrao(df, coluna) / media_val if media_val != 0 else np.nan

def quartis(df, coluna):
    return {
        'Q1': df[coluna].quantile(0.25),
        'Q2': df[coluna].quantile(0.50),
        'Q3': df[coluna].quantile(0.75)
    }

def iqr(df, coluna):
    q = quartis(df, coluna)
    return q['Q3'] - q['Q1']

def histograma(df, coluna):
    plt.figure()
    df[coluna].hist(bins=10, edgecolor='black')
    titulo = rotulos_questoes.get(int(coluna[1:]), coluna)
    plt.title(f'Histograma - {titulo}')
    plt.xlabel(titulo)
    plt.ylabel('Frequência')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'histograma_{coluna}.png')
    plt.close()

# ====== FUNÇÕES PARA VARIÁVEIS CATEGÓRICAS ======

def freq_absoluta(df, coluna):
    return df[coluna].value_counts()

def freq_relativa(df, coluna):
    return df[coluna].value_counts(normalize=True) * 100

def moda_categoria(df, coluna):
    return df[coluna].mode().iloc[0] if not df[coluna].mode().empty else None

def grafico_pizza(df, coluna):
    plt.figure()
    titulo = rotulos_questoes.get(int(coluna[1:]), coluna)
    df[coluna].value_counts().plot.pie(autopct='%1.1f%%')
    plt.title(f'Gráfico de Pizza - {titulo}')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(f'pizza_{coluna}.png')
    plt.close()

def grafico_barras(df, coluna):
    plt.figure()
    titulo = rotulos_questoes.get(int(coluna[1:]), coluna)
    df[coluna].value_counts().plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title(f'Gráfico de Barras - {titulo}')
    plt.xlabel(titulo)
    plt.ylabel('Frequência')
    plt.xticks(rotation=0)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(f'barras_{coluna}.png')
    plt.close()

def medida_entropia(df, coluna):
    probs = df[coluna].value_counts(normalize=True)
    return entropy(probs, base=2)

def teste_chi2(df, col1, col2):
    cont = pd.crosstab(df[col1], df[col2])
    stat, p, dof, _ = chi2_contingency(cont)
    return {'chi2': stat, 'p': p, 'dof': dof}

def proporcoes(df, coluna):
    return freq_relativa(df, coluna)

def comparacao_subgrupos(df, cat_col, target_col):
    return df.groupby(cat_col)[target_col].value_counts(normalize=True).unstack().fillna(0)

def matriz_confusao(df, col1, col2):
    return pd.crosstab(df[col1], df[col2])

def analise_correspondencia(df, col1, col2):
    cont = pd.crosstab(df[col1], df[col2])
    stat, p, dof, _ = chi2_contingency(cont)
    return {'contingencia': cont, 'p_valor': p}

# === Analise Conjunta ===
def pearson_corr(df, col1, col2):
    r, p = pearsonr(df[col1], df[col2])
    return {"correlação_pearson": r, "p_valor": p}

def qui_quadrado(df, col1, col2):
    tabela = pd.crosstab(df[col1], df[col2])
    chi2, p, dof, _ = chi2_contingency(tabela)
    return {"qui2": chi2, "p_valor": p, "graus_liberdade": dof, "tabela": tabela.to_dict()}

def media_por_grupo(df, grupo_col, valor_col):
    grupos = df.groupby(grupo_col)[valor_col].mean()
    return grupos.to_dict()

def teste_t_por_grupo(df, grupo_col, valor_col):
    grupo1 = df[df[grupo_col] == 1][valor_col]
    grupo2 = df[df[grupo_col] == 2][valor_col]
    t_stat, p_valor = ttest_ind(grupo1, grupo2, equal_var=False)
    return {
        "media_grupo_1": grupo1.mean(),
        "media_grupo_2": grupo2.mean(),
        "t_stat": t_stat,
        "p_valor": p_valor
    }

def clusterizar(df, cols, n_clusters=3):
    scaler = StandardScaler()
    X_norm = scaler.fit_transform(df[cols])
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init="auto")
    df['cluster'] = kmeans.fit_predict(X_norm)
    return df['cluster'], df.groupby('cluster')[cols].mean()

##################################################################

resultados_quantitativos = {}
resultados_categoricos = {}
resultados_relacionaveis = {}
questoes_quant = ["Q1", "Q3", "Q4", "Q7", "Q9", "Q11", "Q13"]
questoes_cat = ["Q2", "Q5", "Q6", "Q8", "Q10", "Q12"] + [f"Q{i}" for i in range(14, 28)]

float_df_numericos = df_numerico.astype(float)

print("Calculando dados quantitativos... \n")
for q in questoes_quant:
    resultados_quantitativos[q] = {
        'Contagem': contagem(float_df_numericos, q),
        'Média': media(float_df_numericos, q),
        'Mediana': mediana(float_df_numericos, q),
        'Moda': moda(float_df_numericos, q),
        'Mínimo': minimo(float_df_numericos, q),
        'Máximo': maximo(float_df_numericos, q),
        'Intervalo': intervalo(float_df_numericos, q),
        'Desvio padrão': desvio_padrao(float_df_numericos, q),
        'Variância': variancia(float_df_numericos, q),
        'Coeficiente de variação': coef_var(float_df_numericos, q),
        'Quartis': quartis(float_df_numericos, q),
        'IQR': iqr(float_df_numericos, q)
    }
    histograma(float_df_numericos, q)

print("Calculando dados categóricos... \n")
for q in questoes_cat:
    resultados_categoricos[q] = {
        'Frequência absoluta': freq_absoluta(float_df_numericos, q).to_dict(),
        'Frequência relativa (%)': freq_relativa(float_df_numericos, q).to_dict(),
        'Moda': moda_categoria(float_df_numericos, q),
        'Entropia': medida_entropia(float_df_numericos, q)
    }
    grafico_pizza(float_df_numericos, q)
    grafico_barras(float_df_numericos, q)

print("Calculando dados relacionaveis... \n")
# 1. Correlação entre idade e tempo de uso do computador
pares_correlacao = [("Q1", "Q9")]
for col1, col2 in pares_correlacao:
    resultados_relacionaveis[f"correlacao_{col1}_{col2}"] = pearson_corr(float_df_numericos, col1, col2)

# 2. Associação entre trabalhar e uso da internet para trabalho
pares_qui2 = [("Q6", "Q14"), ("Q24", "Q16")]
for col1, col2 in pares_qui2:
    resultados_relacionaveis[f"qui_quadrado_{col1}_{col2}"] = qui_quadrado(float_df_numericos, col1, col2)

# 3. Associação entre dispositivo e tempo conectado (média por grupo)
pares_media = [("Q12", "Q13")]
for grupo_col, valor_col in pares_media:
    resultados_relacionaveis[f"media_{valor_col}_por_{grupo_col}"] = media_por_grupo(float_df_numericos, grupo_col, valor_col)

# 4. Comparação de médias por sexo (teste t)
pares_teste_t = [("Q2", "Q13")]
for grupo_col, valor_col in pares_teste_t:
    resultados_relacionaveis[f"teste_t_{valor_col}_por_{grupo_col}"] = teste_t_por_grupo(float_df_numericos, grupo_col, valor_col)

# 5. Clusterização
colunas_cluster = [f"Q{i}" for i in range(5, 27)]
float_df_numericos["cluster"], perfil_clusters = clusterizar(float_df_numericos, colunas_cluster)
resultados_relacionaveis["perfil_clusters"] = perfil_clusters.to_dict(orient="index")

# === SALVAR JSONs
# with open("resultados_quantitativos.json", "w", encoding="utf-8") as f:
#     json.dump(resultados_quantitativos, f, indent=4, ensure_ascii=False)

# with open("resultados_categoricos.json", "w", encoding="utf-8") as f:
#     json.dump(resultados_categoricos, f, indent=4, ensure_ascii=False)

# with open("resultados_relacionaveis.json", "w", encoding="utf-8") as f:
#     json.dump(resultados_relacionaveis, f, indent=4, ensure_ascii=False)

# === SALVAR XLS
print("Salvandos dados calculados em XLS... \n")

# Quantitativos
df_quant = pd.DataFrame(resultados_quantitativos).T
df_quant.to_excel("resultados_quantitativos.xlsx")

# Categóricos (colocando cada resultado como string json para caber na célula do Excel)
df_cat = pd.DataFrame({k: {sk: str(v[sk]) for sk in v} for k, v in resultados_categoricos.items()}).T
df_cat.to_excel("resultados_categoricos.xlsx")

# Relacionáveis
df_rel = pd.DataFrame({k: str(v) for k, v in resultados_relacionaveis.items()}.items(), columns=["Análise", "Resultado"])
df_rel.to_excel("resultados_relacionaveis.xlsx", index=False)