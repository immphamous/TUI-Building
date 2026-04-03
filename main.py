import os, random
import mmlib

global INVENTORY_SIZE
global player_inventory

SCREEN_WIDTH = 24
SCREEN_HEIGHT = 20

MAP_WIDTH = 1024
MAP_HEIGHT = 1024

INVENTORY_SIZE = 3

def add_one_more_slot():
    global INVENTORY_SIZE
    global player_inventory
    INVENTORY_SIZE += 1
    player_inventory.append({ "id": 0, "count": 0 })

TILE_DEFAULT_SETTINGS = {
    "art": " ",
    "background": "",
    "collideable": True,
    "replaceable": False,
    
    "drop_items": [],
    "min_drop": 1,
    "max_drop": 1,
}

TILE_DICT = {
    0: {
        "collideable": False,
        "replaceable": True,
    },
    1: {
        "art": "[]",
        "drop_items": [3]
    },
    2: {
        "art": "↟",
        "drop_items": [2],
        "min_drop": 1,
        "max_drop": 3,
    },
    3: {
        "art": "##",
        "drop_items": [2,2,1],
    },
    4: {
        "art": "˯ ",
        "collideable": False,
        "replaceable": True,
    },
    5: {
        "background": "\x1b[107m",
        "art": " ",
        "collideable": False,
        "replaceable": True,
    },
    6: {
        "art": "⮽ ",
        "drop_items": [1,2,3,5,6],
        "min_drop":2,
        "max_drop":4,
    }
}
for tile in TILE_DICT.values():
    mmlib.set_default(tile, TILE_DEFAULT_SETTINGS)

ITEM_DEFAULT_SETTINGS = {
    "name": "Air",
    "art": " ",
    "use_properties": {
        "placeable": False,
        "place_tile": -1,

        "breaking_tool": False,
        "breaking_tiles": [],

        "remove_after_use": True,

        "custom_action": None
    }
}

ITEM_DICT = {
    0: {
        "use_properties": {
            "breaking_tool": True,
            "breaking_tiles": [6],
        }
    },
    1: {
        "name": "Stick",
        "art": "/",
        "use_properties": {
            "breaking_tool": True,
            "breaking_tiles": [1],
            "remove_after_use": False,
        }
    },
    2: {
        "name": "Wood",
        "art": "#",
        "use_properties": {
            "placeable": True,
            "place_tile": 3
        }
    },
    3: {
        "name": "Rock",
        "art": "☐",
        "use_properties": {
            "placeable": True,
            "place_tile": 1
        }
    },
    4: {
        "name": "Axe",
        "art": "𐃈",
        "use_properties": {
            "breaking_tool": True,
            "breaking_tiles": [2,3],
            "remove_after_use": False,
        }
    },
    5: {
        "name": "Slot Expander",
        "art": "♥",
        "use_properties": {
            "custom_action": add_one_more_slot
        }
    },
    6: {
        "name": "Shovel",
        "art": "↥",
        "use_properties": {
            "placeable": True,
            "place_tile": 5,
            "remove_after_use": False,
        }
    },
}
for item in ITEM_DICT.values():
    mmlib.set_default(item, ITEM_DEFAULT_SETTINGS)

world_map = [[0 for col in range(MAP_HEIGHT)] for row in range(MAP_WIDTH)]

for i in range(40*128):
    tile = random.randint(1,2)
    if random.randint(1, 30) == 1:
        tile = 4
    if random.randint(1, 6) == 1:
        tile = 6
    world_map[random.randint(0, MAP_WIDTH - 1)][random.randint(0, MAP_HEIGHT - 1)] = tile

player_x = MAP_WIDTH / 2
player_y = MAP_HEIGHT / 2
player_inventory = [{ "id": 0, "count": 0 } for _ in range(INVENTORY_SIZE)]
current_slot_index = 0
player_inventory[0] = { "id": 4, "count": 1 }
# player_inventory[1] = { "id": 6, "count": 1 }

def clear_item(index):
    player_inventory[index] = { "id": 0, "count": 0 }

def remove_item(index, amount):
    player_inventory[index]["count"] -= amount
    if player_inventory[index]["count"] <= 0:
        clear_item(index)

def add_item(item_index, amount):
    for i in range(INVENTORY_SIZE):
        if player_inventory[i]["id"] == item_index:
            player_inventory[i]["count"] += amount
            return
    for i in range(INVENTORY_SIZE):
        if player_inventory[i]["id"] == 0:
            player_inventory[i]["id"] = item_index
            player_inventory[i]["count"] += amount
            return

def out_of_bounds(x, y):
    return (x < 0 or x >= MAP_WIDTH) or (y < 0 or y >= MAP_HEIGHT)

