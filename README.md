# cs305_2022

## [Assignment 2](https://drive.google.com/file/d/1M2gu-h4suRn6CH0LmYtmJgDCyS4IsVUl/view?usp=sharing)

## [Repository Link](https://github.com/dhakad-anant/cs305_2022)

### Submitter name: Anant Dhakad

### Roll No.: 2019CSB1070

### Course: Software Engineering (CS305)

=================================

1. What does the program do?
This programme is a web application that allows users to search for people using their faces in a database of photos. This application provides an API for uploading a single image or a collection of images in a zip file, and it keeps them in a MySQL database. It also has an endpoint for retrieving information about a picture if the image id matches the id contained in the database. The facial search function is provided by another endpoint.

2. How does the program work?
This program uses the following tech stack. 
Mysql : for database
Web framework: flask
For the programme to work properly, you'll need the face recognition library. This software will run on a Linux system.
The app.py file contains the app's main code. The four api endpoints are represented by four functions in this application.
When the insert in bulk endpoint is called, it extracts all of the photos from the zip file into a separate folder and then copies them all into the images folder. After that, the files were pushed into the database. It just pushes a single file into the database with the add face method.
The add face, add face in bulk, get face info, and search faces APIs are all available.
Some endpoints require data to be sent by pressing the upload button. When uploading a file, make sure it's the right one.


It is assumed that the images used are of the format of the lzw_database images. 

3. How to run the program?

a) First unzip the file provided. Then make sure to install the following python modules: (face_recognition,mysqlclient,flask-mysqldb,coverage,pytest,requests).
Then run.
```
>> pip install -r requirements.txt
```

b) Then enter your mysql credentials in pkg/main.py

c) create a database named "face" in your mysql shell using command "create database face;"


For running the server:
a) navigate to into the extrated folder and run
```
>> python initialize_db_start.py
```
This command will create the tables automatically. Close this server by ctrl+c

b) then run
```
>> python main_start.py
```
This command will start the server at http://127.0.0.1:5001/
Go to any of the endpoints to interact with the endpoints.


For running the test (make sure you have executed "python initialize_db_start.py" before this)
```
>> coverage run -m pytest
```

To get report in shell
```
>> coverage report -m
```

To get the coverage in html
```
>> coverage html
```
Go to the index.html page to get the coverage.
The coverage is well above the limit (85%) 
