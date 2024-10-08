# Welcome to the second part of the ELT with DLT Workshop 2.0!

<p align="center">
  <img src="hi.gif" alt="hi.gif" />
</p>


In this part of the course, you will get hands-on experience with `dlt` and the world of Pythonic data engineering as you deepen your understanding of topics previously touched upon.

## **Here’s what we’ll be covering:**

All these topics are covered in a single Colab notebook this time, [here](https://colab.research.google.com/drive/12rqKWoEQ1C8EEKUU45_FVmz5-hU8IMy0). You can either make a copy of the notebook, or open it in Playground mode to do all the exercises!

Content:

### 1. [Custom incremental loading](https://colab.research.google.com/drive/1C7KSuFhhD6mGc-uPm8gtMZm18YFT7hvO?usp=drive_link)
Implement custom strategies for incremental loading using `last_value_func`. These methods will help you efficiently manage data updates and ensure your pipelines are always up to date.
### 2. [Data Contracts](https://colab.research.google.com/drive/1RTAeZIbuMvKQxlGVJ0n3TeQF2w_ZFg9e?usp=drive_link)
Delve into schema configuration and data contracts. This module covers setting data types, enabling autodetection, and establishing data contracts to ensure data integrity and consistency across your pipelines.
### 3. [Tracing and Logging](https://colab.research.google.com/drive/1CR8MaiYPbjS4xSFegq3b9fZdKmiwjloJ?usp=sharing)
Gain expertise in configuring logging, managing logging levels. This will help you monitor and debug your pipelines more effectively.
### 4. [Retries](https://colab.research.google.com/drive/10FgjtqzamGY9YUyeyKyzeZ1b2ReRvOD7?usp=drive_link)
Learn how to customize retry logic using a `requests` wrapper.
### 5. [Performance optimization](https://colab.research.google.com/drive/1vzixI_gWhp_g9me2_raIW2qoo16n4q_f?usp=drive_link)
Explore various performance optimization techniques. Learn about parallelization, memory management, and how to control the extraction, normalization, and loading processes separately. You'll also discover how to speed up data processing with different file loader formats and chunking methods.
### 6. [Custom source: Rest API helpers](https://colab.research.google.com/drive/1NbHbvbx1HD8NRIO1eaznHMd0kZg6ykrD#scrollTo=HPbMniZ23Ulu)
Learn how to create custom data sources using a `rest_api` verified source and the `RestAPIClient` helper. This module will guide you through the process of integrating external APIs and other data sources into your `dlt` pipelines using Rest API helpers.
### 7. [Custom destinations](https://colab.research.google.com/drive/1UA4UCSO5UGngu_upUvorvPuarSxw7wVK?usp=drive_link)
Learn about custom destinations in the `dlt` library are user-defined locations where data can be loaded, allowing for flexibility in managing data flow and enabling the implementation of reverse ETL components that push data back to REST APIs.
### 8. **[Deployment](./deployment/)** 
    
Learn how to deploy your pipelines using popular tools like Lambda, Airflow, or Dagster. This module ensures that your pipelines are not only functional but also ready for production environments.

That’s it! 🎉
As a summary of everything we covered in this course, 
there’s a homework quiz for you to go through. Hopefully it’ll refresh your memory on everything we covered. Here you go: https://forms.gle/fgWYrX7BT4JUFQpEA