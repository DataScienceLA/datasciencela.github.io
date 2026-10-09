---
title: "Packrat presentation at useR! 2014"
date: 2014-09-26T11:25:44
lastmod: 2014-09-26T11:25:44
slug: "packrat-presentation-at-user-2014"
authors: ["eduardo"]
categories: ["user-conference", "sessions"]
tags: ["r", "rstudio", "enterprise", "reproducibility", "deployment", "packrat", "jj-allaire"]
description: "Packrat is a client-side solution allowing a project to manage dependencies within its own directory tree. Watch a presentation on the benefits of Packrat recorded at UseR! 2014."
wpID: 359
---

There comes a time in a software toolchain’s lifecycle where the focus shifts from developer productivity and preference to the ability to deploy solutions in production which coexist gracefully in the enterprise. [Configuration management](http://en.wikipedia.org/wiki/Configuration_management) and dependency management are two of the first points of friction in this transition, as the free-wheeling methods preferred by developers are at odds with the structured methods and isolation desired by administrators, who serve as gatekeepers to enterprise deployment. R is currently at this very point in the transition, in the midst of transformation from a language and environment used primarily in academic research to its growing place in the enterprise. At [useR! 2014](http://user2014.stat.ucla.edu/) there were a [series](http://user2014.stat.ucla.edu/abstracts/talks/223_Smith.pdf) [of](http://user2014.stat.ucla.edu/abstracts/talks/901_Allaire.pdf) [presentations](http://user2014.stat.ucla.edu/abstracts/talks/61_Elprin.pdf) on how dependency management can be addressed within the R ecosystem, ranging from “provider” side options (e.g. freezing CRAN and private repositories) to the client side options, where a project maintains its own dependencies as part of its codebase.

In the video above, [JJ Allaire](http://en.wikipedia.org/wiki/Joseph_J._Allaire) and [Kevin Ushey](http://kevinushey.github.io/) give a detailed presentation of [Packrat](http://rstudio.github.io/packrat/) at useR! 2014. Packrat is a client-side solution which allows a project to manage dependencies within its own directory tree. This is a tried and true approach, currently utilized in communities from [Ruby](https://rubygems.org/) to [Perl](https://metacpan.org/release/local-lib). Packrat allows the developer to isolate projects from each other, even though they may share the same operating system image and physical hardware. This allows two separate projects to use completely different versions of the same library and coexist gracefully, an impossibility without such solutions. Packrat also allows for greater [reproducibility](/yihui-xie-the-user-2014-interview/), as underlying changes in system libraries will no longer impact the results of a run. Finally, packrat provides deployment portability by bundling all of an R application’s dependencies within the project, thereby freeing the DevOps group from having to build [Puppet](http://puppetlabs.com/)/[Ansible](http://www.ansible.com/home)/[Chef](https://www.getchef.com/chef/) code which installs R packages as a dependency for deploying a project.

I have adopted this package for all new R projects and have personally experienced greater peace of mind in knowing that in some small part, this approach makes the integration of my projects easier on the enterprise and helps make R a “well behaved” member of the enterprise toolchain. I hope you find similar benefits by using Packrat in your own work!

{{< youtube-lite id="aXajMa-OnOw" title="Rstudio's \"Packrat\" talk by J.J Allaire and Kevin Ushey" >}}
