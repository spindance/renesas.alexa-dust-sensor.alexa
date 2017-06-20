import Alexa
import Analytics

def build_response(output):
    """Build JSON Alexa response"""
    return {
        'version': '1.0',
        'sessionAttributes': {},
        'response' : {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output
            },
            'card': {
                'type': 'Simple',
                'title': 'Brainy Office',
                'content': output
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': ""
                }
            },
            'shouldEndSession': True
        }
    }

def get_response_txt(request):
    """Get the response text from handling the Alexa request"""
    if request['type'] == 'IntentRequest':
        if request['intent']['name'] == 'SensorStatusIntent':
            sensor_selection = request['intent']['slots']['Sensor_Selection'].get('value')
            if sensor_selection == 'air quality':
                tag_name = "processed.qualitative_air_quality"
                val = Analytics.last_n_values(tag_name, 1)
                if val:
                    return "The most recent " + sensor_selection + " is " + str(val[0][tag_name])
                return "I could not find any recent " + sensor_selection + " values"
    return "I cannot find the information you are requesting"

def handle_event():
    """Handle the Alexa request event"""
    event = IONode.get_event()
    request = event['request']
    uuid_marker = event.get("uuid", "")
    response_txt = get_response_txt(request)
    response_json = build_response(response_txt)
    log(response_json)
    Alexa.response(uuid_marker, response_json)

handle_event()
