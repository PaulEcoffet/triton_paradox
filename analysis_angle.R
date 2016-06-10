rm(list = ls())
library(tcltk)
library(CircStats)


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
plot(mean_for_plot, type="l", main="ratio montant en fonction de distance", ylim=c(-0.1, 1.1))

angles_i = seq(pi/2,2*pi+pi/2, length=13)
angles_i = angles_i[1:12]
angles_i = angles_i %% (2*pi)
notes_name = c('A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab')


angles = c()
for (ind in 1:nrow(data)){
  if (data$heared_raising[ind]) {
    note = data$note2[ind]
  } else {
    note = data$note1[ind]
  }
  angles = c(angles, angles_i[note + 1])
}
trit_mean = aggregate(heared_raising ~ note1, data[data$dist == 6,], mean)
plot(trit_mean, type="l", ylim=c(-0.1, 1.1))

data = cbind(data, angles)

for (d in c(5, 6, 7)) {
  cat("\n\n")
  cat(paste("******** intervalle:", d, "********\n"))
  cur = data[data$dist==d,]
  mean_angle = circ.mean(cur$angles)
  disp = circ.disp(cur$angles)
  rbar = disp$rbar
  cat(paste("angle moyen:", mean_angle, "\n"))
  print(disp)
  test = r.test(cur$angles)
  print(test)
  if (test$p.value > 0.05) {
    cat("\\\\ L'effet n'est pas significatif //\n")
  } else {
    cat("\\\\ L'effet est significatif //\n")
  }
  
  ### PLOTTING ###
  # +1/1000 because circ.plot bugs if angles are at a 0 value
  circ.plot(cur$angles+1/1000, stack=TRUE, bins=360, shrink=5.5, main=paste("horloge pour", d))
  arrows(0, 0, rbar*cos(mean_angle), rbar*sin(mean_angle))
  abline(0, -cos(mean_angle)/sin(mean_angle))
  text(0.9*cos(angles_i), 0.9*sin(angles_i), notes_name)
  dev.print(png, width=800, file=paste("/tmp/graph_", d, ".png",sep=""));

}

print("lol")

trit_mean = aggregate(heared_raising ~ note1, data[data$dist == 6,], mean)
plot(trit_mean, type="l", ylim=c(-0.1, 1.1))

best = NA
score_best = 0
for (i in 0:5) {
  prv = (i - 1)%%12
  nxt = (i + 1)%%12
  score = abs(trit_mean[trit_mean$note1 == prv,]$heared_raising - trit_mean[trit_mean$note1 == nxt,]$heared_raising)
  prv = (i + 5)%%12
  nxt = (i + 7)%%12
  score = score + abs(trit_mean[trit_mean$note1 == prv,]$heared_raising - trit_mean[trit_mean$note1 == nxt,]$heared_raising)
  print(paste(i, "score:", score))
  if (score > score_best) {
    best = i
    score_best = score
  }
}

print(paste("frontiere raising is at", notes_name[best+1], "-", notes_name[best+7]))
