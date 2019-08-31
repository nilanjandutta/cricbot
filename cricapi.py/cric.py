import requests
from datetime import datetime


class ScoreGet:  # defining a class
    def __init__(self):  # creating an constructor with an object name self as first parameter
        self.url_get_all_matches = " http://cricapi.com/api/matches"  # creating variables stroing different api values
        self.get_score = "http://cricapi.com/api/cricketScore"
        self.apikey = "jWhf6Gz8xmdRlaZfHFWHzR9QbWN2"
        self.unique_id = ""

    def get_unique_id(self):  # creating a function for fetching the unique id
        uri_params = {"apikey":self.apikey}
        resp = requests.get(self.url_get_all_matches,params=uri_params)
        resp_dict=resp.json()
        uid_found=0

        for i in resp_dict['matches']:
            if (i['team-1']=="West Indies" or i['team-2']=="India" and i['matchStarted']):
                todays_date = datetime.today().strftime('%Y-%m-%d')
                if todays_date==i['date'].split("T")[0]:
                    self.unique_id=i['unique_id']
                    uid_found=1
                    break

        if not uid_found:
            self.unique_id=-1

        send_data=self.get_score_current(self.unique_id)
        return send_data

    def get_score_current(self,unique_id):
        data=""
        if unique_id==-1:
            data="No India Matches today"
        else:
            uri_params={"apikey":self.apikey,"unique_id":unique_id}
            resp=requests.get(self.get_score,params=uri_params)
            data_json=resp.json()
            try:
                data="Here's the Score:  \n"+data_json['stat']+"\n"['score']
            except KeyError as e:
                print(e)

        return data

if __name__=="__main__":
    obj_score=ScoreGet()
    whatsapp_message=obj_score.get_unique_id()
    from twilio.rest import Client
    a_sid="AC3692d1b7fa2ecfe35ae4cf3d4b3a7b1c"
    auth_token="990cead45a2627532fd7bc4bdcef3443"
    client = Client(a_sid,auth_token)
    message = client.messages.create(body=whatsapp_message, from_='whatsapp:+14155238886', to='whatsapp:+919758315640')


