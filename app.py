import pymongo
from bson.json_util import dumps
import json
from flask import Flask, request, render_template, session, redirect, url_for, flash, Response, abort, render_template_string, send_from_directory
#from flask_cors import CORS
import requests
from datetime import date
from bson.objectid import ObjectId

app = Flask(__name__)
#CORS(app)
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#app.secret_key = b'\xd2(*K\xa0\xa8\x13]g\x1e9\x88\x10\xb0\xe0\xcc'

#Loads the Database and Collections
#mongo = pymongo.MongoClient('mongodb+srv://admin:temporarypassword@cluster0-4qcuj.mongodb.net/test?retryWrites=true&w=majority', maxPoolSize=50, connect=True)
#db = pymongo.database.Database(mongo, 'aq_db_1')
mongo = pymongo.MongoClient('mongodb://127.0.0.1:27017', maxPoolSize=50, connect=True)
db = pymongo.database.Database(mongo, 'aq_db_1')


@app.route('/api/add_new_device', methods=['POST'])
def add_new_device():
	#Maybe some authentication can be added to prevent unauthorized people from adding new devices
	inputData = request.json
	Device_Info = pymongo.collection.Collection(db, 'Device_Info')
	devices = json.loads(dumps(Device_Info.find({'device_id': inputData['device_id']})))
	if len(devices) == 0:
		Device_Info.insert_one({'device_id':inputData['device_id']})
		return Response(status=200)
	else:
		return Response(status=409)


@app.route('/api/get_device_list')
def get_device_list():
	Device_Info = pymongo.collection.Collection(db, 'Device_Info')
	devices = json.loads(dumps(Device_Info.find()))
	data = {'count':len(devices), 'data':devices}
	return data


@app.route('/api/get_sensor_data', methods=['POST'])
def get_senor_data():
	inputData = request.json
	if 'device_id' in inputData:
		Sensor_Info = pymongo.collection.Collection(db, inputData['device_id'])
		data = json.loads(dumps(Sensor_Info.find()))
		data_json = {'count':len(data), 'data':data}
		return data_json
	else:
		return Response(status=404)


@app.route('/api/add_sensor_data', methods=['POST'])
def add_sensor_data():
	inputData = request.json
	Device_Info = pymongo.collection.Collection(db, 'Device_Info')
	devices = json.loads(dumps(Device_Info.find({'device_id':inputData['device_id']})))
	today = date.today()
	currdate = today.strftime("%d-%m-%Y")
	lastcontact = currdate + str(' ') + str(inputData['timestamp'])
	Device_Info.insert_one({'device_id':inputData['device_id'], 'last_contact':lastcontact, 'last_altitude':inputData['altitude'], 'last_latitude':inputData['longitude'], 'last_longitude':inputData['longitude'], 'last_battery':inputData['battery_level']})
	if(len(devices) == 0):
		return Response(status=403)
	else:
		Device_Info.update_one({'device_id':inputData['device_id']}, {'$set': {'last_contact':lastcontact, 'last_altitude':inputData['altitude'], 'last_latitude':inputData['latitude'], 'last_longitude':inputData['longitude'], 'last_battery':inputData['battery_level']}})
	Sensor_Info = pymongo.collection.Collection(db, inputData['device_id'])
	Sensor_Info.insert_one({'device_id':inputData['device_id'], 'timestamp':lastcontact, 'altitude':inputData['altitude'], 'latitude':inputData['latitude'], 'longitude':inputData['longitude'], 'aq1':{'pm10':inputData['aq1']['pm10'], 'pm75':inputData['aq1']['pm75'], 'pm25':inputData['aq1']['pm25']}, 'aq2':{'pm10':inputData['aq2']['pm10'], 'pm75':inputData['aq2']['pm75'], 'pm25':inputData['aq2']['pm25']}, 'aq3':{'pm10':inputData['aq3']['pm10'], 'pm75':inputData['aq3']['pm75'], 'pm25':inputData['aq3']['pm25']}, 'battery_level':inputData['battery_level']})
	return Response(status=200)


#------------------------------
#Other stuff
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/test/test')
def test():
	return "Works"

#Another Basic Route
@app.route('/')
def homepage():
	return render_template('index.html')
