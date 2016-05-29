rm(list = ls())
library(tcltk)

file_names = tk_choose.files()
data <- data.frame()
for (file_name in file_names) {
  ldata <- read.csv(file_name) # Mettre le nom du fichier à analyser
  data <- rbind(data, ldata)
}

dist = (data$note2 - data$note1)%%12
data <- cbind(data, dist)
expected = rep(0, nrow(data))
expected[(data$note2 - data$note1)%%12 > 6] = -1
expected[(data$note2 - data$note1)%%12 < 6] = 1

data <- cbind(data, expected)

same <- data$resp == data$expected
same[data$expected == 0] = NA
data <- cbind(data, same)

cat("La réponse était celle attendue dans \n")
cat(mean(data$same, na.rm = TRUE))
cat(" des cas en supprimant les tritons\n")

heared_raising = data$resp == 1
data <- cbind(data, heared_raising)
mean_for_plot = aggregate(heared_raising ~ dist, data, mean)
plot(mean_for_plot, type="l", main="ratio montant en fonction de distance")


tbl = table(data[data$dist == 5 | data$dist == 7,]$note1, paste(data[data$dist == 5 | data$dist == 7,]$resp, data[data$dist == 5 | data$dist == 7,]$expected, sep=","))
res = chisq.test(tbl)
cat("************************\n")
cat("Table des réponses en fonction de la note jouée\n")
cat("Premier nombre: réponse, deuxième: réponse attendue")
print(tbl)
print(res)
if (res$p.value < 0.05) {
  cat("Il y a dépendance entre la note jouée et la direction de l'intervalle\n")
} else {
  cat("Il y a indépendance entre la note jouée et la direction de l'intervalle\n")
}

tbl = table(data[data$dist == 5 | data$dist == 7,]$note1, data[data$dist == 5 | data$dist == 7,]$same)
res = chisq.test(tbl)
cat("************************\n")
cat("Table des corresp entre réponse et attendu en fonction de la note jouée")
print(tbl)
print(res)
if (res$p.value < 0.05) {
  cat("Il y a dépendance entre la note jouée et la direction de l'intervalle\n")
} else {
  cat("Il y a indépendance entre la note jouée et la direction de l'intervalle\n")
}


tbl = table(data[data$dist == 5,]$note1, data[data$dist == 5,]$resp)
res = chisq.test(tbl)
cat("************************\n")
cat("Table des réponses en fonction de la note jouée (quarte uniquement)\n")
cat("Premier nombre: réponse, deuxième: réponse attendue")
print(tbl)
print(res)
if (res$p.value < 0.05) {
  cat("Il y a dépendance entre la note jouée et la direction de l'intervalle\n")
} else {
  cat("Il y a indépendance entre la note jouée et la direction de l'intervalle\n")
}


tbl = table(data[data$dist == 7,]$note1, data[data$dist == 7,]$resp)
res = chisq.test(tbl)
cat("************************\n")
cat("Table des réponses en fonction de la note jouée (quinte uniquement)\n")
cat("Premier nombre: réponse, deuxième: réponse attendue")
print(tbl)
print(res)
if (res$p.value < 0.05) {
  cat("Il y a dépendance entre la note jouée et la direction de l'intervalle\n")
} else {
  cat("Il y a indépendance entre la note jouée et la direction de l'intervalle\n")
}

#