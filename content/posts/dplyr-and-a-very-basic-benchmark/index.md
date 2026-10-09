---
title: "dplyr and a very basic benchmark"
date: 2014-12-03T09:35:05
lastmod: 2014-12-02T17:44:39
slug: "dplyr-and-a-very-basic-benchmark"
authors: ["szilard"]
categories: ["r"]
tags: ["r", "data-science-2", "data-table", "dplyr", "pandas"]
archivedComments: 6
showComments: true
wpID: 457
---

Earlier this month I gave a short talk about dplyr at the Los Angeles R meetup. It was one of the 5 talks about the useR! 2014 conference, and you can see the summaries and slides from the other 4 talks [here](/la-r-meetup-summary-highlights-from-user-2014-part-2/).

Of course, by now we hope everyone using R has heard of [dplyr](https://github.com/hadley/dplyr). So why the h@#\* would we have another talk about dplyr? And why another blog post? First, dplyr is that awesome! Second, I was suspecting that despite this awesomeness, many people are still not using this tool. Indeed, a quick show of hands at last month's meetup revealed that while over 90% of those present have heard about dplyr, only about 20% are using it. Finally, most talks and blog posts (see e.g. many good ones on [r-bloggers](http://www.r-bloggers.com/?s=dplyr)) describe how to use it or reflect on how awesome the API is (which cannot be reiterated enough!), but only a few posts speak about performance. It so happened that a week before the meetup I was exploring dplyr and came up with a very basic/simple benchmark that I thought worthwhile to share in both a talk and in this post.

In fact, in the first half of my talk I presented a short overview of dplyr and reflected a bit on its features and philosophy. (Note: I'll save this part for a subsequent blog post here on DataScience.LA.) As for the benchmark, my main goal was to get an idea about the performance of dplyr's building blocks (filter, aggregate, join etc.) for largish datasets (and with as little work to do as possible).

For a few values of size parameters *n* and *m* (*n* = 10 and 100 million, *m* = 100, 1000 and 1 million, respectively) I generated data.frames with *n* rows and 2 columns: *x* integers between 1 and *m,* and *y* random numbers (the size of the datasets in RAM is ~100MB and ~1GB, respectively). A second data.frame of size *m* is generated for benchmarking joins.

The basic tabular operations (filter, aggregate, join etc.) were applied using base R, dplyr (with data.frame and data.table backends, respectively) and standard data.table (with and without key).

I acknowledge this is just a simple/basic/limited/incomplete benchmark, one could do more with various data types (e.g. character), several grouping variables (*x*1,*x*2,...), more values for size parameters (*n*,*m*), different distributions of values in the data.frames etc. (or with real-world datasets). In fact Matt Dowle has published a more complete benchmark for group by operations [here](https://github.com/Rdatatable/data.table/wiki/Benchmarks-%3A-Grouping), and Brodie Gaslam has also done previously some simple benchmarking of group by, mutate and filter (but not join!) [here](http://www.brodieg.com/?p=7).

The full R code and results are available for your own exploration on [github](https://github.com/szilard/benchm-dplyr-dt). Latest CRAN versions of R, dplyr and data.table at the time of the study have been used (R 3.1.1, dplyr 0.3.0.2 and data.table 1.9.4). The main results (relative run-times, smaller is better) are summarized below:

|  | base | dplyr-df | dplyr-dt | dplyr-dt-k | dt | dt-k |
| --- | --- | --- | --- | --- | --- | --- |
| Filter | 2 | 1 | 1 | 1 | 1 | 1 |
| Sort | 30-60 | 20-30 | 1.5-3 | [1] | 1.5-3 | [1] |
| New column | 1 | 1 | (6) 4 | (6) 4 | (4) 1 | (4) 1 |
| Aggregation | 8-100 | 4-30 | 4-6 | 1.5 | 1.5-5 | 1 |
| Join | &gt;100 | 4-15 | 4-6 | 1.5-2.5 | - | 1 |

(Notes: the larger numbers usually appear for larger *m*, i.e. for more (and smaller) groups; the fastest runtimes are usually a few seconds, pretty good for 10-100 million row datasets).

Some comments:

(1) base R is slow for aggregates (base::tapply) and hopelessly slow for (large) joins (base::merge).

(2) Having a key for data.table or dplyr with data.table source (i.e. having data pre-sorted in place) obviously helps with aggregation and joins (and analyzing sorting in this case is a bit pointless).

(3) dplyr with data.table backend/source is almost as fast as plain data.table (because in this case dplyr acts as a wrapper and mainly calls data.table functions behind the scenes) - so, you can kinda have both: dplyr API (my personal preference) and speed

(4) Sorting in dplyr is slower on data.frames, but [Hadley says](https://twitter.com/hadleywickham/status/527162872200065025) it can be made faster.

(5) The main reason why dplyr (with data.frame) is slower than data.table for aggregates and joins is explained [here](https://gist.github.com/arunsrinivasan/db6e1ce05227f120a2c9) (data.table uses radix sort and binary search vs dplyr using hashing for joins).

(6) While on my first run of the benchmark data.table was surprisingly 4x slower in defining a new column relative to either base R or dplyr (see numbers in parenthesis in the table above), the data.table developers have made some [changes](https://github.com/Rdatatable/data.table/issues/921) and now it's all square (in the development version of data.table on github for now, and in the next CRAN release in the future).

(7) One unrelated thing I learned with this little project is that R 3.1 (released earlier this year) has made a change that made some data.frame manipulations 100-1000x faster (see [here](http://stackoverflow.com/questions/7029944/when-should-i-use-the-operator-in-data-table/7030140#7030140) for how slow it was, and adding a new column to a data.frame in base R now is on par with data.table as you can see in the table above).

(8) The developers of both packages (Hadley & Romain for dplyr and Matt & Arun for data.table) have done outstanding jobs and are constantly improving with features and speed (and they are very responsive to questions/suggestions).

Since most data scientists are using R or Python as their primary tool (see the [results](/data-science-toolbox-survey-results-surprise-r-and-python-win/) of our survey from the Los Angeles Data Science meetup), I also created a similar benchmark for [pandas](http://pandas.pydata.org/) (the main data munging tool in the Python world) vs R's data.table. It looks like pandas (0.15.1) is slower than data.table for both aggregates and joins (contrary to [measurements and claims](https://stackoverflow.com/questions/8991709/why-are-pandas-merges-in-python-faster-than-data-table-merges-in-r) from almost 3 years ago and which cannot be verified in absence of source code publicly available). For example for *n* = 10 million and *m* = 1 million, runtimes (in seconds) are below (and full code and results are in this [IPython notebook](http://nbviewer.ipython.org/github/szilard/benchm-dplyr-dt/blob/master/bm-pd.ipynb)):

|  | pandas | data.table |
| --- | --- | --- |
| Aggregate | 1.5 | 1 |
| Aggregate (keys/pre-sorted) | 0.4 | 0.2 |
| Join | 5.9 | - |
| Join (keys/pre-sorted) | 2.1 | 0.5 |
| Creating keys (sort) | 3.7 | 0.7 |

(Note: the first line is similar to Matt Dowle's benchmark for group by without keys published [here](https://github.com/Rdatatable/data.table/wiki/Benchmarks-:-Grouping)).

In conclusion, dplyr is pretty fast (way faster than base R or plyr) but data.table is somewhat faster especially for very large datasets and a large number of groups. For datasets under a million rows operations on dplyr (or data.table) are subseconds and the speed difference does not really matter. For larger datasets one can choose dplyr with data.table as a backend, for example. For even larger datasets, or for those preferring the data.table syntax, data.table might be the choice. Either way, R is the best tool for data munging tabular data with millions of rows.

Stay tuned for some reflections on dplyr's API and philosophy later this week, with a new post published here soon!
