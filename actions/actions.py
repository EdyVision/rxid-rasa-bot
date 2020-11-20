# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import logging
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    SlotSet,
    EventType,
    ActionExecuted,
    SessionStarted,
    Restarted,
    FollowupAction,
    UserUtteranceReverted,
)

logger = logging.getLogger(__name__)

class ActionIdentifyDrug(Action):

    def name(self) -> Text:
        return "action_identify_drug"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Executes the full drug search action"""

        ## Confirm search for user
        # search_confirmation = "Performing search for {color} pill with a {shape} shape and imprint of {imprint}."
        dispatcher.utter_message("Ok, I can help with that. I'll need some information from you first. What is the color of the pill?")

        return []

class ActionSearchDrugByName(Action):

    def name(self) -> Text:
        return "action_search_drug_by_name"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Executes the drug search by name"""

        slots = {
            "drug_name": None,
        }

        ## Get slots for drug identification search
        slots["drug_name"] = tracker.get_slot("drug_name")

        ## Confirm search for user
        search_confirmation = "Performing search for {name}."
        dispatcher.utter_message(text=search_confirmation.format(name=slots["drug_name"]))

        return [SlotSet(slot, value) for slot, value in slots.items()]


class ActionIdentifyDrugFullSearch(Action):

    def name(self) -> Text:
        return "action_identify_drug_full_search"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Executes the full drug search action"""

        slots = {
            "drug_color": None,
            "drug_shape": None,
            "drug_imprint": None,
        }

        ## Get slots for drug identification search
        slots["drug_color"] = tracker.get_slot("drug_color")
        slots["drug_shape"] = tracker.get_slot("drug_shape")
        slots["drug_imprint"] = tracker.get_slot("drug_imprint")

        ## Confirm search for user
        search_confirmation = "Performing search for {color} pill with a {shape} shape and imprint of {imprint}."
        dispatcher.utter_message(text=search_confirmation.format(color=slots["drug_color"], shape=slots["drug_shape"], imprint=slots["drug_imprint"]))

        return [SlotSet(slot, value) for slot, value in slots.items()]

# This is intended to restart the session
class ActionRestart(Action):
    def name(self) -> Text:
        return "action_restart"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:

        return [Restarted(), FollowupAction("action_session_start")]