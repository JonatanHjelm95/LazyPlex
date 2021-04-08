import sqlite3


def init_db():
    con = sqlite3.connect('lazyplex.db')
    
# Create table for movies
def create_movie_table():
    pass
    # TODO
    # title, year, imdb-rating, genre?


def create_order_table():
    con = sqlite3.connect('lazyplex.db')
    cur = con.cursor()
    #origin_title, title, magnet, status
    cur.execute('''CREATE TABLE orders
               (origin_title text, title text, magnet text primary key ON CONFLICT REPLACE, order_status text)''')
    con.commit()


def insert_order(order):
    con = sqlite3.connect('lazyplex.db')
    cur = con.cursor()
    cur.execute(f"INSERT INTO orders VALUES ('{order['origin_title']}','{order['title']}','{order['magnet']}','{order['status']}')")
    con.commit()

def finished_downloading_magnet(magnet):
    con = sqlite3.connect('lazyplex.db')
    cur = con.cursor()
    cur.execute(f"UPDATE orders SET order_status = 'finished' WHERE magnet = '{magnet}'")
    con.commit()

def finished_downloading_title(title):
    con = sqlite3.connect('lazyplex.db')
    cur = con.cursor()
    cur.execute(f"UPDATE orders SET order_status = 'finished' WHERE title = '{title}'")
    con.commit()

def get_torrent(title):
    con = sqlite3.connect('lazyplex.db')
    cur = con.cursor()
    cur.execute(f"SELECT * from orders WHERE title = '{title}'")
    return cur.fetchone()

def set_origin_title(origin_title, title):
    con = sqlite3.connect('lazyplex.db')
    cur = con.cursor()
    cur.execute(f"UPDATE orders SET origin_title = '{origin_title}' WHERE title = '{title}'")
    con.commit()
    return f'title has been changed to {origin_title}'

def get_title_from_origin_title(title):
    con = sqlite3.connect('lazyplex.db')
    cur = con.cursor()
    cur.execute(f"SELECT * from orders WHERE title = '{title}'")
    return cur.fetchone()[0]


# Returns list of dicts containing torrent info
def get_active_torrents():
    con = sqlite3.connect('lazyplex.db')
    cur = con.cursor()
    q = f"SELECT * from orders where order_status = 'active'"
    cur.execute(q)
    return list(cur.fetchall())

def init_app():
    init_db()
    create_order_table()

if __name__ == '__main__':
    init_app()
    #set_origin_title('test', 'Avengers.Infinity.War.2018.1080p.BRRip.x264-MP4')
    #print(get_title_from_origin_title('Avengers.Infinity.War.2018.1080p.BRRip.x264-MP4'))
    #get_active_torrents()
    #pass
    #mag = 'magnet:?xt=urn:btih:8FD93E1A5B18EBF27972E3E8650CD577C9075AC7&dn=John.Wick.Chapter.3+-+Parabellum.2019.1080p.BRRip.x264-MP4&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2920%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.pirateparty.gr%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.cyberia.is%3A6969%2Fannounce'
    #finished_downloading(mag)
    #order = {'origin_title': 'test', 'title': 'test1', 'magnet': '123', 'status': 'active'}
    #insert_order(order)