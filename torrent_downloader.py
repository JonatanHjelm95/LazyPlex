from qbittorrent import Client
import database as db
import application_data as ad
import json
from dotenv import load_dotenv
import os

load_dotenv('.env')
user = os.getenv('USER')
password = os.getenv('PASS')

def get_save_path():
    with open('application.json', 'r') as f:
        prinf.readlines()

def download_torrent(order):
    qb = Client("http://127.0.0.1:8085/")
    qb.login(user, password)
    app_data = ad.get_library_path()
    qb.download_from_link(order['magnet'], savepath=app_data['path'])
    db.insert_order(order)
    return 'downloading torrent'


def pause_all():
    qb = Client("http://127.0.0.1:8085/")
    qb.login(user, password)
    qb.pause_all()

def start_all():
    qb = Client("http://127.0.0.1:8085/")
    qb.login(user, password)
    qb.resume_all()

def control_torrents(control):
    if control == 'start':
        start_all()
        return 'resuming downloads'
    elif control == 'stop':
        pause_all()
        return 'pausing downloads'
    else:
        return 'unknown command'

def get_origin_title(title):
    return db.get_title_from_origin_title(title)

def set_origin_title(original_title, title):
    return db.set_origin_title(original_title, title)


def get_torrent_info():
    qb = Client("http://127.0.0.1:8085/")
    qb.login(user, password)
    torrents = qb.torrents()
    active_torrents = db.get_active_torrents()
    torr = []
    for i in range(len(torrents)):
        for a in active_torrents:
            if a[1] == torrents[i]['name']:
                info  = {'name' : torrents[i]["name"], 'hash': torrents[i]["hash"], 'seeds': torrents[i]["num_seeds"], 'progress': torrents[i]['progress'], 'size': get_size_format(torrents[i]["total_size"]), 'speed': get_size_format(torrents[i]["dlspeed"]) +'/s'}
                torr.append(info)
                if torrents[i]['progress'] == 1:
                    db.finished_downloading_title(torrents[i]['name'])
                    ad.fix_files(torrents[i]['name'])
    # if no active torrents / stop seeding
    if len(torr) == 0:
        pause_all()
        return 'no torrents'
    return torr

def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"

if __name__ == '__main__':
    #download_torrent('magnet:?xt=urn:btih:223F7484D326AD8EFD3CF1E548DED524833CB77E&dn=Avengers.Endgame.2019.1080p.BRRip.x264-MP4&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2920%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.pirateparty.gr%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.cyberia.is%3A6969%2Fannounce')
    #download_torrent('magnet:?xt=urn:btih:6B56C0579AD115B4AE9E32D9459FFE2C721FEE32&dn=VMware+Workstation+PRO+15.0+%2B+Serials+%5BTechTools%5D&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2920%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.pirateparty.gr%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.cyberia.is%3A6969%2Fannounce')
    #pause_all()
    #start_all()
    print(get_torrent_info())