import boto3
import os

class Storage:

	def __init__(self):

		self.s3 = boto3.client(
		  service_name="s3",
		  endpoint_url=os.getenv("STORAGE_HOST"),
		  aws_access_key_id=os.getenv("STORAGE_ACESS_KEY_ID"),
		  aws_secret_access_key=os.getenv("STORAGE_SECRET_ACCESS_KEY"),
		  region_name="auto",
		)

	def download(self, bucketname: str, object_key: str):
		response = self.s3.get_object(Bucket=bucketname, Key=object_key)
		image_data = response["Body"].read()

		filename = object_key.split("/")[::-1][0]

		with open(f"/tmp/{filename}", "wb") as f:
			f.write(image_data)
			print(" [*] Downloaded Successfully. File: {filename}")

	def upload(self, bucketname:str, object_key:str, new_object_key:str, content_type:str):

		filename = object_key.split("/")[::-1][0]

		with open(f"/tmp/{object_key}", "rb") as f:
			response = self.s3.put_object(
		        Bucket=bucketname,
		        Key=new_object_key,
		        Body=f,
		        ContentType=content_type,
		    )
			print(f" [*] Uploaded Successfully. ETag: {response['ETag']}")

	def delete(self, bucketname: str, object_key: str):
		self.s3.delete_object(Bucket=bucketname, Key=object_key)
