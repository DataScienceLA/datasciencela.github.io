---
title: "Secure your Shiny apps (against SQL injection)"
date: 2015-01-12T09:25:12
lastmod: 2015-01-12T09:41:19
slug: "secure-your-shiny-apps-against-sql-injection"
authors: ["szilard"]
categories: ["r"]
tags: ["r", "data-science-2", "production", "shiny", "sql", "security"]
archivedComments: 15
showComments: true
wpID: 494
---

[Shiny](http://shiny.rstudio.com/) takes inputs from UI elements and sends them to the server, where the application can access them as R variables. While Shiny has security measures in place, as in any typical web application, it remains the developer's responsibility to sanitize the inputs before using them. For example, Shiny has no way to protect you if you are using an input in a SQL query such as `select ... from ... where field = 'input'`. Someone manipulating the websocket communication can craft a specially-formatted input that can force the database to execute a query that it is not supposed to do, termed an [SQL injection](http://en.wikipedia.org/wiki/SQL_injection). This might give an attacker access to private data or the ability to do other nefarious things, and it is a common security issue.

To see this in action, take a look at this [Shiny app](https://szilard.shinyapps.io/shinyvalidinp-demo/) demo. The input is read from a dropdown menu and it is used on the server side to construct a SQL query

```r
abbr <- input$inp_abbr
dbGetQuery(con, paste0("select * from states where abbr = '",abbr,"'"))
```

<small>Source: [gist ef1d145](https://gist.github.com/szilard/ef1d14534945a2fc5115) by szilard</small>

Even if the input is read from a list of predetermined values (such as a dropdown) it is quite easy for someone accessing the app to send arbitrary input. For example, using Chrome browser's Developer Tools' Network panel one can see that for each UI update the following data is sent: `{"method":"update","data":{"inp_abbr":"CA"}}`. You can now use the Developer Tools' Javascript Console to send `' or 1=1 --` instead of `CA`, and then the SQL query constructed by the code above becomes `select * from states where abbr = '' or 1=1 --'`. The app will then run this query and return all the values from that table, which is very different from the original intent of the app. With these kinds of simple tricks someone could read data from other tables as well, and in certain cases even alter or delete data.

It's important to note that this is not a deficiency of Shiny per se; it is instead a problem in any web framework - and it is the developer's responsibility to check the inputs and act accordingly. If you are developing Shiny apps in a corporate environment while accessing data from a SQL database, you should definitely pay attention to these possibilities. Luckily there are several ways to deal with this problem, a few of which I describe below.

One way is to check the inputs and if they don't conform with certain patterns, do not run the query and give an error to the user. You could also use Shiny's [validate](http://shiny.rstudio.com/articles/validation.html) function to have a more user friendly message if you prefer. It is usually safer to specify which patterns are allowed (i.e. whitelist) such as "only alphanumeric characters, dot, space and hyphen" rather then specifying those characters not allowed (i.e. blacklist) such as "single quote, backslash etc". I wrote a very basic R package that provides functions for validating numeric, character, logical and Date values for the various Shiny UI elements. You can [find it on github](https://github.com/szilard/shinyvalidinp) and use it by wrapping your inputs like this, and note that you can use regular expressions for specifying the pattern.

```r
abbr <- validinp_character(input$inp_abbr)
## or:
abbr <- validinp_character(input$inp_abbr, pattern="^((CA)|(NY))$")
```

<small>Source: [gist 86c14fe](https://gist.github.com/szilard/86c14fe74d65271809bf) by szilard</small>

It is also always recommended to restrict the input as much as possible (e.g. to a set of known values as I described in the second option above).

Another approach to secure web applications is to sanitize the inputs, or in other words replace non-alphanumeric characters (like single quotes) with "escaped" ones before continuing with the query. For example, if you are using MySQL via the RMySQL package you can use the mysqlEscapeStrings function to achieve this. Unfortunately there are numerous edge cases that must be considered during implementation and this sanitizing approach is usually considered error prone. On the other hand, if you are using the excellent [dplyr](/dplyr-some-more-reflections/) package you are provided basic safeguards by escaping automatically. This is primarily meant to prevent accidental misuse rather than an explicit attack, however. As Hadley says in the dplyr docs, "This is unlikely to prevent any serious attack, but should make it unlikely that you produce invalid SQL."

Perhaps the [most secure approach](https://www.owasp.org/index.php/SQL_Injection_Prevention_Cheat_Sheet) would be to use [prepared statements](http://en.wikipedia.org/wiki/Prepared_statement), also called parameterized queries. Unfortunately the RMySQL package does not currently support this feature and the support in the other R database connectors is also somewhat in its infancy.

Regardless of how you address this issue, you should also have additional layers of security such as granting minimal privileges to the database user used by the application. For a Shiny app, this means you might provide read-only access to a few tables. In addition, you should also restrict the Shiny app to a limited set of users whenever possible - either by using [Shiny Server Pro](http://www.rstudio.com/products/shiny-server-pro/), [ShinyApps.io](http://www.shinyapps.io/) or by proxying via a web server and using its authentication features. You should also encrypt the traffic (https) if it is not on a private network. Furthermore, other than running Shiny as an unprivileged user (which is the default), you could also run the app in an isolated environment and/or use the [RAppArmor](https://github.com/jeroenooms/RAppArmor) package for extra security.

Finally, while in this blog post I have focused upon SQL injection, validating the inputs is crucial in several other situations. With R being a 'hyper-dynamic' language, there are countless functions in base R and common packages that do eval-like things, such as when data becomes code and it is executed. While a blacklisting approach seems hopeless to me in this case, the [sandboxR](https://github.com/Rapporter/sandboxR) project has attempted to map R's 'unsafe' functions - and the long [blacklist therein](https://github.com/Rapporter/sandboxR/blob/master/R/blacklist.R) should horrify you with how many ways things can go wrong. Therefore, you must think carefully and thoroughly check your inputs if you are developing a Shiny app (or any web application, for that matter). Be safe!
