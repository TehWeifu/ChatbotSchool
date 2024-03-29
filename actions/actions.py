# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import csv


class ActionProfessionalFamilies(Action):
    def name(self) -> Text:
        return "action_professional_families"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        families_list = "Aquí están las familias profesionales disponibles:\n"
        with open('external_data/Families.csv', mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                families_list += f"- {row['Family']}\n"

        dispatcher.utter_message(text=families_list)
        return []


class ActionSchedule(Action):
    def name(self) -> Text:
        return "action_schedule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        turn = tracker.get_slot("turn")
        if turn == "mañana":
            message = "Las clases de la mañana empiezan a las 8:00 y terminan a las 12:00."
        elif turn == "tarde":
            message = "Las clases de la tarde empiezan a las 13:00 y terminan a las 17:00."
        else:
            message = "Por favor, especifica si te interesan las clases de la mañana o de la tarde."

        dispatcher.utter_message(text=message)
        return []
