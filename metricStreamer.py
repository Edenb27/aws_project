import boto3
import json

region_name = 'us-east-2'


def lambda_handler(event, context):
    # AWS configuration
    AUTOSCALING_GROUP_NAME = 'edenb27-yolo-AS'
    QUEUE_NAME = 'edenb-yolo5'
    NAMESPACE = 'edenb27-AWS-metric'
    METRIC_NAME = 'BacklogPerInstance'

    # Initialize AWS clients
    sqs_client = boto3.client('sqs', region_name=region_name)
    asg_client = boto3.client('autoscaling', region_name=region_name)
    cloudwatch_client = boto3.client('cloudwatch', region_name=region_name)

    try:
        # Get the number of messages in the SQS queue
        queue_url = f'https://sqs.us-east-2.amazonaws.com/352708296901/edenb-yolo5'
        response = sqs_client.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=['ApproximateNumberOfMessages']
        )
        msgs_in_queue = int(response['Attributes']['ApproximateNumberOfMessages'])

        # Get the desired capacity of the Auto Scaling Group
        asg_response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[AUTOSCALING_GROUP_NAME])
        if not asg_response['AutoScalingGroups']:
            raise RuntimeError('Autoscaling group not found')
        asg_size = asg_response['AutoScalingGroups'][0]['DesiredCapacity']

        print(f'Messages in Queue: {msgs_in_queue}')
        print(f'Desired Capacity of ASG: {asg_size}')

        # Avoid division by zero
        if asg_size == 0:
            backlog_per_instance = msgs_in_queue
        else:
            backlog_per_instance = msgs_in_queue / asg_size

        # Send the metric to CloudWatch
        response = cloudwatch_client.put_metric_data(
            Namespace=NAMESPACE,
            MetricData=[
                {
                    'MetricName': METRIC_NAME,
                    'Value': backlog_per_instance,
                    'Unit': 'None'
                }
            ]
        )

        print(f'BacklogPerInstance: {backlog_per_instance}')

    except Exception as e:
        print(f'Error: {str(e)}')

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
