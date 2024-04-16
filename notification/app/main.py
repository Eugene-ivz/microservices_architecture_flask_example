import os
import sys

import pika
from dotenv import find_dotenv, load_dotenv

from app.utils import file_ready

env_file = find_dotenv(f'.env.{os.getenv("APP_ENV", "dev")}')
load_dotenv(env_file)


def main() -> None:
    '''
    connect to RabbitMQ server and start consuming messages
    from queue to get id of the text file
    and send it to file_ready function
    
    '''

    conn = pika.BlockingConnection(pika.URLParameters(os.getenv("RABBITMQ_HOST")))
    ch = conn.channel()

    def callback(ch, method, properties, body):
        error = file_ready(body)
        if error:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    ch.basic_consume(
        queue=os.getenv("TEXT_TO_CONSUMER_QUEUE"), on_message_callback=callback
    )
    print("Waiting for messages. To exit press CTRL+C")
    try:
        ch.start_consuming()
    except pika.exceptions.ConnectionClosedByBroker:
        ch.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
