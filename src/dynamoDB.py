import json
import base64
from hashlib import sha224

import boto3
import botocore

from lambdaEventMessages import kinesisEvent, sqsEvent, bigSqsEvent

feedTable = "feedlys"
dynamo = boto3.client("dynamodb")

feedlyConverter = {
	"hashId":("S", lambda f:sha224(f["title"].encode("utf-8")).hexdigest()),
	"datetime":("N", lambda f:"%d"%f["published"]),
	"title":"S",
	"fingerprint":"S",
	"feedlyId":("S", "id"),
	"engagement":"S",
	"summary":("M", lambda f:{"content":{"S":f["summary"]["content"]}, "direction":{"S":f["summary"]["direction"]}}),
	"url":("S","canonicalUrl"),
	"originId":"S",
	"crawled":"N",
# 	"enclosure":("L", lambda f:[{"type":{"S":enc["type"]},"href":{"S":enc["href"]},"length":{"N":int(enc["length"])}} for enc in f["enclosure"]]),
	"origin":("M", lambda f:{
		"title":{"S":f["origin"]["title"]},
		"htmlUrl":{"S":f["origin"]["htmlUrl"]},
		"streamId":{"S":f["origin"]["streamId"]}
	}),
# 	"alternate":("L", lambda f:[{
# 		"type":{"S":_f["type"]},
# 		"href":{"S":_f["href"]}
# 	} for _f in f["alternate"]])
}
always = ["hashId", "datetime"]
attrLists = []

def converterInit():
	global attrLists
	for key, value in feedlyConverter.items():
		targetName = None
		if type(value) == str:
			targetName = (lambda key:lambda f:str(f[key]))(key)
		else:
			if type(value[1]) == str:
				targetName = (lambda key:(lambda f:f[key] if key in f else ""))(value[1])
			else:
				targetName = value[1]
		attrLists.append((key, value[0], targetName))

def escape(feed):
	attrs = {}
	for (k,t,v) in attrLists:
		if k in feed or k in always:
			attrs[k] = {t:v(feed)}
	return attrs

def upload(attrs, failed=lambda e,item:exit(0)):
	try:
		dynamo.put_item(
			TableName=feedTable,
			Item=attrs
		)
	except botocore.exceptions.ParamValidationError as e:
		print(e)
		for k,v in attrs.items():
			print(k, v)
		failed()
		
def handleSqs(record):
	return json.loads(record["body"])

def handleKinesis(record):
	encodedJson = record["kinesis"]["data"]
	jsonString = base64.b64decode(encodedJson).decode("utf-8")
	return json.loads(jsonString)

def handle(event, context, handleMessage=handleSqs):
	converterInit()
	print(event)
	
	for record in event["Records"]:
		data = handleMessage(record)
		escapeData = escape(data)
		upload(escapeData)
	
if __name__ == "__main__":
	handle(bigSqsEvent, None)