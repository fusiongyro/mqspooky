#!/usr/bin/env python

import pika
import json

def on_message(ch, method, props, body):
    print(body)
    response = input('> ')
    ch.basic_publish(exchange    = '',
                     routing_key = props.reply_to,
                     body        = response)
    ch.basic_ack(delivery_tag = method.delivery_tag)


# let's listen for "input needed" events and handle them until we quit
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# let's make a queue for us to talk to our tasks
channel.queue_declare('launcher', durable=True)
channel.basic_consume(on_message, queue='launcher')
channel.start_consuming()