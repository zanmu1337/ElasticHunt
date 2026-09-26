import os
import json
import requests
import urllib3
from urllib.parse import quote, urlparse
from colorama import Fore, init

URL_FILE = "input.txt"
OUT_DIR = "output"
TIMEOUT = 5

init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

session = requests.Session()
session.verify = False

os.makedirs(OUT_DIR, exist_ok=True)

with open(URL_FILE, encoding="utf-8") as f:
    urls = [x.strip().rstrip("/") for x in f if x.strip()]

for base_url in urls:
    try:
        r = session.get(
            f"{base_url}/_cat/indices",
            params={"format": "json", "h": "index"},
            timeout=TIMEOUT
        )
        r.raise_for_status()

        indices = [
            x["index"]
            for x in r.json()
            if x.get("index")
        ]


        useful = [
            i for i in indices
            if i.lower() != "readme"
        ]

        if not useful:
            print(Fore.RED + f"[-] INVALID {base_url}")
            continue

        print(
            Fore.GREEN +
            f"[+] VALID {base_url} -> {', '.join(useful)}"
        )


        parsed = urlparse(base_url)

        filename = (
            f"{parsed.hostname}_{parsed.port or 'default'}.txt"
        )

        output_path = os.path.join(OUT_DIR, filename)

        found = False

        with open(output_path, "w", encoding="utf-8") as out:

            out.write(f"URL: {base_url}\n")
            out.write("=" * 80 + "\n\n")

            for index in useful:
                try:
                    encoded_index = quote(index, safe="")

                    res = session.get(
                        f"{base_url}/{encoded_index}/_search",
                        params={"size": 1000},
                        timeout=TIMEOUT
                    )
                    res.raise_for_status()

                    data = res.json()
                    hits = data.get("hits", {}).get("hits", [])

                    if not hits:
                        continue

                    found = True

                    out.write(f"\n### INDEX: {index}\n")
                    out.write("-" * 80 + "\n")


                    for hit in hits:
                        out.write(
                            json.dumps(
                                hit,
                                ensure_ascii=False,
                                indent=2
                            )
                        )
                        out.write("\n\n")

                    print(
                        Fore.GREEN +
                        f"    [+] {index}: {len(hits)} hits"
                    )

                except Exception as e:
                    print(
                        Fore.RED +
                        f"    [-] {index}: {e}"
                    )


        if not found:
            os.remove(output_path)
            print(Fore.RED + f"[-] NO DATA {base_url}")
        else:
            print(
                Fore.GREEN +
                f"[+] SAVED -> {output_path}"
            )

    except Exception as e:
        print(
            Fore.RED +
            f"[-] INVALID {base_url}: {e}"
        )