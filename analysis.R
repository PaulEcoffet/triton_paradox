data <- read.csv("results/paul_1462814788.csv") # Mettre le nom du fichier à analyser
View(data)
expected = rep(0, 33)
expected[(data$note2 - data$note1)%%12 > 6] = -1
expected[(data$note2 - data$note1)%%12 < 6] = 1
cbind(data, expected)

data <- cbind(data, expected)
View(data)
same <- data$resp == data$expected
same[data$expected == 0] = NA
data <- cbind(data, same)

cat("La réponse était celle attendue dans \n")
print(mean(data$same, na.rm = TRUE))
cat("des cas en supprimant les tritons")
