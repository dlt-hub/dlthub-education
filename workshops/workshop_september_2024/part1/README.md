# Welcome to the first part of the ELT with DLT Workshop 2.0!

![simpsons-hello.gif](simpsons-hello.gif)

In this course you will learn the fundamentals of dlt alongside some of the most important topics in the world of Pythonic data engineering.

## **Here’s what we’ll be covering:**

### 0. Presentation: [Kickoff](https://docs.google.com/presentation/d/1KeTJ_MHpCxmjGTkEhpv5-UYcwpil76adbXUlzA59lFM/edit?usp=sharing)

This will introduce you the concept of ETL, best practices in DE, and the biggest troubles a person can have in their Data Engineering duties. 

It’ll move ahead with introducing `dlt` - as the solution to many of these problems right within Python.

### 1. [Getting Started: dlt Resources and Sources](https://colab.research.google.com/drive/1laas5XkGEQIqmpFX48pIL48-OoV_mEye)

In this notebook, we’ll take a simple `dict` object in Python and run it in a `dlt` pipeline, and store it in a `duckdb` destination!
You’ll see how to explore your loaded data with `streamlit`, and also query it with `dlt`’s SQL client.

You will also look into how to create custom `dlt` resources and sources to extract data from.

### 2. [Defining Secrets and Configs](https://colab.research.google.com/drive/11JW9efItqa31iQeQtABN6Qbc6RcQQMbW)

Since it is never a good idea to publicly put your API keys into your code, different environments have different methods to set and access these secret keys. `dlt` is no different. 

So this notebook will provide an overview of different methods of how to configure your secret keys to run your pipelines! TOML files and ENVs. 

### 3. [Incremental Loading](https://colab.research.google.com/drive/1izVY7a-CuRkV6rKok7Z8MNVIZ11PhMqN)

We can load data into our destinations in many different methods. Different sources handle the addition of new data differently, and because of that, data has to be loaded into destinations differently, and incrementally.

This notebook will help us understand the problem of incremental loading, and the 3 main methods of loading data into a destination with `dlt`.

### 4. [Using dlt’s pre-built Sources and Destinations](https://colab.research.google.com/drive/1Xig8yGmZ5gmbm_NjJ8mR1QMC1C5NUGPZ)
Now that you took a data source and loaded it into a destination (`duckdb`), it is time to look into what other possibilities `dlt` offers. 

In this notebook we will take a quick look at pre-built verified sources and destinations and how to use them.

### 5. [dlt Destinations & Sources: Filesystem](https://colab.research.google.com/drive/1jMW9RfFsvEZ54ehLJkeaEm6ViVaZs5sG)

Are you data Scientist and prefer csv files instead of Database? Or you want to use a cloud storage as a staging? This section is for you! 

Load your data directly into filesystem!

### 6. [Staging](https://colab.research.google.com/drive/1EeJoTkKcqB8-UnsS9cqTwbudo2YN6_Ne)

The goal of staging is to bring the data closer to the database engine so the modification of the destination dataset happens faster and without errors.

We covered some staging datasets and tables while covering the merge write disposition and filesystem destination. Let's go deeper!

### 7. [Inspecting & Adjusting Schema](https://colab.research.google.com/drive/1an46jq5wCv8jQrqShIN1xG45mr92ljor)

dlt creates and manages the schema automatically, but what if you want to control it yourself? Explore the schema and customize it to your needs easily with dlt!


### 8. [Understanding Pipeline Metadata](https://colab.research.google.com/drive/1ABHITE9BlXcN5pxzqIjIz_zcXY9EXlp0#scrollTo=l7Y1oCAvJ79I)

After having learnt about pipelines and how to move data from one place to another. We now learn about information about the pipeline itself. Or, metadata of a pipeline that can be accessed and edited through dlt.
This notebook explores `dlt` states, what it collected and where this *extra* information is stored. It also expands a bit more on what the load info and trace in `dlt` is capable of.


## That’s it! 🎉

You finished the first part of dlt Workshop 2.0! As a summary of everything we covered in this course, 
there’s a homework quiz for you to go through. Hopefully it’ll refresh your memory on everything we covered. Here you go: https://forms.gle/MwQfFQ2PC2R7YejQ7