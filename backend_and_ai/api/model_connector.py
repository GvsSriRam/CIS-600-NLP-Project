"""Module to connect different functionalities of model with endpoint routes."""
from pathlib import Path
from datetime import datetime

from log import logger
from intent_recognition.intent_recognition import IntentRecognition
from autocorrect.autocorrect import Autocorrect
from response.response_generation import ResponseGeneration

# Define project root directory
PROJECT_ROOT_DIR = str(Path(__file__).parent.parent.parent)

# Instantiate components of the model
ic = IntentRecognition()
ac = Autocorrect()
rg = ResponseGeneration()

# Train the model when the API is started
ic.train()

class ModelConnector:
    """Connects model operations to endppoint-router"""

    def __init__(self) -> None:
        pass

    def train(self):
        """
        Train the model.
        
        Returns:
            str: Error message if training fails, otherwise an empty string.
        """
        error = ""
        try:
            ic.train()
        except Exception as e:
            logger.error(str(e))
            error = str(e)
        return error

    def q_a(self, input_str: str):
        """
        Perform question answering with the model.
        
        Args:
            input_str (str): Input text.
        
        Returns:
            tuple: A tuple containing the response dictionary and any error message.
        """
        current_date_and_time = datetime.now()
        current_time = current_date_and_time.strftime("%H:%M")
        res = {
            "input_str": input_str,
            "autocorrect": True,
            "corrected_str": None,
            "intent": None,
            "response": None,
            "timestamp": current_time
        }
        error = ""

        try:
            corrected_str, res["autocorrect"] = ac(input_str)

            if res["autocorrect"]:
                res["corrected_str"] = corrected_str
            predicted_intent = ic.predict(corrected_str)
            res["intent"] = predicted_intent

            response = rg.random_response(predicted_intent)
            res["response"] = response
        except Exception as e:
            logger.error(str(e))
            error = str(e)

        return res, error
