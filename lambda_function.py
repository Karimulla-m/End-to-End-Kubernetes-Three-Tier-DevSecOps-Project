import json
import os
import psycopg2
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # Database connection parameters
    db_host = os.environ['DB_HOST']
    db_name = os.environ['DB_NAME']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
        cursor = connection.cursor()
        
        # Execute a query to get Node_group_name
        cursor.execute("SELECT Node_group_name FROM node_groups;")
        records = cursor.fetchall()
        
        # Process the records
        node_group_names = [row[0] for row in records]
        
        # Close the cursor and connection
        cursor.close()
        connection.close()
        
        # Print Node_group_names
        print("Node group names:", node_group_names)
        
        # Call function to scale down ASGs
        scale_down_asgs(node_group_names)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'node_group_names': node_group_names})
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def scale_down_asgs(node_group_names):
    # AWS AutoScaling client
    asg_client = boto3.client('autoscaling')
    
    # Due date for scaling down
    due_date_str = '2024-10-29'
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
    current_date = datetime.now()

    if current_date >= due_date:
        for node_group_name in node_group_names:
            try:
                # Describe the Auto Scaling group
                response = asg_client.describe_auto_scaling_groups(
                    AutoScalingGroupNames=[node_group_name]
                )
                
                # Check if the ASG exists
                if response['AutoScalingGroups']:
                    # Update the ASG to set desired capacity to 0
                    asg_client.update_auto_scaling_group(
                        AutoScalingGroupName=node_group_name,
                        DesiredCapacity=0,
                        MinSize=0  # Also set MinSize to 0 to allow scaling to 0
                    )
                    print(f"Scaled down ASG: {node_group_name} to desired capacity: 0")
                else:
                    print(f"ASG not found: {node_group_name}")
            
            except Exception as e:
                print(f"Error scaling down ASG {node_group_name}: {str(e)}")
    else:
        print("Current date is before the due date. No action taken.")

# If you want to test the scale_down_asgs function locally
if __name__ == "__main__":
    test_node_group_names = [
        'eks-udp-premium-stage-general-d0c896e0-0cac-07d6-a6d7-aea762ea47d3',
        'eks-udp-premium-stage-prod-04c896d9-36c3-cb3a-359f-2ceff3865e96'
    ]
    scale_down_asgs(test_node_group_names)