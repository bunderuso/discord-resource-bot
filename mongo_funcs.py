from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def connect_mongo():
    #getting mongo connection string from secret file
    mongo_url = open("mongo_file.txt", "r")
    url = mongo_url.readlines()
    #connecting to mongoDB
    uri = url[0].strip()
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
        return e

def user_check(client, user_id):
    #going to the main table
    main_db = client['resource-bot-staging']['main']

    #checking for the userid
    result = main_db.find_one(filter = {'_id': user_id})
    print(result)
    if result is not None:
        return result
    else:
        main_db.insert_one({'_id': user_id,
                            'beans':0,
                            'cheese':0})
        return {'_id': user_id, 'beans':0, 'cheese':0}

def update_inventory(client, user_id, inv_struct):
    #going to the database and updating the structure
    main_db = client['resource-bot-staging']['main']
    update_struct = {"$set": inv_struct}

    #putting the new inventory in the DB
    result = main_db.update_one(filter = {'_id':user_id}, update = update_struct)
    return


#adding debug function
if __name__ == "__main__":
    client = connect_mongo()
    user_id = "test"
    user_check(client, user_id)