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
    speech_output = "Welcome to the Alexa Skill Fave Team. " \
                    "Please tell me your favorite team by saying like, " \
                    "my favorite football team is raiders"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your favorite team by saying like, " \
                    "my favorite football team is forty niners."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skill Fave Team. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def get_favorite_team_attributes(session_attributes, sport_name, favorite_team):

    if not session_attributes:
        session_attributes =  {}
        
    fave_sport_team_moniker = "favorite" + sport_name + "Team"
    session_attributes[fave_sport_team_moniker] = favorite_team
        
    return session_attributes


def set_team_in_session(intent, session):
    """ Sets the team in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = session.get('attributes', {})
    should_end_session = False

    if 'Team' in intent['slots'] and 'Sport' in intent['slots']:
        favorite_team = intent['slots']['Team']['value']
        sport_name = intent['slots']['Sport']['value']
        session_attributes = get_favorite_team_attributes(session_attributes, sport_name, favorite_team)
        speech_output = "I now know your favorite " + sport_name + " team is " + \
                        favorite_team + \
                        ". You can ask me your favorite team by saying like, " \
                        "what's my favorite baseball team?"
        reprompt_text = "You can ask me your favorite team by saying like, " \
                        "what's my favorite basketball team?"
    else:
        speech_output = "I'm not sure what your favorite team is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite team is. " \
                        "You can tell me your favorite team by saying like, " \
                        "my favorite ice hockey team is sharks."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_team_from_session(intent, session):
    session_attributes = session.get('attributes', {})
    reprompt_text = None

    if 'Sport' in intent['slots'] and intent['slots']['Sport']['value'] != 'favorite' :
        sport_name = intent['slots']['Sport']['value']
        fave_sport_team_moniker = "favorite" + sport_name + "Team"
        if session_attributes and fave_sport_team_moniker in session_attributes:
            favorite_team = session_attributes[fave_sport_team_moniker]
            speech_output = "Your favorite " + sport_name + " team is " + favorite_team + "."
            should_end_session = True
        else:
            speech_output = "I'm not sure what your favorite " + sport_name + " team is. " \
                            "You can say like, my favorite baseball team is giants."
            should_end_session = False
    else:
        speech_output = "I'm not sure which sport you are referring to. " \
                        "You can say like, what's my favorite baseball team."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


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
    if intent_name == "MyTeamIsIntent":
        return set_team_in_session(intent, session)
    elif intent_name == "WhatsMyTeamIntent":
        return get_team_from_session(intent, session)
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
