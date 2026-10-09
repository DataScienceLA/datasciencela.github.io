---
title: "Overview of H2O's GBM implementation"
date: 2021-05-10T09:13:53
lastmod: 2022-10-13T00:02:41
slug: "overview-of-h2os-gbm-implementation"
authors: ["szilard"]
categories: []
tags: []
wpID: 798
---

**Update: Video Recording:**

{{< youtube-lite id="sNTlt2SMwkU" title="LA Data Science Meetup, June 8, 2021 - Michal Kurka: H2O's GBM" >}}

**Slides: [here](https://github.com/h2oai/h2o-meetups/blob/master/2021_06_08_GBM_LA/gbm-la-meetup.pdf)**

After our last 3 meetups with core developers of XGBoost, LightGBM and Catboost, respectively, it is now H2O's turn (with H2O's Director of Engineering speaking)! Just as the last few times, we'll fit in a 1-hour slot, talk 35 minutes + Q&A 20 minutes (10:00-10:55am Pacific Time).

**Overview of H2O GBM implementation**

**by Michal Kurka**

H2O started its mission to let data scientists train their models on datasets of any size in 2011 with just a few machine learning algorithms, Gradient Boosting Machine (GBM) being one of them. To this day H2O GBM is one of our most popular and full featured algorithms in what grew out to be a well-rounded and diverse machine learning framework. In this talk we will briefly introduce H2O’s ML framework and discuss how it differs from its competitors. Then we will dive into the internals and discover how GBM implementation leverages H2O's MapReduce framework to train models fast in both single-node and distributed environments. Furthermore, we will take a look at the ecosystem that we built to support data scientists to inspect, debug and learn from their models (tree visualization, Shapley, feature interactions, …). We will touch on some of the more nuanced features of H2O GBM - applying monotonic constraints and implementing a custom loss function. We will explore options H2O provides for deploying models in production. Finally, we will take a look at our roadmap and discuss how users can contribute to make H2O GBM better.

**Speaker Bio:**

Michal holds a Masters degree in Mathematical Optimization. For the last 10 years he was involved in implementing scalable ML algos using frameworks like Hadoop MapReduce, Spark and H2O. As a Director of Engineering in H2O.ai he is responsible for development of H2O's open source machine learning framework H2O-3. He is passionate about performance of distributed systems and he contributed to performance improvements of the overall platform as well as GBM specifically. He implemented a variety of GBM features including TreeSHAP and monotonicity constraints. He also maintains H2O’s implementation of PSVM, CoxPH, word2vec and was responsible for H2O's XGBoost integration.

**Date/Time:** Tuesday, June 8, 10:00-10:55am Pacific Time\
**Venue:**online (zoom)\
**RSVP:** [here on meetup](https://www.meetup.com/Los-Angeles-Deep-Learning-Big-Data-Science-AI/events/278096842/)\
**Note:**The zoom link will be posted in comments on meetup (link above) at 9:55am and due to our zoom’s 100-attendee limit, the first 100 people will be able to join the zoom call.
