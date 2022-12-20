Start_town = {
    "LocationName": "Start_town",
    "LocationID": 1,
    "XCoord": 0,
    "YCoord": 0,
    "LocationType": "city"
}

Tolbana = {
    "LocationName": "Tolbana",
    "LocationID": 2,
    "XCoord": 3,
    "YCoord": 3,
    "LocationType": "city"
}

dungeon = {
    "LocationName": "dungeon",
    "LocationID": 3,
    "XCoord": 2,
    "YCoord": 2,
    "LocationType": "dungeon"
}

subterranean = {
    "LocationName": "subterranean",
    "LocationID": 4,
    "XCoord": 7,
    "YCoord": 7,
    "LocationType": "dungeon"
}

Usco_Village = {
    "LocationName": "Usco_Village",
    "LocationID": 5,
    "XCoord": 9,
    "YCoord": 4,
    "LocationType": "city"
}

labyrinth = {
    "LocationName": "labyrinth",
    "LocationID": 6,
    "XCoord": 15,
    "YCoord": 12,
    "LocationType": "dungeon"
}

forest = {
    "LocationName": "forest",
    "LocationID": 7,
    "XCoord": 14,
    "YCoord": 3,
    "LocationType": "dungeon"
}

Available_plays = {
    "Start_town": ["Tolbana", "dungeon", "subterranean", "Usco_Village"],
    "Tolbana": ["Start_town", "dungeon", "subterranean", "Usco_Village"],
    "dungeon": ["Start_town", "Tolbana", "subterranean", "Usco_Village"],
    "subterranean": ["Start_town", "dungeon", "Tolbana", "Usco_Village", "labyrinth", "forest"],
    "Usco_Village": ["Tolbana", "dungeon", "subterranean", "Start_town", "labyrinth", "forest"],
    "labyrinth": ["subterranean", "Usco_Village", "forest"],
    "forest": ["subterranean", "Usco_Village", "labyrinth"]
}

locations_dict = {
    "Start_town": Start_town,
    'dungeon': dungeon,
    "Tolbana": Tolbana,
    "subterranean": subterranean,
    "Usco_Village": Usco_Village,
    "labyrinth": labyrinth,
    "forest": forest
}
