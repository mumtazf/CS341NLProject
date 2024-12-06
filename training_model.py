# Vectorize text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
import pandas as pd
from collections import defaultdict


class TrainModel:
    
    def __init__(self):
        self.queries = []
        self.labels = []

    def set_labels(self):
        """
        """
        # Initialize slot-specific contexts and answers
        brand_context = []
        brand_answers = []
        price_context = []
        price_answers = []
        processor_context = []
        processor_answers = []
        display_context = []
        display_answers = []

        # Dictionary to store slots and their unique values
        slot_dic = defaultdict(lambda: defaultdict(set))

        # Load the files
        with open("data/train_utt.txt", encoding = 'utf-8') as f1, open("data/train_ans.txt",  encoding = 'utf-8') as f2:
            utterances = f1.readlines()
            for i, line in enumerate(f2.readlines()):
                a_line = line.strip()
                ans = a_line.split('|')
                # The intent (always 'find_laptop')
                intent = ans[0] 
                
                # Process slots in the answer
                for a in ans[1:]:
                    if "!=" in a:  # Handle negated slots
                        slot_name, slot_value = a.split("!=")
                    else:  # Handle regular slots
                        slot_name, slot_value = a.split("=")
                    
                    # Collect context and answers for specific slots
                    if slot_name == "brand":
                        brand_context.append(utterances[i].strip())
                        brand_answers.append(slot_value)
                    if slot_name == "price":
                        price_context.append(utterances[i].strip())
                        price_answers.append(slot_value)
                    if slot_name == "processor_tier":
                        processor_context.append(utterances[i].strip())
                        processor_answers.append(slot_value)
                    if slot_name == "display_size":
                        display_context.append(utterances[i].strip())
                        display_answers.append(slot_value)
                    
                    # Add slot values to the slot dictionary
                    slot_dic[slot_name]["values"].add(slot_value)

                    # Display the slot dictionary
        return slot_dic
    
    def train_model(self, queries, labels):
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(queries)

        # Encode labels
        mlb = MultiLabelBinarizer()
        y = mlb.fit_transform(labels)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        # Train multi-label classifier
        clf = MultiOutputClassifier(SVC(probability=True))
        clf.fit(X_train, y_train)

        # Prediction function
        def predict_slots(query):
            query_vectorized = vectorizer.transform([query])
            predictions = clf.predict(query_vectorized)
            
            # Convert binary predictions back to labels
            predicted_labels = mlb.inverse_transform(predictions)
            return predicted_labels[0]


if __name__ == "__main__":
    model = TrainModel()
    result = model.set_labels()
    print(result)
    # test_query = "dell laptop under 500 dollars"
    # print(predict_slots(test_query))

