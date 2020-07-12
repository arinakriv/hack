# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template
import dialogflow
import os
#import requests
import json
# import requests
import json
import os

import dialogflow
from flask import Flask, request, jsonify, render_template

#$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\username\Downloads\my-key.json"

url="https://arinakriv.github.io/testoviijsonmativashu.json"
app = Flask(__name__)
f = open('testoviijsonmativashu(2).json', 'r')
answersList = [0,0,1,2,3,2,1,2,3,0,1,2,3,3,0,1,1,2,2,0]

print('Credendtials from environ: {}'.format(
    os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')))

def explicit():
  from google.cloud import storage

  # Explicitly use service account credentials by specifying the private key
  # file.
  storage_client = storage.Client.from_service_account_json(
    'E:\\conda\\envs\\gputest\\datafliter\\abdulbot-tieaal-9c48d9c9cf5f.json')

  # Make an authenticated API request
  buckets = list(storage_client.list_buckets())
  print(buckets)


@app.route('/bot')
def bot():
   # explicit()
    return render_template('bot.html')

@app.route('/test')
def index():

    return render_template('index1.html')

@app.route('/get')
def root_response():
  d=open("testoviijsonmativashu.json",'r',encoding='utf-8')
  print(d)
 # with open("testoviijsonmativashu.json'", "w") as sf:
    #json.dumps(d)
  j=d.read()
  #print(j)
  jdata=json.loads(j)
  print(jdata)
  return jsonify(jdata)

@app.route('/answer')
def answer_response():
  counter=0

  l=request.data.split()
  for i in range(len(answersList)):
    if l[i]==answersList[i]:
      counter+=1

  ans=counter/len(answersList)


  return jsonify(ans)


@app.route('/webhook', methods=['POST'])
def webhook():
  data = request.get_json(silent=True)
  if data['queryResult']['queryText'] == 'yes':
    reply = {
      "fulfillmentText": "Ok. Будет сделано.",
    }
    return jsonify(reply)

  elif data['queryResult']['queryText'] == 'no':
    reply = {
      "fulfillmentText": 'Ок.Все отлично.',
    }
    return jsonify(reply)


def detect_intent_texts(project_id, session_id, text, language_code):
  session_client = dialogflow.SessionsClient()
  session = session_client.session_path(project_id, session_id)

  if text:
    text_input = dialogflow.types.TextInput(
      text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(
      session=session, query_input=query_input)
    return response.query_result.fulfillment_text


@app.route('/send_message', methods=['POST'])
def send_message():
  message = request.form['message']
  project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
  fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
  response_text = {"message": fulfillment_text}
  return jsonify(response_text)


#json.dumps(d)WWW


# @app.route('/api', methods=['POST', 'GET'])
# def api_response():
#     from flask import jsonify
#     if request.method == 'POST':
#         return jsonify(**testoviijsonmativashu.json)


if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=80)

