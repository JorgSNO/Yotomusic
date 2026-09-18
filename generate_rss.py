import os
import xml.etree.ElementTree as ET
from urllib.parse import quote
from datetime import datetime, timedelta

# Konfigurasjon - Bytt ut med dine egne detaljer
GITHUB_USER = "DITT_GITHUB_BRUKERNAVN"
REPO_NAME = "my-podcast-feed"
BASE_URL = f"https://{GITHUB_USER}.github.io/{REPO_NAME}/mp3/"
# Det er sterkt anbefalt å legge til et kvadratisk JPG-bilde i repositoriet ditt for Yoto-appen!
IMAGE_URL = f"https://{GITHUB_USER}.github.io/{REPO_NAME}/podcast_cover.jpg"

# Definer namespaces korrekt for iTunes/Yoto
ET.register_namespace('itunes', 'http://itunes.com')

rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")

# Obligatoriske Yoto-felt
ET.SubElement(channel, "title").text = "Mine Yoto Sanger og Lydbøker"
ET.SubElement(channel, "link").text = f"https://github.com{GITHUB_USER}/{REPO_NAME}"
ET.SubElement(channel, "description").text = "Lydfiler tilpasset Yoto-spilleren via GitHub."
ET.SubElement(channel, "language").text = "no"

# iTunes/Yoto spesifikke kanalinnstillinger
ET.SubElement(channel, "{http://itunes.com}author").text = "Yoto Creator"
ET.SubElement(channel, "{http://itunes.com}explicit").text = "no"

image_element = ET.SubElement(channel, "{http://itunes.com}image")
image_element.set("href", IMAGE_URL)

# Hent alle MP3-filer og sorter dem alfabetisk (slik at spor 1, spor 2 osv. blir riktig)
mp3_files = sorted([f for f in os.listdir("mp3") if f.endswith(".mp3")])

# Yoto foretrekker publiseringsdatoer for å sortere rekkefølgen på sporene i appen
base_date = datetime.now() - timedelta(days=len(mp3_files))

for index, filename in enumerate(mp3_files):
    item = ET.SubElement(channel, "item")
    
    # Fjern filendelse for en ren tittel i Yoto-appen
    clean_title = filename.replace(".mp3", "")
    ET.SubElement(item, "title").text = clean_title
    
    file_url = BASE_URL + quote(filename)
    
    # Enclosure forteller Yoto hvor MP3-filen ligger
    ET.SubElement(item, "enclosure", url=file_url, type="audio/mpeg", length="0")
    ET.SubElement(item, "guid", isPermaLink="true").text = file_url
    
    # Unik publiseringsdato per spor sikrer riktig rekkefølge i Yoto-appen
    track_date = base_date + timedelta(days=index)
    ET.SubElement(item, "pubDate").text = track_date.strftime("%a, %d %b %Y %H:%M:%S +0000")
    
    # iTunes-tagger for sporet
    ET.SubElement(item, "{http://itunes.com}title").text = clean_title
    ET.SubElement(item, "{http://itunes.com}episode").text = str(index + 1)

tree = ET.ElementTree(rss)
ET.indent(tree, space="  ")
tree.write("feed.xml", encoding="utf-8", xml_declaration=True)
