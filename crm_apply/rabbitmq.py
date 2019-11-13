# -*- coding: utf-8 -*-
"""
Simple RabbitMq Client for demo purpose
"""
import json
import pika

QUEUE = 'backend'
HOST = 'localhost'


class RabbitMqClient(object):
    """Simple client for publishing messages to RabbitMq"""

    def __init__(self):
        self.connection = None
        self.channel = None

    def get_connection(self):
        """Returns RabbitMq connection"""
        if not self.connection:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(HOST))
        return self.connection

    def get_channel(self):
        """Returns defined channel"""
        if not self.channel:
            self.channel = self.get_connection().channel()
            self.channel.queue_declare(queue=QUEUE)
        return self.channel

    def publish(self, data):
        return self.get_channel().basic_publish('', QUEUE,
                                                json.dumps(data))

    def __del__(self):
        self.connection.close()


client = RabbitMqClient()
