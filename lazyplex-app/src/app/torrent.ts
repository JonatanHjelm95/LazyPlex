export interface Torrent {
        magnet: string;
        name: string;
        info: string;
        seeders: number;
        leechers: number;
        trusted: boolean;
}
