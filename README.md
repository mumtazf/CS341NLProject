# Laptop Recommendation Chatbot

## Description

We utilize the Slot Filling and Intent Classification method of Task-Based Dialogue Systems to find the laptops best fit on the user dialogue's needs.

The dataset that we worked with is the Kaggle ["Brand Laptops Dataset"](https://www.kaggle.com/datasets/bhavikjikadara/brand-laptops-dataset/data) by Bhavik Jikadara that contains a collection of 991 unique laptops sourced from the 'Smartprix' website. 

We are also utilizing the GitHub Repo [Slot_Filling](https://github.com/StarrySkyrs/Slot_Filling) developed by Mrinal Grover, Andrew Stich, Varadraj Poojary, and Sijia Han, specifically the "BERT for Name and Cuisine Prediction". However, for our case it is BERT for Laptop Prediction based on the users' requests. We've narrowed down the features from 22 to 5 which are "brand", "price" (converted from Indian Rupees to USD), "processor_tier", "ram_memory", and "display_size" by manually annotating the first 40 entries of the dataset.

## Contents

This repository contains the code for our laptop recommendation chatbot. Navigate to `chat.py` and run it to start the chatbot interaction. Currently, the chatbot uses
rule-based NER to find keywords in the user responses. 

`user.py` contains User class that stores user preferences

`rule_based_ner.py` contains the skeleton of keywords being used for rule-based ner. The extraction of keywords from responses takes place in `chat.py`.
