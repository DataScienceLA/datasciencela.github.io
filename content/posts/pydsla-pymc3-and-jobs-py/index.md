---
title: "PyDSLA: PyMC3 and jobs.py"
date: 2017-01-19T21:15:07
lastmod: 2022-10-13T00:02:42
slug: "pydsla-pymc3-and-jobs-py"
authors: ["eduardo"]
categories: ["meetups", "pydsla"]
tags: []
wpID: 731
---

**Update: Video recording of the meet up here:**

{{< youtube-lite id="DZ0Y7fbipXs" unavailable="true" >}}

---

Come to the PyDSLA January Meetup to hear talks about PyMC3 and jobs.py!

[REGISTER HERE](https://www.eventbrite.com/e/pydsla-pymc3-and-jobspy-tickets-31133151093)

For this event we are incredibly fortunate to have two incredibly speakers give really interesting talks.

---

Our first speaker is [Dr. Josiah Carlson](https://www.linkedin.com/in/josiahcarlson). He lives and works in Los Angeles, currently as VP of Technology at OpenMail.

**Title:** jobs.py

**Talk Abstract**

One of the difficulties with distributed concurrency is caused by concurrent data access. While transactional databases in the SQL and NoSQL varieties abound, transactions and ACID compliance may not be enough to prevent data consistency, availability, and deadlock failures in a concurrent environment - even when you are only accessing a single database on a single server

After surveying Luigi, Airflow, and various Jenkins plugins intended to solve this particular problem, we realized that OpenMail needed something that could be used from more than just our ETL flows, and we couldn't spend months rewriting everything to use it. Enter jobs.py, developed to be easily added to an existing Python codebase, meant to handle locking around named "input" and "output" resources with a decorator or context manager.

At the talk, we will be discussing what jobs.py does, why we explicitly limited the scope of jobs.py the way we did, how OpenMail has used it to ensure success in our processes, and how you might want to use jobs.py.

---

Our second speaker is [Dr. Chris Fonnesbeck](http://biostat.mc.vanderbilt.edu/wiki/Main/ChrisFonnesbeck). Chris is an Assistant Professor in the Department of Biostatistics at the Vanderbilt University Medical Center in Nashville, TN. He specializes in computational statistics, Bayesian methods, meta-analysis, and applied decision analysis. Chris started the PyMC project, a package for Bayesian statistical analysis in Python, and continues as a PyMC developer today. He originally hails from Vancouver, BC and received his Ph.D. from the University of Georgia.

**Title**: Building Bayesian Models in Python with PyMC3

**Talk Abstract**

Computationally-intensive statistical algorithms, such as newer gradient-based MCMC methods, reveal computing tradeoffs inherent in making useful statistical software. On one hand, acceptable performance typically requires a compiled language; on the other, the flexibility to easily implement a variety of models, custom statistical distributions and algorithms are best satisfied by high-level scripting languages. We will describe how Python in general and PyMC3 in particular offer statisticians the sweet spot in this tradeoff. PyMC3 includes several newer computational methods for fitting Bayesian models, including Hamiltonian Monte Carlo (HMC) and automatic differentiation variational inference (ADVI). Python's intuitive syntax is helpful for new users, and has allowed developers to keep the PyMC3 code base simple, making it easy to extend the software to meet analytic needs. PyMC3 itself extends Python's powerful "scientific stack" of development tools, which provide automatic differentiation, fast and efficient data structures, parallel processing, and interfaces for describing statistical models.

---

**Timeline**:

- 6:30pm arrival, food/drinks and networking
- 7:15pm introductions, main talks start
- 8:30pm or 9:30 p.m. - networking and conversation
- 10:00pm closing

You must have a confirmed RSVP and please arrive by 7:15pm the latest.

[Please RSVP here on Eventbrite](https://www.eventbrite.com/e/pydsla-pymc3-and-jobspy-tickets-31133151093).\
Venue: Venice Arts, 1702 Lincoln Boulevard\
Thanks OpenMail for being our amazing sponsors!
