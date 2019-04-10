import os.path
import psycopg2
from PIL import Image

image_map = { 
    'standard': {
        'width': 200,
        'height': 200,
        'path': '.200x200.1.1.100',
    },  
    'large': {
        'width': 400,
        'height': 400,
        'path': '.400x400.1.1.100',
    },  
    'small': {
        'width': 102,
        'height': 102,
        'path': '.102x102.1.1.100',
    },  
    'x-small': {
        'width': 60, 
        'height': 60, 
        'path': '.60x60.1.1.100',
    },  
    'thumb': {
        'width': 200,
        'height': 55, 
        'path': '.200x55.1.1.75',
    },  
}

def get_file_path(filename, profile=True):
    if profile:
        return '/home/ubuntu/job/uploads/profile/' + filename
    else:
        return '/home/ubuntu/uploads/' + filename


def get_thumb_path(filename, size_map, profile=True):
    file_parts = os.path.splitext(filename)
    file_path = file_parts[0] + size_map.get('path') + file_parts[1]
    if profile:
        return '/home/ubuntu/job/uploads/ooipThumber/uploads/profile/' + file_path
    else:
        return '/home/ubuntu/uploads/ooipThumber/uploads/' + file_path


conn = psycopg2.connect("dbname='sporple' user='postgres' host='sporple-db-master-postgresql' password='ae3aeFau7fah'")

curr = conn.cursor()

curr.execute("""SELECT image FROM sf_guard_user_profile LIMIT 15000""")

rows = curr.fetchall()
for row in rows:
    print "Finding file",row[0]
    if not row[0]:
        continue
    file_path = get_file_path(row[0])
    if not os.path.exists(file_path):
        print "Could not find file", file_path
        continue

    for size in ['large', 'small', 'x-small']:
        size_map = image_map.get(size)
        thumb_path = get_thumb_path(row[0], size_map=size_map)
        if not os.path.exists(thumb_path):
            print "Generating thumb:", thumb_path
            try:
                image = Image.open(file_path)
            except Exception,e:
                print "OPENERROR:", e
                continue
            image.thumbnail((size_map.get('width'), size_map.get('height')), Image.ANTIALIAS)
            try:
                image.save(thumb_path)
            except Exception,e:
                print "ERROR: ", e
                continue
            print "Generated thumb", thumb_path
        else:
            print "Found thumb", thumb_path

    print "Done", file_path

print "ALL DONE"
