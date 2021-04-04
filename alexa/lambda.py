from os import environ
from time import time

import boto3

url = environ["SQS_URL"]
client = boto3.client('sqs',
                      aws_access_key_id=environ["AWS_KEY"],
                      aws_secret_access_key=environ["AWS_SECRET"])
beep = "<audio src='soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_neutral_response_01'/>"


def lambda_handler(event, context):
    print("*" * 30)
    print(event)
    print("*" * 30)

    if event['request']['type'] == "LaunchRequest":
        return call_rpi("rainbow", "Started the strip")
    elif event['request']['type'] == "IntentRequest":
        return intent_scheme(event)
    elif event['request']['type'] == "CanFulfillIntentRequest":
        return can_fulfill(event)
    elif event['request']['type'] == "SessionEndedRequest":
        print("Session Ended.")


def intent_scheme(event):
    intent_name = event['request']['intent']['name']

    if intent_name == "clear":
        return call_rpi("clear", "Clearing the strip")
    elif intent_name == "fire":
        return call_rpi("fire", "Fire mode")
    elif intent_name == "rainbow":
        return call_rpi("rainbow", "Rainbow mode")
    elif intent_name == "rainbow_color_wipe":
        return call_rpi("rainbow_color_wipe", "Rainbow color wipe mode")
    elif intent_name == "rainbow_fade":
        return call_rpi("rainbow_fade", "Rainbow fade mode")
    elif intent_name == "random_fade":
        return call_rpi("random_fade", "Random fade mode")
    elif intent_name == "snake_color":
        return call_rpi("snake_color", "Snake color mode")
    elif intent_name == "snake_fade":
        return call_rpi("snake_fade", "Snake fade mode")
    elif intent_name == "snake_rainbow":
        return call_rpi("snake_rainbow", "Snake rainbow mode")
    elif intent_name == "color":
        name = event['request']['intent']['slots']['color_name']['value']
        return call_rpi("static_color_name/" + name, "Color " + name)
    elif intent_name == "strobe":
        return call_rpi("strobe", "Strobe mode")
    elif intent_name in ["AMAZON.NoIntent", "AMAZON.StopIntent", "AMAZON.CancelIntent"]:
        return stop_the_skill()
    elif intent_name == "AMAZON.HelpIntent":
        return assistance()
    elif intent_name == "AMAZON.FallbackIntent":
        return fallback_call()


def call_rpi(sqs_message, card_title="", card_text="", answer=beep):
    response = client.send_message(
        QueueUrl=url,
        MessageBody=sqs_message,
        MessageDeduplicationId=str(int(round(time() * 1000))),
        MessageGroupId='lambda')

    if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        answer = card_text = "I couldn't do it"
        card_title = ""

    return output_json_builder(answer, card_text, card_title, end_session=True)


def stop_the_skill():
    return output_json_builder(card_title="Bye!", end_session=True)


def assistance():
    answer = "You can choose the following modes: clearn, fire, rainbow, rainbow color wipe, rainbow fade, " \
             "random fade, snake color, snake fade, snake rainbow, static color, strobe"
    return output_json_builder(answer, answer, "Help")


def fallback_call():
    answer = "I can't help you with that, ask for help by saying HELP."
    return output_json_builder(answer, answer)


def can_fulfill(event):
    return can_fulfill_builder("YES")


def ssml_builder(message):
    text_dict = dict()
    text_dict['type'] = 'SSML'
    text_dict['ssml'] = '<speak>' + message + '</speak>'
    return text_dict


def reprompt_builder(message):
    reprompt_dict = dict()
    reprompt_dict['outputSpeech'] = ssml_builder(message)
    return reprompt_dict


def card_builder(c_text, c_title):
    card_dict = dict()
    card_dict['type'] = "Simple"
    card_dict['title'] = c_title
    card_dict['content'] = c_text
    return card_dict


def response_field_builder(answer, card_text, card_title, reprompt, end_session):
    speech_dict = dict()
    speech_dict['outputSpeech'] = ssml_builder(answer)
    speech_dict['card'] = card_builder(card_text, card_title)
    speech_dict['reprompt'] = reprompt_builder(reprompt)
    speech_dict['shouldEndSession'] = end_session
    return speech_dict


def can_fulfill_builder(can_do_it):
    json_dict = dict()
    json_dict['version'] = '1.0'

    response_dict = dict()
    canfulfill_dict = dict()

    slots_dict = dict()
    slot1_dict = dict()

    slot1_dict['canUnderstand'] = "YES"
    slot1_dict['canFulfill'] = "YES"

    slots_dict['color_name'] = slot1_dict

    canfulfill_dict['slots'] = slots_dict
    canfulfill_dict['canFulfill'] = can_do_it

    response_dict['canFulfillIntent'] = canfulfill_dict
    json_dict['response'] = response_dict
    return json_dict


def output_json_builder(answer="", card_text="", card_title="", reprompt="", end_session=False):
    response_dict = dict()
    response_dict['version'] = '1.0'
    response_dict['response'] = response_field_builder(answer, card_text, card_title, reprompt, end_session)
    return response_dict
