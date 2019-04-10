import os.path
MAP = {
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
    'icon': {
        'width': 72,
        'height': 72,
        'path': '.72x72.1.1.100',
    },
}

'''
Generate resize url.
'''
def get_resized(path, size):
    file_parts = os.path.splitext(path)
    resize_path = ('/uploads/ooipThumber'
            + file_parts[0]
            + MAP.get(size).get('path')
            + file_parts[1])
    return resize_path
