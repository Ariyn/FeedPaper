from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import parse_qs, quote, urlencode
from itertools import groupby

import json
import random
import re
import os

rootPath = "../"
absPath = lambda path:os.path.join(rootPath, path)
feedSize = {
	1:507,
	2:1407,
	4:3338,
	507 : "single",
	1407 : "double",
	3338 : "quadruple"
}
	
def removeYoutube(body):
	return re.sub("(<iframe.*?</iframe>)", "<span class=\"youtube\">youtube</span>",body)
def realLength(body):
	return len(re.sub("<.*?>", "", body))

def preCalculate(feeds):
	sizeFeeds = {1:[],2:[],4:[]}
	for f in feeds:
		if "summary" not in f and "content" not in f:
			continue
		elif "content" in f:
				content = f["content"]["content"]
		else:
			content = f["summary"]["content"]
		c = removeYoutube(content)
		_realLength = realLength(c)
		if _realLength <= feedSize[1]:
			_size = 1
		elif _realLength <= feedSize[2]:
			_size = 2
		else:
			_size = 4
		f["realContent"], f["realSize"] = c, _size
		sizeFeeds[_size].append(f)
	for f in sizeFeeds:
		sorted(sizeFeeds[f], key=lambda x:x["engagement"])
		
	return sizeFeeds

def create(feeds, page=2):
	main = open(absPath("colums/main.html")).read()
	stretigyData = json.loads(open(absPath("colums/page.json")).read())
	colum = {
		"single": open(absPath("colums/single.colum")).read().replace("\n",""),
		"double": open(absPath("colums/double.colum")).read().replace("\n",""),
		"quadruple" : open(absPath("colums/quadruple.colum")).read().replace("\n","")
	}
	
	stretigyList, sizeList = [], {1:len(feeds[1]),2:len(feeds[2]),4:len(feeds[4])}
	print(sizeList)
	i=0
	while i< page:
		x = random.choice(stretigyData)
		_sizeList = [
			sizeList[1]-x.count(1)<0,
			sizeList[2]-x.count(2)<0,
			sizeList[4]-x.count(4)<0
		]
		if True in _sizeList:
			if sizeList[2] <= 0 or sizeList[4] <=0:
				break
			continue
		i += 1
		sizeList[1] -= x.count(1)
		sizeList[2] -= x.count(2)
		sizeList[4] -= x.count(4)
		
		stretigyList.append(x)

	pages = []

	for stretigy in stretigyList:
		feedList = [feeds[i].pop(0) for i in stretigy]
		
		targetList = []
		for f in feedList:
			t, c, s = f["title"], f["realContent"], feedSize[f["realSize"]]
			columTarget = colum[feedSize[s]]
			
			t = "<span>%s</span>"%t.replace("\n","")
			c = "".join(["<p>%s</p>"%i for i in c.split("\n")])
			columTarget = columTarget.format(title=t, body=c)
			targetList.append((s, columTarget))
			
		pages.append("<page size=\"A4\">"+"\n".join([i[1] for i in targetList])+"</page>")

	main = main.format(pages="\n".join(pages))
	open(absPath("html/sample2.html"),"w").write(main)
#	 counts = {k:len(list(g)) for k, g in groupby(targetList, lambda x:x[0])}
#	 print(counts)
	 
if __name__ == "__main__":
	feedList = json.loads(open("sample3.json","r").read())
	feedDict = preCalculate(feedList)
	create(feedDict, 5)
# $ curl -H 'Authorization: OAuth [your access token]' https://cloud.feedly.com/v3/profile