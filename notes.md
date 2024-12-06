User query: Could you please recommend me budget friendly dell laptops? [features]
Response: find-laptop|budget=low [labels]

For feature extraction, we can use tf-idf to find the frequency of words and ranking what the most important words in a particular query is

We then encode the labels => it is a way to represent the words numerically. 4



FEATURES ---> MODELLL ---> RESPONSES (LABELS)

Features -> tf-idf

Label 

sklearn -> Binary

https://scikit-learn.org/dev/modules/generated/sklearn.preprocessing.MultiLabelBinarizer.html 