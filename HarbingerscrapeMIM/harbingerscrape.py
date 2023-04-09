import os
import datetime
import urllib
import urllib.request
import http
import re
from <redacted> import Email 
import json
import subprocess
from typing import Any, Union, Tuple, Dict
from pprint import pprint

# <Redacted>
# Code belongs to @alekhyal 
class harbingerScrape(object):
    smUrl = object
    def __init__(self, eventID, amsAction, customerImpact, chimeBridge):
      self.smUrl = None
      self.requrl = None
      self.filename = None
      self.eventID = eventID
      self.amsAction = amsAction
      self.customerImpact = customerImpact
      self.chimeBridge = chimeBridge
      self.services = set()
      self.regions = set()
      self.message = []
      self.arn_list = []
      self.regionDict = {'bom': 'ap-south-1',
                         'cmh': 'us-east-2',
                         'dca': 'us-iso-east-1',
                         'dub': 'eu-west-1',
                         'fra': 'eu-central-1',
                         'global': 'Global',
                         'gru': 'sa-east-1',
                         'iad': 'us-east-1',
                         'icn': 'ap-northeast-2',
                         'kix': 'ap-northeast-3',
                         'lhr': 'eu-west-2',
                         'nrt': 'ap-northeast-1',
                         'pdx': 'us-west-2',
                         'sfo': 'us-west-1',
                         'cdg': 'use-west-3',
                         'sin': 'ap-southeast-1',
                         'syd': 'ap-southeast-2',
                         'yul': 'ca-central-1'}

    def openFile(self):
        with open(self.filename, 'rt') as myfile:
          for line in myfile:
              #print("=================================================================")
              if len(line)>3:
                  self.smUrl = line
                  File = self.openUrl(self.smUrl)
                  if type(File) == str:
                      print("This URL doesnt open:",self.smUrl)
                      return File
                  d = json.loads(File)
                  dict = {}
                  dict1 = {"Service: ": d["data"]["events"][0]["service"],
                           "StartTime: ": d["data"]["events"][0]["startTime"],
                           "EndTime: ": d["data"]["events"][0]["endTime"],
                            "Region: ": d["data"]["events"][0]["region"],
                            "Message: ": d["data"]["events"][0]["metadata"]["apiMessage"]
                            }
                  self.services.add(d["data"]["events"][0]["service"]) 
                  if d["data"]["events"][0]["region"] in self.regionDict.keys():
                    self.regions.add(self.regionDict[d["data"]["events"][0]["region"]])
                  else:
                    self.regions.add(d["data"]["events"][0]["region"])
                  if d["data"]["events"][0]["metadata"]["apiMessage"] is None:
                    pass
                  else:
                    self.message.append(d["data"]["events"][0]["metadata"]["apiMessage"])
                  #pprint(dict1)
                  #for k, v in dict1.items():
                      #print("{:<10} {:<10}".format(k, v))

              else:
                  break
        return dict1
    
    def verifyUrl(self, url) -> object:
        try:
            self.requrl = urllib.request.urlopen(url)
            return "works1"
        except (urllib.error.HTTPError, urllib.error.URLError, http.client.HTTPException) as e:
            if "HTTPError" in str(e):
                return "Cant open the url. HTTPError ", e.status, datetime.datetime.now()
            else:
                return "Cant open the page because the page can not be reached. Error ", datetime.datetime.now() 

    def openUrl(self, url): 
        if self.verifyUrl(url) == "works1":
            cmd = "kcurl '"+url+"' -L -s | python3 -m json.tool"
            cmd = ''.join(line.strip("\n") for line in cmd)
            File = subprocess.check_output(cmd, shell=True)
            return File
        else:
            return self.verifyurl(url)

    def getMIMSIM(self):
        URL = "kcurl '<redacted>"+self.eventID+"%22&sort=lastUpdatedConversationDate+desc&rows=500&omitPath=conversation&maxis%3Aheader%3AAmzn-Version=1.0' -s|python3 -m json.tool|"
        URL1 = """jq '.documents | .[].aliases |.[].id|select(. | contains("MC-PROD"))' |awk -F'"' '{print "<redacted>/"$2}'"""
        cmd = URL+URL1
        File = subprocess.check_output(cmd, shell=True)
        list = File.decode('UTF-8')
        return list

    def sendEmail(self, receiving_dict):
        # <redacted>
        # <redacted>
        me = os.getlogin()
        em = Email(
            from_=f"<redacted>", #security concern
            to=f"<redacted>",
            cc=f"",
            bcc="",
            subject="[MIM Event] Harbinger Event: "+self.eventID,
            body="""\
                <html>
                  <head></head>
                  <body>
                    <p>
                 <table border = "1" width = 700>
                 <col style="width:25%">
                  <tr>
                    <td>Title:</td>
                    <td>"""+ receiving_dict['Title: '] + """</td>
                  </tr>
                  <tr>
                    <td>Harbinger Link:</td>
                    <td>"""+ receiving_dict['Harbinger Link: '] + """</td>
                  </tr>
                  <tr>
                    <td>Event start time [PST]:</td>
                    <td>"""+ receiving_dict['Event start time: '] + """</td>
                  </tr>
                  <tr>
                    <td>MIM SIM:</td>
                    <td>"""+ receiving_dict['MIM SIM: '] + """</td>
                  </tr>
                  <tr>
                    <td>Services:</td>
                    <td>"""+ self.getAffectedServices() + """</td>
                  </tr>
                  <tr>
                    <td>Regions:</td>
                    <td>"""+ receiving_dict['Regions: '] + """</td>
                  </tr>
                  <tr>
                    <td>Root Cause:</td>
                    <td>"""+ receiving_dict['Root Cause: '] + """</td>
                  </tr>
                  <tr>
                    <td>Status:</td>
                    <td>"""+ receiving_dict['Status: '] + """</td>
                  </tr>
                  <tr>
                    <td>AMS Action Plan:</td>
                    <td>"""+ self.amsAction + """</td>
                  </tr>
                  <tr>
                  <tr>
                    <td>Customer Impact:</td>
                    <td>"""+ self.customerImpact + """</td>
                  </tr>
                  <tr>
                  <tr>
                    <td>Chime Bridge:</td>
                    <td>"""+ self.chimeBridge + """</td>
                  </tr>
                  <tr>
                    <td>Recent Update [PST]:</td>
                    <td>"""+ receiving_dict['Recent Update: '] + """</td>
                  </tr>
                  <tr>
                    <td>Notification Sent to:</td>
                    <td>"""+ receiving_dict['Notification Sent to: '] + """</td>
                  </tr>
                  <tr>
                    <td>Latest Harbinger message:</td>
                    <td>"""+ receiving_dict['Latest message: '] + """</td>
                  </tr>
                </table> 
                  </body>
                </html>
                """,                         
        )
        try:
            em.send(is_html=True)
                # If the is_html argument is set to True, HTML mail can be sent.
        finally:
            em.close()

    def splitMessage(self, message):
        end = len(message)-1
        result = ''
        for i in range(0, end):
            if i == end:
                result += message[i]
            if i < end:
                if i in [80, 160, 240, 320, 400, 480]:
                    result += message[i]+"\n"
                else:
                    result += message[i]
        return result

    def checkPosts(self):
        text =  " kcurl <redacted>/"+self.eventID
        text2 = """/refresh_partial/customer_communication -L -s | grep '/silvermine/'"""
        cmd = text+text2
        try:
          File = subprocess.check_output(cmd, shell=True)
          html_text = File.decode('UTF-8')
          html_text = html_text.split('"')
          for text in html_text:
            if text.startswith("<redacted>"):
              self.arn_list.append(text.split("/silvermine/")[1])
            elif text.startswith("/silvermine/arn"):
              self.arn_list.append(text.split("/silvermine/")[1])
          return None
        except Exception:
          return None   
    
    def getAffectedServices(self):
        text = " kcurl <redacted>/"+self.eventID
        text2 = """/refresh_partial/event_details -L -s | grep '/services/'"""
        cmd = text+text2
        try:
          File = subprocess.check_output(cmd, shell=True)
          html_text = File.decode('UTF-8')
          html_text = html_text.split('"')
          html_text1 = []
          for text in html_text:
            if text.startswith("/services"):
              html_text1.append(text.split("/services/")[1])
          html_string = ",".join(html_text1)
          return html_string
        except Exception:
          return None       

    def openHarbinger(self):
        URL = "<redacted>"+self.eventID
        File = self.openUrl(URL)
        jsonFile = json.loads(File)
        MIM = self.getMIMSIM()
        self.checkPosts()
        if "error" in jsonFile:
            print("The event does not exist anymore. Please verify if the harbinger has been aggregated.")
            return None
        self.filename = os.path.expanduser( '~/HarbingerscrapeMIM/phdFile.txt' )
        with open(self.filename, 'w') as f:
            pass
        with open(self.filename, 'a') as f:
            for i in self.arn_list:
                f.write("<redacted>="+i+"\n")
        if os.path.getsize(self.filename) == 0:
            print("\nThere are no PHD posts for this harbinger yet. Please go to the harbinger console to verify more info: <redacted>"+self.eventID)
            return None      
        self.openFile()
        a = self.message[0].split("[")
        result = self.splitMessage(a[len(a)-1])
        dict2 = {"Title: ": jsonFile["title"],
                 "Harbinger Link: ": "<redacted>/"+self.eventID,
                 "Event start time: ": jsonFile["event_start_time"],
                 "MIM SIM: ": MIM,
                 "Services: ": str(list(self.services)),
                 "Regions: ": str(list(self.regions)),
                 "Root Cause: ": jsonFile["root_cause"],
                 "Status: ": jsonFile["status"],
                 "Recent Update: ": jsonFile["updated_at"],
                 "Notification Sent to: ": "<redacted>",
                 "Latest message: ": result
        }
        self.sendEmail(dict2)
        return dict2

