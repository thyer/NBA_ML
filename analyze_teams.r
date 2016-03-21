#!/usr/bin/env Rscript

path <- NULL
args = commandArgs(trailingOnly=TRUE)
if (length(args) == 0) {
  stop("Please provide a path to NBA_ML repo", call.=FALSE)
} else if (length(args) == 1) {
  path <- args[1]
}

install.packages("foreign", repos="http://cran.us.r-project.org")
install.packages("ggplot2", repos="http://cran.us.r-project.org")
install.packages("dplyr", repos="http://cran.us.r-project.org")
install.packages("gridExtra", repos="http://cran.us.r-project.org")

library(foreign)
library(ggplot2)
library(gridExtra)
library(dplyr)

# change into NBA_ML direcotry
setwd(path)

#Best: Cleveland Cavaliers, Golden State Warriors, Atlanta Hawks, Houston Rockets, Chicago Bulls.
cleavland <- read.arff("arffs/teams/Cleveland_Cavaliers.arff")
golden_state <- read.arff("arffs/teams/Golden State_Warriors.arff")
atlanta <- read.arff("arffs/teams/Atlanta_Hawks.arff")
huston <- read.arff("arffs/teams/Houston_Rockets.arff")
chicago <- read.arff("arffs/teams/Chicago_Bulls.arff")

#Worst: New York Knicks, Minnesota Timberwolves, Philadelphia 76ers, Sacramento Kings
nyknicks <- read.arff("arffs/teams/New York_Knicks.arff")
minnesota <- read.arff("arffs/teams/Minnesota_Timberwolves.arff")
philadelphia <- read.arff("arffs/teams/Philadelphia_76ers.arff")
sacramento <- read.arff("arffs/teams/Sacramento_Kings.arff")

allTeams <- list(cleavland, golden_state, atlanta, huston, chicago, nyknicks, minnesota, philadelphia, sacramento)
teamNames <- c("Cleveland_Cavaliers", "Golden_State_Warriors", "Atlanta_Hawks", "Houston_Rockets", "Chicago_Bulls", 
               "New_York_Knicks", "Minnesota_Timberwolves", "Philadelphia_76ers", "Sacramento_Kings")

multiplot <- function(..., plotlist=NULL, cols) {
  
  require(grid)
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  numPlots = length(plots)
  
  # Make the panel
  plotCols = cols                          # Number of columns of plots
  plotRows = ceiling(numPlots/plotCols) # Number of rows needed, calculated from # of cols
  
  # Set up the page
  grid.newpage()
  pushViewport(viewport(layout = grid.layout(plotRows, plotCols)))
  vplayout <- function(x, y)
    viewport(layout.pos.row = x, layout.pos.col = y)
  
  # Make each plot, in the correct location
  for (i in 1:numPlots) {
    curRow = ceiling(i/plotCols)
    curCol = (i-1) %% plotCols + 1
    print(plots[[i]], vp = vplayout(curRow, curCol ))
  }
}

# Generate all plots
for (i in 1:length(allTeams)) {
  team <- allTeams[[i]]
  teamName <- teamNames[i]
  
  # Plot 3-pointers
  fg3_attmpt_plot <- ggplot(arrange(team, season_year, game_id), aes(x=1:length(team[,1]), y=fg3_attempted_total, color = finals_match)) + geom_point() + geom_smooth() + xlab("Game Number")
  fg3_made_plot <- ggplot(arrange(team, season_year, game_id), aes(x=1:length(team[,1]), y=fg3_made_total, color = finals_match)) + geom_point() + geom_smooth() + xlab("Game Number")
  fg3_percen_avg_plot <- ggplot(arrange(team, season_year, game_id), aes(x=1:length(team[,1]), y=fg3_percent_average, color = finals_match)) + geom_point() + geom_smooth() + xlab("Game Number")
  
  # Calculate 2-pointers
  f2_attempted <- team$fg_attempted_total - team$fg3_attempted_total
  fg2_made <- team$fg_made_total - team$fg3_made_total
  fg2_avg <- fg2_made / f2_attempted
  
  # Plot 2-pointers
  fg2_attmpt_plot <- ggplot(arrange(team, season_year, game_id), aes(x=1:length(team[,1]), y=f2_attempted, color = finals_match)) + geom_point() + geom_smooth() + xlab("Game Number")
  fg2_made_plot <- ggplot(arrange(team, season_year, game_id), aes(x=1:length(team[,1]), y=fg2_made, color = finals_match)) + geom_point() + geom_smooth() + xlab("Game Number")
  fg2_percen_avg_plot <- ggplot(arrange(team, season_year, game_id), aes(x=1:length(team[,1]), y=fg2_avg, color = finals_match)) + geom_point() + geom_smooth() + xlab("Game Number")

  # Plot all free throws 
  fg_attmpt_plot <- ggplot(arrange(team, season_year, game_id), aes(x=1:length(team[,1]), y=fg_attempted_total, color = finals_match)) + geom_point() + geom_smooth() + xlab("Game Number")
  fg_made_plot <- ggplot(arrange(team, season_year, game_id), aes(x=1:length(team[,1]), y=fg_made_total, color = finals_match)) + geom_point() + geom_smooth() + xlab("Game Number")
  fg_percen_avg_plot <- ggplot(arrange(team, season_year, game_id), aes(x=1:length(team[,1]), y=fg_percent_average, color = finals_match)) + geom_point() + geom_smooth() + xlab("Game Number")
  
  # Total players accounted v. Average time played
  players_v_time_total <- ggplot(arrange(team, season_year, game_id), aes(x=total_players_accounted, y=average_time_played, color = finals_match)) + geom_point() + geom_smooth() + scale_y_continuous(breaks=seq(from=min(team$average_time_played), to=max(team$average_time_played), by = 200))
  players_v_time_notfinals <- ggplot(arrange(team[team$finals_match == " F",], season_year, game_id), aes(x=total_players_accounted, y=average_time_played)) + geom_point() + geom_smooth() + scale_y_continuous(breaks=seq(from=min(team$average_time_played), to=max(team$average_time_played), by = 200)) + ggtitle("Non-final games")
  players_v_time_finals <- ggplot(arrange(team[team$finals_match == " T",], season_year, game_id), aes(x=total_players_accounted, y=average_time_played)) + geom_point() + geom_smooth() + scale_y_continuous(breaks=seq(from=min(team$average_time_played), to=max(team$average_time_played), by = 200)) + ggtitle("Final games")
  
  if (!file.exists("plots")) {
  	dir.create(path = paste(getwd(), "/plots", sep = ""))
  }
  outfileName <- paste("plots/", teamName, ".tiff", sep = "")
  tiff(file = outfileName, width = 6200, height = 6200, units = "px", res = 400)
  multiplot(fg3_attmpt_plot, fg3_made_plot, fg3_percen_avg_plot,
  			fg2_attmpt_plot, fg2_made_plot, fg2_percen_avg_plot, 
  			fg_attmpt_plot, fg_made_plot, fg_percen_avg_plot,
            players_v_time_total, players_v_time_notfinals, players_v_time_finals,
            cols = 3)
 dev.off()
}
