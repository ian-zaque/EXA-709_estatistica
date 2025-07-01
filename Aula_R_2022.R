############################################
#Instala??o de pacotes no ambiente R#
############################################
install.packages('readxl') #importar banco em excel
install.packages('descr') #crosstable e teste qui-quadrado

                 
##################
#Chamadar pacote #
##################                
library(readxl) #importar banco em excel
library(descr)#crosstable

#########################
#Chamar o banco de dados#
#########################                 
#1) Import Dataset

#2) Escolha a extens?o do seu arquivo (Excel, spss, stata, csv, dta...)

#3) V? em Browse

#OBS: Para abrir banco com extens?o csv ou dta n?o ? necess?rio baixar pacote
#library(readxl) #biblioteca necess?ria para abrir o banco em excel
#library(haven) #biblioteca necess?ria para abrir o banco em stata, spss e sas


#######################
#Ver o banco de dados #
#######################

View(dados) # ver o banco de dados
fix(dados)  #alterar valores 
names(dados) # ver o nome das vari?veis que est?o no arquivo

#####################
#Manipular vari?vel #
#####################

dim(dados) #vendo a dimens?o do banco de dados
length(dados)

#dados$nome da vari?vel ver a vari?vel separadamente
dados$DIETA

attach(dados) #Separar a vari?vel do banco de dados
DIETA

#detach(dados) # Tirar a fun??o attach



######################
#Medidas descritivas #
######################

range(PESO) #Valor m?nimo e m?ximo
diff(range(PESO, na.rm=T)) #Amplitude
mean(PESO) #M?dia
median(PESO) #M?diana

sd (PESO) #Desvio padr?o
var(PESO)#Vari?ncia


cv=sd(PESO)/mean(PESO)*100 #coeficiente de varia??o
cv


summary(PESO)

###########################
#TROCAR O NOME DA VARIAVEL#
###########################

names(dados)[8] <- c("Diferenca")
names(dados)[3:4] <- c("PESOINICIAL", "PESOFINAL")
names(dados)
#####################################
# Transformar uma variavel em fator #
#####################################

factor(DIETA)

##Codificando vari?veis num?ricas como categ?ricas.


Social=factor(SOCIAL, levels = c(1,2,3),labels = c("baixa", "media", "alta")) # Colocando labels
Social
###########incluir no banco de dados 
social.new <- matrix(Social,ncol=1)
social.new
dados["social.new"]<-social.new


#################
# Fun??o tapply #
#################

## Agrega os valores de um vetor num?rico segundo os valores de alguma vari?vel categ?rica.

tapply(IDADE, Social,summary) #sumario da idade por tipo de dieta

tapply(IDADE, DIETA,summary) #sumario da idade por tipo de dieta

tapply(IDADE, DIETA ,mean)

tapply(dados$PESOINICIAL, list(IDADE>=28),summary)

attach(dados)
tapply(PESOINICIAL, list(IDADE>=28),summary)

###########################
# Frqu?ncia das vari?veis #
###########################

####Vari?veis  qualitativa####

table(DIETA)
table(Social)
prop.table(table (DIETA))

##cruzando duas vari?veis

table (DIETA,Social)
prop.table(table(DIETA,Social))

crosstab(DIETA,Social, prop.r = TRUE, plot = FALSE)# precisa do pacote descr
crosstab (DIETA,Social,prop.c = TRUE, plot = FALSE)
crosstab (DIETA,Social, prop.t = TRUE,plot = FALSE)

table(DIETA,Social, IDADE)
table(DIETA,Social, IDADE>=28) #GRUPO COM IDADE MAIOR QUE 28
crosstab (DIETA,Social,IDADE>=28, prop.r = TRUE, plot = FALSE)

summary(DIETA,IDADE)



###########################
# Teste qui-quadrado     #
###########################

crosstab (DIETA,Social,expected = FALSE, prop.r = TRUE, 
          chisq = TRUE, fisher = TRUE, plot = FALSE)

crosstab (DIETA,Social,expected = TRUE, prop.r = TRUE,
          chisq = TRUE, fisher = TRUE, plot = FALSE)

chisq.test(DIETA,Social) # N?o sai a tabela, s? o resultado de teste qui-quadrado



############
# Gráficos #
############


pie(table(DIETA), main = "Dieta dos pacientes",labels = c("Dieta 1","Dieta 2"))
x11()
pie(table(SOCIAL), main = "Classe social",labels = c("Baixa","Média","Alta"))
plot(IDADE,Diferenca, main = "Distribuição da idade por diferença do peso.")
hist(IDADE, main = "Histograma da Idade do Aluno.")
    
boxplot(PESOINICIAL~social.new,main = "Classe social pelo peso inicial", xlab="Classe social",ylab="Peso inicial")
boxplot(PESOFINAL~social.new,main = "Classe social pelo peso final", xlab="Classe social",ylab="Peso Final")
    
x11()# visualizando graficos fora da tela
par(mfrow=c(1, 2)) # visualizando graficos em pares
boxplot(PESOINICIAL~DIETA,main = "Dietas pelo peso inicial",names= c("Dieta 1","Dieta 2"), xlab="Dietas",ylab="Peso inicial")
boxplot(PESOFINAL~DIETA,main = "Dietas pelo peso final",names= c("Dieta 1","Dieta 2"), xlab="Dietas",ylab="Peso inicial")
    
    
    
#####################
#   Colocando Cores #
#####################

pie(table(DIETA), main = "Dieta dos pacientes",labels = c("Dieta 1","Dieta 2"),col = c("blue", "red"))
pie(table(SOCIAL), main = "Classe social dos pacientes",labels = c("Baixa","MéDIA","Alta"),col = c("palevioletred1", "sienna","blue"))
plot(IDADE,Diferenca, main = "Distribui??o da idade por diferen?a do peso.", col="blue")
    
    

pie(table(DIETA), main = "DIETAS DOS PACIENTES",labels = c("Dieta 1","Dieta 2"),col = c("blue", "red"))

plot(IDADE,DIFF, main = "Distribui??o da por diferen?a do peso.", col="blue")

hist(IDADE, main = "Histograma da Idade do Aluno.", col="pink")



barplot (table (DIETA,SOCIAL), ylab="Freq.",xlab="Faixa et?ria",ylim=c(0,40),names=c("baixa", "media", "alta"), col=c(4,7,3),beside=TRUE)
legend (6,40, c("Dieta1", "Dieta2"),fill=c(4,7))



x11()
par(mfrow=c(1, 2)) # visualizando graficos em pares
boxplot(PESOINICIAL~DIETA,main = "Dietas pelo peso inicial",names= c("Dieta 1","Dieta 2"), xlab="Dietas",ylab="Peso inicial",col = c("blue", "red"))
boxplot(PESOFINAL~DIETA,main = "Dietas pelo peso final",names= c("Dieta 1","Dieta 2"), xlab="Dietas",ylab="Peso inicial",col = c("blue", "red"))

