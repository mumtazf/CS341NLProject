import cmd
import pandas as pd
import numpy as np
from user import User
from rule_based_ner import RuleBasedNER

class Chatbot:
    """
    This is the Chatbot class that contains information about the database used by the chatbot and creates
    a session for the user. 

    """
    def __init__(self):
        self.name = "Laptops Nerd"
        self.database = pd.read_csv("data\laptops.csv")
        self.prompts = {}
        self.user = User()
        self.entities = ['brand', 'display_size', 'ram_memory', 'budget', 'processor_tier']

    
    def set_prompts(self):
        """
        This method initializes prompts that the chabot uses
        """
        self.prompts['greeting'] = f"Hello {self.user.get_username()}! I'm LaptopNerd and I can help you find a laptop that meets your specifications. \n\t-I will ask you a series of questions and use your responses to generate my recommendation. \n\t-You can end this session anytime by typing :quit"       
        self.prompts['confirmation'] = f"Would you like me to show you the current recommendation?"
        self.prompts['recommendation'] = f"Based on your preferences, I think you will like: "
        self.prompts['goodbye'] = f"Thank you! Hope you have a great day :)"

        self.prompts["brand"] = f"What brand of laptop would you like?\n[Some examples are: Acer, Dell, Apple, etc...]"
        self.prompts["ram_memory"] = f"What RAM size would you like?\n [For example, 8GB, 16GB, etc.]"
        self.prompts["display_size"] = f"What display size of screen do you like? [For example, 13 inch, 14 inch, 15.6 inch, etc.]"
        self.prompts["budget"] = f"What's your budget like? [Choose from: low, medium, high]"
        self.prompts["processor_tier"] = f"What kind of processor are you envisioning? [Examples are: amd, ryzen, core i9, core i7, m1, m2, etc.]"


    def get_prompt(self, description):
        if description not in self.prompts.keys():
            return "prompt does not exist"
        else:
            return self.prompts[description]
    
    def ask(self):
        """
        This method returns the questions to be asked to the user. 
        If all questions have been exhausted, it return the prompt for generating recommendation
        """
        # If all entities are filled, return confirmation
        if all(self.user.get_entities(entity) != "" for entity in self.entities):
            return self.get_prompt("confirmation")
        
        for entity in self.entities:
            if self.user.get_entities(entity) == "":
                return self.get_prompt(entity)
                
    def process_response(self, user_response):
        """
        This method processes and parses user responses. 
        It fills the slots based on user responses
        """
        if user_response.lower() == ":quit":
            return False
        
        method = RuleBasedNER()

        matched_entities = False
        for category, items in method.get_entities().items():
            for item in items:
                if item.lower() in user_response.lower():
                    self.user.set_entities(category, item) # fills the slots here
                    matched_entities = True
                    break
        
        if not matched_entities:
            print("No entities matched in the response")
        
        return True
    
    def score_laptops(self, row):
        score = 0
        if row['brand'] == self.user.get_entities("brand"):
            score+=1

        if row['display_size'] == self.user.get_entities("display_size"):
            score+=1

        if row['processor_tier'] == self.user.get_entities("processor_tier"):
            score+=1

        if row['price_range'] == self.user.get_entities("budget"):
            score+=1

        if row['ram_memory'] == self.user.get_entities("ram_memory"):
            score+=1

        return score

    def recommend_laptop(self):
        """
        This method calculates the score of each laptop in the database and sorts the results according 
        to the highest score 

        Score is calculated by checking how many of the total preferences match
        Each laptop gets a score based on the user profile
        """
        self.database['score'] = self.database.apply(lambda row : self.score_laptops(row), axis = 1)

        recommended_laptops = pd.DataFrame(self.database[self.database['score'] >=3])
        recommended_laptops.sort_values(by='score', ascending=False)
        recommendation_names = (recommended_laptops['Model'])

        if len(recommendation_names) == 0:
            print(f"No recommendations suit your choices.")
            print(self.user.return_all_entities())
            # TODO: Handle when no recommendations are met
            return None
        else:
            return recommendation_names.iloc[0]


class InteractionLoop(cmd.Cmd):
    """
    Loop that handles communication with the user. We use command prompt for now.
    
    NOTE: We learned how to have interactionLoop thanks to Heather's code activity in class.
    """
    prompt = '> '

    def __init__(self):
        super().__init__()
        self.chatbot = Chatbot()
        self.name = self.chatbot.name
        self.bot_prompt = '\001\033[96m\002%s> \001\033[0m\002' % self.name
        self.intro_user()
        self.asking_question = True


    def intro_user(self):
        print(self.bot_says("Hello! Welcome to the laptop reccommender chatbot! To start, please enter your username below."))
        username = input("Username: ")
        self.chatbot.user.set_username(username)

        # set the prompts after i got the username
        self.chatbot.set_prompts()

        # communicating the rules
        greeting = self.chatbot.get_prompt("greeting")
        print(self.bot_says(greeting))
        input("Press any key to continue.")
        self.prompt_user()

    def prompt_user(self):
        while True:
            prompt = self.chatbot.ask()
            print(self.bot_says(prompt))

            if "recommendation" in prompt:
                result = self.chatbot.recommend_laptop()
                if result != None:
                    print(self.bot_says("Based on your preferences, I think you will like: " + result))
                False
                break
            else:     
                user_response = input("Your response: ")

                ## if user asks to quit
                if self.chatbot.process_response(user_response) == False:
                    print(self.bot_says(self.chatbot.get_prompt('goodbye')))
                    break

    def bot_says(self, response):
        return self.bot_prompt + response
    
    def set_asking_question(self):
        self.asking_question = not (self.asking_question)
    

my_chatbot = InteractionLoop()
my_chatbot.cmdloop()