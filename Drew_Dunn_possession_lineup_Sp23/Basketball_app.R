library(DT)
require(data.table)

library(stringr)

library(tidyr)

library(grid)

library(gridExtra)

library(mosaic)

library(shinydashboard)

library(tidyverse)

library(fs)

library(readr)

library(shinyWidgets)

library(shiny)

library(shinyWidgets)

library(dplyr)

library(ggplot2)

library(sportyR)

library(plotly)

library(mgcv)

library(tidyr)

library(splitstackshape)

library(scales)

library(htmlwidgets)
df = read_csv('/Users/drewdunn/Desktop/Python code for research/Lineup/test.csv')
jacob = read_csv('/Users/drewdunn/Desktop/Python code for research/Research R stuff/ jacob bates _stats.csv')
bailey = read_csv('/Users/drewdunn/Desktop/Python code for research/Research R stuff/ bailey rakes _stats.csv')
jalen = read_csv('/Users/drewdunn/Desktop/Python code for research/Research R stuff/ jalen williams _stats.csv')
dawson = read_csv('/Users/drewdunn/Desktop/Python code for research/Research R stuff/ dawson crump _stats.csv')
art = read_csv('/Users/drewdunn/Desktop/Python code for research/Research R stuff/ art walker _stats.csv')
carter = read_csv('/Users/drewdunn/Desktop/Python code for research/Research R stuff/ carter baughman _stats.csv')
keegan = read_csv('/Users/drewdunn/Desktop/Python code for research/Research R stuff/ keegan brewer _stats.csv')
will = read_csv('/Users/drewdunn/Desktop/Python code for research/Research R stuff/ will britt _stats.csv')
rj = read_csv('/Users/drewdunn/Desktop/Python code for research/Research R stuff/ rj smith _stats.csv')
drew = read_csv('/Users/drewdunn/Desktop/Python code for research/Research R stuff/ drew wilson _stats.csv')
jakob = read_csv('/Users/drewdunn/Desktop/Python code for research/Research R stuff/ jakob spitzer _stats.csv')
kc = read_csv('/Users/drewdunn/Desktop/Python code for research/Research R stuff/ kc purvis _stats.csv')
dustin = read_csv('/Users/drewdunn/Desktop/Python code for research/Research R stuff/ dustin gerald _stats.csv')
perry = read_csv('/Users/drewdunn/Desktop/Python code for research/Research R stuff/ perry ayers _stats.csv')
pete = read_csv('/Users/drewdunn/Desktop/Python code for research/Research R stuff/ pete knochelmann _stats.csv')

sidebar <- dashboardSidebar(sidebarMenu(id = "tabs",
                                        menuItem(
                                          "Lineups", tabName = "Player", icon = icon("chart-bar"),
                                          pickerInput(
                                            inputId = "TeamInput", label = "Select Team",
                                            choices = c(sort(unique(df$boxscore_home_name))), selected = "CEN_COL",
                                            options = list(`actions-box` = TRUE), multiple = TRUE
                                          ),
                                          selectizeInput(
                                            inputId = "PlayerInput", label = "Select Player",
                                            choices = sort(unique(df$player1)), selected = NULL
                                          ))
))
#Once a player is clicked on their stats will show up
body <- dashboardBody(tabItems(
  tabItem(tabName = "Possession Stats",h2(fluidRow(
    tabPanel("Possession Stats", br(), tableOutput("df")))) #all plot outputs will be abbreviated 
  )))

ui <- dashboardPage(skin="yellow",
                    dashboardHeader(title = "Centre Sabermetrics"),
                    sidebar,
                    dashboardBody(
                      fluidRow(
                      box(tableOutput("table1"))
                    )
                    ))
server <- function(input, output) {
  
  output$table1 <- renderTable({{
    if (input$PlayerInput == 'jacob bates')
      jacob
    else if (input$PlayerInput == 'bailey rakes')
      bailey
    else if (input$PlayerInput == 'jalen williams')
      jalen
    else if (input$PlayerInput == 'dawson crump')
      dawson
    else if (input$PlayerInput == 'art walker')
      art
    else if (input$PlayerInput == 'carter baughman')
      carter
    else if (input$PlayerInput == 'keegan brewer')
      keegan
    else if (input$PlayerInput == 'will britt')
      will
    else if (input$PlayerInput == 'rj smith')
      rj
    else if (input$PlayerInput == 'drew wilson')
      drew
    else if (input$PlayerInput == 'jakob spitzer')
      jakob
    else if (input$PlayerInput == 'kc purvis')
      kc
    else if (input$PlayerInput == 'dustin gerald')
      dustin
    else if (input$PlayerInput == 'perry ayers')
      perry
    else if (input$PlayerInput == 'pete knochelmann')
      pete
  }}, bordered = TRUE)
  }
  

shinyApp(ui = ui, server = server)

df2 = df[df$`Possession Change` == 'O', ]
sum(df2$`Points Per Possession`)

