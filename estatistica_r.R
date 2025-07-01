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
questoes_quant <- c("Q1", "Q3", "Q4", "Q7", "Q9", "Q11", "Q13")
questoes_cat <- c("Q2", "Q5", "Q6", "Q8", "Q10", "Q12", paste0("Q", 14:27))

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
  hist(x, main = paste("Histograma de", q), xlab = q, col = c("blue", "red", "orange"))
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