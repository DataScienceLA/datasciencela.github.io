---
title: "Win Books and T-shirts in Our DataScience.LA Meetup Raffles, Powered by R and dplyr!"
date: 2014-09-02T09:41:54
lastmod: 2014-09-02T09:41:54
slug: "win-books-and-t-shirts-in-our-datascience-la-meetup-raffles-powered-by-r-and-dplyr"
authors: ["szilard"]
categories: ["meetups"]
tags: ["r", "data-science-2", "meetups-2", "dplyr", "raffles"]
description: "To participate in DSLA raffles, sign up for our premium mailing list. Those on the premium list receive priority meetup announcements and important community news!"
wpID: 288
---

We have a few pieces of swag that we are raffling off to the community at our upcoming meetup events. Our stash consists of 25 data-oriented books, primarily from O’Reilly plus 25 T-shirts from useR! 2014 conference and Revolution Analytics (see picture above). Did we get your attention?

In order to participate in the raffles, you will need to [sign up for our premium mailing list](/join-membership/?utm_source=raffle&utm_medium=post-Sep2&utm_campaign=dslaposts). In addition to the raffles, those on the premium mailing list will receive priority announcements for meetups and important community news as it happens, plus much, much more.

Before each meetup (LA R, DataVis or Machine Learning/Data Science), we’ll select the names of that event’s winners and will start calling each name, one-by-one. When your name is called (and you are present at the meetup), you will have your choice of one raffle item (book or T-shirt) until the day’s items have all been claimed. We will have four winners at each meetup, i.e. 2 books and 2 shirts will be given away each time. Are you one of the lucky names who will be called? Read more below to see our algorithm for determining the raffle winners.

The drawing will consist of sampling names from the premium mailing list, however the relative weights (i.e. your chance of winning) will not be equal, but instead a linear decreasing function of your signup time rank so that the first person who signed up will have 3x the chance compared to the last person on the list, using chronological order. As an example, if at the time of a drawing the list has 100 names, #1 gets weight 3.00, #2 gets weight 2.98, and so on continuously decreasing, #100 gets weight 1.00.

To increase the fun and your chances of winning, you can double your relative weight by providing a link to your LinkedIn profile when [you sign up for the premium list](/join-membership/?utm_source=raffle&utm_medium=post-Sep2&utm_campaign=dslaposts) (or later, by updating your preferences if you have already signed up).

With R and dplyr we can do all this with a few lines of code:

```r
library(dplyr)

read.csv("members_export.csv") %>%
  mutate(pcrnk = percent_rank(CONFIRM_TIME), wdbl = ifelse(LinkedIn!="",2,1),
      w = (3-2*pcrnk)*wdbl) %>%
  sample_n(30, weight = w) %>%
  mutate(name = paste(First.Name,Last.Name)) %>% select(name)
```

<small>Source: [gist 7850049](https://gist.github.com/szilard/78500494d7cd422dceda) by szilard</small>

You can see, to **maximize your chances of winning**, sign up to the premium mailing list **as soon as possible** and **provide your LinkedIn profile**. There are over 50 fantastic items waiting for our lucky winners! [Sign up here now and increase your chances today!](/join-membership/?utm_source=raffle&utm_medium=post-Sep2&utm_campaign=dslaposts)
