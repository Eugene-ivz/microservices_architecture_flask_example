import json
import os
import tempfile

import fitz
import pika
from bson.objectid import ObjectId


def convert_to_txt(ch, gfs_pdf, gfs_txt, msg):
	msg = json.loads(msg)

	tm =  tempfile.NamedTemporaryFile(suffix='.pdf', mode='r+b')
	f = gfs_pdf.get(ObjectId(msg['pdf_id']))
	tm.write(f.read())

	txt = tempfile.NamedTemporaryFile(mode='r+b')
	with fitz.open(tm) as doc:
		for page in doc: # iterate the document pages
			text = page.get_text().encode("utf-8") # get plain text (is in UTF-8)
			txt.write(text) # write text of page
			txt.write(bytes((12,)))
	txt.flush()
	txt.seek(0)
	data = txt.read()
	print(tm.name)
	tm.close()
	text_id = gfs_txt.put(data, filename=msg["pdf_id"])
	txt.close()
	msg['text_id'] = str(text_id)
	try:
		ch.basic_publish(exchange='', routing_key=os.getenv('TEXT_TO_CONSUMER_QUEUE'), \
			properties=pika.BasicProperties(delivery_mode=2), body=json.dumps(msg))
	except Exception as e:
		gfs_txt.delete(text_id)
		print('message publish failed', 500)
		return e
     