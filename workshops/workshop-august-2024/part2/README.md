# Welcome to the second part of the dlt Workshop!

![welcome.gif](comedian-welcome.gif)

This workshop is designed to deepen your understanding of advanced topics in dlt and data pipeline engineering. By the end of this course, you will have mastered a range of skills, from creating custom data sources to deploying robust pipelines.

## **Here’s what we’ll be covering:**

1. **Custom incremental loading**
    
    Implement custom strategies for incremental loading, including lookback periods, and backfill techniques, using `last_value_func`. These methods will help you efficiently manage data updates and ensure your pipelines are always up to date.
    
2. **Schema Configuration & Data Contracts**
    
    Delve into schema configuration and data contracts. This module covers setting data types, enabling autodetection, and establishing data contracts to ensure data integrity and consistency across your pipelines.
    
3. **Tracing, Logging, & Retries**
    
    Gain expertise in configuring logging with Sentry, managing logging levels, and customizing retry logic using a `requests` wrapper. This will help you monitor and debug your pipelines more effectively.
    
4. **Performance optimization**
    
    Explore various performance optimization techniques. Learn about parallelization, memory management, and how to control the extraction, normalization, and loading processes separately. You'll also discover how to speed up data processing with different file loader formats and chunking methods.
    
5. **Custom sources**
    
    Learn how to create custom data sources using a `rest_api` verified source and the `RestAPIClient` helper. This module will guide you through the process of integrating external APIs and other data sources into your dlt pipelines using Rest API helpers.
    
6. **Reverse ETL**
    
    Implement custom destinations for your data pipelines. This section will show you how to push data back into systems like CRMs, marketing platforms, or other operational tools, completing the data lifecycle.
    
7. **Deployment**
    
    Learn how to deploy your pipelines using popular tools like Lambda, Airflow (GCP), or Dagster. This module ensures that your pipelines are not only functional but also ready for production environments.
    
    **Bonus: Staging**
    
    Understand the significance of staging in data pipelines. You'll learn how to effectively stage data, ensuring that your ETL processes are both reliable and scalable.
    
8. **Bonus: dbt Runner**
    
    Integrate and run dbt models within your dlt workflows. This bonus section offers a hands-on approach to combining dbt's transformation capabilities with the flexibility of dlt pipelines.

