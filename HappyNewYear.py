import pandas as pd
from math import radians, cos, sin, asin, sqrt

USTUG_LAT = 60.7603243
USTUG_LON = 46.3053893
MAX_WEIGHT = 100


def geo_distance(lon1, lat1, lon2, lat2):
    dlon = radians(lon2) - radians(lon1)
    dlat = radians(lat2) - radians(lat1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r

def calculate_route_distance(route, gift_data):
    total_distance = 0
    prev_lon, prev_lat = USTUG_LON, USTUG_LAT
    for gift_id in route:
        lon, lat = gift_data.loc[gift_id, ['Longitude', 'Latitude']]
        total_distance += geo_distance(prev_lon, prev_lat, lon, lat)
        prev_lon, prev_lat = lon, lat
    total_distance += geo_distance(prev_lon, prev_lat, USTUG_LON, USTUG_LAT)
    return total_distance


def nearest_neighbor(group, gift_data):
    unvisited = set(group)
    route = []
    current_lon, current_lat = USTUG_LON, USTUG_LAT

    while unvisited:
        nearest = None
        min_distance = float('inf')
        for gift_id in unvisited:
            lon, lat = gift_data.loc[gift_id, ['Longitude', 'Latitude']]
            distance = geo_distance(current_lon, current_lat, lon, lat)
            if distance < min_distance:
                min_distance = distance
                nearest = gift_id
        route.append(nearest)
        unvisited.remove(nearest)
        current_lon, current_lat = gift_data.loc[nearest, ['Longitude', 'Latitude']]
    return route

def group_gifts_by_weight(gift_data):
    groups = []
    current_group = []
    current_weight = 0

    for _, row in gift_data.iterrows():
        weight = row['Weight']
        if weight > MAX_WEIGHT:
            print(f"Подарок {row.name} превышает максимальный вес и будет пропущен.")
            continue

        if current_weight + weight <= MAX_WEIGHT:
            current_group.append(row.name)
            current_weight += weight
        else:
            groups.append(current_group)
            current_group = [row.name]
            current_weight = weight
    if current_group:
        groups.append(current_group)
    return groups

def plan_drone_routes(file_path):
    try:
        gift_data = pd.read_csv(file_path, delim_whitespace=True, encoding='utf-8')
        gift_data.set_index('GiftId', inplace=True)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []

    grouped_gifts = group_gifts_by_weight(gift_data)

    routes = []
    for i, group in enumerate(grouped_gifts, start=1):
        optimized_route = nearest_neighbor(group, gift_data)
        distance = calculate_route_distance(optimized_route, gift_data)
        routes.append((i, optimized_route, distance))

    result = []
    for route in routes:
        route_id, gift_ids, distance = route
        result.append([route_id, ",".join(map(str, gift_ids)), distance])

    return result



file_path = "FileNew.txt"
routes = plan_drone_routes(file_path)

output_file = "output_routes.csv"
df_routes = pd.DataFrame(routes, columns=["RouteId", "GiftIds", "Distance"])
df_routes.to_csv(output_file, index=False, encoding='utf-8')
print(f"Маршруты успешно сохранены в файл {output_file}")