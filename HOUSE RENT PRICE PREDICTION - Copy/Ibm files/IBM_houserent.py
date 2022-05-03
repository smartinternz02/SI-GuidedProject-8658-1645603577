import numpy as np
import pickle
from flask import Flask,request, render_template
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "_zH6cMcUfBEHT1fUd-9nfziqXv3EswlvHBXOY2areEbf"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
#payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}

#response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/ae2e7cb4-9a84-4dcf-91aa-0fd1ccb5cc61/predictions?version=2022-03-07', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
#print("Scoring response")
#print(response_scoring.json())
app=Flask(__name__,template_folder="templates")
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')
@app.route('/home', methods=['GET'])
def about():
    return render_template('home.html')
@app.route('/pred',methods=['GET'])
def page():
    return render_template('upload.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    input_features = [float(x) for x in request.form.values()]
    features_value = [np.array(input_features)]
    print(features_value)
    
    #features_name = ['city','BHKS','sqft_per_inch','build_up_area','Type_of_property','deposit'] 
    prediction = model.predict(features_value)
    output=prediction[0]    #np.exp(predictions)
    output = np.exp(output)
    output = np.round(output)
    print(output)
    return render_template('upload.html', prediction_text= 'House Rent is {} '.format((output)))

    
if __name__ == '__main__':
      app.run(debug=False)