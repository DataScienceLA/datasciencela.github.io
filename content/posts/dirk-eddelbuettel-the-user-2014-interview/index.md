---
title: "Dirk Eddelbuettel, the useR! 2014 Interview"
date: 2014-09-22T10:35:04
lastmod: 2014-09-22T10:35:04
slug: "dirk-eddelbuettel-the-user-2014-interview"
authors: ["eduardo"]
categories: ["user-conference", "interviews"]
tags: ["r", "finance", "rcpp", "dirk", "hpc"]
wpID: 349
---

First things first, Dirk Eddelbuettel was recently [named ordinary](https://stat.ethz.ch/pipermail/r-announce/2014/000577.html). This seems contradictory, since Dirk is a known [HPC](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0CB4QFjAA&url=http%3A%2F%2Fdirk.eddelbuettel.com%2Fpapers%2FuseR2010hpcTutorial.pdf&ei=PlogVL_oNYXEggSZqYHYAQ&usg=AFQjCNFViWLjHYMvJLSbxS1Sn31cFbwZSw&sig2=LWc4tZf_hrUp6yzHKtcm0Q&bvm=bv.75775273,d.eXY) expert, an organizer of the [R in Finance](http://www.rinfinance.com/) conference, the creator of [Rcpp](http://cran.r-project.org/web/packages/Rcpp/index.html), and a [Debian](http://dirk.eddelbuettel.com/debian.html) contributor. These are only a few of the many accolades bestowed upon Dirk without even a hint of puffery. And yet, Dirk Eddelbuettel is considered ordinary. What makes Dirk ordinary? It should be mentioned that to the Vienna-based nonprofit that provides R’s leadership, the [R Foundation for Statistical Computing](http://www.r-project.org/foundation/main.html), ‘ordinary’ means something quite different to the lay person. Ordinary members provide guidance and direction for the R Project for Statistical Computing. It’s hard to imagine someone more qualified than Dirk for this task.

A longtime R user, Dirk’s professional life is in finance as a self-described [quant](http://en.wikipedia.org/wiki/Quantitative_analyst) (one of the ‘[Rocket Scientists of Wall Street](http://www.investopedia.com/articles/financialcareers/08/quants-quantitative-analyst.asp)’). Dirk has [worked](https://www.linkedin.com/in/dirkeddelbuettel) for some of the largest financial organizations in the world, and has [open sourced](http://dirk.eddelbuettel.com/code/) packages which allow for tasks ranging from [vanilla options pricing](http://en.wikipedia.org/wiki/Option_(finance)#Option_styles) to [discounted cash flow analysis](http://en.wikipedia.org/wiki/Discounted_cash_flow). Even though the world of finance is a “massive net importer” of open source tools, he has succeeded in providing finance packages for the open source community. In addition to these contributions, he has also provided the larger R community with the infinitely useful Rcpp package.

[Rcpp](http://www.rcpp.org/) is the most widely used language extension for R, and this package provides a novel and seamless method of integrating high performance C++ code with R without requiring the usual extension [incantations](http://cran.r-project.org/doc/manuals/R-exts.html). Dirk’s book, [*Seamless R and C++ Integration with Rcpp*](http://www.amazon.com/Seamless-Integration-Rcpp-Dirk-Eddelbuettel/dp/1461468671/ref=sr_1_sc_1?ie=UTF8&qid=1411406675&sr=8-1-spell&keywords=rcpp) (Springer, 2013) makes it surprisingly easy to pick up the Rcpp basics in an afternoon. For example, I recently found myself facing a CPU-bound data manipulation task and was able to convert the code from R to Inline C++ using Rcpp - and my code received a [26x speedup](http://earino.wordpress.com/2014/01/05/speeding-up-r-code/) for a few hours of work invested.

It’s easy to see why, with all of these contributions, the R Foundation would find Dirk ordinary. I was incredibly fortunate at useR! 2014 to sit down with Dirk and have a long conversation about many of these ordinary topics, the video of which is included here. Enjoy!

{{< youtube-lite id="OcxynQbKk44" title="Dirk Eddelbuettel - Interview by DataScience.LA at useR 2014" >}}
