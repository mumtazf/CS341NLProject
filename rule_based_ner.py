class RuleBasedNER:
       """
       This class serves as the implementation of our baseline method. We initialize the different
       keywords associated with 5 characteristics we are using for our recommendation. 

       This class implements Rule-based NER, which refers to finding entities in user response just 
       on the basis of whether that keyword exists in their response or not.

       For example, 
       user response: I want a Dell laptop
       matched_entity: brand => Dell

       user response: I want a good laptop for school
       matched_entity: NONE

       ----------------------------
       Attributes

       - entities = entities consist of keywords related to brand, ram_memory, processor_tier, budget, and display_size
       """
       def __init__(self):
              self.entities = {
                     'brand': ['tecno', 'hp', 'acer', 'lenovo', 'apple', 'infinix', 'asus', 'dell', 'samsung', 'msi', 'wings', 'ultimus', 'primebook', 'iball', 'zebronics', 'chuwi','gigabyte', 'jio', 'honor', 'realme', 'avita', 'microsoft', 'fujitsu', 'lg', 'walker', 'axl'],
                     'ram_memory': ['8', '16', '32',  '4',  '2', '12', '36'],
                     'processor_tier': ['core i3', 'core i7', 'ryzen 5', 'core i5', 'ryzen 3', 'm1', 'core i9', 'ryzen 7', 'other', 'm3', 'm2', 'ryzen 9', 'celeron', 'core ultra 7', 'pentium', 'amd'],
                     'budget': ['low', 'medium', 'high'],
                     'display_size': ['13', '14', '15']
              }

       def get_entities(self):
           return self.entities
        