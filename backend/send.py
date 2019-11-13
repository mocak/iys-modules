#!/usr/bin/env python
"""
Backend Project demo code that sends lead data to erp queue.
Another receiver will consume and create leads in Odoo
"""
import base64
import json
import pika
import requests

from io import BytesIO
from PyPDF2 import PdfFileWriter
from random import randint

ENCODING = 'utf-8'

# Sample user generator API
r = requests.get('https://randomuser.me/api/')
r.raise_for_status()

sample = r.json().get('results')[0]

r = requests.get(sample.get('picture').get('large'))
r.raise_for_status()

writer = PdfFileWriter()
writer.addBlankPage(height=30, width=20)
buffer = BytesIO()
writer.write(buffer)
buffer_encoded = base64.encodebytes(
    buffer.getvalue()).decode(ENCODING)

location = sample.get('location')
name = sample.get('name')
segments = ['large', 'medium', 'small']

data = {
    'reference': str(randint(111111, 999999)),
    'company_name': sample.get('login').get('username').upper(),
    'logo': base64.encodebytes(r.content).decode(ENCODING),
    'vat': str(randint(1000000000, 9999999999)),
    'invoice_address': "%s No: %s %s/%s" % (
        location.get('street').get('name'),
        location.get('street').get('number'),
        location.get('city'),
        location.get('country')),
    'contact_name': name.get('first'),
    'contact_surname': name.get('last'),
    'contact_tckn': sample.get('id').get('value'),
    'contact_dob': sample.get('dob').get('date'),
    'contact_gsm': sample.get('cell'),
    'contact_email': sample.get('email'),
    'is_high_priority': randint(0, 1),
    'segment': segments[randint(0, 2)],
    'documents': [
        {'name': 'file1', 'file': buffer_encoded},
        {'name': 'file2', 'file': buffer_encoded},
        {'name': 'file3', 'file': buffer_encoded},
        {'name': 'file4', 'file': buffer_encoded},
    ],
}

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='odoo')
channel.basic_publish(exchange='', routing_key='odoo',
                      body=json.dumps(data))

print(" [x] Lead data has sent to ERP")
connection.close()
