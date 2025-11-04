# AI-Ready Data in Action: Powering Smarter Agents

Workshop is led by Violetta Mishechkina (dltHub) and Chang She (LanceDB).

## Abstract
Modern AI applications are only as powerful as the data that fuels them. Yet, much of the real-world data AI engineers encounter is messy, incomplete, or unoptimized data. In this hands-on tutorial, AI-Ready Data in Action: Powering Smarter Agents, participants will walk through the full lifecycle of preparing unstructured data, embedding it into LanceDB, and leveraging it for search and agentic applications. Using a real-world dataset, attendees will incrementally ingest, clean, and vectorize text data, tune hybrid search strategies, and build a lightweight chat agent to surface relevant results. The tutorial concludes by showing how to take a working demo into production. By the end, participants will gain practical experience in bridging the gap between messy raw data and production-ready pipelines for AI applications.

## Links

1. [Workshop Colab](https://colab.research.google.com/drive/1JGwdyQl7oKG1nsEF9Ol32qnTt0hFURzd#scrollTo=eC87VYRnaPBf&forceEdit=true&sandboxMode=true)
2. [Slides](https://docs.google.com/presentation/d/1geGYVEyftY8FNiNu9YTPUhLZiTNYNYBnGgQQdl6ffUQ/edit?usp=sharing)

## Key Takeaways

By the end of the tutorial, participants will:

1. Understand the end-to-end workflow of taking raw, real-world data and preparing it for AI applications.
2. Build and run an incremental dlt pipeline to ingest real data into LanceDB.
3. Apply text preprocessing and generate embeddings for semantic search.
4. Optimize retrieval with vector and hybrid search strategies.
5. Implement a lightweight AI agent capable of surfacing relevant issues from a natural language description.
6. Learn how to transition from a demo project to a production setup using LanceDB Cloud.

## Outline

- Introduce dlt (data load tool) and how it enables schema evolution, incremental loading, and normalization in pipelines.
- Introduce LanceDB and explain embeddings, vector search, hybrid retrieval and multi-modal data for AI applications.
- Ingest and preprocess a real dataset with dlt, generate embeddings, and load it into LanceDB following best data engineering practices.
- Optimize search in LanceDB by tuning parameters, selecting distance metrics, and adding hybrid retrieval.
- Build a lightweight AI agent that queries LanceDB and returns the most relevant issues from natural-language prompts.
- Demonstrate the path to production using automation, monitoring, and LanceDB Cloud for scaling and reliability.
- Conclude with key takeaways and an open Q&A.