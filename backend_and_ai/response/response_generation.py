"""Module to generate response for an intent."""
import random

from response.intent_responses import intent_responses_1, intent_responses_2

class ResponseGeneration:
    """Class for response generation for an intent"""
    def __init__(self):
        pass

    def random_response(self, input_question: str):
        """Randomize response generation

        Args: input_intent (str): intent identified by model

        Returns: (str) - response for the intent
        """
        responses={}
        responses.update(intent_responses_1)
        responses.update(intent_responses_2)
        if input_question in responses:
            chosen_set = random.choice([intent_responses_1, intent_responses_2])
            return chosen_set.get(input_question)
        return responses.get(input_question, "The requested information is not available.")

# input_question=input()
# rg = ResponseGeneration()
# print(rg.random_response(input_question))
