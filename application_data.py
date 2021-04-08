import json
import database as db
import os
import glob
import jellyfish

whitelist = ['YIFY', 'srt', 'mkv', 'mp4', 'wmv']
blacklist = ['sample']

def set_application_path(path):
    payload = json.dumps({'path':path, 'theme': 'Light'})
    with open('application.json', 'w') as f:
        f.write(payload)
        f.close()
        return f'changed library path to {path}'

def get_library_path():
    with open('application.json', 'r') as f:
        lines = f.readlines()
        return json.loads(lines[0])

def fix_files(title):
    path = get_library_path()['path']
    torrent = db.get_torrent(title)
    #dirs = os.listdir(path)
    files = glob.glob(f'{path}\\*')
    newest_file = max(files , key = os.path.getctime)
    # if file is Dir
    if os.path.isdir(newest_file):
        print(newest_file)
        # Rating similary of filename vs actual title
        ratings = []
        dir_items = os.listdir(newest_file)
        for item in dir_items:
            ratings.append(jellyfish.levenshtein_distance(item, title))
        # finding best match(es)
        matches = []
        for i in range(len(dir_items)):
            if ratings[i] == min(ratings):
                matches.append(dir_items[i])
        for m in matches:
            extension = m.split('.')[-1]
            os.rename(f'{newest_file}\\{m}', f'{path}\\{torrent[0]}.{extension}')
        #print(dir_items)
    else:
        # renaming file
        old_filename = newest_file.split('\\')[-1]
        extension = old_filename.split('.')[-1]
        os.rename(f'{path}\\{old_filename}', f'{path}\\{torrent[0]}.{extension}')

if __name__ == '__main__':
    fix_files('Shrek (2001) 1080p BrRip x264 - 1GB- YIFY')
    #set_application_path('test')
    #print(get_library_path()['path'])