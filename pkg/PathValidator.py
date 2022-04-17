import os
import sys

ALLOWED_EXTENSIONS = ['jpeg', 'png', 'jpg']

class PathValidator:

    def exitProgram(self, message):
        sys.exit("------------------- " + message + "\n\nExiting Program...\n")

    def validate(self, path, flag) -> bool:
        # checking if the flag is valid
        if flag not in ('-file', '-dir'):
            self.exitProgram(f"Error: Invalid flag value -> {flag}")

        isFile = (flag == '-file')

        # checking if the path is valid
        if isFile:
            self.validExtension(path)
        if isFile and not os.path.isfile(path):
            self.exitProgram(f"Error: Invalid file path -> {path}")
        if not isFile and not os.path.isdir(path):
            self.exitProgram(f"Error: Invalid directory path -> {path}")
        
        print("Path Validated...")
        return True

    def validExtension(self, path):
        extension = ''
        if path[-4] == '.':
            extension = path[-3:]
        elif path[-5] == '.':
            extension = path[-4:]
        
        print(f'file extension is -> {extension}...')
        
        if extension not in ALLOWED_EXTENSIONS:
            self.exitProgram(f"Error: Invalid file extension -> {extension}")


        