from pymongo import MongoClient

import Items
import locations
from Player import Player


cluster = MongoClient("mongodb+srv://mashak:52649aaa@cluster1.tyxnpnn.mongodb.net/Player?retryWrites=true&w=majority")

db = cluster["Player"]
collection = db["Collection_player"]


def new_user(user_id, nickname):
    player = dict(Player)
    player["UserId"] = user_id
    player["Nickname"] = nickname
    collection.insert_one(player)


def check_user(user_id):
    if collection.find_one({"UserId": user_id}) is not None:
        return True
    else:
        return False


def loc(user_id):
    player_data = collection.find_one({"UserId": user_id})
    lst = locations.Available_plays[player_data["LocationID"]]
    return lst


def restore(user_id):
    player_data = collection.find_one({"UserId": user_id})
    collection.delete_one(player_data)
    player_data["CurHP"] = player_data["HP"]
    collection.insert_one(player_data)


def go_to_location(user_id, location):
    player_data = collection.find_one({"UserId": user_id})
    if location in locations.Available_plays[player_data["LocationID"]]:
        collection.delete_one(player_data)
        player_data["LocationID"] = location
        collection.insert_one(player_data)
        if locations.locations_dict[location]["LocationType"] == "city":
            restore(user_id)
        return 1
    else:
        return 0


def cur_loc(user_id):
    player_data = collection.find_one({"UserId": user_id})
    return player_data["LocationID"]


def check_city(user_id):
    player_data = collection.find_one({"UserId": user_id})
    if locations.locations_dict[player_data["LocationID"]]["LocationType"] == "city":
        return True
    else:
        return False


def check_money(user_id, item_name):
    player_data = collection.find_one({"UserId": user_id})
    if player_data["Money"] >= Items.items_dict[item_name]["Cost"]:
        return True
    else:
        return False


def check_name(item):
    if item in Items.items_dict:
        return True
    else:
        return False


def buy_item(user_id, item_name):
    player_data = collection.find_one({"UserId": user_id})
    if check_city(user_id):
        if check_name(item_name):
            if check_money(user_id, item_name):
                collection.delete_one(player_data)
                player_data["Money"] = player_data["Money"] - Items.items_dict[item_name]["Cost"]
                player_data["Inventory"].append(item_name)
                collection.insert_one(player_data)
                return 0
            else:
                return 1
        else:
            return 2
    else:
        return 3


def sell_item(user_id, item_name):
    player_data = collection.find_one({"UserId": user_id})
    if check_city(user_id):
        if check_name(item_name):
            if item_name in player_data["Inventory"]:
                collection.delete_one(player_data)
                player_data["Money"] += Items.items_dict[item_name]["Cost_to_sale"]
                player_data["Inventory"].remove(item_name)
                collection.insert_one(player_data)
                return 0
            else:
                return 1
        else:
            return 2
    else:
        return 3


def equip(user_id, item_name):
    item = Items.items_dict[item_name]
    player_data = collection.find_one({"UserId": user_id})
    if item_name not in player_data["Inventory"]:
        return 1
    collection.delete_one(player_data)
    item_type = item["ItemType"]
    if player_data[item_type] is not None:
        player_data["Inventory"].append(player_data[item_type])
        temp = player_data[item_type]
        player_data["Armour"] -= temp["Armour"]
        player_data["Attack"] -= temp["Attack"]
        player_data["Magic Armour"] -= temp["Magic_Armour"]
        player_data[item_type] = None
    player_data["Armour"] += item["Armour"]
    player_data["Attack"] += item["Attack"]
    player_data["Magic Armour"] += item["Magic_Armour"]
    player_data[item_type] = item_name
    player_data['Inventory'].remove(item_name)
    collection.insert_one(player_data)
    return 0


def unequip(user_id, item_type):
    player_data = collection.find_one({"UserId": user_id})
    if player_data.get(item_type, None) is None:
        return 1
    collection.delete_one(player_data)
    player_data["Inventory"].append(player_data[item_type])
    temp = Items.items_dict[player_data[item_type]]
    player_data["Armour"] -= temp["Armour"]
    player_data["Attack"] -= temp["Attack"]
    player_data["Magic Armour"] -= temp["Magic_Armour"]
    player_data[item_type] = None
    collection.insert_one(player_data)
    return 0

def stats(user_id):
    player_data = collection.find_one({"UserId": user_id})
    lvl = player_data["Level"]
    hp = player_data["CurHP"]
    xp = player_data["XP"]
    money = player_data["Money"]
    loc = player_data["LocationID"]
    attack = player_data["Attack"]
    armour = player_data["Armour"]
    return [lvl, hp, xp, money, loc, attack, armour]

