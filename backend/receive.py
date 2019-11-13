#!/usr/bin/env python
"""
Odoo demo consumer code that receives messages from odoo queue
and sends massage body to Odoo for creating lead via Odoo's externa client
"""

import json
import pika
import sys
import time

from xmlrpc import client
from pika.exceptions import AMQPConnectionError

url = 'http://web:8069'
username = 'admin'
password = 'admin'
db = 'demo'

start_time = time.time()
print("Starting consumer...")

# rabbitmq connection
while (time.time() - start_time) < 60:
    try:
        print("Trying to connect RabbitMQ...")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq'))
        error = ''
        break
    except AMQPConnectionError as e:
        error = e
    time.sleep(1)

if error:
    print("RabbitMQ connection failure: %s" % error, file=sys.stderr)
    sys.exit(1)

start_time = time.time()

# odoo connection
while (time.time() - start_time) < 60:
    try:
        print("Trying to connect Odoo...")
        common = client.ServerProxy('%s/xmlrpc/2/common' % url)
        error = ''
        break
    except OSError as e:
        error = e
    time.sleep(3)

if error:
    print("XMLRPC connection failure: %s" % error, file=sys.stderr)
    sys.exit(1)

uid = common.authenticate(db, username, password, {})
models = client.ServerProxy('%s/xmlrpc/2/object' % url,
                            allow_none=True)

channel = connection.channel()
channel.queue_declare(queue='odoo')
channel.queue_declare(queue='backend')


def odoo_callback(ch, method, properties, body):
    lead_id = models.execute_kw(db, uid, password, 'crm.lead', 'register',
                                [json.loads(body)])
    print('Lead record has created. ID: %s' % lead_id)


def backend_callback(ch, method, properties, body):
    print('Message received form Odoo: %r' % body)


channel.basic_consume(queue='odoo', on_message_callback=odoo_callback,
                      auto_ack=True)
channel.basic_consume(queue='backend', on_message_callback=backend_callback,
                      auto_ack=True)

print('Waiting for messages...')
channel.start_consuming()
