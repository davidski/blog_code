from restkit import OAuthFilter, request
import simplejson as json
import oauth2
import io
from datetime import date, timedelta
import time

def _fetch_data(fromdate, todate):
	"""worker function to fetch a chunk of osvdb"""
	debug = True
	#url = 'https://vulndb.cyberriskanalytics.com/api/v1/vulnerabilities/96956'
	url = 'https://vulndb.cyberriskanalytics.com/api/v1/vulnerabilities/find_by_date?start_date=' + fromdate + '&end_date=' + todate + '&size=1000'
	if debug: print "Working on url: " + url

	consumer = oauth2.Consumer(key='<CONSUMER>',secret='<SECRET>')
	auth = OAuthFilter('*',consumer)
	resp = request(url, filters=[auth], timeout=600)

	if debug:
		print resp.status_int
		#print resp.body_string()

	reply = json.loads( resp.body_string() )
	return reply

thedate = date(2010, 1, 1)
while (thedate < date(2013,1,1)):
	fromdate = thedate.strftime("%Y-%m-%d")
	thedate = thedate + timedelta(days=7)
	todate = thedate.strftime("%Y-%m-%d")

	reply = _fetch_data(fromdate, todate)

	with io.open('vulndb/data_' + fromdate + '.json', 'w', encoding='utf-8') as f:
		f.write(unicode(json.dumps(reply, ensure_ascii=False)))
		f.close
