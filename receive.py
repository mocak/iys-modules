#!/usr/bin/env python
"""
Odoo demo consumer code that receives messages from odoo queue
and sends massage body to Odoo for creating lead via Odoo's externa client
"""

import json
import pika

from xmlrpc import client

url = 'http://localhost:8069'
username = 'admin'
password = 'admin'
db = 'test5'

common = client.ServerProxy('%s/xmlrpc/2/common' % url)
uid = common.authenticate(db, username, password, {})
models = client.ServerProxy('%s/xmlrpc/2/object' % url, allow_none=True)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='odoo')


def callback(ch, method, properties, body):
    lead_id = models.execute_kw(db, uid, password, 'crm.lead', 'register',
                                [json.loads(body)])
    print('Lead record created. ID: %s' % lead_id)


channel.basic_consume(queue='odoo', on_message_callback=callback,
                      auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
