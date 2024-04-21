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

        turn = next(tracker.get_latest_entity_values("turn"), None)

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

        scholarship_subject = next(tracker.get_latest_entity_values("scholarship_subject"), None)

        if scholarship_subject in ["documentos", "documentación", "papeles", "requisitos"]:
            message = "Para la beca, necesitas tu DNI, certificado de notas, y el formulario de solicitud completado."
        elif scholarship_subject in ["plazo", "tiempo", "periodo"]:
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

        enrollment_subject = next(tracker.get_latest_entity_values("enrollment_subject"), None)

        if enrollment_subject in ["documentos", "documentación", "papeles", "requisitos"]:
            message = ("Para inscribirte, necesitas tu DNI, el certificado de estudios anteriores, y el formulario de "
                       "inscripción completado.")
            follow_up = "deadline"
        elif enrollment_subject in ["plazo", "tiempo", "periodo"]:
            message = "El plazo de inscripción para nuevos estudiantes termina el 30 de julio."
            follow_up = "documentation"
        else:
            message = ("Puedo proporcionarte información sobre la documentación necesaria y los plazos para la "
                       "inscripción. ¿Qué necesitas saber?")
            follow_up = None

        dispatcher.utter_message(text=message)

        return [SlotSet("enrollment_subject", follow_up)] if follow_up else []


class ActionProvideAccessRequirements(Action):
    def name(self) -> Text:
        return "action_access_requirements"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        education_level = next(tracker.get_latest_entity_values("education_level"), None)

        if education_level in ["Grado medio", "FP medio", "Ciclo formativo de grado medio", "CFGM"]:
            message = ("Para acceder a Grado Medio necesitas tener el título de ESO o haber superado la prueba de "
                       "acceso.")
        elif education_level in ["Grado superior", "FP superior", "Ciclo formativo de grado superior", "CFGS"]:
            message = "Para Grado Superior es necesario tener el título de Bachillerato o superar la prueba de acceso."
        else:
            message = ("Puedo informarte sobre los requisitos de acceso para Grado Medio y Grado Superior. ¿Cuál te "
                       "interesa?")

        dispatcher.utter_message(text=message)
        return []


class ActionGiveItModule(Action):
    def name(self) -> Text:
        return "action_give_it_module"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        module = next(tracker.get_latest_entity_values("it_module"), None)

        if module in ["programación", "informática"]:
            message = "El módulo de programación se imparte en el primer curso de Grado Superior de Desarrollo de Aplicaciones Multiplataforma."
        elif module in ["electricidad", "electrónica"]:
            message = "El módulo de electricidad se imparte en el primer curso de Grado Medio de Instalaciones Eléctricas y Automáticas."
        else:
            message = "No tengo información sobre ese módulo. ¿Te interesa algún otro?"

        dispatcher.utter_message(text=message)
        return []
