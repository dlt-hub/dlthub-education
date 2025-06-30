# Welcome to the self-paced **dlt Advanced Holiday Course!**

![welcome](welcome-hello.gif)

*Ready to level up your pipelines and build like a pro?*

In this course, you'll go far beyond the basics. You’ll build custom sources, integrate with complex APIs and databases, control how your data lands in warehouses or files, transform it, and deploy pipelines in real-world production environments like Airflow or Lambda.

> Master the internals of `dlt`, learn best practices, and confidently build modern, production-grade data pipelines.

---

## **Here’s what we’ll be covering:**

### [**Lesson 1: Custom Sources – REST APIs & RESTClient**](https://colab.research.google.com/drive/1Q7URzYPKDdvxpRvXyIYwrTs8WGFM2GTk#forceEdit=true&sandboxMode=true)
Learn how to build flexible REST API connectors from scratch using `@dlt.resource` and the powerful `RESTClient`. 

### [**Lesson 2: Custom Sources – SQL Databases**](https://colab.research.google.com/drive/1lQ8VkrGJwZMsVtbkuYympcvbv0_CCgYo#forceEdit=true&sandboxMode=true)
Connect to any SQL-compatible database, reflect table schemas, write query adapters, and selectively ingest data using `sql_database`.

### [**Lesson 3: Custom Sources – Filesystems & Cloud Storage**](https://colab.research.google.com/drive/1P8pOw9C6J9555o2jhZydESVuVb-3z__y#forceEdit=true&sandboxMode=true)
Build sources that read from local or remote files (S3, GCS, Azure).

### [**Lesson 4: Custom Destinations – Reverse ETL**](https://colab.research.google.com/drive/14br3TZTRFwTSwpDyom7fxlZCeRF4efMk#forceEdit=true&sandboxMode=true)
Use `@dlt.destination` to send data back to APIs like Notion, Slack, or Airtable. Learn batching, retries, and idempotent patterns.

### [**Lesson 5: Transforming Data Before & After Load**](https://colab.research.google.com/drive/1--wNVd26TqNolnnECnUYZqeE2CXOeVZE#forceEdit=true&sandboxMode=true)
Learn when and how to apply `add_map`, `add_filter`, `@dlt.transformer`, or even post-load transformations via SQL or Ibis. Control exactly how your data looks.

### [**Lesson 6: Write Disposition Strategies & Advanced Tricks**](https://colab.research.google.com/drive/1XT1xUIQIWj0nPWOmTixThgdXzi4vudce#forceEdit=true&sandboxMode=true)
Understand how to use `replace` and `merge`, and combine them with schema hints and incremental loading. 

### [**Lesson 7: Data Contracts**](https://colab.research.google.com/drive/1mC09rjkheo92-ycjjq0AlIzgwJC8-ZMX#forceEdit=true&sandboxMode=true)
Define expectations on schema, enforce data types and behaviors, and lock down your schema evolution. Ensure reliable downstream use of your data.

### [**Lesson 8: Logging & Tracing**](https://colab.research.google.com/drive/1YCjHWMyOO9QGC66t1a5bIxL-ZUeVKViR#forceEdit=true&sandboxMode=true)
Track every step of your pipeline: from extraction to load. Use logs, traces, and metadata to debug and analyze performance.

### [**Lesson 9: Performance Optimization**](https://colab.research.google.com/drive/11P5O2R40ExtFtPfX4o1O5mF7nFbibtuZ#forceEdit=true&sandboxMode=true)
Handle large datasets, tune buffer sizes, parallelize resource extraction, optimize memory usage, and reduce pipeline runtime.

### [**Lesson 10: Deployment with GitHub Actions, Lambda, Airflow, or Dagster**](./deployment)
Bring your pipelines into production. Learn how to run dlt on AWS Lambda, GitHub Actions, DAGs in Airflow, or within Dagster projects. 

## Homework & certification

You’ve finished the dlt Advanced Course — well done!  
Test your skills with the **Advanced Certification Homework**: https://forms.gle/eDt2Tuuz6g7wNsJPA

**Deadline:** July 31, 18:00 (CET)  
**Passing grade:** 70%+

---

## Feedback & questions

We love improving this course with your help.  
Please share your thoughts: TBA 


Need help or stuck on something?  
[Join the Community](https://dlthub.com/community) and ask away in #dlthub-education channel — we’re happy to help.

