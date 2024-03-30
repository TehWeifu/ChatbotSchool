# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


import csv
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


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

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        turn = tracker.get_slot("turn")
        if turn == "mañana":
            message = "Las clases de la mañana empiezan a las 8:00 y terminan a las 14:00."
        elif turn == "tarde":
            message = "Las clases de la tarde empiezan a las 16:00 y terminan a las 20:00."
        else:
            message = "Por favor, especifica si te interesan las clases de la mañana o de la tarde."

        dispatcher.utter_message(text=message)
        return []


class ActionScholarship(Action):
    def name(self) -> Text:
        return "action_scholarship"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        subject = tracker.get_slot("scholarship_subject")

        if subject == "documentos":
            message = "Para la beca, necesitas tu DNI, certificado de notas, y el formulario de solicitud completado."
        elif subject == "plazo":
            message = "El plazo para solicitar becas termina el 30 de septiembre."
        else:
            message = ("Puedo proporcionarte información sobre la documentación necesaria y los plazos para las becas. "
                       "¿Qué necesitas saber?")

        dispatcher.utter_message(text=message)
        return []


class ActionEnrollment(Action):
    def name(self) -> Text:
        return "action_enrollment"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        subject = tracker.get_slot("enrollment_subject")

        if subject == "documentos":
            message = ("Para inscribirte, necesitas tu DNI, el certificado de estudios anteriores, y el formulario de "
                       "inscripción completado.")
            follow_up = "deadline"
        elif subject == "plazo":
            message = "El plazo de inscripción para nuevos estudiantes termina el 30 de julio."
            follow_up = "documentation"
        else:
            message = ("Puedo proporcionarte información sobre la documentación necesaria y los plazos para la "
                       "inscripción. ¿Qué necesitas saber?")
            follow_up = None

        dispatcher.utter_message(text=message)

        return [SlotSet("enrollment_subject", follow_up)] if follow_up else []
