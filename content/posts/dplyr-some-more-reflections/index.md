---
title: "dplyr - some more reflections"
date: 2014-12-04T09:30:00
lastmod: 2014-12-03T10:25:55
slug: "dplyr-some-more-reflections"
authors: ["szilard"]
categories: ["r"]
tags: ["r", "data-science-2", "dplyr", "hadleyverse"]
archivedComments: 2
showComments: true
wpID: 461
---

Yesterday, I published a post [here](/dplyr-and-a-very-basic-benchmark/) on DataScience.LA with a simple/basic benchmark for dplyr. It was the main part of a short talk at our last Los Angeles R meetup. Below, I continue my thoughts with some reflections on dplyr's API and philosophy, AKA the other part of my talk.

I think of dplyr as an awesome API for data munging tabular data in R. It implements a "grammar of data manipulation" similar in impact to the grammar of graphics of ggplot2. It can be considered a mini-DSL. (If you'd like to get more insights about [Hadley](http://had.co.nz/)'s approach and emphasis on designing good APIs, check out [his interview with DataScience.LA](/a-conversation-with-hadley-wickham-the-user-2014-interview/)). The strength of the syntax comes from both the very well-thought building blocks (like select, filter, group by etc.) and the %&gt;% (pipe) operator that increases enormously the readability of your code.

What strikes me is how using dplyr changed my views and understanding about SQL. In dplyr the building blocks are simple but powerful primitives that do one thing and do it well, similar to the Unix philosophy. (The analogy happens to go even further with the use of pipes to combine the elements.) SQL is more convoluted, but in essence it provides the same data transformations for tabular data. I've come to see SQL as not quite so dumb after all, although it's still not that nice from an API point of view. (Also worth mentioning that in order to scale out to larger datasets stored in databases, dplyr generates SQL under the hood.)

Another point I'd like to make is that despite its awesomeness, dplyr does not solve all your data manipulation problems. It does provide, however, a very efficient solution to say 80% of them, thus increasing your productivity by leaps and bounds. In fact, somewhat surprisingly, by "restricting" you to think in these simple primitives, it helps you solve problems faster - this might sound counterintuitive at first, but trust me and give it a try.

Besides the awesome API, dplyr is also fast! [Romain François](https://twitter.com/romain_francois) re-wrote the critical parts using Rcpp/C++ and now dplyr is way faster than base R, plyr or sqldf and it is approaching data.table's speed. Note that all of these tools are single threaded for now, yet manipulating large datasets with millions of rows takes subseconds or seconds at most. Further speed increases - possibly relevant for even larger datasets - could be achieved with parallelization, something that we've heard the developers are thinking about.

One final feature to mention here is the ability to work with several "data sources" (data.frames, data.tables, several database backends) that can be manipulated using the same API. For the databases (e.g. SQLite, MySQL, PostgreSQL etc.) dplyr generates SQL that is executed in the database, as previously mentioned.

For the past decade or so since I have been using R, my workflow has been (1) write some SQL to extract the data from the database (while also reducing the data size by filtering, aggregating, etc.), (2) get that data into R via the corresponding DBI connector and (3) perform data munging, data visualization and modeling in R. (Note that the SQL was always embedded in the R code and called from there, so this did not fragment the workflow.) In recent years, all three steps fit nicely in a Rmarkdown file processed by knitr at a push of a button in RStudio.

What I've been experimenting with lately instead is to grab all the data into R - contrary to the myth, the R database connectors are blazing fast and can read for example 10GB of data in a few minutes. From there I can use dplyr for data munging and the rest of my workflow remains the same. (It remains to be seen how this works out with large datasets.)

All these changes have been made possible lately by several factors: (1) large amounts of RAM (~100GB) are now cheap, (2) for many well-established companies datasets - contrary to the big data hype - are not exploding (in fact, affordable RAM has increased faster than most datasets), (3) R itself has become way more memory efficient (Did you know that since R 3.1 if you create a new column in a data.frame, R is not going to make copies of all the other columns? This makes some operations 100x faster and with less memory overhead) and (4) packages like dplyr or data.table provide blazing fast operations (and are much more memory efficient).

With all this it is no doubt that dplyr is the most awesome in-memory data manipulation tool on the planet. Or Universe. Go, Hadleyverse!

(If you did not catch it yesterday, check out my [post with the benchmark](/dplyr-and-a-very-basic-benchmark/).)
