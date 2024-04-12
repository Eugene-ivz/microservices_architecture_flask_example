import os
import sys

import pika
from dotenv import load_dotenv

from utils import file_ready

load_dotenv()

def main():

    conn = pika.BlockingConnection(pika.URLParameters(os.getenv('RABBITMQ_HOST')))
    ch = conn.channel()

    def callback(ch, method, properties, body):
        error = file_ready(body)
        if error:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    ch.basic_consume(queue=os.getenv('TEXT_TO_CONSUMER_QUEUE'), on_message_callback=callback)
    
    ch.start_consuming()
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)