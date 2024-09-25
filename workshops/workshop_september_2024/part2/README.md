# Welcome to the second part of the ELT with DLT Workshop 2.0!

<p align="center">
  <img src="hi.gif" alt="hi.gif" />
</p>


In this part of the course, you will get hands-on experience with `dlt` and the world of Pythonic data engineering as you deepen your understanding of topics previously touched upon.

## **Here’s what we’ll be covering:**

All these topics are covered in a single Colab notebook this time, [here](https://colab.research.google.com/drive/1u3sOsQpUJ1cCNbKs4ExobPxklk5wEeaF?usp=sharing). You can either make a copy of the notebook, or open it in Playground mode to do all the exercises!

Content:
### 1. Recap from [Part 1](../part1)
### 2. [Custom incremental loading](https://colab.research.google.com/drive/15c2PSsqB6Wlsx4soKV8a-QEGIuJKdmAc)
Implement custom strategies for incremental loading using `last_value_func`. These methods will help you efficiently manage data updates and ensure your pipelines are always up to date.
### 3. [Data Contracts](https://colab.research.google.com/drive/1BOUvAzP7_H0NvXhZOtNsJO-Nn3c30dXL)
Delve into schema configuration and data contracts. This module covers setting data types, enabling autodetection, and establishing data contracts to ensure data integrity and consistency across your pipelines.
### 4. [Tracing and Logging](https://colab.research.google.com/drive/1JdgwPlnKJ4oCDEIX7_dzzJhS9oqaGNv7)
Gain expertise in configuring logging, managing logging levels. This will help you monitor and debug your pipelines more effectively.
### 5. [Retries](https://colab.research.google.com/drive/1wqeIv0nD6S9r8ImJEbZ_PYBgeE3C3kMO)
Learn how to customize retry logic using a `requests` wrapper.
### 5. [Performance optimization](https://colab.research.google.com/drive/1aC2V27rNko2dLkb2IP4UmiyhtD3MoqFX)
Explore various performance optimization techniques. Learn about parallelization, memory management, and how to control the extraction, normalization, and loading processes separately. You'll also discover how to speed up data processing with different file loader formats and chunking methods.
### 6. [Custom source: Rest API helpers](https://colab.research.google.com/drive/1CRaS_4HEST9pvIiFZ2JW5HJZqLP_LeI-#scrollTo=-TqpaPEKkqKq)
Learn how to create custom data sources using a `rest_api` verified source and the `RestAPIClient` helper. This module will guide you through the process of integrating external APIs and other data sources into your `dlt` pipelines using Rest API helpers.
### 7. [Custom destinations](https://colab.research.google.com/drive/1UA4UCSO5UGngu_upUvorvPuarSxw7wVK?usp=sharing)
Learn about custom destinations in the `dlt` library are user-defined locations where data can be loaded, allowing for flexibility in managing data flow and enabling the implementation of reverse ETL components that push data back to REST APIs.

That’s it! 🎉