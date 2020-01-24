# -*- coding: utf-8 -*-
import os
import datetime
import logging
import boto3
from aws_ec2 import EC2

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']
sns = boto3.client('sns')


def backup_alarm(instance_id):
    message = 'SSM Backup Error.\nInstanceId: {}'.format(instance_id)
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=message,
        Subject='Alert! SSM Daily Backup Error!'
    )
    logger.error('SSM Backup Error. InstanceId: {}'.format(instance_id))


def backup_time_range():
    time_range_hour = 4
    now = datetime.datetime.utcnow()
    now_str = now.strftime("%Y-%m-%dT%H.%M.%S")
    before = now - datetime.timedelta(hours=time_range_hour)
    before_str = before.strftime("%Y-%m-%dT%H.%M.%S")
    return before_str, now_str


def backup_time(image_name):
    date_time_list = image_name.split('_')[-2:]
    date_time = 'T'.join(date_time_list)
    return date_time


def is_backup_executed(instance_id, backup_image_list):
    before, now = backup_time_range()

    images_of_instance = [name for name in backup_image_list if instance_id in name]
    logger.info('Images of instance: {}'.format(images_of_instance))

    result = False
    for image_name in images_of_instance:
        _backup_time = backup_time(image_name)
        logger.info('if {} <= {} <= {}'.format(before, _backup_time, now))
        if before <= _backup_time <= now:
            result = True

    return result


def check_backup(instance_id_list, backup_image_list):

    for instance_id in instance_id_list:

        result = is_backup_executed(instance_id, backup_image_list)
        if result is False:
            backup_alarm(instance_id)
        logger.info('result: {}'.format(result))


def lambda_handler(event, context):
    ec2 = EC2()

    instance_id_list = ec2.describe_instances_with_tag()
    logger.info('instance_id_list: {}, '.format(instance_id_list))

    backup_image_list = ec2.describe_images()
    logger.info('instance_image_list: {}, '.format(backup_image_list))

    check_backup(instance_id_list, backup_image_list)
    return True
