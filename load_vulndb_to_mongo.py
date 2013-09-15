from pymongo import MongoClient
import simplejson as json
import sys
import glob

# the filter to read in all the json files
fileglob = "vulndb/data_*.json"

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
           key = key.encode('utf-8')
        if isinstance(value, unicode):
           value = value.encode('utf-8')
        elif isinstance(value, list):
           value = _decode_list(value)
        elif isinstance(value, dict):
           value = _decode_dict(value)
        rv[key] = value
    return rv


#connect to our MongoDB instance, diy_dbir DB and VERIS collection
client = MongoClient(host = "192.168.58.164")
db = client.vulndb
collection = db.osvdb

for filename in glob.glob(fileglob):
	debug = False
	print filename
	json_data = open(filename).read()
	try:
		#auto-handling unicode object hook derived from
		#http://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-unicode-ones-from-json-in-python
		data = json.loads(json_data, object_hook = _decode_dict)
	except:
		print sys.argv[0], " Unexpected error:", sys.exc_info()[1]
	for vulndb in data['results']:
		if debug: print json.dumps(vulndb, sort_keys=True, indent=4 * ' ')
		vulndb['_id'] = vulndb['osvdb_id']
		osvdb_id = collection.save(vulndb)
		print "Saved: ", filename, " with MongoDB id: ", osvdb_id
