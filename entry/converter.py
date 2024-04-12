import json
import os

from bson import ObjectId
from flask import Blueprint, request
import gridfs
import pika

from entry.auth_utils import validate_jwt
from entry.db_utils import upload_file
from entry.extensions import mongo

converter_bp = Blueprint('converter', __name__, url_prefix='/converter')

# pymongo
mongo_pdf = mongo.cx[os.getenv('FLASK_MONGO_URI_PDF')]
mongo_txt = mongo.cx[os.getenv('FLASK_MONGO_URI_TXT')]

# gridfs
gfs_pdf = gridfs.GridFS(mongo_pdf)
gfs_txt = gridfs.GridFS(mongo_txt)


# rabbitmq
conn = pika.BlockingConnection(pika.URLParameters(os.getenv('FLASK_RABBITMQ_HOST')))
ch = conn.channel()
    
# validate token in auth service and upload file to gridfs    
@converter_bp.route('/upload', methods=['GET','POST'])
def upload():
    payload, error = validate_jwt(request)
    
    if error:
        return error
    
    payload = json.loads(payload)
    
    if payload['allowed']:
        if len(request.files) != 1:
            return 'need 1(one) file', 400
        for key, f in request.files.items():
            error = upload_file(f, gfs_pdf, ch, payload)
            
            if error:
                return error
        return 'ok', 200
    else:
        return 'not authorized', 403
    
@converter_bp.route('/download', methods=['GET'])
def download():
    payload, error = validate_jwt(request)
    
    if error:
        return error
    
    payload = json.loads(payload)
    if payload['allowed']:
        text_id = request.args.get('text_id')
        
        if not text_id:
            return 'need text_id', 400
        try:
            f = gfs_txt.get(ObjectId(text_id))
            return 'OK FILE READY FOR DOWNLOAD', 200
        except Exception as e:
            print('file not found', e)
            return 'file not found', 500  
    else:
        return 'not authorized', 403