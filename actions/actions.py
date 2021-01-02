from typing import Any, Text, Dict, List
import logging
import requests
import os
import json
from .rxid_search import rxid_search_util
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

_rx_id_url = os.environ.get('RXID_DRUG_SEARCH_URL')
_rx_id_api_key = os.environ.get('RXID_DRUG_SEARCH_API_KEY')

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
        search_confirmation_message = "Performing search for {name}."
        dispatcher.utter_message(text=search_confirmation_message.format(name=slots["drug_name"]))

        ## Perform search
        search_url = _rx_id_url + '/dev/drug/search/getRxIdentifier?drugName=' + slots["drug_name"]
        search_response = requests.get(search_url, headers={"x-api-key":_rx_id_api_key})
        if search_response.status_code == 200:
            # The search was successful
            response_content = json.loads(search_response.content)["identifier"]["nlmRxImages"]

            # Check to see if more than one match came back
            search_success_message = rxid_search_util.is_multiple_match(self, search_results=response_content)
            dispatcher.utter_message(text=search_success_message.format(name=slots["drug_name"], response=response_content[0], matches=len(response_content)))
        else:
            # The search was unsuccessful
            search_failure_message = "The search for {name} was unsuccessful. The error was {error}"
            dispatcher.utter_message(text=search_failure_message.format(name=slots["drug_name"], error=search_response.content))

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

        ## Perform search
        # TODO: Convert the drug imprint to numerical format: https://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers
        search_url = _rx_id_url + '/dev/drug/search/getRxIdentifier?drugColor=' + slots["drug_color"] + '&drugShape=' + slots["drug_shape"] + '&drugImprint=' + slots["drug_imprint"]
        search_response = requests.get(search_url, headers={"x-api-key":_rx_id_api_key})
        search_url_message = "{url}"
        dispatcher.utter_message(text=search_url_message.format(url=search_url))
        if search_response.status_code == 200:
            # The search was successful
            #response_content = json.loads(search_response.content)["identifier"]["nlmRxImages"]

            # Check to see if more than one match came back
            search_success_message = "{response}"#rxid_search_util.is_multiple_match(self, search_results=response_content)
            dispatcher.utter_message(text=search_success_message.format(response=json.loads(search_response.content)))
        else:
            # The search was unsuccessful
            search_failure_message = "The search for a prescription with was unsuccessful. The error was {error}"
            dispatcher.utter_message(text=search_failure_message.format(error=search_response.content))

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