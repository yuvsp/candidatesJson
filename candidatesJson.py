import json
import logging
import datetime
import urllib.request
from colorama import init
init()
from colorama import Fore, Back, Style


# logging configurations
now = datetime.datetime.now().strftime("%Y-%m-%d")
logging.basicConfig(filename=f"log{now}.txt",    format='%(asctime)s %(levelname)-8s %(message)s',    level=logging.INFO,    datefmt='%Y-%m-%d %H:%M:%S',    filemode='a+')
logging.info(" - candidate extraction initiated")

# getting json data from url and converting to python object
def get_json(json_url):
    try:
        with urllib.request.urlopen(json_url) as url:
            data = json.loads(url.read().decode())
            logging.info("Online Json retrieved")
            print("Online Json retrieved")
            return data
    except:
        logging.error("Could not retrieve Online Json")
        print("Could not retrieve Online Json")
        return None

data = get_json("https://hs-recruiting-test-resume-data.s3.amazonaws.com/allcands-full-api_hub_b1f6-acde48001122.json")
print("_____\n\n")    

for candidate in data:
    print(f"Hello {candidate['contact_info']['name']['formatted_name']},\n")

    # Creating experience list
    experience = candidate['experience']
    experience_list = []
    for e in experience:
        # converting date string to python date object
        start_date = datetime.datetime.strptime(e['start_date'], '%b/%d/%Y')
        end_date = datetime.datetime.strptime(e['end_date'], '%b/%d/%Y')
        # saving list of relevant experience data as list-of-dicts
        experience_list.append({"start":start_date,"end":end_date,"title":e['title'],"location":e['location']['short_display_address']})
    
    # ordering list by dates
    orderd_list = sorted(experience_list, key=lambda d: d['start']) 
    
    # output: printing ordered list
    for i in range(len(orderd_list)):
        if i > 0:  # checking for gaps, starting from second workplace
            former_end = orderd_list[i-1]['end']
            current_start= orderd_list[i]['start']
            gap = current_start - former_end
            if gap.days > 1:
                gap_text = f" X Gap in CV for {gap.days} days"
                print (Fore.RED + gap_text + Style.RESET_ALL)
        print (f"Worked as {orderd_list[i].get('title')}, From {orderd_list[i].get('start').strftime('%b/%d/%Y')}, To {orderd_list[i].get('end').strftime('%b/%d/%Y')} in {orderd_list[i].get('location')}")
    if len(orderd_list) == 0:
        print (f" X No Experience records at all")
    print("------------------------------------------\n")


input("press any key...")



