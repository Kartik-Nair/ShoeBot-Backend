from flask import Flask, jsonify
from pymongo import MongoClient
from bson import ObjectId
 
app = Flask(__name__)
 
# Replace 'YOUR_MONGODB_URI' with your actual MongoDB URI
MONGO_URI = 'mongodb+srv://ramvilla997:Qwerty123@cluster0.b8wxule.mongodb.net/shoebot_db?retryWrites=true&w=majority'
 
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