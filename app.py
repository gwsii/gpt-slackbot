import os
from time import sleep
from slack_bolt import App
from openai import OpenAI

openaiClient = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    # api_key="My API Key",
)

def complete_chat(messages):
    chat_completion = openaiClient.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo",
    )

    return chat_completion.choices[0].message.content

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

def respond_in_thread(ack, say, event, bot_user_id):
    print(bot_user_id)
    print(event)
    ack()
    # sleep(10)
    ts = event['thread_ts'] if 'thread_ts' in event else event['ts']
    # print(app.client.conversations_replies(channel=event['channel'], ts=ts))
    messages = []
    while True:
        messagesPage = app.client.conversations_replies(channel=event['channel'], ts=ts)
        # print(messagesPage)
        messages += messagesPage['messages']
        if not messagesPage['has_more']:
            break
        ts = messagesPage['messages'][-1]['ts']

    openaiMessages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    for message in messages:
        # print(message)
        print(f"{message['user']}: {message['text']}")
        if not 'text' in message:
            continue
        if message['user'] == bot_user_id:
            openaiMessages.append({"role": "assistant", "content": message['text']})
        else:
            openaiMessages.append({"role": "user", "content": message['text']})

    print(openaiMessages)

    ai_response = complete_chat(openaiMessages)

    say(ai_response, thread_ts=ts)


@app.event("message")
def handle_direct_message_events(ack, say, event, bot_user_id):
    respond_in_thread(ack, say, event, bot_user_id)

@app.event("app_mention")
def handle_app_mentions(ack, say, event, bot_user_id):
    respond_in_thread(ack, say, event, bot_user_id)

@app.event("app_home_opened")
def update_home_tab(client, event, logger, ack):
  ack()
  print(event)
  try:
    # views.publish is the method that your app uses to push a view to the Home tab
    client.views_publish(
      # the user that opened your app's app home
      user_id=event["user"],
      # the view object that appears in the app home
      view={
        "type": "home",
        "callback_id": "home_view",

        # body of the view
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Welcome to your _App's Home_* :tada:"
            }
          },
          {
            "type": "divider"
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app."
            }
          },
          {
            "type": "actions",
            "elements": [
              {
                "type": "button",
                "text": {
                  "type": "plain_text",
                  "text": "Click me!"
                }
              }
            ]
          }
        ]
      }
    )

  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 5000)))