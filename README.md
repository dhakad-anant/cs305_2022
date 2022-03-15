# cs305_2022

## [Midsem](https://drive.google.com/file/d/1GUqhOd0hJp9H-s3L1thqFIvVfYrumzmv/view?usp=sharing)

## [Repository Link](https://github.com/dhakad-anant/cs305_2022)

### Submitter name: Anant Dhakad

### Roll No.: 2019CSB1070

### Course: Software Engineering (CS305)

=================================


Steps for compilation:

1. Create three instances of command line in the 'midsem/' directory
2. for initiating the server run
    - python server.py
3. for running the source (client who sends message)
    - python source.py [ipAddress of source] [port number of source]
    - Example: python source.py 127.0.0.1 23001 
3. for running the receiver (client who receivers message)
    - python receiver.py [ipAddress of receiver] [port number of receiver]
    - Example: python receiver.py 127.0.0.1 44001 
4. then go to 'http://127.0.0.1:23001/foo' (whatever link is specified in the message.xml)