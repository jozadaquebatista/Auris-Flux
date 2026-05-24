#!/usr/bin/env python
import pika
import json
import os

class Producer:

    def __init__(self, queue):

        self.RABBITMQ_HOST=os.getenv("RABBITMQ_HOST")
        self.RABBITMQ_LOGIN=os.getenv("RABBITMQ_LOGIN")
        self.RABBITMQ_PASSWORD=os.getenv("RABBITMQ_PASSWORD")
        self.RABBITMQ_PORT=os.getenv("RABBITMQ_PORT")

        self.queue=queue

        self.credentials=pika.PlainCredentials(self.RABBITMQ_LOGIN,
                                               self.RABBITMQ_PASSWORD)

        parameters=pika.ConnectionParameters(
            host=self.RABBITMQ_HOST,
            port=self.RABBITMQ_PORT,
            credentials=self.credentials
        )

        self.connection=pika.BlockingConnection(parameters)
        self.channel=self.connection.channel()

        self.channel.queue_declare(queue=self.queue, durable=True, arguments={'x-queue-type': 'quorum'})

    def __del__(self):
        self.connection.close()

    def publish(self, body: dict):

        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue,
                                   body=json.dumps(body))

        print(f" [*] Sent '{json.dumps(body)}'")
