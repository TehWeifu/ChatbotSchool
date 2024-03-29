# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionInformClassSchedule(Action):

    def name(self) -> Text:
        return "action_inform_class_schedule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        schedule_type = tracker.get_slot("schedule_type")

        if schedule_type == "morning":
            message = "Las clases en turno de mañana comienzan a las 8:15 a.m."
        elif schedule_type == "afternoon":
            message = "Las clases en turno de tarde comienzan a las 2:00 p.m."
        else:
            message = "Por favor, especifica si deseas conocer el horario de la mañana o de la tarde."

        dispatcher.utter_message(text=message)

        return []
