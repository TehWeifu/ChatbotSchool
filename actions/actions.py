import csv
from typing import Any, Text, Dict, List

import pandas as pd
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from tabulate import tabulate


# Single response #

# Professional families
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


# Schedule
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


# Extended response

# Scholarships
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


# Enrollment
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


# Access requirements
class ActionProvideAccessRequirements(Action):
    def name(self) -> Text:
        return "action_access_requirements"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        education_level = next(tracker.get_latest_entity_values("education_level"), None)
        education_level = education_level.lower()

        if education_level in ["grado medio", "fp medio", "ciclo formativo de grado medio", "cfgm"]:
            message = ("Para acceder a Grado Medio necesitas tener el título de ESO o haber superado la prueba de "
                       "acceso.")
        elif education_level in ["grado superior", "fp superior", "ciclo formativo de grado superior", "cfgs"]:
            message = "Para Grado Superior es necesario tener el título de Bachillerato o superar la prueba de acceso."
        else:
            message = ("Puedo informarte sobre los requisitos de acceso para Grado Medio y Grado Superior. ¿Cuál te "
                       "interesa?")

        dispatcher.utter_message(text=message)
        return []


# Multiple responses
# IT offer
class ActionGiveItModule(Action):
    def name(self) -> Text:
        return "action_give_it_module"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        df_modules = pd.read_csv('external_data/Groups.csv', encoding='utf-8', sep=';')
        list_unique_modules = df_modules['Nombre'].unique().tolist()

        response = f"Aquí están los módulos de informática disponibles:\n {', '.join(list_unique_modules)}"

        dispatcher.utter_message(text=response)
        return []


class ActionGiveItModuleTurns(Action):

    def name(self):
        return "action_give_it_module_turns"

    def run(self, dispatcher, tracker, domain):
        turns = {
            "D": "Diurno (Presencial)",
            "T": "Tarde (Presencial)"
        }

        it_module = tracker.get_slot('it_module')

        df_modules = pd.read_csv('external_data/Groups.csv', encoding='utf-8', sep=';')
        module_turn = df_modules[df_modules['Nombre'] == it_module]['Turno'].values[0]

        response = f"El módulo {it_module} se imparte en el turno de {turns[module_turn]}"

        dispatcher.utter_message(text=response)
        return []


class ActionGiveItModuleSubjects(Action):
    def name(self):
        return "action_give_it_module_subjects"

    def run(self, dispatcher, tracker, domain):
        it_module = tracker.get_slot('it_module')

        df_modules = pd.read_csv('external_data/Groups.csv', encoding='utf-8', sep=';')
        module_code = df_modules[df_modules['Nombre'] == it_module]['Grupo'].values[0]

        df_subjects = pd.read_csv('external_data/Modules.csv', encoding='utf-8', sep=';')
        modules_subjects_and_hours = df_subjects[df_subjects['Grupo'] == module_code][
            ['Nom_Cas_Modulo', 'HORAS']].values.tolist()

        subjects_formatted = tabulate(modules_subjects_and_hours, headers=['Asignatura', 'Horas'], tablefmt='pretty')
        response = f"Las asignaturas del módulo {it_module} son:\n{subjects_formatted}"

        dispatcher.utter_message(text=response)
        return []
