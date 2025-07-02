import questionario
import utils
import pandas as pd
import numpy as np
import json
import os

# os.makedirs("DB/", exist_ok=True)
rotulos_questoes = questionario.rotulos_questoes

# Limites e tipos de respostas
limites = questionario.limites

# Mapeamento DE/PARA baseado nas alternativas do questionário
de_para = questionario.de_para

# Geração dos dados
# dados_numericos = pd.read_excel("DB/respostas_questionario_internet.xlsx")
# dados_textuais = []

# print(f"Gerando {utils.TOTAL_NUMBER} dados aleatórios... \n")

# for _ in range(utils.TOTAL_NUMBER):
#     entrada_numerica = {f"Q{q}": limites[q]() for q in range(1, 28)}
#     entrada_textual = {
#         f"Q{q}": de_para[q][entrada_numerica[f"Q{q}"]] if q in de_para else entrada_numerica[f"Q{q}"]
#         for q in range(1, 28)
#     }

#     dados_numericos.append(entrada_numerica)
#     dados_textuais.append(entrada_textual)

# Criação de DataFrames
df_numerico = pd.read_excel('DB/respostas_questionario_internet.xlsx')
# df_textual = pd.DataFrame(dados_textuais)

# # Salvando arquivos
# print("Salvando arquivos XLS... \n")
# df_numerico.to_excel("DB/dados_numericos.xlsx", index=False)
# df_textual.to_excel("DB/dados_textuais.xlsx", index=False)

# with open("DB/dados_numericos.json", "w", encoding="utf-8") as f:
#     json.dump(dados_numericos, f, ensure_ascii=False, indent=4)

# with open("DB/dados_textuais.json", "w", encoding="utf-8") as f:
#     json.dump(dados_textuais, f, ensure_ascii=False, indent=4)

resultados_quantitativos = {}
resultados_qualitativos = {}
resultados_relacionaveis = {}
questoes_quant = ["Q3"]
questoes_cat = ["Q1", "Q2"] + [f"Q{i}" for i in range(4, 28)]
float_df_numericos = df_numerico.astype(float).round(2)

print("Calculando dados quantitativos... \n")
for q in questoes_quant:
    intervalo = utils.intervalo(float_df_numericos, q).astype(np.int64)
    resultados_quantitativos[q] = {
        'Contagem': utils.contagem(float_df_numericos, q),
        'Média': utils.media(float_df_numericos, q),
        'Mediana': utils.mediana(float_df_numericos, q),
        'Moda': utils.moda(float_df_numericos, q),
        'Mínimo': utils.minimo(float_df_numericos, q),
        'Máximo': utils.maximo(float_df_numericos, q),
        'Intervalo': intervalo,
        'Desvio padrão': utils.desvio_padrao(float_df_numericos, q),
        'Variância': utils.variancia(float_df_numericos, q),
        'Coeficiente de variação': utils.coef_var(float_df_numericos, q),
        'Quartis': utils.quartis(float_df_numericos, q),
        'IQR': utils.iqr(float_df_numericos, q)
    }

    utils.histograma(float_df_numericos, q, intervalo)

print("Calculando dados qualitativos... \n")
for q in questoes_cat:
    resultados_qualitativos[q] = {
        'Frequência absoluta': utils.freq_absoluta(float_df_numericos, q).to_dict(),
        'Frequência relativa (%)': utils.freq_relativa(float_df_numericos, q).to_dict(),
        'Moda': utils.moda_categoria(float_df_numericos, q),
        'Entropia': utils.medida_entropia(float_df_numericos, q)
    }

    utils.grafico_pizza(float_df_numericos, q)
    utils.grafico_barras(float_df_numericos, q)

print("Calculando dados relacionaveis... \n")

# === RELACIONÁVEIS ===
# 1. Correlação entre idade e tempo de uso do computador
pares_correlacao = [("Q1", "Q9")]
for col1, col2 in pares_correlacao:
    resultado = utils.pearson_corr(float_df_numericos, col1, col2)
    resultados_relacionaveis[f"correlacao_{col1}_{col2}"] = resultado
    
    with open(f"DB/correlacao_{col1}_{col2}.txt", "w", encoding="utf-8") as f:
        f.write(f"Correlação de Pearson entre {col1} - {rotulos_questoes[int(col1[1:])]} e {col2} - {rotulos_questoes[int(col2[1:])]}\n")
        f.write(f"Coeficiente de correlação: {resultado['correlação_pearson']:.4f}\n")
        f.write(f"p-valor: {resultado['p_valor']:.4g}\n")

# 2. Relação entre trabalhar e uso da internet para trabalho
pares_qui2 = [("Q6", "Q14"), ("Q24", "Q16")]
for col1, col2 in pares_qui2:
    resultado = utils.qui_quadrado(float_df_numericos, col1, col2)
    resultados_relacionaveis[f"qui_quadrado_{col1}_{col2}"] = resultado

    with open(f"DB/qui_quadrado_{col1}_{col2}.txt", "w", encoding="utf-8") as f:
        f.write(f"Relação entre {col1} - {rotulos_questoes[int(col1[1:])]} e {col2} - {rotulos_questoes[int(col2[1:])]}\n")
        f.write(f"Qui-quadrado: {resultado['qui2']:.4f}\n")
        f.write(f"p-valor: {resultado['p_valor']:.4g}\n")

