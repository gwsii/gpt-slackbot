import os
from time import sleep
from slack_bolt import App

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.event("message")
def handle_direct_message_events(ack, say, event, respond):
    print(event)
    ack()
    sleep(10)
    if 'thread_ts' in event:
        say(f"Thanks for your message: {event['text']}", thread_ts=event['thread_ts'])
    else:
        say(f"Thanks for your message: {event['text']}", thread_ts=event['ts'])

@app.event("app_mention")
def handle_app_mentions(ack, say, event, respond):
    print(event)
    ack()
    sleep(10)
    if 'thread_ts' in event:
        say(f"Thanks for your message: {event['text']}", thread_ts=event['thread_ts'])
    else:
        say(f"Thanks for your message: {event['text']}", thread_ts=event['ts'])
        # say(f"Thanks for your message: {event['text']}")

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