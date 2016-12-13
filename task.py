#!/usr/bin/env python

import time
import pika
import sys
import json

print("Doing some work... la da di da...")
#time.sleep(5)

print('I just realized I need some input!')

# let's connect to AMQP
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
declare_result = channel.queue_declare(exclusive=True)
channel.basic_publish(exchange    = '',
                      routing_key = 'launcher',
                      properties  = pika.BasicProperties(reply_to=declare_result.method.queue),
                      body        = "Feed me a number!")

def on_consume(ch, method, properties, body):
    print('Life is great now that I have the input I needed: {}'.format(body))
    ch.basic_ack(delivery_tag = method.delivery_tag)
    sys.exit()

channel.basic_consume(on_consume, declare_result.method.queue)
channel.start_consuming()
