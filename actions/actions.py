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
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import Restarted
# from rasa_core_sdk.events import SlotSet

# class ActionCoronaTracker(Action):

#     def name(self) -> Text:
#         return "action_corona_tracker"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         response = requests.get("https://api.covid19india.org/data.json").json()
#         entities = tracker.latest_message['entities']
#         print("Last messag now ",entities)
#         state = None
     
#         for e in entities:
#             if e['entity'] == "state":
#                 state = e['value']

#         message="Please enter correct state name"

#         if state == "india":
#             state = "Total"
         
#         for data in response["statewise"]:
#             if data["state"] == state.title():
#                 print(data)      
#                 message = "Active:"+ data["active"] +" Confirmed:"+data["confirmed"]+" Recovered:"+data["recovered"]
        
        
#         dispatcher.utter_message(message)

#         return []
class ActionRestart(Action):
    
  def name(self) -> Text:
      return "action_restart"

  async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
  ) -> List[Dict[Text, Any]]:

      # custom behavior

      return [Restarted()]
class ActionCovidFacility(FormAction):
    
    def name(self) -> Text:
        return "facility_form"
    @staticmethod
    def required_slots(tracker:Tracker)->List[Text]:
        """A list of required slots that the form has to fill"""

        print("required_slots(tracker:Tracker)")
        return ["facility","location"]

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
            baseURL="https://twitter.com/search?q="
            latest="&f=live"
            URL=baseURL
            resource=tracker.get_slot('facility').lower()
            city=tracker.get_slot('location').lower()

            if resource=="bed" or resource=="beds":
               URL=baseURL+"verified+"+city+"+(bed+OR+beds)"+latest
               print(URL)

            elif resource=="O2" or resource=="oxygen" or resource=="oxy":
                URL=baseURL+"verified+"+city+"+(oxygen)"+latest
                print(URL)

            elif resource=="icu":
                URL=baseURL+"verified+"+city+"+(icu)"+latest
                print(URL)

            elif resource=="ventilator" or resource=="ventilators" :
                URL=baseURL+"verified+"+city+"+(ventilator+OR+ventilators)"+latest
                print(URL)

            elif resource=="plasma":
                URL=baseURL+"verified+"+city+"+(plasma)"+latest
                print(URL)

            elif resource=="remdesivir" or resource=="remdesivir":
                URL=baseURL+"verified+"+city+"+(remdesivir)"+latest
                print(URL)

            elif resource=="food" or resource=="tiffin":
                URL=baseURL+"verified+"+city+"+(tiffin+OR+food)"+latest
                print(URL)
            else:
                URL=baseURL+"covid19"+latest
                print(URL)    
            dispatcher.utter_message(response ="utter_slots_values")
            dispatcher.utter_message(response ="utter_submit")
            dispatcher.utter_message(text = URL)
            
            return [Restarted()]