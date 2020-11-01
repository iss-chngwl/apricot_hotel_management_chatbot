from chatbot_agent import agent_jarvis2
from slack import RTMClient
import pandas as pd

#database = pd.read_csv("./Data/demo_reviews (edited cols).csv", header=0, index_col=0)
jarv = agent_jarvis2()

@RTMClient.run_on(event="message")
def say_hello(**payload):
  data = payload['data']
  web_client = payload['web_client']
  if 'text' in data:
    print(data['text'])
    channel_id = data['channel']
    thread_ts = data['ts']
    user = data['user'] # This is not username but user ID (the format is either U*** or W***)
    response = jarv.run(data['text'])

    web_client.chat_postMessage(
      channel=channel_id,
      text=response,
      thread_ts=thread_ts
    )

slack_token = 'paste_your_token_here'
rtm_client = RTMClient(
  token=slack_token,
  connect_method='rtm.start'
)
rtm_client.start()