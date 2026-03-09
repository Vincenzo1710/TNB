import requests
import re
import os

url_sito = "https://thisnot.business/eventi.php"
nome_file_m3u = "playlist.m3u"

def get_link():
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        r = requests.get(url_sito, headers=headers, timeout=15)
        # Cerchiamo il link .mpd nel testo della pagina
        match = re.search(r'https?://[^\s"\'<>]+?\.mpd', r.text)
        if match:
            return match.group(0)
    except Exception as e:
        print(f"Errore: {e}")
    return None

link_mpd = get_link()

# Creiamo sempre il file, anche se vuoto, per non far fallire GitHub Actions
with open(nome_file_m3u, "w") as f:
    f.write("#EXTM3U\n")
    if link_mpd:
        f.write("#EXTINF:-1, Evento Live\n")
        f.write(f"{link_mpd}\n")
        print(f"Link trovato: {link_mpd}")
    else:
        f.write("#EXTINF:-1, Nessun evento attivo al momento\n")
        f.write("http://0.0.0.0/no-link.mp4\n")
        print("Nessun link trovato, creato file di segnaposto.")
