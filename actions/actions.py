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
# from actions.vaccine_api import get_for_seven_days
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import Restarted
from datetime import date
import requests 

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
            pincode=tracker.get_slot('pincode')
            city=tracker.get_slot('location').lower()
            # def getcity():

            #     url = "https://api.postalpincode.in/pincode/"+pincode
            #     #params = {"pincode": 495001, "date": start_date.strftime("%d-%m-%Y")}
            #     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
            #     resp = requests.get(url, headers=headers)
            #     data = resp.json()
            #     po=data[0]['PostOffice']
            #     return po[0]['Block']
            # city= getcity().replace(" ", "")

            print(city)

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

class ActionCovidVaccineSlot(FormAction):
    
    def name(self) -> Text:
        return "vaccine_form"
    @staticmethod
    def required_slots(tracker:Tracker)->List[Text]:
        """A list of required slots that the form has to fill"""

        print("required_slots(tracker:Tracker)")
        return ["pincode"]
    
    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
            pincode=tracker.get_slot('pincode')
            today = date.today()
            current_date=today.strftime("%d-%m-%Y")
            
            url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
            # baseurl=  "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin"
            params = {"pincode": pincode, "date": current_date}
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
            resp = requests.get(url, params=params, headers=headers)
            data = resp.json()
            message="Available Slots\n"
            for center in data["centers"]:
                for session in center["sessions"]:
                    name= center["name"]
                    date_current= session["date"]
                    vaccine=session["vaccine"]
                    dose_1_capacity= session["available_capacity_dose1"]
                    dose_2_capacity= session["available_capacity_dose2"]
                    age_limit= session["min_age_limit"]
                    if(dose_1_capacity>0 or dose_2_capacity>0):
                       message= message+"\nCenter Name: "+name+"\nDate: "+date_current+"\nDose 1 Available:"+str(dose_1_capacity)+"\nDose 2 Available:"+str(dose_2_capacity)+"\nVaccine: "+vaccine+"\nMin Age Limit :"+str(age_limit)
            # age=tracker.get_slot('age')
           
            # current_date=today.strftime("%d-%m-%Y")
            # data=get_for_seven_days(today,pincode)
            print(data)
            if message=="Available Slots\n":
                message="Sorry ! No Available Slots."
            dispatcher.utter_message(message)
            
            return [Restarted()]