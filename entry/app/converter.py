import json

import gridfs
import pika
from bson import ObjectId
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

from app.auth_utils import validate_jwt
from app.config import Config
from app.db_utils import upload_file
from app.extensions import mongo
from app.forms import File_download_form, File_upload_form

converter_bp = Blueprint("converter", __name__, url_prefix="/converter")
    
# pymongo
mongo_pdf = mongo.cx[Config.MONGO_URI_PDF]
mongo_txt = mongo.cx[Config.MONGO_URI_TXT]

# gridfs
gfs_pdf = gridfs.GridFS(mongo_pdf)
gfs_txt = gridfs.GridFS(mongo_txt)


# rabbitmq
conn = pika.BlockingConnection(pika.URLParameters(Config.RABBITMQ_HOST))
ch = conn.channel()


# validate token in auth service and upload file to gridfs
@converter_bp.route("/upload", methods=["GET", "POST"])
def upload():
    '''
    check if token is valid in jwt cookie and pass file to upload function
    
    :return: flask redirect response
    
    '''
    payload, error = validate_jwt(request)
    if error:
        return 'need to login', 401

    form = File_upload_form()

    if form.validate_on_submit():

        payload = json.loads(payload)

        if payload["allowed"]:
            f = form.file.data
            error = upload_file(f, gfs_pdf, ch, payload)
            if error:
                flash('failed to upload file')
                return redirect(url_for("converter.upload"), 303)
            return redirect(url_for("converter.download"), 303)
        else:
            return "not authorized", 403
    return render_template("upload.html", form=form)


@converter_bp.route("/download", methods=["GET", "POST"])
def download():
    '''
    check if token is valid in jwt cookie
    gets id of text file from form and get file from mongodb
    saves file on user's computer
    
    :return: file | flask redirect response
    
    '''
    payload, error = validate_jwt(request)

    if error:
        return 'need to login', 401

    form = File_download_form()

    if form.validate_on_submit():
        payload = json.loads(payload)
        if payload["allowed"]:
            text_id = request.form.get("text_id")
            if not text_id:
                return "need text_id", 400
            try:
                f = gfs_txt.get(ObjectId(text_id))
                return send_file(f, as_attachment=True, download_name=f"{text_id}.txt")
            except Exception as e:
                flash("file not found")
                return redirect(url_for("converter.download"), 303)
        else:
            return "not authorized", 403
    return render_template("download.html", form=form)
