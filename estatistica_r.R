# Instalar pacotes necessários
install.packages(c("readxl", "descr", "ggplot2", "dplyr", "psych", "entropy", "stats", "tidyr"))

# Carregar bibliotecas
library(readxl)
library(descr)
library(ggplot2)
library(dplyr)
library(psych)
library(entropy)
library(tidyr)

# ================================
# 1. Carregar dados
# ================================
#dados <- read_excel("dados_numericos.xlsx")

# Transformar tudo em numérico (igual ao df_numerico.astype(float))
dados <- dados %>% mutate(across(everything(), as.numeric))

# ================================
# 2. Listas de questões
# ================================
questoes_quant <- c("Q1", "Q3", "Q7", "Q9", "Q11", "Q13")
questoes_cat <- c("Q2", "Q4", "Q5", "Q6", "Q8", "Q10", "Q12", paste0("Q", 14:27))

# ================================
# 3. Análise Quantitativa
# ================================
for (q in questoes_quant) {
  cat("\n----- Estatísticas para", q, "-----\n")
  x <- dados[[q]]
  print(summary(x))
  cat("Moda:", as.numeric(names(sort(table(x), decreasing = TRUE))[1]), "\n")
  cat("Desvio padrão:", sd(x, na.rm = TRUE), "\n")
  cat("Variância:", var(x, na.rm = TRUE), "\n")
  cat("Coef. de variação:", sd(x, na.rm = TRUE) / mean(x, na.rm = TRUE) * 100, "%\n")
  cat("IQR:", IQR(x, na.rm = TRUE), "\n")
  
  # Histograma
  x11()
  hist(x, main = paste("Histograma de", q), xlab = q, labels=TRUE, col = c("blue", "red", "orange"))
}

# ================================
# 4. Análise Qualitativa
# ================================
for (q in questoes_cat) {
  cat("\n----- Frequência para", q, "-----\n")
  x <- as.factor(dados[[q]])
  tab <- table(x)
  print(tab)
  print(prop.table(tab) * 100)
  cat("Moda:", names(which.max(tab)), "\n")
  cat("Entropia:", entropy(tab, unit = "log2"), "\n")
  
  # Gráficos
  x11()
  pie(tab, main = paste("Distribuição de", q))
  x11()
  barplot(tab, main = paste("Frequência de", q), col = c("blue", "red", "orange"), ylab = "Frequência")
}

# ================================
# 5. Análises Relacionais
# ================================

# 1. Correlação entre idade e tempo de uso do computador
cat("\n===== Correlação Q1 ~ Q9 =====\n")
print(cor.test(dados$Q1, dados$Q9, method = "pearson"))

# 2. Associação (Qui-quadrado)
cat("\n===== Qui-quadrado Q6 x Q14 =====\n")
print(chisq.test(table(dados$Q6, dados$Q14)))

cat("\n===== Qui-quadrado Q24 x Q16 =====\n")
print(chisq.test(table(dados$Q24, dados$Q16)))

# 3. Média de Q13 por Q12 (tipo de dispositivo)
cat("\n===== Média de Q13 por Q12 =====\n")
print(tapply(dados$Q13, dados$Q12, mean, na.rm = TRUE))

# 4. Teste t de Q13 por sexo (Q2)
cat("\n===== Teste t de Q13 por Q2 (Sexo) =====\n")
print(t.test(Q13 ~ as.factor(Q2), data = dados))

# 5. Clusterização (usando kmeans)
cat("\n===== Clusterização (k=3) =====\n")
dados_cluster <- dados[, paste0("Q", 5:27)]
dados_cluster <- na.omit(dados_cluster)  # remover NA
set.seed(123)
modelo_kmeans <- kmeans(dados_cluster, centers = 3)
dados$cluster <- modelo_kmeans$cluster

# Perfil dos clusters
perfil <- aggregate(dados_cluster, by = list(cluster = dados$cluster), mean)
print(perfil)



# === Carregar dados ===
#dados <- read_excel("dados_numericos.xlsx")
#dados <- dados %>% mutate(across(everything(), as.numeric))

# === Criar pasta para salvar os resultados ===
#dir.create("resultados_txt", showWarnings = FALSE)

# === Correlações ===
sink("correlacoes.txt")
cat("Correlação Q1 (Idade) ~ Q13 (Tempo conectado):\n")
print(cor.test(dados$Q1, dados$Q13, method = "pearson"))

cat("\nCorrelação Q9 (Tempo de uso do computador) ~ Q11 (Tempo estudo internet):\n")
print(cor.test(dados$Q9, dados$Q11, method = "pearson"))

cat("\nCorrelação Q7 (Tempo de estudo diário) ~ Q11 (Tempo estudo internet):\n")
print(cor.test(dados$Q7, dados$Q11, method = "pearson"))
sink()

# === Qui-quadrado ===
sink("qui_quadrado.txt")
cat("Qui-quadrado Q10 x Q14:\n")
print(chisq.test(table(dados$Q10, dados$Q14)))

cat("\nQui-quadrado Q14 x Q18:\n")
print(chisq.test(table(dados$Q14, dados$Q18)))

cat("\nQui-quadrado Q15 x Q21:\n")
print(chisq.test(table(dados$Q15, dados$Q21)))

cat("\nQui-quadrado Q16 x Q24:\n")
print(chisq.test(table(dados$Q16, dados$Q24)))
sink()

# === Teste t e ANOVA ===
sink("testes_t_anova.txt")
cat("Teste t Q2 (Sexo) ~ Q13 (Tempo conectado):\n")
print(t.test(Q13 ~ as.factor(Q2), data = dados))

cat("\nTeste t Q5 (Período) ~ Q13 (Tempo conectado):\n")
print(t.test(Q13 ~ as.factor(Q5), data = dados))

cat("\nANOVA Q26 (O que representa o computador) ~ Q11 (Tempo estudo internet):\n")
print(summary(aov(Q11 ~ as.factor(Q26), data = dados)))
sink()

# === Regressão Linear ===
sink("regressao_linear.txt")
cat("Regressão linear: Q13 ~ Q1 + Q9 + Q6\n")
modelo <- lm(Q13 ~ Q1 + Q9 + as.factor(Q6), data = dados)
print(summary(modelo))
sink()

# === Clusterização ===
sink("clusterizacao.txt")
dados_cluster <- dados[, paste0("Q", 14:25)]
dados_cluster <- na.omit(dados_cluster)
set.seed(123)
modelo_cluster <- kmeans(dados_cluster, centers = 3)
dados$cluster <- modelo_cluster$cluster
cat("Clusterização com k = 3 (base Q14 a Q25)\n")
print(aggregate(dados_cluster, by = list(cluster = dados$cluster), mean))
sink()

# === (Opcional) Análise de correspondência múltipla ===
# install.packages("FactoMineR")
# library(FactoMineR)
# acm_data <- dados[, c("Q5", "Q12", "Q24")]
# acm_data[] <- lapply(acm_data, as.factor)
# res.mca <- MCA(acm_data, graph = TRUE)

