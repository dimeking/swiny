"""
This demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions will be publsihed.

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Skill Swiny. " \
                    "Please tell me a phrase that you want hear in pig latin by saying like, " \
                    "What's Fake News in pig latin."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me a phrase that you want hear in pig latin by saying like, " \
                    "What's Good Morning in pig latin."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skill Swiny. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def is_vowel(letter):
    vowels = ["a", "e", "i", "o", "u"]
    return letter.lower() in vowels

def to_piglatin(session_attributes, english_phrase):

    phrase = ""
    if not english_phrase:
        return "Swiny"

    words = english_phrase.split()
    for word in words:
        for letter in word:
            if is_vowel(letter): 
                index = word.index(letter)
                if index == 0:
                    phrase = phrase + " " + word + " yay"
                else:
                    phrase = phrase + " " + word[index:] + " " + word[:index] + "ay"
                break

      
    return phrase.lstrip()

def to_english(session_attributes, piglatin_phrase):

    phrase = ""
    if not piglatin_phrase:
        return "Swiny"
        
        
    return phrase


def to_piglatin_in_session(intent, session):
    """ Translates English to Pig Latin in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = session.get('attributes', {})
    should_end_session = False

    if 'Phrase' in intent['slots']:
        phrase = intent['slots']['Phrase']['value']
        piglatin_phrase = to_piglatin(session_attributes, phrase)
        speech_output = "In Pig Latin it sounds like, " + piglatin_phrase
    else:
        speech_output = "I didn't understand that. Try again by saying like, " \
                        "What's Virtual Reality in pig latin."


    reprompt_text = "Tell me a phrase that you want hear in pig latin by saying like, " \
                    "What's Good Morning in pig latin."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def to_english_in_session(intent, session):
    """ Translates Pig Latin to English in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = session.get('attributes', {})
    should_end_session = False

    if 'Phrase' in intent['slots']:
        phrase = intent['slots']['Phrase']['value']
        english_phrase = to_english(session_attributes, phrase)
        speech_output = "In English should sound like, " + english_phrase
    else:
        speech_output = "I didn't understand that. Try again by saying like, " \
                        "What's ue tray ove lay in pig latin."


    reprompt_text = "Tell me a phrase that you want hear in pig latin by saying like, " \
                    "What's ake way up yay in pig latin."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "ToPigLatinIsIntent":
        return to_piglatin_in_session(intent, session)
    elif intent_name == "ToEnglishIsIntent":
        return to_english_in_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] !=
             "amzn1.ask.skill.b4a4ac73-cc86-4975-89a8-45f76f20dfd5"):
         raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
