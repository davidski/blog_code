//MongoDB query to pull exploitable vuln data
foo = db.osvdb.aggregate([
	{ $match: { "ext_references.type" : 'CVE ID' } },  
	{ $match: { "ext_references.type" : 'Metasploit URL' }},
	{ $unwind : "$ext_references" },
	{ $match: { "ext_references.type" : {$in : [ 'CVE ID' , 'Metasploit URL' ]} }},
	{ $project: { reftype: "$ext_references.type", refvalue: "$ext_references.value"} },
	{ $group: { "_id": "$_id", 
			ourvalues : { $addToSet : "$refvalue"} } },
	{ $sort: { _id: 1 } }

])

print("OSVDB_ID,METASPLOIT_URL,CVE_ID")
for (var i = 0; i < foo['result'].length; i++) {	
	print(foo['result'][i]['_id'] + "," +
		foo['result'][i]['ourvalues'][0] +  "," + 
		"CVE-" + foo['result'][i]['ourvalues'][1])
}


