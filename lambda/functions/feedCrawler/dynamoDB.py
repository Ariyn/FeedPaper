import boto3
import botocore

feedTable = "feedlys"

dynamo = boto3.client("dynamodb")
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