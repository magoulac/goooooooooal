import os
import requests
from slackclient import SlackClient

SLACK_API_TOKEN = os.environ.get("SLACK_API_TOKEN")
slack_client = SlackClient(SLACK_API_TOKEN)

def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call.get('ok'):
        return channels_call['channels']
    return None

def channel_info(channel_id):
    channel_info = slack_client.api_call("channels.info", channel=channel_id)
    if channel_info:
        return channel_info['channel']
    return None

def send_message(channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='worldcup-bot',
        icon_emoji=':soccer:'
    )
def delete_message(channel_id, message_ts):
    slack_client.api_call(
        "chat.delete",
        channel=channel_id,
        ts=message_ts
    )
    
if __name__ == '__main__':
    channels = list_channels()
    if channels:
        print("Channels: ")
        for channel in channels:
            if(channel['name'] != 'testmatchbot'):
                print(channel['name'] + " (" + channel['id'] + ")")
                detailed_info = channel_info(channel['id'])
                if detailed_info:
                    print('Latest text from ' + channel['name'] + ":")
                    print(detailed_info['latest']['text'])                
                    if channel['name'] == 'general':
                        all_history = slack_client.api_call("channels.history", channel=channel['id'])
                        response = requests.get("http://worldcup.sfg.io/matches/today")
                        data = response.json()
                        mystring = "Today's matches are: \n"
                        for i in data:
                            mystring = mystring + i['home_team']['code'] + "vs" + i['away_team']['code'] + '\n'
                        print(mystring)
                        print(slack_client.api_call("api.test"))
                        
                        #delete_message(channel['id'],'1529546162.000205')
                        #send_message(channel['id'],mystring)
                        #for x in all_history['messages']:
                        #    print(x)
                        
                            #    send_message(channel['id'], "Hello " + channel['name'] + "! I changed my emoji!")            
        print('-----')

    else:
        print("Unable to authenticate.")

