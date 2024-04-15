import json
import os

import pika

from app.config import Config


# upload file to gridfs, get file id and put it as string in message for rabbitmq queue
def upload_file(f, gfs, ch, payload):
    try:
        file_id = gfs.put(f, filename=f.filename, contentType=f.mimetype)
    except Exception as e:
        return "upload failed", 500
    # file_id object need to be converted to string
    msg = {"pdf_id": str(file_id), "text_id": None, "username": payload["sub"]}
    try:
        # basic exchange with rkey == queue name
        ch.basic_publish(
            exchange="",
            routing_key=Config.PDF_TO_TEXT_QUEUE,
            properties=pika.BasicProperties(delivery_mode=2),
            body=json.dumps(msg),
        )
    except Exception as e:
        gfs.delete(file_id)
        return "message publish failed", 500
