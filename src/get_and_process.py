import requests
from wdcuration import query_wikidata
import json
import pandas as pd
import time
import tqdm

country = "PA"
query = """SELECT ?code WHERE {
  ?item wdt:P297 ?code .
  wd:Q18 wdt:P150 ?item . # South America
  }"""
countries = query_wikidata(query)

hotspots = []
for country in tqdm.tqdm(countries):
    code = country["code"]
    new_hotspots = requests.get(
        f"https://api.ebird.org/v2/ref/hotspot/{code}?fmt=json"
    ).json()
    hotspots.extend(new_hotspots)
    time.sleep(0.2)

processed_hotspots = []
for entry in hotspots:
    loc_id = entry["locId"]
    name = entry["locName"].split("--")[-1]
    blurb = entry["locName"].split("--")[0].strip()
    name = entry["locName"].split("-")[-1]
    blurb = entry["locName"].split("-")[0].strip()

    description = f' country: {entry["countryCode"]}, region: {entry["subnational1Code"]} ({blurb})'
    processed_hotspots.append({"id": loc_id, "name": name, "description": description})


df = pd.DataFrame.from_dict(processed_hotspots)
df.to_csv("ebird_south_america.csv", index=False)
