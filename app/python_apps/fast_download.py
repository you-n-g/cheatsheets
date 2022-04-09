"""
conda install scrapy
"""
import requests
from tqdm.auto import tqdm
from scrapy.selector import Selector
from pathlib import Path

out_dir = Path("lectures")
out_dir.mkdir(parents=True, exist_ok=True)

url = "https://www.stat.cmu.edu/~ryantibs/convexopt/"
resp = requests.get(url, verify=False)

ps = Selector(resp)

index = 1
for f_url in tqdm(ps.xpath('//*[@id="bord"]/a/@href').extract()):
    if f_url.startswith("lectures"):
        resp = requests.get(f"{url}{f_url}", verify=False)
        fname = f"{index:02d}-{f_url.split('/')[-1]}"
        with (out_dir / fname).open("wb") as f:
            f.write(resp.content)
        index += 1
