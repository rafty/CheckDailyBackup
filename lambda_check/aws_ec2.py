# -*- coding: utf-8 -*-
import boto3
from botocore.exceptions import ClientError
from retrying import retry
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# for retry
def retry_if_client_error(exception):
    # Retry until returning false
    logger.warning('_is_retryable_exception: {}, '.format(exception))
    return not isinstance(exception, ClientError)


class EC2(object):

    def __init__(self, region=None):
        self._client = boto3.client('ec2')

    @retry(wait_exponential_multiplier=500,
           stop_max_delay=62000,
           retry_on_exception=retry_if_client_error)
    def describe_instances_with_tag(self):

        response = self._client.describe_instances(
            Filters=[
                {'Name': 'tag-key', 'Values': ['Role']},
                {'Name': 'tag-value', 'Values': ['ifsv']},
            ]
        )

        instances = list()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append(instance['InstanceId'])

        # paging for describe_instances
        while 'NextToken' in response:
            response = self._client.describe_instances(NextToken=response['NextToken'])
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instances.append(instance['InstanceId'])

        return instances

    @retry(wait_exponential_multiplier=500,
           stop_max_delay=62000,
           retry_on_exception=retry_if_client_error)
    def describe_images(self):
        logger.info('describe_images:')
        response = self._client.describe_images(Owners=["self"])

        instance_images = list()
        for image in response['Images']:
            instance_images.append(image['Name'])

        # paging for describe_images
        while 'NextToken' in response:
            response = self._client.describe_images(NextToken=response['NextToken'])
            for image in response['Images']:
                instance_images.append(image['Name'])
        return instance_images
