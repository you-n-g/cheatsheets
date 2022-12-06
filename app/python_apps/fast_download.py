"""
conda install scrapy
"""
import re
import urllib
import requests
from tqdm.auto import tqdm
from scrapy.selector import Selector
from pathlib import Path


def download(url="https://www.stat.cmu.edu/~ryantibs/convexopt/", download_url_xpath='//*[@id="bord"]/a/@href', url_reg="^lectures", out_dir="download", dry_run=False, verbose=False):
    """
    python app/python_apps/fast_download.py "https://www.bradyneal.com/causal-inference-course" "//table//a/@href"  "^/slides/"
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    resp = requests.get(url, verify=False)

    ps = Selector(resp)

    index = 1

    for f_url in tqdm(ps.xpath(download_url_xpath).extract()):
        if verbose:
            print(f_url)
        m = re.match(url_reg, f_url)
        if m is not None:
            fname = f"{index:02d}-{urllib.parse.unquote(f_url).split('/')[-1]}"
            if dry_run:
                print(fname, f_url)
            else:
                if f_url.startswith("/"):
                    up = urllib.parse.urlparse(url)
                    req_url = f"{up.scheme + '://' + up.hostname}{f_url}"
                else:
                    req_url = f"{url}{f_url}"
                resp = requests.get(
                    req_url,
                    verify=False,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
                    },
                )
                with (out_dir / fname).open("wb") as f:
                    f.write(resp.content)
            index += 1

import fire
if __name__ == "__main__":
    fire.Fire(download)
