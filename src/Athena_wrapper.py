import boto3
import time
import botocore
class Athena_Wrapper:
    def __init__(self,database,result_output_s3):
        self.client = boto3.client('athena',region_name='us-east-1')
        self.database = database
        self.result_output_s3 = result_output_s3
    
    def execute_query(self,query):
        try:
            response = self.client.start_query_execution(
                QueryString = query,
                ResultConfiguration={"OutputLocation": self.result_output_s3}
            )
            return response['QueryExecutionId']
        except botocore.exceptions.ClientError as e:
            print(f'Failed to exectue the query. Error: {e}')
    def has_query_succeeded(self,execution_id):
        state = "RUNNING"
        max_execution = 5
        try:
            while max_execution > 0 and state in ["RUNNING", "QUEUED"]:
                max_execution -= 1
                response = self.client.get_query_execution(QueryExecutionId=execution_id)
                if (
                    "QueryExecution" in response
                    and "Status" in response["QueryExecution"]
                    and "State" in response["QueryExecution"]["Status"]
                ):
                    state = response["QueryExecution"]["Status"]["State"]
                    if state == "SUCCEEDED":
                        return True
                time.sleep(5)
        except botocore.exceptions.ClientError as e:
            print(f'[Error]: {e}')

        return False
    def get_query_results(self,execution_id):
        try:
            response = self.client.get_query_results(
                QueryExecutionId=execution_id
            )
            results = response['ResultSet']['Rows']
        except botocore.exceptions.ClientError as e:
            print(f'Failed to fetch query results: {e}')
        return results

client = Athena_Wrapper('spotify','s3://athena-spotify-results-poc/')
exec_id = client.execute_query(
    f"""
    MERGE INTO spotify.Artists_Silver t
    USING(
        
        SELECT 
            SUBSTR("$path",21,10) as Date,
            json_extract_scalar(json_string,'$.name') as Name,
            CAST(json_extract_scalar(json_extract(json_string,'$.followers'),'$.total') as INT) as Followers
        FROM 
            spotify.Artists
        WHERE 
            SUBSTR("$path",21,10) = date_format(current_date, '%Y-%m-%d')
            ) s
    ON s.date=t.date and s.name=t.name
    WHEN NOT MATCHED THEN INSERT (Date,Name,followers) VALUES (s.date,s.name,s.followers)
    """
)
print(f'Query status: {client.has_query_succeeded(exec_id)}')
result = client.get_query_results(exec_id)
print(result)