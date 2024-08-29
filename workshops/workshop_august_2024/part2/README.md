# Welcome to the second part of the dlt Workshop!

![welcome.gif](comedian-welcome.gif)

This workshop is designed to deepen your understanding of advanced topics in dlt and data pipeline engineering. By the end of this course, you will have mastered a range of skills, from creating custom data sources to deploying robust pipelines.

## **Here’s what we’ll be covering:**

## 1. **[Custom incremental loading](https://colab.research.google.com/drive/15c2PSsqB6Wlsx4soKV8a-QEGIuJKdmAc)** 
Implement custom strategies for incremental loading using `last_value_func`. These methods will help you efficiently manage data updates and ensure your pipelines are always up to date.

## 2. **[Schema Configuration & Data Contracts](https://colab.research.google.com/drive/1BOUvAzP7_H0NvXhZOtNsJO-Nn3c30dXL)** 
Delve into schema configuration and data contracts. This module covers setting data types, enabling autodetection, and establishing data contracts to ensure data integrity and consistency across your pipelines.
    
## 3. **[Tracing, Logging](https://colab.research.google.com/drive/1JdgwPlnKJ4oCDEIX7_dzzJhS9oqaGNv7)**
Gain expertise in configuring logging with Sentry, managing logging levels. This will help you monitor and debug your pipelines more effectively.

## 4. **[Retries](https://colab.research.google.com/drive/1wqeIv0nD6S9r8ImJEbZ_PYBgeE3C3kMO)** 
    
Learn how to customize retry logic using a `requests` wrapper. 

## 5. **[Bonus: dbt Runner](./dbt_runner_demo/)**
    
Integrate and run dbt models within your dlt workflows. This bonus section offers a hands-on approach to combining dbt's transformation capabilities with the flexibility of dlt pipelines.
    
## 6. **[Performance Optimization](https://colab.research.google.com/drive/1aC2V27rNko2dLkb2IP4UmiyhtD3MoqFX)**
    
Explore various performance optimization techniques. Learn about parallelization, memory management, and how to control the extraction, normalization, and loading processes separately. You'll also discover how to speed up data processing with different file loader formats and chunking methods.
    
## 7. **[Custom sources](https://colab.research.google.com/drive/1CRaS_4HEST9pvIiFZ2JW5HJZqLP_LeI-#scrollTo=-TqpaPEKkqKq)**
    
Learn how to create custom data sources using a `rest_api` verified source and the `RestAPIClient` helper. This module will guide you through the process of integrating external APIs and other data sources into your dlt pipelines using Rest API helpers.
    
## 8. **[Reverse ETL](https://colab.research.google.com/drive/1Cfm65sISqOluNXvY_qvXJn9eST2opTyE#scrollTo=e1ftZXpthVjX)**
    
Implement custom destinations for your data pipelines. This section will show you how to push data back into systems like CRMs, marketing platforms, or other operational tools, completing the data lifecycle.
    
## 9. **[Deployment](./deployment/)** 
    
Learn how to deploy your pipelines using popular tools like Lambda, Airflow, or Dagster. This module ensures that your pipelines are not only functional but also ready for production environments.

## That’s it! 🎉

You finished the second dlt workshop! As a summary of everything we covered in this course, there’s a homework quiz for you to go through. Hopefully it’ll refresh your memory on everything we covered. Here you go: https://forms.gle/xfaWFSYq1vKc96EJA