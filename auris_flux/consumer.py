#!/usr/bin/env python
import pika
import sys
import os

class Consumer:

    def __init__(self, queue, callback):

        self.RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
        self.RABBITMQ_LOGIN = os.getenv("RABBITMQ_LOGIN")
        self.RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
        self.RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")

        self.queue = queue
        self.callback = callback

        self.credentials = pika.PlainCredentials(self.RABBITMQ_LOGIN,
                                                 self.RABBITMQ_PASSWORD)

        parameters = pika.ConnectionParameters(
            host=self.RABBITMQ_HOST,
            port=self.RABBITMQ_PORT,
            credentials=self.credentials
        )

        connection = pika.BlockingConnection(parameters)
        self.channel = connection.channel()

        self.channel.queue_declare(queue=self.queue, durable=True, arguments={'x-queue-type': 'quorum'})

        self.channel.basic_qos(prefetch_count=1)

    def rabbit_callback(self, ch, method, properties, body):
        try:
            self.callback(body)

            print(f" [*] Received {body}")

            # ACK MANUAL
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            print(f" [!] Erro: {e}")

            # requeue
            ch.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=True
            )

    def listen(self):
        self.channel.basic_consume(queue=self.queue,
                                   auto_ack=False,
                                   on_message_callback=self.rabbit_callback)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()
