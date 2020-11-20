# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionIdentifyDrug(Action):

#     def name(self) -> Text:
#         return "action_identify_drug"

#     def run(self, 
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         ## Get slots for drug identification search
#         drug_color = tracker.get_slot("drug_color")
#         drug_shape = tracker.get_slot("drug_shape")
#         drug_imprint = tracker.get_slot("drug_imprint")

#         ## Confirm search for user
#         search_confirmation = "Performing search for {color} pill with a {shape} shape and imprint of {imprint}."
#         dispatcher.utter_message(text=search_confirmation.format(color=drug_color, shape=drug_shape, imprint=drug_imprint))

#         return []

# This is intended to restart the session
# class ActionRestart(Action):
#     def name(self) -> Text:
#         return "action_restart"

#     async def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[EventType]:

#         return [Restarted(), FollowupAction("action_session_start")]