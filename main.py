import questionario
import utils
import pandas as pd
import json

rotulos_questoes = questionario.rotulos_questoes

# Limites e tipos de respostas
limites = questionario.limites

# Mapeamento DE/PARA baseado nas alternativas do questionário
de_para = questionario.de_para

# Geração dos dados
dados_numericos = []
dados_textuais = []

print(f"Gerando {utils.TOTAL_NUMBER} dados aleatórios... \n")

for _ in range(utils.TOTAL_NUMBER):
    entrada_numerica = {f"Q{q}": limites[q]() for q in range(1, 28)}
    entrada_textual = {
        f"Q{q}": de_para[q][entrada_numerica[f"Q{q}"]] if q in de_para else entrada_numerica[f"Q{q}"]
        for q in range(1, 28)
    }

    dados_numericos.append(entrada_numerica)
    dados_textuais.append(entrada_textual)

# Criação de DataFrames
df_numerico = pd.DataFrame(dados_numericos)
df_textual = pd.DataFrame(dados_textuais)

# Salvando arquivos
print("Salvando arquivos XLS... \n")
df_numerico.to_excel("DB/dados_numericos.xlsx", index=False)
df_textual.to_excel("DB/dados_textuais.xlsx", index=False)

with open("DB/dados_numericos.json", "w", encoding="utf-8") as f:
    json.dump(dados_numericos, f, ensure_ascii=False, indent=4)

with open("DB/dados_textuais.json", "w", encoding="utf-8") as f:
    json.dump(dados_textuais, f, ensure_ascii=False, indent=4)

resultados_quantitativos = {}
resultados_categoricos = {}
resultados_relacionaveis = {}
questoes_quant = ["Q1", "Q3", "Q4", "Q7", "Q9", "Q11", "Q13"]
questoes_cat = ["Q2", "Q5", "Q6", "Q8", "Q10", "Q12"] + [f"Q{i}" for i in range(14, 28)]

float_df_numericos = df_numerico.astype(float).round(2)

print("Calculando dados quantitativos... \n")
for q in questoes_quant:
    resultados_quantitativos[q] = {
        'Contagem': utils.contagem(float_df_numericos, q),
        'Média': utils.media(float_df_numericos, q),
        'Mediana': utils.mediana(float_df_numericos, q),
        'Moda': utils.moda(float_df_numericos, q),
        'Mínimo': utils.minimo(float_df_numericos, q),
        'Máximo': utils.maximo(float_df_numericos, q),
        'Intervalo': utils.intervalo(float_df_numericos, q),
        'Desvio padrão': utils.desvio_padrao(float_df_numericos, q),
        'Variância': utils.variancia(float_df_numericos, q),
        'Coeficiente de variação': utils.coef_var(float_df_numericos, q),
        'Quartis': utils.quartis(float_df_numericos, q),
        'IQR': utils.iqr(float_df_numericos, q)
    }

    utils.histograma(float_df_numericos, q)

print("Calculando dados categóricos... \n")
for q in questoes_cat:
    resultados_categoricos[q] = {
        'Frequência absoluta': utils.freq_absoluta(float_df_numericos, q).to_dict(),
        'Frequência relativa (%)': utils.freq_relativa(float_df_numericos, q).to_dict(),
        'Moda': utils.moda_categoria(float_df_numericos, q),
        'Entropia': utils.medida_entropia(float_df_numericos, q)
    }

    utils.grafico_pizza(float_df_numericos, q)
    utils.grafico_barras(float_df_numericos, q)

print("Calculando dados relacionaveis... \n")

# 1. Correlação entre idade e tempo de uso do computador
pares_correlacao = [("Q1", "Q9")]
for col1, col2 in pares_correlacao:
    resultados_relacionaveis[f"correlacao_{col1}_{col2}"] = utils.pearson_corr(float_df_numericos, col1, col2)

# 2. Associação entre trabalhar e uso da internet para trabalho
pares_qui2 = [("Q6", "Q14"), ("Q24", "Q16")]
for col1, col2 in pares_qui2:
    resultados_relacionaveis[f"qui_quadrado_{col1}_{col2}"] = utils.qui_quadrado(float_df_numericos, col1, col2)

# 3. Associação entre dispositivo e tempo conectado (média por grupo)
pares_media = [("Q12", "Q13")]
for grupo_col, valor_col in pares_media:
    resultados_relacionaveis[f"media_{valor_col}_por_{grupo_col}"] = utils.media_por_grupo(float_df_numericos, grupo_col, valor_col)

# 4. Comparação de médias por sexo (teste t)
pares_teste_t = [("Q2", "Q13")]
for grupo_col, valor_col in pares_teste_t:
    resultados_relacionaveis[f"teste_t_{valor_col}_por_{grupo_col}"] = utils.teste_t_por_grupo(float_df_numericos, grupo_col, valor_col)

# 5. Clusterização
colunas_cluster = [f"Q{i}" for i in range(5, 27)]
float_df_numericos["cluster"], perfil_clusters = utils.clusterizar(float_df_numericos, colunas_cluster)
resultados_relacionaveis["perfil_clusters"] = perfil_clusters.to_dict(orient="index")

# === SALVAR XLS
print("Salvandos dados calculados em XLS... \n")

# Quantitativos
df_quant = pd.DataFrame(resultados_quantitativos).T
df_quant.to_excel("DB/resultados_quantitativos.xlsx")

# Categóricos (colocando cada resultado como string json para caber na célula do Excel)
df_cat = pd.DataFrame({k: {sk: str(v[sk]) for sk in v} for k, v in resultados_categoricos.items()}).T
df_cat.to_excel("DB/resultados_categoricos.xlsx")

# Relacionáveis
df_rel = pd.DataFrame({k: str(v) for k, v in resultados_relacionaveis.items()}.items(), columns=["Análise", "Resultado"])
df_rel.to_excel("DB/resultados_relacionaveis.xlsx", index=False)