import json
from hashlib import sha224

import boto3
import botocore

streamName = "feedConsumer"
queueUrl = "https://sqs.ap-northeast-2.amazonaws.com/549757146116/feedQueueDelay"
MB = 1024*1024

sizeOfJson = lambda x:len(json.dumps(x))
kinesis = boto3.client("kinesis")
sqs = boto3.client("sqs")

def handleKinesis(datas):
	index = 0
	print(type(datas))
	while index < len(datas):
		x = []
		while sizeOfJson(x) < MB and index < len(datas):
			x.append(datas[index])
			index += 1

		x.pop(-1)
		index -= 1
		if not x:
			break
		result = kinesis.put_records(
			Records = [{
				"Data":json.dumps(r).encode("utf-8"),
				"PartitionKey":sha224(r["title"].encode("utf-8")).hexdigest()}
			for r in x],
			StreamName = streamName
		)
		print("%d/%d"%(result["FailedRecordCount"],len(x)))
		failedResults = [i for i in result["Records"] if "ErrorCode" in i]
		if failedResults:
			print(len(failedResults), failedResults[0])
			
def handleSqs(datas):
	print(len(datas))
	for i in range(0, len(datas), 3):
		for data in datas[i:min(i+3,len(datas))]:
			result = sqs.send_message(
				QueueUrl=queueUrl,
				MessageBody=json.dumps(data),
				DelaySeconds=i//5
			)

def upload(datas, handler=handleSqs):
	handler(datas)