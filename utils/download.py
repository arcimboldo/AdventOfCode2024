import requests
import requests.cookies
import os

BASEURL = "https://adventofcode.com/2024/day/{day}/input"

SESSION_COOKIE = os.getenv("AOC_SESSION")


def get(day: int, path: str):
    if os.path.exists(path):
        return
    if not SESSION_COOKIE:
        raise ValueError(
            f"You need to set AOC_SESSION environment variable to download the input file into {path}"
        )
    url = BASEURL.format(day=day)
    s = requests.session()
    s.cookies.set("session", SESSION_COOKIE, domain=".adventofcode.com")
    resp = requests.get(url=url, cookies=s.cookies)
    if resp.status_code != 200:
        raise Exception(f"{url} returned error {resp.status_code}: {resp.content}")
    print(f"Input for day {day} returned {resp.status_code}")
    with open(path, "w") as fd:
        fd.write(resp.text)


def read(day: int) -> str:
    path = f"{os.getcwd()}/{day:02}.input.txt"
    get(day, path)
    return open(path).read().strip()
