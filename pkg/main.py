from sre_constants import SUCCESS
from flask import Flask, jsonify, redirect, request, render_template

# from flask_mysqldb import MySQL

import face_recognition
import numpy as np

from pkg.FileOperations import FileOperations  
from pkg.Database import Database  

import os, zipfile, shutil

# creating the flask app
app = Flask(__name__, template_folder='templates')


# This LIST will store encodings of all the images present in the database at any point
# of execution during the program.
KNOWN_IMAGE_ENCODINGS = []


# Mapping (idx in KNOWN_IMAGE_ENCODINGS --> images_id)
GET_IMAGE_ID = []

# *********************** USEFUL functions *********************************

def isFileTypeZip(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'zip'

# *********************** USEFUL functions ENDS*********************************


# *********************** ENDPOINTS *********************************
db = Database(app)

def populate_encodings_from_db():
    print("**************************************populate_encodings_from_db STARTS")
    
    query = (
        "select image_id, image_encoding from images"
    )
    rows = None 

    with app.app_context():
        rows = db.query(query_stmt=query, param=(), debug=False)

    if rows is not None:
        print("populating in en, id")
        global KNOWN_IMAGE_ENCODINGS
        KNOWN_IMAGE_ENCODINGS = []
        global GET_IMAGE_ID
        GET_IMAGE_ID = []
        
        gappend = GET_IMAGE_ID.append
        kappend = KNOWN_IMAGE_ENCODINGS.append
        for image_id, image_encoding in rows:
            gappend(image_id)
            kappend([float(i) for i in image_encoding.split(',')])
        print("en number of images in db: ", len(KNOWN_IMAGE_ENCODINGS))
        print("id number of images in db: ", len(GET_IMAGE_ID))

    # print(GET_IMAGE_ID)
    print("**************************************populate_encodings_from_db ENDS")


# CURL command: TODO
@app.route('/search_faces/', methods=['GET', 'POST'])
def search_faces():
    #Implement the logic for performing the facial search
    
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        print("**************************************search_faces POST STARTS")
        
        print("!!!!!!!!!! populating database images !!!!!!!!!!!!!!!!! STARTS")
        populate_encodings_from_db()
        print("!!!!!!!!!! populating database images !!!!!!!!!!!!!!!!! ENDS")
        
        fileOp = FileOperations()
        if not fileOp.isValid(request):
            return redirect(request.url), 400

        file = request.files['file']

        if fileOp.isFileTypeAllowed(file):

            print("filename: ", file.filename)
            k = int(request.form['k'])
            print("k: ", k)
            confidence_level = float(request.form['confidence_level'])
            print("confidence_level: ", confidence_level)
            tolerance_level = 1 - confidence_level
            print("tolerance_level: ", tolerance_level)

            # Load the uploaded image file
            unknown_image = face_recognition.load_image_file(file)
            # Get face locations for all faces in the uploaded image
            unknown_faces_locations = face_recognition.face_locations(unknown_image)
            # Get face encodings for all faces in the uploaded image
            unknown_faces_encodings = face_recognition.face_encodings(unknown_image, unknown_faces_locations)

            print("number of faces are: ", len(unknown_faces_encodings))
            print("en number of images in db: ", len(KNOWN_IMAGE_ENCODINGS))
            print("id number of images in db: ", len(GET_IMAGE_ID))
            
            if k >= len(GET_IMAGE_ID):
                k = len(GET_IMAGE_ID)-1
            
            matches = {}
            face_number = 0
            for face in unknown_faces_encodings:
                face_number += 1
                distances = face_recognition.face_distance(KNOWN_IMAGE_ENCODINGS, face)
                print("distances: ", distances)
                distances = np.array(distances)

                #top k highest confidences level encodings.
                top_k_indices = np.argpartition(distances, k)[:k]
                print("top_k_indices: ", top_k_indices)

                acceptable_image_idx = []

                _add = acceptable_image_idx.append
                for idx in top_k_indices:
                    if distances[idx] <= tolerance_level:
                        _add(GET_IMAGE_ID[idx])

                if not acceptable_image_idx:
                    print("!!!No acceptable images")
                    continue

                print("acceptable_image_idx: ", acceptable_image_idx)

                query = (
                    "Select image_id, person_name from images where image_id in %(image_ids)s"
                )
                param = {
                    "image_ids": acceptable_image_idx
                }
                image_info = db.query(query_stmt=query, param=param, debug=True)
                print("image_info: ", image_info)

                matches[f'face{face_number}'] = []
                for (image_id, person_name) in image_info:
                    matches[f'face{face_number}'].append({"image_id_in_db": image_id, "person_name": person_name})
            
            print("**************************************search_faces POST ENDS")
            return jsonify({
                "status" : "OK",
                "body" : {
                    "matches" : matches
                }
            }), 200
            
        print("**************************************search_faces POST ENDS")
    
    if request.method == 'GET':
        print("**************************************search_faces GET STARTS")
        print("rendering search_faces.html...")
        print("**************************************search_faces GET ENDS")

    # If no valid image file was uploaded, show the file upload form:
    return render_template('search_faces.html'), 200


# CURL command: TODO
@app.route('/add_face/', methods=['GET', 'POST'])
def add_face():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        print("**************************************add_face POST STARTS")
        
        fileOp = FileOperations()
        if not fileOp.isValid(request):
            return redirect(request.url), 400

        file = request.files['file']

        if fileOp.isFileTypeAllowed(file):
            # The image file seems valid! Save this image into the database.            
    
            # Extracting requried metadata.
            print("fileName: ", file.filename)
            version = fileOp.get_version(file.filename)
            print("version: ", version)
            person_name = fileOp.get_person_name(file.filename)
            print("person_name: ", person_name)
            location, date = fileOp.get_location_and_date(file)
            print("location: ", location)
            print("date: ", date)
            
            # Load the uploaded image file
            uploaded_image = face_recognition.load_image_file(file)
            # Get face encodings for face in the uploaded image
            image_encodings = face_recognition.face_encodings(uploaded_image)

            for image_encoding in image_encodings:
                # store encoding as a string
                image_encoding = ','.join([str(i) for i in image_encoding])
                print("len of encoding: ", len(image_encoding))
                
                query = (
                    "INSERT into images(person_name, version, date, location, image_encoding) values(%s, %s, %s, %s, %s)"
                )
                param = (
                    person_name, version, date, location, image_encoding
                )
                #saving record in database.
                db.transactional_query(query_stmt=query, param=param)

            print("--->>>>>>>>type file: ", type(file))
            
            print("**************************************add_face POST ENDS")
    
            return jsonify({
                 "status": "OK", 
                 "IMAGE_ADDED" : "TRUE",
                 "person_name" : person_name,
                 "version" : version
            }), 200

        print("**************************************add_face POST ENDS")
    
    if request.method == 'GET':
        print("**************************************add_face GET STARTS")
        print("rendering add_face.html...")
        print("**************************************add_face GET ENDS")

    # If no valid image file was uploaded, show the file upload form:
    return render_template('add_face.html'), 200


# CURL command: TODO
@app.route('/add_faces_in_bulk/', methods=['GET', 'POST'])
def add_faces_in_bulk():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        print("**************************************add_faces_in_bulk POST STARTS")
        
        fileOp = FileOperations()
        if not fileOp.isValid(request):
            return redirect(request.url), 400

        file = request.files['file']

        if file and isFileTypeZip(file.filename):
            # The image file seems valid! Save this image into the database.            
            print("--->>>type file: ", type(file))
            print("Zip filename: ", file.filename)
            zipfileName = file.filename.split('.')[0]
            
            try:
                if os.path.exists('./temp_images') and os.path.isdir('./temp_images'):
                    shutil.rmtree('./temp_images')
                
                os.mkdir('./temp_images')

                with zipfile.ZipFile(file) as zip_ref:
                    zip_ref.extractall('./temp_images')
                
                version, person_name, location, date = "", "", "", ""

                success = 0

                for root, dirs, files in os.walk('temp_images'):
                    for file_name in files:
                        filepath = f'./temp_images/{zipfileName}/' + file_name

                        # Extracting requried metadata.
                        print("fileName: ", file_name)
                        version = fileOp.get_version(file_name)
                        print("version: ", version)
                        person_name = fileOp.get_person_name(file_name)
                        print("person_name: ", person_name)
                        location, date = fileOp.get_location_and_date(filepath)
                        print("location: ", location)
                        print("date: ", date)  
            
                        # Load the uploaded image file
                        uploaded_image = face_recognition.load_image_file(filepath)
                        # Get face encodings for face in the uploaded image
                        image_encodings = face_recognition.face_encodings(uploaded_image)

                        for image_encoding in image_encodings:
                            # store encoding as a string
                            image_encoding = ','.join([str(i) for i in image_encoding])
                            print("len of encoding: ", len(image_encoding))
                            
                            query = (
                                "INSERT into images(person_name, version, date, location, image_encoding) values(%s, %s, %s, %s, %s)"
                            )
                            param = (
                                person_name, version, date, location, image_encoding
                            )
                            #saving record in database.
                            db.transactional_query(query_stmt=query, param=param)
                        
                        print(f'{file_name} saved in database!!!')
                        success += 1

                print("*******total number of files saved in bulk is!: ", success)
                shutil.rmtree('./temp_images')

            except Exception as e:
                if os.path.exists('./temp_images') and os.path.isdir('./temp_images'):
                    shutil.rmtree('./temp_images')
                print("Error in add_faces_in_bulk!!: ", e)
            
            print("**************************************add_faces_in_bulk POST ENDS")
            
            return jsonify({
                 "status": "OK", 
                 "ZIPfile_images_added" : "TRUE",
                 "ZipfileName": zipfileName,
                 "No. of files add successfully": success
            }), 200

        print("**************************************add_faces_in_bulk POST ENDS")
    
    if request.method == 'GET':
        print("**************************************add_faces_in_bulk GET STARTS")
        print("rendering add_faces_in_bulk.html...")
        print("**************************************add_faces_in_bulk GET ENDS")

    return render_template('add_faces_in_bulk.html'), 200


# CURL command: TODO
@app.route('/get_face_info/', methods=['GET', 'POST'])
def get_face_info():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        print("**************************************get_face_info POST STARTS")
        
        image_id = int(request.form['image_id'])

        query = (
            "select person_name, version, location, date from images where image_id = %(image_id)s"
        )
        param = {
            "image_id": image_id
        }
        (person_name, version, location, date) = db.query(query_stmt=query, param=param, debug=True)[0]

        print("**************************************get_face_info POST ENDS")
        return jsonify({
            "status": "OK", 
            "person_name": person_name,
            "version": version,
            "location": location,
            "date": date
        }), 200
    
    if request.method == 'GET':
        print("**************************************get_face_info GET STARTS")
        print("rendering get_face_info.html...")
        print("**************************************get_face_info GET ENDS")

    # If no valid image file was uploaded, show the file upload form:
    return render_template('get_face_info.html'), 200


@app.route('/', methods=['GET'])
def home():
    print("**************************************home GET STARTS")
    print("rendering homepage.html...")
    print("**************************************home GET ENDS")
    return render_template('homepage.html'), 200


# *********************** ENDPOINTS ENDS*********************************


# driver function
if __name__ == '__main__':
    # populate_encodings_from_db()
    app.run(host='127.0.0.1', port=5001, debug = True)