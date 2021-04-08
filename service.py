from flask import Flask, render_template, request, url_for, jsonify
from flask_cors import CORS
import torrent_lookup as tl
import application_data as ad
import torrent_downloader as td
import database as db
import json

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins":["http://localhost:5000"]}},supports_credentials=True)

# Scrapes piratebay for torrent with input name
@app.route('/lookup', methods=['POST'])
def lookup():
    try:
        input_json = request.get_json(force=True)
        return jsonify(tl.lookup(input_json['name']))
    except Exception as e:
        return jsonify(str(e))

# returns the defined library path for plex
@app.route('/path', methods=['GET'])
def get_path():
    try:
        return ad.get_library_path()
    except Exception as e:
        return jsonify(str(e))

# returns torrent download information
@app.route('/torrents', methods=['GET'])
def get_active_torrents():
    try:
        return jsonify(td.get_torrent_info())
    except Exception as e:
        return jsonify(str(e))

# Sets plex library path to given input
@app.route('/setpath', methods=['POST'])
def set_path():
    try:
        input_json = request.get_json(force=True)
        return ad.set_application_path(input_json['path'])
    except Exception as e:
        return jsonify(str(e))

# starts download of torrent with qtbittorent client
@app.route('/download', methods=['POST'])
def download_torrent():
    try:
        input_json = request.get_json(force=True)
        # Creating order dict for db logging
        order = {'origin_title': input_json['origin_title'], 'title': input_json['title'], 'magnet': input_json['magnet'], 'status': input_json['status']}
        return jsonify(td.download_torrent(order))
    except Exception as e:
        return jsonify(str(e))


# resumes or pauses qtbittorrent client
@app.route('/control', methods=['POST'])
def control_torrents():
    try:
        input_json = request.get_json(force=True)
        return td.control_torrents(input_json['control'])
    except Exception as e:
        return jsonify(str(e))

# returns original title from origin_title
@app.route('/title', methods=['POST'])
def get_origin_title():
    try:
        input_json = request.get_json(force=True)
        print(input_json)
        return jsonify(td.get_origin_title(input_json['title']))
    except Exception as e:
        return jsonify(str(e))


# set new origin title
@app.route('/settitle', methods=['POST'])
def set_origin_title():
    try:
        input_json = request.get_json(force=True)
        return jsonify(td.set_origin_title(input_json['origin_title'], input_json['title']))
    except Exception as e:
        return jsonify(str(e))



if __name__ == '__main__':
    db.init_app()
    app.run(host="0.0.0.0", port="5000")
