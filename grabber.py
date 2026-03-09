import requests
import re

url_sito = "https://thisnot.business/eventi.php"
nome_file_m3u = "playlist.m3u"

def get_links():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Referer': 'https://thisnot.business/'
    }
    try:
        response = requests.get(url_sito, headers=headers, timeout=20)
        content = response.text
        
        # Cerca tutti i link che finiscono con .mpd o .m3u8
        # Cerchiamo anche link che iniziano con // (senza http)
        found_links = re.findall(r'(https?://[^\s"\'<>]+?\.(?:mpd|m3u8))', content)
        
        # Rimuove duplicati mantenendo l'ordine
        return list(dict.fromkeys(found_links))
    except Exception as e:
        print(f"Errore durante il recupero: {e}")
        return []

links = get_links()

with open(nome_file_m3u, "w") as f:
    f.write("#EXTM3U\n")
    if links:
        print(f"Trovati {len(links)} link!")
        for i, link in enumerate(links):
            f.write(f"#EXTINF:-1, Evento {i+1}\n")
            f.write(f"{link}\n")
    else:
        f.write("#EXTINF:-1, Nessun evento trovato - Riprova tra un'ora\n")
        f.write("http://0.0.0.0/no-link.mp4\n")
        print("Nessun link trovato nel codice della pagina.")
