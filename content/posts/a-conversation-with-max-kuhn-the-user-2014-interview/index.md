---
title: "A Conversation with Max Kuhn - The useR! 2014 Interview"
date: 2014-08-11T10:02:16
lastmod: 2014-08-25T19:23:29
slug: "a-conversation-with-max-kuhn-the-user-2014-interview"
authors: ["eduardo"]
categories: ["interviews"]
tags: ["r", "user", "caret", "predictive-modeling"]
description: "Max provides some amazing insights into the why and how of caret, an R package he created. Watch him speak on Applied Predictive Modeling!"
wpID: 195
---

#### The Interview

In the video above, Max provides some amazing insights into the why and how of caret, an R package he created. He also discusses his book on [Applied Predictive Modeling](http://appliedpredictivemodeling.com) which he co-authored with Kjell Johnson, including details on how he set out to write the book he wished he would have had. As a special bonus, Max also describes [Quinlan's](http://en.wikipedia.org/wiki/Ross_Quinlan) [C5.0](http://en.wikipedia.org/wiki/Ross_Quinlan#C5.0), an alternate "forest of decision trees" algorithm, the secrets of which were hidden behind commercial licensing for years - and which has recently been ported and made available to the R ecosystem. Whether you are a beginner just getting your feet wet with R and predictive modeling, or a seasoned data scientist, this interview has something for everyone.

#### Expanding Your Superpowers with Caret

“What is your favorite superpower?” is a classic icebreaker, and the answers will tell you quite a lot about the people answering. Someone in the group will immediately claim that the ability to fly is paramount. Someone else invariably brings up invisibility. Super strength, super speed, laser vision, the ability to talk to sea creatures - these are all fine choices. For me, however, the best answer has always been the ability to predict the future. No other superpower seems to compare - if you can predict the future, then you know how a Flying Superhero will attack, and that you’ll need to bring a mirror to battle Laser-Vision Man. If you can predict the future, perhaps you’ll skip out on that whale watching adventure if you know Sea-Creatures Guy has it out for you. Considering the (current) impossibility of choosing one’s superpower, it’s a fun thought exercise but not much else.

In the context of data science, however, there may be a little something to be done about this “predicting the future” thing, and maybe, just maybe, Max Kuhn is the guy to show you how to do it.

> A non-clinical statistician, is kind of exactly what it sounds like. - Max Kuhn

Max is the Director of Nonclinical Statistics at Pfizer, a position that involves supporting a great many scientists with software tools, analysis, and machine learning during the creation and validation of molecules in the pipeline to become potentially life-saving and life-giving medicines. He is also the creator of the caret package for the R language. [caret](http://caret.r-forge.r-project.org) (short for *C*lassification *A*nd *RE*gression *T*raining) is a set of functions which attempt to streamline the process of creating predictive models. Put succintly, the caret package provides the ‘train’ function. This function is your gateway to nearly every awesome machine learning model that can be implemented in R. Want to train a [neural network](http://en.wikipedia.org/wiki/Artificial_neural_network) to predict Species from all other variables in the iris data set?

```
train(Species ~ ., data=iris, method="nnet”)
```

Turns out that a neural network didn’t provide the accuracy you wanted and instead you decide to try out a more powerful machine learning technique, like [random forests](http://en.wikipedia.org/wiki/Random_forest)?

```
train(Species ~ ., data=iris, method="rf")
```

Perhaps you’re willing to trade a little bit of predictive power in exchange for interpretability, in which case you’d switch over to traditional [decision trees](http://en.wikipedia.org/wiki/Decision_tree_learning).

```
train(Species ~ ., data=iris, method="rpart")
```

That’s all it takes to get started. That’s it.

Inside of the train function, Max has taken his combined decades of experience and expertise creating predictive models and has hidden that complexity for the sake of usability. Each method has its own series of smart defaults and behavior, so that even if you only stick to the basics you can still hit the ground running and be productive. However, the caret package contains much, much more than just the train function.

Inside of the package, Max has encoded best-practice approaches for handling those pitfalls that both new and experienced data scientists might face. Perennial questions such as ‘How do you handle unbalanced classes?’ are answered in caret, providing functions to create [balanced data partitions](http://caret.r-forge.r-project.org/splitting.html). How do you approach feature selection? Caret is helpful and provides [recursive feature elimination](http://caret.r-forge.r-project.org/featureselection.html). How do you make sure that scaling/centering/PCA pre-processing are properly handled during your cross-validation steps and that they don’t add bias to your results? Caret [has your back](http://caret.r-forge.r-project.org/preprocess.html). How do you test your newly-trained model on a held-back training set and view the accuracy metrics? Caret has a a [buffet of options](http://caret.r-forge.r-project.org/other.html#test) waiting patiently at your fingertips. Suddenly, you can start to predict the future… and you’re certainly a little closer to having a superpower with caret in your toolbox.
