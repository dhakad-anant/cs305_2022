from PIL import Image
from PIL.ExifTags import TAGS

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class FileOperations():
    def __init__(self):
        pass 
    def isValid(self,request):
        if 'file' not in request.files:
            return False
        
        if request.files['file'].filename=="":
            return False
        
        return True
    
    def isFileTypeAllowed(self,file):
        if file and allowed_file(file.filename):
            return True 
        return False
    
    def get_version(self,fileName):
        version = int(fileName.split('.')[0].split('_')[-1], 10)
        return version
    
    def get_person_name(self,fileName):
        name = fileName.split('.')[0].split('_')[:-1]
        name = '_'.join(name)
        return name

    def get_location_and_date(self, file): 
        """ we can also pass filePath """
        location = ''
        date = ''

        image = Image.open(file)
        exifdata = image.getexif()
        
        for tag_id in exifdata:
            tagname = str(TAGS.get(tag_id, tag_id))
            value = exifdata.get(tag_id)
            
            if tagname == 'DateTimeOriginal':
                date = str(value)
            if tagname == 'GPSInfo':
                location = str(value)
        
        return location, date

        