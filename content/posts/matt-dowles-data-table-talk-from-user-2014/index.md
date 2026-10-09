---
title: "Matt Dowle's data.table Talk from useR! 2014"
date: 2014-08-28T11:04:36
lastmod: 2014-09-01T12:37:03
slug: "matt-dowles-data-table-talk-from-user-2014"
authors: ["eduardo"]
categories: ["user-conference", "sessions"]
tags: ["r", "user", "data-table", "cran", "read-csv"]
description: "Matt Dowle gave a talk at user! 2014 on his data.table R package, including code examples of the fundamental ideas that structured this open-source package."
wpID: 272
---

[Matt Dowle](http://stackoverflow.com/users/403310/matt-dowle) holds a wealth of knowledge and is worth listening to for a variety of reasons. He has worked for some of the world’s largest financial organizations, holding positions at the focal point between money and data. He has been programming in R for well over a decade. He has lived the open source mantra, by not only consuming open source software but also releasing his own community contributions to CRAN. On top of those accomplishments, he’s also quite funny and spins a heck of a good yarn.

At [useR! 2014](http://user2014.stat.ucla.edu) Matt Dowle gave a presentation on his [data.table](http://cran.r-project.org/web/packages/data.table/index.html) package, including the history and context behind its development. For the uninitiated, data.table provides extensions of the R data.frame object which allow fast aggregation of large data (e.g. 100GB in RAM), fast ordered joins, fast add/modify/delete of columns by group using no copies at all, list columns and a fast file reading.

However, to say that Matt Dowle’s presentation was **only** about data.table is disingenuous. Matt’s presentation is a fantastic autobiographical snippet of how one practitioner moved from commercial tools for data science, where he was at the mercy of commercial entities for support and a blessing, towards open source tools where he has been in control of his destiny. Or, as he puts it:

> "... if I don't know how to fix it, I can hire somebody else to fix it for me.”

In this talk he gives examples of how he started out as a new user with preconceptions about how the world should work, then quickly learned that the tools simply didn’t work the way he wanted. With open source software, however, he could bend the tools to his will. He also discusses his choice to distribute his R package under an open source license, feeling a strong responsibility to do so as both a user and developer.

Matt provides a number of great code examples which illuminate the fundamental ideas that structured the data.table package, in addition to benchmark examples of how operations which previously took hours to run instead complete in seconds with this package. Finally, he covers one of the great bugaboos for new (and experienced) R programmers: the dismal speed of importing a CSV file. He also discusses the incantations we are encouraged to learn in order to combat the issue, and his alternate implementation ([fread](http://www.inside-r.org/packages/cran/data.table/docs/fread), or ‘fast/friendly/file or finagle read’) which outpaces even the most elaborately crafted read.csv parameters. His slides are also available for download [here](http://user2014.stat.ucla.edu/files/talk_Matt.pdf). Enjoy!

{{< youtube-lite id="qLrdYhizEMg" title="Matt Dowle's \"data.table\" talk at useR 2014" >}}
