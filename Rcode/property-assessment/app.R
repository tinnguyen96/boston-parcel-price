#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(tidyverse)
library(ggplot2)
theme_set(theme_gray(base_size = 15))
library(lme4)
library(shiny)


finaldf <- read.csv("../combineddf.csv")

# LUs <- finaldf %>% dplyr::pull(LU) %>% unique()
# we are interested in residential use codes 
LUs <- finaldf %>% dplyr::pull(LU) %>% unique()
years <- finaldf %>% dplyr::pull(YEAR) %>% unique()

source("../preprocess_lib.R")

# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("Boston Property Assessment"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
          width=2,
          selectInput("year", "Select year", choices=years,selected=2022),
          selectInput("LU", "Select land usage code", choices=LUs)
        ),

        # Show a plot of the generated distribution
        mainPanel(
           plotOutput("distPlot")
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
  
    output$distPlot <- renderPlot({
      subdf <- finaldf %>% dplyr::filter((YEAR == input$year) & (LU == input$LU))
      p <-  subdf  %>% ggplot(aes(x = log(LIVING_AREA), y = log(TOTAL_VALUE))) + 
        geom_point(size = 0.3) + 
        geom_smooth(method="lm") + 
        facet_wrap(vars(ZIPCODE))
      p
      # subdf <- subdf %>% mutate(LOG_TOTAL_VALUE = log(TOTAL_VALUE), LOG_LIVING_AREA = log(LIVING_AREA))
      # fit <- lmer("LOG_TOTAL_VALUE ~ LOG_LIVING_AREA + (LOG_LIVING_AREA | ZIPCODE)", subdf)
      # summary(fit)
    }, width = 1200, height = 700)
    
    output$timeplot <- renderPlot({
      zipcode <- "02116"
      lu <- "R1"
      subdf <- finaldf %>% dplyr::filter((ZIPCODE == zipcode) & (LU == lu)) %>% mutate(LOG_TOTAL_VALUE = log(TOTAL_VALUE), LOG_LIVING_AREA = log(LIVING_AREA))
      p <- subdf  %>% ggplot(aes(x = LOG_LIVING_AREA, y = LOG_TOTAL_VALUE, color=factor(YEAR))) + geom_point() 
      p
    }) 
}

# Run the application 
shinyApp(ui = ui, server = server)
