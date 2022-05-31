# GoAlgo-v1.0

**About GoAlgo**
================

  

### What is GoAlgo?

**GoAlgo** is a **search engine**, i.e nothing but a software system designed to carry out web searches. It scans its corpus (consisting of a whopping 6500+ documents!) in a systematic way for particular information specified in a textual web search query. The **top 5** search results are presented in a line of results, referred to as search engine results pages.  

Notably, **GoAlgo** is a **Vertical Search Engine.** Vertical search, or specialized search, is a way of narrowing your search to one topic category, rather than the entirety of the web.  
In the case of GoAlgo, the specific topic it deals with is **'Commonly used Data Structures and Algorithms and problems based upon them.'**

Some other examples of vertical search engines include:

*   The search bar on shopping sites like eBay and Amazon
*   Google Scholar, which indexes scholarly literature across publications
*   Searchable social media sites and apps like Pinterest

### How does it work?

Using GoAlgo is easy, isn't it? You open up the search page, type a few words into the search bar, and voilà — a list of top 5 of results appear, in mere seconds!  
But under the hood, a lot of heavy lifting is being done. Search engines out there in the wild are pretty complex when it comes to the algorithms they use.  
GoAlgo follows a pretty basic formula. It's a simple two step process -

  

##### Step 1. Search

When you enter your, GoAlgo must first **preprocess** your words into relevant terms. This is done via a host of techniques including **natural language processing**. The output of this initial translation process is a **rewritten query that identifies the important parts of your query, corrects misspellings, lemmatizes the query, converts numbers to their word-equivalents** etc. GoAlgo then skims through its corpus to find web pages that match the rewritten query.

  

##### Step 2. Rank

A single search may turn up thousands of relevant documents, so part of the job of GoAlgo is to sort these listings using some **ranking algorithm**. And although these algorithms are designed to provide you with the best answers to your questions, they are biased towards certain factors. GoAlgo wants you to show you results that you’ll click on, and they use a variety of factors to rank results according to what it think syou’ll engage with.

GoAlgo uses [**Okapi BM-25**](https://en.wikipedia.org/wiki/Okapi_BM25) algorithm to present you with a list of top-5 results prioritized by what it thinks will best answer your query.  
  
So, in a nutshell, that was all about the working of GoAlgo.  
  

