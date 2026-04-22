from os import mkdir
from os.path import isdir

import json
import parser
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from bs4 import BeautifulSoup

if not isdir("./data"):
    mkdir("data")

institutions = {
    65718: "Biologisk Institut",
    1932: "Datalogisk Institut",
    2245: "Institut for Fødevare- og Ressourceøkonomi",
    1915: "Institut for Geovidenskab og Naturforvaltning",
    1950: "Institut for Idræt og Ernæring",
    1869: "Institut for Matematiske Fag",
    2160: "Institut for Naturfagenes Didaktik",
    2238: "Institut for Plante- og Miljøvidenskab",
    1568: "Kemisk Institut",
    65707: "Niels Bohr Institutet"
}

url = "https://karakterstatistik.stads.ku.dk/Search/Courses"

# Get fresh cookie
session = requests.Session()
_ = session.get(url)
# use _ to indicate that we do not need the returned response (new convention I learned through LSP)

# headers and payload for request
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "XMLHttpRequest",
}
payload = {
    "searchText": "",
    "term": "",
    "block": "",
    "faculty": 1868, # Basing to the faculty of "Natur- og Biovidenskabelige fakultet"
    "institute": 0,
    "page": 0,
}


for ins_id, ins_name in institutions.items():
    print(f"Scraping {ins_name}")
    payload["institute"] = ins_id
    payload["page"] = 1
    data = {}
    while True:
        # Make request and initiate beautifulsoup instance
        res = session.post(url, headers=headers, data=payload)
        soup = BeautifulSoup(res.text, "html.parser")

        if soup.find("td").text.strip() == "Søgning returnerede ingen resultater.":
            # no more pages break and go to next institute
            print("Finished scrapping institution")
            break
        print(f"scraping page {payload["page"]}")

        # Get all links in html (every link to a course Histogram) 
        # trying to do it concurrently to make it faster, tqdm just for progress bar
        links = [a.get("href") for a in soup.find_all("a") if a.get("href") and "Histogram" in a.get("href")]
        with ThreadPoolExecutor(max_workers=20) as ex:
            results = list(tqdm(ex.map(parser.parse_link, links), total=len(links)))

        data.update({result[0]: result[1] for result in results}) 
        payload["page"] += 1


    with open(f"./data/{institutions[ins_id]}.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
