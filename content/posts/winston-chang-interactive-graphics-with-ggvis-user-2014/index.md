---
title: "Winston Chang's \"Interactive Graphics with ggvis\" at useR! 2014 "
date: 2014-08-14T10:15:15
lastmod: 2014-08-25T19:15:49
slug: "winston-chang-interactive-graphics-with-ggvis-user-2014"
authors: ["eduardo"]
categories: ["sessions"]
tags: ["r", "ggplot2", "ggvis", "rstudio"]
description: "At this useR! 2014 talk, Winston introduces ggvis, lays out the fundamental architecture of this R package, and discusses reactive architectures."
archivedComments: 2
showComments: true
wpID: 214
---

Winston Chang's "Interactive Graphics with ggvis" talk at useR! 2014 was in many ways a watershed moment for the the data science community, as the future directions of rich data visualization for analytics, communication, and the web were revealed. In this talk, Winston introduces the viewer to [ggvis](http://blog.rstudio.org/2014/06/23/introducing-ggvis/), lays out the fundamental architecture, and provides an overview of reactive architectures.

> The commonality between science and art is in trying to see profoundly - to develop strategies of seeing and showing.
>
> -Edward Tufte

Data Science does not happen solely in the large matrices hidden inside the dark confines of servers, it happens through the practitioner’s senses and in their mind. A practicing data scientist collects data from any number of data sources, forms theories about its underlying structure, and proceeds to (attempt to) discover an inkling of the secrets contained therein. Visualization is the tool most often used to accomplish this process in data science, and it’s not hard to understand why. When you consider the senses available to us and how long human beings have spent desperately harnessing scarce resources to sustain ourselves, it makes even more sense.

The most critical tool our ancient ancestors used was not the sense of touch or taste, but instead was our vision. Through thousands of years of evolution, humans developed the ability to know which red berry was sweet, and which was toxic. We developed the ability to spot out of the corner of our eye the slight rustling of some leaves, which betrayed a fawn and our next meal. We depend on these senses to let us know when something is right, when something is wrong, and when something is dangerous. Human are born explorers, and we hone the sharpest of our tools towards that goal. We see new things, new connections, and infer what we can’t directly see from what we can see in order to predict the unknown around us.

> Intuition fails in high dimensions
>
> -Unknown

The field of data visualization piggybacks on this evolutionary masterpiece of vision-driven cognition. This understanding allows humans to use intuition by mapping from many-dimensional data down to the dimensions humans work well in - like the two dimensional plane of your monitor. For many years R has contained *the* premiere visualization system as a “baked in” offering. Hadley Wickham’s [ggplot2 library](http://ggplot2.org/), an implementation of [Leland Wilkinson](http://www.cs.uic.edu/~wilkinson/)’s “The Grammar of Graphics”, has been cited repeatedly as one of R’s competitive advantages in the data science toolbox. However, ggplot2 was not designed for the modern computing age where the deployment target for all non-trivial development is the web browser.

The ggvis package provides a modern re-conceptualization of many of the core concepts of ggplot2 and reframes them in the context of a reactive framework. Whereas ggplot2 created beautiful visualizations which were static and framed in the moment of the creators mind, ggvis allows the creator to assemble a pipeline of ideas, package them, and present them to the consumer. With ggvis, the reader is empowered through interactivity and responsiveness through the data to gain new perspectives. We hope this video encourages you to develop new and innovative visualizations, and empowers your users to interact with data in new ways you've never before thought possible!

UPDATE: Slides and code for this presentation are available [here](http://bit.ly/1qgE8xU).
