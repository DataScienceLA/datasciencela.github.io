---
title: "2 talks: GBM Benchmark In-Depth | The State of XGBoost"
date: 2020-10-15T23:31:01
lastmod: 2022-10-13T00:02:41
slug: "2-talks-gbm-benchmark-in-depth-the-state-of-xgboost"
authors: ["szilard"]
categories: ["machine-learning-data-science"]
tags: []
wpID: 769
---

**Update: Video recordings:**

Talk #1 (Szilard Pafka: GBM Benchmarks)

{{< youtube-lite id="ecUUUdisKAc" title="LA Data Science Meetup, Nov. 10, 2020 - Talk #1 - Szilard Pafka: GBM Benchmarks" >}}

Slides [here](http://docs.google.com/presentation/d/1hRJveGyFArYzfpPSD9XeOi6oCHRjrj12yx4MDIrtPZg/edit)

Talk #2 (Hyunsu Cho: The State of XGBoost)

{{< youtube-lite id="yJJlhdns54A" title="LA Data Science Meetup, Nov. 10, 2020 - Talk #2 - Hyunsu Cho: The State of XGBoost" >}}

Slides: [here](https://drive.google.com/file/d/1YD8s6x0ZR3ON99UbiZpPM5OPjtQqVyH3/view?usp=sharing)

---

**In this first ONLINE event we'll have 2 fantastic talks from 2 gradient boosting experts/open source contributors.** Szilard Pafka is the author of benchm-ml and GBM-perf benchmarks and in this talk he will go in-depth like never before. Hyunsu Cho is the lead maintainer of XGBoost and he will give us a firsthand on the project's history, major milestones and its roadmap for the future.

**And the Winner Is...: Insights from a Gradient Boosting (GBM) Benchmark**

**Szilard Pafka, PhD\
Chief Scientist, Epoch**

With all the hype about deep learning and "AI", it is not well publicized that for structured/tabular data widely encountered in business applications it is actually another machine learning algorithm, the gradient boosting machine (GBM) that most often achieves the highest accuracy in supervised learning/prediction tasks. In this talk we'll review some of the main open source GBM implementations such as xgboost, h2o, lightgbm, catboost, Spark MLlib and we'll discuss some of their main performance characteristics. We'll go more in-depth vs all my previous talks on the topic, and we'll discuss in details training speed, memory footprint, scaling to multiple CPU cores, performance degradation on hyperthreaded cores and multi-socket CPUs, performance on latest Intel and AMD CPUs, GPU implementations, GPU utilization patterns etc. and also several 2020 recent updates such as improved multi-core performance in xgboost and speedups in catboost.

Szilard studied Physics in the 90s and obtained a PhD by using statistical methods to analyze the risk of financial portfolios. He worked in finance, then more than a decade ago moved to become the Chief Scientist of a tech company in Santa Monica, California doing "everything data". He is the founder/organizer of several meetups in the Los Angeles area (R, data science etc) and the data science community website datascience.la. He is the author of a well-known machine learning benchmark on github (1000+ stars), a frequent speaker at conferences (keynote/invited at KDD, R-finance, Crunch, eRum etc.), and he has developed and taught graduate data science courses at two universities (UCLA and CEU in Europe).

**The State of XGBoost: history and community overview**

**Hyunsu Cho\
Senior Systems Software Engineer, NVIDIA**

What used to be a research prototype to process several GBs of data on a single workstation, XGBoost has now grown to be a production-quality software that can process hundreds of GBs of data in a cluster. In the last few years, XGBoost has added multiple major features, such as support for NVIDIA GPUs as a hardware accelerator and distributed computing platforms including Apache Spark and Dask. This talk will provide a short tour of the history of XGBoost, recognizing its major milestones. We will particularly pay attention to how XGBoost has integrated with major data science packages and frameworks, such as scikit-learn, R, Apache Spark, Dask, and RAPIDS AI. We will also share current efforts to grow the community, to put the open source project on a sustainable path. Finally, we will share the future roadmap of the project and list of wish items.

After receiving Masters degree from University of Washington, Hyunsu went to join Amazon Web Services (AWS) to develop AI as a service. In April 2020, Hyunsu joined the RAPIDS AI team in NVIDIA. He is now focusing on improving end-to-end data science pipelines using NVIDIA GPUs. Hyunsu has been in charge of maintaining the XGBoost project since November 2017. In addition to triaging bug reports and reviewing pull requests, Hyunsu also maintains the test farm for continuous integration (CI), which ensures that all incoming pull requests meet the quality bar.

**Date/Time:** November 10, 2020, 10am Pacific\
**Location: ONLINE (zoom)**\
**RSVP and zoom link:** <https://www.meetup.com/Los-Angeles-Machine-Learning-Data-Science/events/273958512/>\
**NOTE:** The event will be limited to the first 100 attendees joining the zoom meeting.