def print_tile(x, y):
    x, y = int(x), int(y)

    if out_of_bounds(x, y):
        print("↟↟", end="")
        return

    tile_id = world_map[x][y]
    tile = TILE_DICT[tile_id]
    art = tile["art"]
    if x == player_x and y == player_y:
        slot_data = player_inventory[current_slot_index]
        art = "☺" + ITEM_DICT[slot_data["id"]]["art"]
    print(tile["background"], end="")

    if len(art) == 1: # print twice if the char is shorter
        print(art, end="")
    print(art, end="")
    print("\x1b[0m", end="")

def render():
    print("+" + "--" * SCREEN_WIDTH + "+")
    for screen_y in range(-int(SCREEN_HEIGHT / 2), int(SCREEN_HEIGHT / 2)):
        print("|", end="");
        for screen_x in range(-int(SCREEN_WIDTH / 2), int(SCREEN_WIDTH / 2)):
            print_tile(screen_x + player_x, screen_y + player_y)
        print("|")
    print("+" + "--" * SCREEN_WIDTH + "+")

def print_inventory():
    for i in range(INVENTORY_SIZE):
        slot_data = player_inventory[i]
        count = slot_data["count"]
        print(f" {count}  ", end="")
    if player_inventory[current_slot_index]["id"] != 0:
        item_id = player_inventory[current_slot_index]["id"]
        item = ITEM_DICT[item_id]
        print(f" {item['name']}", end="")
    print("")
    for i in range(INVENTORY_SIZE):
        slot_data = player_inventory[i]
        item = ITEM_DICT[slot_data["id"]]
        art = item["art"]
        print("[" + art + "] ", end="")    
    print("")
    print("    " * current_slot_index + " ^")
    print("")

def draw():
    os.system("clear")
    render()
    print_inventory()

while True:
    draw()
    cmd = mmlib.read_key()
    # print(cmd)
    change_x = 0
    change_y = 0
    if cmd == "D": change_x -= 1
    elif cmd == "C": change_x += 1
    elif cmd == "A": change_y -= 1
    elif cmd == "B": change_y += 1
    elif cmd == "q":
        current_slot_index = max(min(current_slot_index - 1, INVENTORY_SIZE - 1), 0)
    elif cmd == "e":
        current_slot_index = max(min(current_slot_index + 1, INVENTORY_SIZE - 1), 0)
    elif cmd == "r":
        clear_item(current_slot_index)
    elif cmd == "w":
        slot_data = player_inventory[current_slot_index]
        item = ITEM_DICT[slot_data["id"]]
        if item["use_properties"]:
            if item["use_properties"]["placeable"]:
                mmlib.read_key() # garbage
                mmlib.read_key() # garbage
                direction = mmlib.read_key()
                tile_change_x = 0
                tile_change_y = 0
                if direction == "D": tile_change_x -= 1
                elif direction == "C": tile_change_x += 1
                elif direction == "A": tile_change_y -= 1
                elif direction == "B": tile_change_y += 1


                
                if out_of_bounds(player_x + tile_change_x, player_y + tile_change_y):
                    continue 
                tile_index = world_map[int(player_x + tile_change_x)][int(player_y + tile_change_y)]
                tile = TILE_DICT[tile_index]
                print(tile["replaceable"], tile["art"])
                if not tile["replaceable"]:
                    continue
                world_map[int(player_x + tile_change_x)][int(player_y + tile_change_y)] = item["use_properties"]["place_tile"]
                
                if item["use_properties"]["remove_after_use"]:
                    remove_item(current_slot_index, 1)
            if item["use_properties"]["breaking_tool"]:
                mmlib.read_key() # garbage
                mmlib.read_key() # garbage
                direction = mmlib.read_key()
                tile_change_x = 0
                tile_change_y = 0
                if direction == "D": tile_change_x -= 1
                elif direction == "C": tile_change_x += 1
                elif direction == "A": tile_change_y -= 1
                elif direction == "B": tile_change_y += 1
                if out_of_bounds(player_x + tile_change_x, player_y + tile_change_y):
                    continue 
                tile_index = world_map[int(player_x + tile_change_x)][int(player_y + tile_change_y)]
                if item["use_properties"]["remove_after_use"]:
                    remove_item(current_slot_index, 1)
                if tile_index in item["use_properties"]["breaking_tiles"]:
                    tile = TILE_DICT[tile_index]
                    world_map[int(player_x + tile_change_x)][int(player_y + tile_change_y)] = 0
                    for _ in range(random.randint(tile["min_drop"], tile["max_drop"])):
                        loot = tile["drop_items"][random.randint(0, len(tile["drop_items"]) - 1)]
                        add_item(loot, 1)
            if item["use_properties"]["custom_action"]:
                if item["use_properties"]["remove_after_use"]:
                    remove_item(current_slot_index, 1)
                item["use_properties"]["custom_action"]()
                draw()
                
    
    if out_of_bounds(player_x + change_x, player_y + change_y): # no movement allowed out of bounds
        continue

    tile_index = world_map[int(player_x + change_x)][int(player_y + change_y)]
    tile = TILE_DICT[tile_index]
    if not tile["collideable"]:
        player_x += change_x
        player_y += change_y
