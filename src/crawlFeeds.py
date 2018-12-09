import hashlib
import json

from urllib.request import Request, urlopen
from urllib.error import HTTPError

from uploader import upload
userId = "ebe7be75-699b-4fa2-b183-8a5d96faeabf"
accessToken="A2w29s6T5cy0T78LEI9fB17cffy1VH3-vc8oQhXASV0h7oG2hkKL0mYXHCU-pd-wX9RlyFzesDSXa-YIBElafhY3muNx74CsFphKiHCfl_Fs115jQN8BceLyvvnz6gY17QT8Ten1JxDrzLW7W5ixmfIciq0xbG7moV_3r3upD1s5GuEUlIhnJUc_NA-MDIj_sZ5hSIi_0rLWR1umTjWKwT8cE9Rqp0V2zSOQVDJjDHvx478vE68YmLSaoqte:feedlydev"

headers = {
	"Authorization":"OAuth %s"%accessToken,
	"Content-Type": "application/json"
}
url = "https://cloud.feedly.com/"
sandbox = "https://sandbox7.feedly.com/"
MINIMUM_ENGAGE = 1

def getFeeds():
	subUrl = url+"v3/subscriptions"
	feedList = []
	try:
		request = Request(subUrl, headers=headers)
		response = urlopen(request)
		feeds = json.loads(response.read().decode("utf-8"))

		print("%d feeds"%len(feeds))
		ids = [i["id"] for i in feeds]

		feedUrl = url+"v3/feeds/.mget"
		request = Request(feedUrl, headers=headers, data = json.dumps(ids).encode("utf-8"))
		response = urlopen(request)
		feed = json.loads(response.read().decode("utf-8"))
		
		for i, f in enumerate(feed):
			streamUrl = url+"v3/streams/contents?streamId=%s"%f["id"]
			request = Request(streamUrl)
			response = urlopen(request)
			streams = json.loads(response.read().decode("utf-8"))
			feedList += list(filter(lambda x:MINIMUM_ENGAGE<=x["engagement"] if "engagement" in x else 0,streams["items"]))
	except HTTPError as e:
		print(e.read())
	return feedList

def handle(event, context):
	feeds = getFeeds()
	upload(feedLists)
	
if __name__ == "__main__":
	import time
	started = time.time()
	feeds = getFeeds()
	open("sample4.json","w").write(json.dumps(feeds))
# 	feeds = json.loads(open("sample3.json","r").read())
	upload(feeds)
	ended = time.time()
	print("took %ss"%(ended-started))