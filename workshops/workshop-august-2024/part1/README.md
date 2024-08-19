# Welcome to the first part of the dlt Workshop!

![welcome-michael-scott.gif](welcome-michael-scott.gif)

In this course you will learn the fundamentals of dlt alongside some of the most important topics in the world of Pythonic data engineering.

## **Here’s what we’ll be covering:**

### 1. Presentation: [Kickoff](https://docs.google.com/presentation/d/1pvi1ohZzzWIdaEDqNwgULAQGL4M-rx7O2SuASr5l7Tc/edit?usp=sharing)

This will introduce you the concept of ETL, best practices in DE, and the biggest troubles a person can have in their Data Engineering duties. 

It’ll move ahead with introducing `dlt`, and how it works - as the solution to many of these problems right within Python.

### 2. Colab: [Run your first dlt pipeline](https://colab.research.google.com/drive/1aKCqSHV5XNUrSusN4eUueIf4dGM1uSlA?usp=sharing)

In this notebook, we’ll take a simple `dict` object in Python and run it in a `dlt` pipeline, and store it in a `duckdb` destination!

You’ll see how to explore your loaded data with `streamlit`, and also query it with `dlt`’s SQL client.


### 3. Colab: [Using dlt’s pre-built Sources and Destinations](https://colab.research.google.com/drive/1b-kMlUSBoeaP0CeTwXOwe55ORM5rHRGz?usp=sharing)
Now that you took a data source (a Python dictionary) and loaded it into a destination (`duckdb`), it is time to look into what other possibilities `dlt` offers. 

In this notebook we will take a quick look at pre-built verified sources and destinations and how to use them.

### 4. Colab: [Creating dlt resources & sources](https://colab.research.google.com/drive/1-moBiFWe4tuFEyfGuAwO3GLbl_hDDbxc?usp=sharing)

Now that we have a sense of what a source and destination can be, we can look into customizing some parts, i.e. defining sources and resources.

In this notebook, you will further look into how to create custom `dlt` resources and sources to extract data from.

### 5. Colab: [dlt Configuration](https://colab.research.google.com/drive/1nB4XAhzJDSMd3ZAmAvqVpNHkE1C62HI4?usp=sharing)

Since it is never a good idea to publicly put your API keys into your code, different environments have different methods to set and access these secret keys. `dlt` is no different. 

So this notebook will provide an overview of different methods of how to configure your secret keys to run your pipelines! Namely, TOML files, ENV, and vaults. 

### 6. Colab: [Exploring Schemas](https://colab.research.google.com/drive/1oFrpDXKY8GmIFRNKDPnGjfI0DTO-mIQC?usp=sharing)

Something about Schema;)

### 7. Colab: [Incremental Loading](https://colab.research.google.com/drive/1INRXRmiYLv5_OGuaYcl5pkvtG5WsFYgm?usp=sharing)

We can load data into our destinations in many different methods. Different sources handle the addition of new data differently, and because of that, data has to be loaded into destinations differently, and incrementally.

This notebook will help us understand the problem of incremental loading, and the 3 main methods of loading data into a destination with `dlt`.

### 8. Colab: [Incremental Loading - Merge Strategies](https://colab.research.google.com/drive/1sL1-yKcjownUgYZE14kpOwHPZkDbHxJt?usp=sharing)

Now that we have some familiarity with **incremental loading** and the **methods** of adding data. We will delve more into the 3 different strategies of the merge method. 

This notebook will walk through the definition and examples of those different strategies. It will help you understand where you might need to employ these different strategies.

### 9. Colab: [Exploring Pipeline Metadata](https://colab.research.google.com/drive/1ynRbV1NI7Mci0_oK6Ib41A-0GpseEZEE?usp=sharing)

After having learnt about pipelines and how to move data from one place to another. We now learn about information about the pipeline itself. Or, metadata of a pipeline that can be accessed and edited through dlt.
This notebook explores `dlt` states, what it collected and where this *extra* information is stored. It also expands a bit more on what the load info and trace in `dlt` is capable of.

## That’s it! 🎉

You finished the first dlt workshop! As a summary of everything we covered in this course, there’s a homework quiz for you to go through. Hopefully it’ll refresh your memory on everything we covered. Here you go: https://forms.gle/iKU9vLym4QbPm3veA