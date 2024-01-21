import boto3
import json
import time
def lambda_handler(event, context):
    sqs_client = boto3.resource('sqs', region_name='us-east-2')
    asg_client = boto3.client('autoscaling', region_name='us-east-2')
    cw_client = boto3.client('cloudwatch', region_name='us-east-2')

    AUTOSCALING_GROUP_NAME = 'edenb27-yolo-AS'
    QUEUE_NAME = 'edenb-yolo5'

    queue = sqs_client.get_queue_by_name(QueueName=QUEUE_NAME)
    msgs_in_queue = int(queue.attributes.get('ApproximateNumberOfMessages'))
    asg_groups = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[AUTOSCALING_GROUP_NAME])[
        'AutoScalingGroups']

    if not asg_groups:
        raise RuntimeError('Autoscaling group not found')
    else:
        asg_size = asg_groups[0]['DesiredCapacity']

# TODO send backlog_per_instance to cloudwatch...
    if msgs_in_queue and asg_size == 0:
        pass
    else:
        backlog_per_instance = msgs_in_queue / asg_size
        put_metric = cw_client.put_metric_data(
            Namespace='edenb27-AWS-metric',
            MetricData=[
                {
                'MetricName': 'BacklogPerInstance',
                'Value': backlog_per_instance,
                'Unit': 'None'
                },
             ]
        )

    return {
        'status Code': 200,
        'body': json.dumps(put_metric)
    }
