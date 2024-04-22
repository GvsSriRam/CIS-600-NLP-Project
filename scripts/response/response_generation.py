import random

from response.intent_responses import intent_responses_1, intent_responses_2

class ResponseGeneration:
    def __init__(self):
        pass

    def random_response(self, input_question):
        responses={}
        responses.update(intent_responses_1)
        responses.update(intent_responses_2)
        if input_question in responses:
            chosen_set = random.choice([intent_responses_1, intent_responses_2])
            return chosen_set.get(input_question)
        else:
            return responses.get(input_question, "The requested information is not available.")

# input_question=input()
# rg = ResponseGeneration()
# print(rg.random_response(input_question))
