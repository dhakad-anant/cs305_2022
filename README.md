# cs305_2022

### Submitter name: Anant Dhakad

### Roll No.: 2019CSB1070
    
### Course: Software Engineering (CS305)

=================================

1. What does the program do?

This program extracts information (metadata such as Title, ISBN, Author, Publisher) from the cover pages of the books. It can also process a batch of images from a directory.

2. How does the program work?

Title:
Program extract title from images based on maximum height of extracted text from the images.
Author & Publisher:
Program verifies using a nlp library "Spacy". It finds most suitable names from the extracted text.
ISBN:
Program extracts ISBN based on keyword match.

3. How to run the program?

---> For running the Program for a single image
```>>> 
python main.py -file 'path_to_image'
```
- Here path_to_image should be relative
- You should run this command from inside pkg folder
Example
```
>>> python main.py -file 'images/cleancode.png'
```

---> For running the Program for multiple images (directory)
```
>>> python main.py -dir 'path_to_dir'
```
- Here path_to_dir should be relative
- You should run this command from inside pkg folder
Example
```
>>> python main.py -file 'images/'
```

---> For testing the code (first open terminal inside the root folder , i.e. parent folder of pkg) or (open terminal just outsiide of pkg)
```
>>> coverage run -m pytest

# for html report
>>> coverage html -i

# for report in shell
>>> coverage report -i
```