# 3. Média por grupo (ex: dispositivo e tempo conectado)
pares_media = [("Q12", "Q13")]
for grupo_col, valor_col in pares_media:
    resultado = utils.media_por_grupo(float_df_numericos, grupo_col, valor_col)
    resultados_relacionaveis[f"media_{valor_col}_por_{grupo_col}"] = resultado

    with open(f"DB/media_{valor_col}_por_{grupo_col}.txt", "w", encoding="utf-8") as f:
        f.write(f"Média de {valor_col} - {rotulos_questoes[int(valor_col[1:])]} por grupo de {grupo_col} - {rotulos_questoes[int(grupo_col[1:])]}\n")
        for grupo, media in resultado.items():
            f.write(f"Grupo {grupo}: média = {media:.2f}\n")

# 4. Teste t (comparação entre grupos)
pares_teste_t = [("Q2", "Q13")]
rotulos_q12 = {1: "Celular", 2: "Tablet", 3: "Computador/Notebook"}
for grupo_col, valor_col in pares_media:
    resultado = utils.media_por_grupo(float_df_numericos, grupo_col, valor_col)
    resultados_relacionaveis[f"media_{valor_col}_por_{grupo_col}"] = resultado

    with open(f"DB/media_{valor_col}_por_{grupo_col}.txt", "w", encoding="utf-8") as f:
        f.write(f"Média de {valor_col} - {rotulos_questoes[int(valor_col[1:])]} por tipo de {grupo_col} - {rotulos_questoes[int(grupo_col[1:])]}\n\n")
        for grupo, media in resultado.items():
            rotulo = rotulos_q12.get(int(grupo), f"Grupo {grupo}")
            f.write(f"Média {rotulo}: {media:.2f}\n")

# 5. Clusterização
colunas_cluster = [f"Q{i}" for i in range(5, 28)]
float_df_numericos["cluster"], perfil_clusters = utils.clusterizar(float_df_numericos, colunas_cluster)
resultados_relacionaveis["perfil_clusters"] = perfil_clusters.to_dict(orient="index")

with open("DB/perfil_clusters.txt", "w", encoding="utf-8") as f:
    f.write("Perfil médio por cluster com base nas questões Q5 a Q26\n\n")
    for cluster_id, perfil in perfil_clusters.iterrows():
        f.write(f"Cluster {cluster_id+1}:\n")
        for col, val in perfil.items():
            f.write(f"  {col} ({rotulos_questoes.get(int(col[1:]), col)}): {val:.2f}\n")
        f.write("\n")

# === SALVAR EM XLS
print("Salvando dados calculados em XLS...\n")

# Quantitativos
df_quant = pd.DataFrame(resultados_quantitativos).T
df_quant.to_excel("DB/resultados_quantitativos.xlsx")

# Qualitativos
df_cat = pd.DataFrame({k: {sk: str(v[sk]) for sk in v} for k, v in resultados_qualitativos.items()}).T
df_cat.to_excel("DB/resultados_qualitativos.xlsx")

# Relacionáveis
df_rel = pd.DataFrame({k: str(v) for k, v in resultados_relacionaveis.items()}.items(), columns=["Análise", "Resultado"])
df_rel.to_excel("DB/resultados_relacionaveis.xlsx", index=False)

# === SALVAR TODAS AS ESTATÍSTICAS QUANTITATIVAS EM UM ÚNICO ARQUIVO ===
with open("DB/estatisticas_quantitativas.txt", "w", encoding="utf-8") as f:
    f.write("QUESTÕES QUANTITATIVAS\n")
    f.write("="*70 + "\n\n")

    for q, resultados in resultados_quantitativos.items():
        f.write(f"Questão {q} - {rotulos_questoes.get(int(q[1:]), q)}\n")
        f.write("-"*60 + "\n")
        for nome, valor in resultados.items():
            if isinstance(valor, dict):
                f.write(f"{nome}:\n")
                for k, v in valor.items():
                    f.write(f"  {k}: {v}\n")
            else:
                f.write(f"{nome}: {valor}\n")
        f.write("\n")

# === SALVAR TODAS AS ESTATÍSTICAS QUALITATIVAS EM UM ÚNICO ARQUIVO ===
with open("DB/estatisticas_qualitativas.txt", "w", encoding="utf-8") as f:
    f.write("QUESTÕES QUALITATIVAS\n")
    f.write("="*70 + "\n\n")

    for q, resultados in resultados_qualitativos.items():
        f.write(f"Questão {q} - {rotulos_questoes.get(int(q[1:]), q)}\n")
        f.write("-"*60 + "\n")
        for nome, valor in resultados.items():
            if isinstance(valor, dict):
                f.write(f"{nome}:\n")
                for k, v in valor.items():
                    f.write(f"  {k}: {v}\n")
            else:
                f.write(f"{nome}: {valor}\n")
        f.write("\n\n")