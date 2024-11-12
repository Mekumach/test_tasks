import requests
import datetime
import json

url = "https://yandex.com/time/sync.json?geo=213"

local_time_before_request = datetime.datetime.now()

response = requests.get(url).json()

deltas = []

# Время сервера и временная зона
server_time_ms = response["time"]
timezone_name = response["clocks"]["213"]["name"]
timezone_offset = response["clocks"]["213"]["offset"]

# Преобразуем время сервера в человекопонятный формат
server_time = datetime.datetime.fromtimestamp(server_time_ms / 1000)

# Дельта
delta = local_time_before_request - (server_time + datetime.timedelta(hours=timezone_offset / 3600000))

for _ in range(5):
    local_time_before_request = datetime.datetime.now()
    response = requests.get(url).json()

    server_time_ms = response["time"]
    server_time = datetime.datetime.utcfromtimestamp(server_time_ms / 1000)
    delta = local_time_before_request - (server_time + datetime.timedelta(hours=timezone_offset / 3600000))
    deltas.append(delta.total_seconds())

# Средняя дельта
avg_delta = sum(deltas) / len(deltas)

print("Сырой ответ:", json.dumps(response, indent=4, ensure_ascii=False))
print("Человекпонятный формат времени с сервера:", server_time.strftime('%Y-%m-%d %H:%M:%S'))
print(timezone_offset)
print("Временная зона:", timezone_name)
print("Международная разница во времени:", timezone_offset / 3600000, "часа")
print("Дельта:", delta)
print("Средняя дельта:", avg_delta)
