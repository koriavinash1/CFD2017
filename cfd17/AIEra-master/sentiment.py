import urllib
import json, api_key
from httplib import HTTPSConnection

headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '5f7318b1fe99429d819a307d752c6deb'
}

# Returns sentiment between 0 and 1, 1 indicating a positive sentence, 0 indicating negative
def getSentiment(message):
    
    documents = { 'documents': [
        { 'id': '0', 'language': 'en', 'text': message }
        ]}

    try:
        conn = HTTPSConnection('westus.api.cognitive.microsoft.com')
        print('1')
        conn.connect()
        print('2')
        conn.request("POST", '/text/analytics/v2.0/sentiment', json.dumps(documents), headers)
        print('3')
        response = conn.getresponse()
        print('4')
        return json.dumps(json.loads(response.read()))
        data = json.loads(response.read().decode())
        print('5')
        score = data['documents'][0]['score'];
        print('6')
        conn.close()
        print('7')
        #return score;
    except Exception as e: #Error occurred, just assume 0.5 sentiment
        print(e)
        #return 0.5;

