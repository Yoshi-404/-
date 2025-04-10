# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime


# 出発駅・到着駅
departure_station = input("出発駅を入力してください：")
destination_station = input("到着駅を入力してください：")

# 出発 or 到着を選択
search_type = input("出発時間で検索するなら1、到着時間で検索するなら4を入力してください：")

# 日付と時間の指定
# 年の固定
year = 2025

# 日付を今日にするか、自分で入力するか選択
date_option = input("日付を今日にするなら 1、自分で指定するなら 2 を入力してください：")

if date_option == "1":
    today = datetime.today()
    month = today.strftime("%m")
    day = today.strftime("%d")
else:
    month = input("月（例：04）：").zfill(2)
    day = input("日（例：10）：").zfill(2)

# 時間入力
hour = input("時（0-23）：").zfill(2)
minute = input("分（0-59）：").zfill(2)
m1 = minute[0]  # 10の位
m2 = minute[1]  # 1の位


# 分を2桁で分割
minute = minute.zfill(2)
m1 = minute[0]  # 10の位
m2 = minute[1]  # 1の位

# URL構築
route_url = (
    "https://transit.yahoo.co.jp/search/print?"
    f"from={departure_station}&to={destination_station}"
    f"&type={search_type}&y={year}&m={month}&d={day}&hh={hour}&m1={m1}&m2={m2}"
)

print("検索URL：", route_url)

# Webページ取得
route_response = requests.get(route_url)
route_soup = BeautifulSoup(route_response.text, 'html.parser')

# 経路サマリー
route_summary = route_soup.find("div", class_="routeSummary")
required_time = route_summary.find("li", class_="time").get_text()
transfer_count = route_summary.find("li", class_="transfer").get_text()
fare = route_summary.find("li", class_="fare").get_text()

print(f"====== {departure_station} から {destination_station} ======")
print("所要時間：" + required_time)
print(transfer_count)
print("料金：" + fare)

# 経路詳細
route_detail = route_soup.find("div", class_="routeDetail")

# 駅名取得
stations = [station.get_text().strip() for station in route_detail.find_all("div", class_="station")]

# 路線名取得
lines = [
    line.find("div").get_text().strip()
    for line in route_detail.find_all("li", class_="transport")
]

# 所要時間取得
estimated_times = [
    estimated_time.get_text()
    for estimated_time in route_detail.find_all("li", class_="estimatedTime")
]

# 料金取得
fars = [
    fare.get_text().strip()
    for fare in route_detail.find_all("p", class_="fare")
]

# 出力
print("======乗り換え情報======")
for station, line, estimated_time, fare in zip(stations, lines, estimated_times, fars):
    print(station)
    print(" | " + line + " " + estimated_time + " " + fare)

print(stations[-1])