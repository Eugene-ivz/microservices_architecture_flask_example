import os
import sys
from dotenv import load_dotenv

import gridfs
import pika
import json
from pymongo import MongoClient
from bson.objectid import ObjectId

from convert_utils import convert_to_txt

load_dotenv()

def main():
    client = MongoClient(os.getenv('MONGO_URI'))
    db_pdf = client['db_pdf']
    db_txt = client['db_txt']
    
    gfs_pdf = gridfs.GridFS(db_pdf)
    gfs_txt = gridfs.GridFS(db_txt)

    conn = pika.BlockingConnection(pika.URLParameters(os.getenv('RABBITMQ_HOST')))
    ch = conn.channel()
    
    
    ch.queue_declare(queue=os.getenv('PDF_TO_TEXT_QUEUE'), durable=True)
    ch.queue_declare(queue=os.getenv('TEXT_TO_CONSUMER_QUEUE'), durable=True)
    
    def callback(ch, method, properties, body):
        error = convert_to_txt(ch, gfs_pdf, gfs_txt, body)
        if error:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            # delete pdf after conversion
            msg = json.loads(body)
            gfs_pdf.delete(ObjectId(msg['pdf_id']))
    ch.basic_consume(queue=os.getenv('PDF_TO_TEXT_QUEUE'), on_message_callback=callback)
    print('Waiting for messages. To exit press CTRL+C')
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