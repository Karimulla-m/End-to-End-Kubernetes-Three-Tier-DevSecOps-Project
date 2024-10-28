import json
import os
import psycopg2

def lambda_handler(event, context):
    # Database connection parameters
    #db_host = os.environ['DB_HOST']
    #db_name = os.environ['DB_NAME']
    #db_user = os.environ['DB_USER']
    #db_password = os.environ['DB_PASSWORD']
    
    db_host ="cust360.ccbt4dgjunuu.us-west-2.rds.amazonaws.com"
    db_name ="xfadmin"
    db_user ="admin123"
    db_password = "test"
   
    
    # Connect to the PostgreSQL database
    try:
        connection = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
        cursor = connection.cursor()
        
        # Execute a query
        cursor.execute("SELECT * FROM node_groups;")
        records = cursor.fetchall()
        
        # Process the records
        result = []
        for row in records:
            result.append(row)
        
        # Close the cursor and connection
        cursor.close()
        connection.close()
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
