import requests
import re

# Il sito da scansionare
url_sito = "https://thisnot.business/eventi.php"
nome_file_m3u = "playlist.m3u"

def get_link():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url_sito, headers=headers, timeout=15)
        # Cerca il link .mpd
        match = re.search(r'https?://[^\s"\'<>]+?\.mpd', r.text)
        if match:
            return match.group(0)
    except Exception as e:
        print(f"Errore: {e}")
    return None

link_mpd = get_link()

if link_mpd:
    with open(nome_file_m3u, "w") as f:
        f.write("#EXTM3U\n")
        f.write("#EXTINF:-1, Evento Live\n")
        f.write(f"{link_mpd}\n")
    print(f"Successo! Link trovato: {link_mpd}")
else:
    print("Nessun link trovato. Forse non ci sono eventi live al momento.")
