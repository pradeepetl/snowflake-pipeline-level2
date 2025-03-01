import requests
import boto3
import json
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from snowflake.snowpark import Session

# URL for the Ditto Pokemon data
url = 'https://pokeapi.co/api/v2/pokemon/ditto'

# S3 bucket and file details
bucket_name = 'mys3bucket'
s3_file_key = 'pokeapi/ditto_data.json'
end_point_url = 'http://127.0.0.1:9000'

# AWS S3 client
s3_client = boto3.client('s3',endpoint_url=end_point_url)

# Make the GET request to the API
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Get the JSON response data
    data = response.json()

    try:
        # Upload JSON data to AWS S3 as a file
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_file_key,
            Body=json.dumps(data, indent=4),
            ContentType='application/json'
        )

        print(f"Data has been successfully uploaded to S3 bucket '{bucket_name}' at '{s3_file_key}'")
    
    except (NoCredentialsError, PartialCredentialsError):
        print("AWS credentials not configured properly. Please check your AWS credentials.")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

else:
    print(f"Failed to retrieve data from the API. Status code: {response.status_code}")

def get_secret(secret_name, region_name="us-west-2"):
    """
    Fetch secret from AWS Secrets Manager.
    
    :param secret_name: Name of the secret in AWS Secrets Manager.
    :param region_name: AWS region where the secret is stored.
    :return: Dictionary containing secret values.
    """
    # Create a Secrets Manager client
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        # Retrieve the secret
        response = client.get_secret_value(SecretId=secret_name)
        print(response)
        # Parse secret value
        if "SecretString" in response:
            secret_data = json.loads(response["SecretString"])
            return secret_data
        else:
            return None
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return None
        
secret_name = "mysnowdbcreds"  # Replace with your secret name
credentials = get_secret(secret_name)

# Make connection and create Snowpark session
connection_parameters = {"account":credentials.get("account"), \
"user": credentials.get("user"),
"password": credentials.get("password"),\
"role":credentials.get("role"), \
"warehouse":credentials.get("warehouse"), \
"database":credentials.get("database"), \
"schema":credentials.get("schema") \
}

session = Session.builder.configs(connection_parameters).create()
print("************ EXECUTING TASK *********************")
session.sql("EXECUTE TASK DEMO_DB.PUBLIC.DAG_COPY_EMP;").collect()
print("****** EXECUTED********")


