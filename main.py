from flask import Flask, jsonify
from pymongo import MongoClient
from bson import ObjectId
import AssistantReq as AR
import CLUreq as CLU
from config import api_url, subscription_key, request_id, openAiKey
 
app = Flask(__name__)
 
MONGO_URI = 'mongodb+srv://ramvilla997:Qwerty123@cluster0.b8wxule.mongodb.net/shoebot_db?retryWrites=true&w=majority'

@app.route('/api/assistant', methods=['GET'])
def run_assistant():

    assistantReq = AR.AssistantReq()

    assistantReq.openAIRequest()

    return

@app.route('/api/clu', methods=['GET'])
def run_CLU():

    clu_req = CLU.CLUReq()

    participant_id = "test_user"  # Set this as appropriate
    text_to_analyze = "What is the difference between football studs and cleats"
    language = "en"  # Replace with the appropriate language code

    result = clu_req.call_clu_model(participant_id, text_to_analyze, language, subscription_key, request_id, api_url)
    response = clu_req.handle_clu_response(result)



    if result is not None:
        #print(json.dumps(result, indent=4))
        print("------------------------------")
        response = clu_req.handle_clu_response(result)
        print(response)

    else:
        print("Error calling the CLU model")

    return



@app.route('/api/records', methods=['GET'])
def get_records():

    try:
        # Create a connection to the MongoDB
        client = MongoClient(MONGO_URI)
 
        # Access the desired database and collection
        db = client.get_database('shoebot_db')
        collection = db.get_collection('products')
 
        # Query the collection to fetch all records
        records = list(collection.find({}))
        for record in records:
            record['_id'] = str(record['_id'])
        # Close the MongoDB connection
        client.close()
 
        # Convert the records to a list of dictionaries
        records_list = [record for record in records]
 
        # Return the records as a JSON response
        return jsonify(records_list)



 
    except Exception as e:
        return jsonify({'error': str(e)}), 500
 
if __name__ == '__main__':
    app.run(debug=True)