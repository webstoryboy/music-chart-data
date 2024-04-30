import requests as req
from bs4 import BeautifulSoup as bs
import json
import datetime

# 현재 날짜를 문자열로 저장
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

head = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
res = req.get("https://www.melon.com/chart/index.htm", headers=head)

# print(res.text)
# print(res.status_code)  #406

soup = bs(res.text, "lxml")

# 데이터 선택
ranking = soup.select("tbody .wrap.t_center > .rank")
title = soup.select("tbody .wrap_song_info .ellipsis.rank01 span > a")
artist = soup.select("tbody .wrap_song_info .ellipsis.rank02 span > a:nth-child(1)")
image = soup.select("tbody .image_typeAll > img")
album = soup.select("tbody .wrap_song_info .ellipsis.rank03 > a")

# print(len(image))

# 데이터 저장
rankings = [r.text.strip() for r in ranking]
titles = [t.text.strip() for t in title]
artists = [a.text.strip() for a in artist]
images = [i.get('src') for i in image]
albums = [a.text.strip() for a in album]

# 데이터 프레임 생성
chart_data = []
for ranking, title, artist, image_url, album in zip(rankings, titles, artists, images, albums):
    chart_data.append({
        "rank": ranking,
        "title": title,
        "artist": artist,
        "imageURL": image_url,
        "album": album
    })

# 파일 이름 설정
file_name = f"melon/melon100_{current_date}.json"

# JSON 파일로 저장
with open(file_name, 'w', encoding='utf-8') as file:
    json.dump(chart_data, file, ensure_ascii=False, indent=4)
