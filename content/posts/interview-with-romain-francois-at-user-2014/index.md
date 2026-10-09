---
title: "Interview with Romain Francois at useR! 2014"
date: 2014-09-15T22:17:41
lastmod: 2014-09-15T22:17:41
slug: "interview-with-romain-francois-at-user-2014"
authors: ["eduardo"]
categories: ["user-conference", "interviews"]
tags: ["r", "cran", "rcpp", "rcpp11", "romain-francois"]
wpID: 342
---

At the [useR! 2014](http://user2014.stat.ucla.edu/) conference, without a doubt one of the overriding themes was R’s history, legacy, and future as an [interface](/john-chambers-user-2014-keynote/) into the “best of the best” algorithms which were available. [Romain Francois](http://blog.r-enthusiasts.com/)’ package, [Rcpp11](http://cran.r-project.org/web/packages/Rcpp11/index.html), is very much the spirit and the letter of this ethos and telos of R as an interface. This package is a reimplementation of [Dirk Eddelbuettel's](http://dirk.eddelbuettel.com/) [Rcpp](http://cran.r-project.org/web/packages/Rcpp/index.html) package with an emphasis on [C++ 11](http://en.wikipedia.org/wiki/C%2B%2B11)’s features. Whether it’s an R user hitting performance limitations, or someone trying to integrate a C/C++ library into their analysis, Romain’s tools are there to help.

An R programmer for over a decade, Romain started as an “R first” developer, only later moving to more traditional software engineering languages. In this interview, Romain and I discuss a wide range of topics, from R’s history as an interface for algorithms, through Romain’s experiences in HPC and his collaboration with Hadley Wickham on dplyr. Romain also shares a little bit about his other passion, stand-up comedy.

#### VIDEO BREAKDOWN

Please click [here](https://www.youtube.com/watch?v=AuYZZGbPKZU) to see the video directly on YouTube. Or if you prefer, subscribe to our [podcast](/announcing-the-dsla-podcast/) to get the audio!

#### An Overview of Rcpp11

At useR! 2014, Romain [presented](https://www.dropbox.com/sh/geljkmz4vvmf8a5/AAAQY7asXnP3dzZFyuljfxS6a) on Rcpp11, (from his abstract):

> Rcpp11 is a complete rewrite of the Rcpp library, it takes advantage of C++11 to make the user experience of combining R and C++ even better and more future proof. Rcpp11 was also an opportunity to review the code base of Rcpp, identify mistakes and fix them. Rcpp11 is a smaller, cleaner implementation of the Rcpp api, written with C++11 in mind.

He presents an introduction to Rcpp here, in the video below.

{{< youtube-lite id="AuYZZGbPKZU" title="Romain Francois - Interview by DataScience.LA at useR 2014" start="2" >}}

#### Collaboration with Hadley Wickham

I have already mentioned using [dplyr](/a-conversation-with-hadley-wickham-the-user-2014-interview/) as my greatest productivity enhancement of 2014. While most people would associate Hadley with dplyr, the pacakge has been the result of a fruitful collaboration between the two of them. Here, Romain discusses what it’s like collaborating with a community leader on such a useful package.

{{< youtube-lite id="AuYZZGbPKZU" title="Romain Francois - Interview by DataScience.LA at useR 2014" start="9" >}}

#### Advice to New Developers

Romain provides some targeted and valuable advice to new users and developers starting their journey with R. While discussing the many twists and turns of a programmers journey, he highlights one singular action to both bolster your confidence and increase your understanding of the larger R ecosystem.

{{< youtube-lite id="AuYZZGbPKZU" title="Romain Francois - Interview by DataScience.LA at useR 2014" start="15" >}}

#### Stand-up Comedy

Romain was kind enough to provide us with a bit of insight into his parellel existence. When he’s isn’t touring around the world giving tutorials and talks about R/HPC, he is also a stand-up comic. Tune in below to hear his insights on how comedy is suited for him and what it allows him to do:

{{< youtube-lite id="AuYZZGbPKZU" title="Romain Francois - Interview by DataScience.LA at useR 2014" start="17" >}}

#### Conclusion

Romain’s technological contributions to our field are many, and his depth of knowledge in how to integrate R with external packages and languages is among the very best. A few weeks ago, Romain found himself speaking to the Budapest R Meetup run by friend of DataScience.LA, [Gergely Daróczy](https://www.linkedin.com/in/daroczig). At this meetup, Romain gave an hour-long presentation (in English) with a great deal of detailed information about Rcpp11. After you’ve checked out our interview above, please make sure to catch his presentation, available [here](http://r-projekt.hu/2014/09/06/romain-francois-r-es-c-eloadasa).
