from pathlib import Path

from log import logger
from intent_recognition.intent_recognition import IntentRecognition
from autocorrect.autocorrect import Autocorrect
from response.response_generation import ResponseGeneration


PROJECT_ROOT_DIR = str(Path(__file__).parent.parent.parent)

ic = IntentRecognition()
ac = Autocorrect()
rg = ResponseGeneration()
ic.train()

class ModelConnector:
    """Connects model operations to endppoint-router"""

    def __init__(self) -> None:
        pass

    def train(self):
        error = ""
        try:
            ic.train()
        except Exception as e:
            logger.error(str(e))
            error = str(e)
        return error
    
    def q_a(self, input_str):
        res = {
            "input_str": input_str,
            "autocorrect": True,
            "corrected_str": None,
            "intent": None,
            "response": None
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