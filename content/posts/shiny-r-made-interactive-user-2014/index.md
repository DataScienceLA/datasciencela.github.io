---
title: "Shiny: R made interactive @ useR! 2014"
date: 2014-09-04T11:13:51
lastmod: 2014-09-04T11:13:51
slug: "shiny-r-made-interactive-user-2014"
authors: ["eduardo"]
categories: ["user-conference", "sessions"]
tags: ["r", "user", "ggvis", "rstudio", "visualization", "shiny", "web", "interfaces"]
wpID: 309
---

At useR! 2014, one of the most anticipated presentations was Joe Cheng’s [Shiny: R made interactive](http://user2014.stat.ucla.edu/abstracts/talks/86_Cheng.pdf). It was but one of the of a fantastic series of talks by RStudio representatives; check out Winston Chang’s [ggvis: Interactive graphics in R](/winston-chang-interactive-graphics-with-ggvis-user-2014/) for another great talk. [Shiny](http://shiny.rstudio.com/) begins with your R code and ends with the customer’s view: an interactive, browser-accessible application. This enables you to place a great deal of power into your users’ hands to customize their view and provides a variety of new and innovative ways to interact with the data, such as by tuning parameters and focusing on sub-populations. Essentially, Shiny functions by allowing you to “wire up” up a reactive application, greatly speeding up the development of a data and analysis based web app.

Shiny comes out of the box with a number of standard industry UI widgets such as date inputs, file inputs, sliders, buttons - the standard widget toolbox. Shiny also leverages a simple panel-based layout manager which, in concert with the widgets, allows for a fluid development experience.

#### Video Highlights

If you’re interested in bypassing Joe Cheng’s fantastic explanation and you want to cut right to his first demo, he presents a web application for k-means clustering on the iris data set:

{{< youtube-lite id="zBazpYEz2Mg" title="Joe Cheng's rShiny at useR! 2014" start="4" >}}

Joe’s next demo involves a slick mapping component. Here you begin to see how Shiny apps have the potential to leverage intriguing data sources and provide first rate visualizations beginning only with ZIP codes and a limited amount of R code:

{{< youtube-lite id="zBazpYEz2Mg" title="Joe Cheng's rShiny at useR! 2014" start="8" >}}

He then shows an amazing example of what an R developer with no previous web development experience can build using Shiny.

{{< youtube-lite id="zBazpYEz2Mg" title="Joe Cheng's rShiny at useR! 2014" start="13" >}}

For his final demo, Joe embeds Shiny interactive documents using R markdown and combines them with [Yihui Xie’s knitR](/yihui-xie-the-user-2014-interview/). This is demoed in the video below with an application which parses the logs for RStudio’s CRAN mirror and visualizes package download trends.

{{< youtube-lite id="zBazpYEz2Mg" title="Joe Cheng's rShiny at useR! 2014" start="15" >}}

Shiny is a fun and easy way to widen the audience interacting with your data analyses. It leverages fantastic modern programming paradigms to provide a system with sane defaults and powerful components to interface the web with R. Enjoy!
