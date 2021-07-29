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
from bs4 import BeautifulSoup
import urllib
import urllib.request
import csv
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

class ActionRestart(Action):
    
  def name(self) -> Text:
      return "action_restart"

  async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
  ) -> List[Dict[Text, Any]]:
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

            # elif resource=="food" or resource=="tiffin":
            #     URL=baseURL+"verified+"+city+"+(tiffin+OR+food)"+latest
            #     print(URL)
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


class ActionJustdialServices(FormAction):
    
    def name(self) -> Text:
        return "justdial_services_form"
    @staticmethod
    def required_slots(tracker:Tracker)->List[Text]:
        """A list of required slots that the form has to fill"""

        print("required_slots(tracker:Tracker)")
        return ["justdial","location"]
    
    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
            service=tracker.get_slot('justdial').lower()
            city=tracker.get_slot('location').lower()
            message=justdialscrap(city,service)
            print(message)
            message=sorted(message.items())
            st=""

            for key,val in message:
                st = st + key +": " + str(val)+"\n "

            # dispatcher.utter_message(response ="utter_submit")
            dispatcher.utter_message(text = st)
            
            
            return [Restarted()]

def innerHTML(element):
    return element.decode_contents(formatter="html")

def get_name(body):
	return body.find('span', {'class':'jcn'}).a.string

def which_digit(html):
    mappingDict={'icon-ji':9,
                'icon-dc':'+',
                'icon-fe':'(',
                'icon-hg':')',
                'icon-ba':'-',
                'icon-lk':8,
                'icon-nm':7,
                'icon-po':6,
                'icon-rq':5,
                'icon-ts':4,
                'icon-vu':3,
                'icon-wx':2,
                'icon-yz':1,
                'icon-acb':0,
                }
    return mappingDict.get(html,'')

def get_phone_number(body):
    i=0
    phoneNo = "No Number!"
    try:
            
        for item in body.find('p',{'class':'contact-info'}):
            i+=1
            if(i==2):
                phoneNo=''
                try:
                    for element in item.find_all(class_=True):
                        classes = []
                        classes.extend(element["class"])
                        phoneNo+=str((which_digit(classes[1])))
                except:
                    pass
    except:
        pass
    body = body['data-href']
    soup = BeautifulSoup(body, 'html.parser')
    for a in soup.find_all('a', {"id":"whatsapptriggeer"} ):
        # print (a)
        phoneNo = str(a['href'][-10:])


    return phoneNo


def get_rating(body):
	rating = 0.0
	text = body.find('span', {'class':'star_m'})
	if text is not None:
		for item in text:
			rating += float(item['class'][0][1:])/10

	return rating

def get_rating_count(body):
	text = body.find('span', {'class':'rt_count'}).string

	# Get only digits
	rating_count =''.join(i for i in text if i.isdigit())
	return rating_count

def get_address(body):
	return body.find('span', {'class':'mrehover'}).text.strip()

def get_location(body):
	text = body.find('a', {'class':'rsmap'})
	if text == None:
		return
	text_list = text['onclick'].split(",")
	
	latitutde = text_list[3].strip().replace("'", "")
	longitude = text_list[4].strip().replace("'", "")
	
	return latitutde + ", " + longitude

def justdialscrap(uloc,want):

    page_number = 1
    service_count = 1


    fields = ['Name', 'Phone', 'Rating', 'Rating Count', 'Address', 'Location']
    out_file = open('hardware.csv','w')
    csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)
    phone_data={}
    # Write fields first
    #csvwriter.writerow(dict((fn,fn) for fn in fields))

    while True:
        # Check if reached end of result
        if page_number > 1:
            break
        url="https://www.justdial.com/"    

        if want=="ambulance" :
             url=url+uloc+"/ambulanceservices"
        elif want=="tiffin" or want=="food" or want=="breakfast" or want=="lunch" or want =="dinner":
             url=url+uloc+"/tiffinservices"
        

       
        
        req = urllib.request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}) 
        page = urllib.request.urlopen( req )
        #page=urllib2.urlopen(url)

        soup = BeautifulSoup(page.read(), "html.parser")
        services = soup.find_all('li', {'class': 'cntanr'})

        #Iterate through the 10 results in the page
        for service_html in services[:3]:
            dict_service = {}
            name = get_name(service_html)
            #print(name);
            phone = get_phone_number(service_html)
            rating = get_rating(service_html)
            count = get_rating_count(service_html)
            address = get_address(service_html)
            location = get_location(service_html)
            if name != None:
                dict_service['Name'] = name
                if phone != None:
                    #print('getting phone number')
                    dict_service['Phone'] = phone
                if rating != None:
                    dict_service['Rating'] = rating
                if count != None:
                    dict_service['Rating Count'] = count
                if address != None:
                    dict_service['Address'] = address
                if location != None:
                    dict_service['Address'] = location

           

            # Write row to CSV
            phone_data[name]=phone
            csvwriter.writerow(dict_service)
             
                    
            #print("#" + str(service_count) + " " , dict_service)
        service_count += 1

        page_number += 1

    out_file.close()
    return phone_data