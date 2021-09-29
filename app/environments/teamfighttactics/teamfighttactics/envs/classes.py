import random

SET_DATA = {
    "ROLL_ODDS": {
        1: [100, 0, 0, 0, 0],
        2: [100, 0, 0, 0, 0],
        3: [75, 25, 0, 0, 0],
        4: [55, 30, 15, 0, 0],
        5: [45, 33, 20, 2, 0],
        6: [25, 40, 30, 5, 0],
        7: [19, 30, 35, 15, 1] ,
        8: [15, 20, 35, 25, 5],
        9: [10, 15, 30, 30, 15]
    }
}

ACTIONS_MAP = {
    "BUY_SHOP_POS_1": 0,
    "BUY_SHOP_POS_2": 1,
    "BUY_SHOP_POS_3": 2,
    "BUY_SHOP_POS_4": 3,
    "BUY_SHOP_POS_5": 4,
    "SELL_BENCH_POS_1": 5,
    "SELL_BENCH_POS_2": 6,
    "SELL_BENCH_POS_3": 7,
    "SELL_BENCH_POS_4": 8,
    "SELL_BENCH_POS_5": 9,
    "SELL_BENCH_POS_6": 10,
    "SELL_BENCH_POS_7": 11,
    "SELL_BENCH_POS_8": 12,
    "SELL_BENCH_POS_9": 13,
    "SELL_CHAMPION_POS_1": 14,
    "SELL_CHAMPION_POS_2": 15,
    "SELL_CHAMPION_POS_3": 16,
    "SELL_CHAMPION_POS_4": 17,
    "SELL_CHAMPION_POS_5": 18,
    "SELL_CHAMPION_POS_6": 19,
    "SELL_CHAMPION_POS_7": 20,
    "SELL_CHAMPION_POS_8": 21,
    "SELL_CHAMPION_POS_9": 22,
    "BENCH_1_TO_BOARD": 23,
    "BENCH_2_TO_BOARD": 24,
    "BENCH_3_TO_BOARD": 25,
    "BENCH_4_TO_BOARD": 26,
    "BENCH_5_TO_BOARD": 27,
    "BENCH_6_TO_BOARD": 28,
    "BENCH_7_TO_BOARD": 29,
    "BENCH_8_TO_BOARD": 30,
    "BENCH_9_TO_BOARD": 31,
    "BOARD_1_TO_BENCH": 32,
    "BOARD_2_TO_BENCH": 33,
    "BOARD_3_TO_BENCH": 34,
    "BOARD_4_TO_BENCH": 35,
    "BOARD_5_TO_BENCH": 36,
    "BOARD_6_TO_BENCH": 37,
    "BOARD_7_TO_BENCH": 38,
    "BOARD_8_TO_BENCH": 39,
    "BOARD_9_TO_BENCH": 40,

    "REROLL": 41,
    "BUY_EXP": 42,
    "READY_NEXT_STAGE": 43,
}

class Traits():
    DAWNBRINGER = "DAWNBRINGER"
    ASSASSIN = "ASSASSIN"
    KNIGHT = "KNIGHT"
    HELLION = "HELLION"
    CAVALIER = "CAVALIER"
    SPELLWEAVER = "SPELLWEAVER"
    DRACONIC = "DRACONIC"
    SKIRMISHER = "SKIRMISHER"
    RENEWER = "RENEWER"
    LEGIONNAIRE = "LEGIONNAIRE"
    NIGHBRINGER = "NIGHBRINGER"
    BRAWLER = "BRAWLER"
    REVENANT = "REVENANT"
    ABOMINATION = "ABOMINATION"
    SENTINEL = "SENTINEL"
    NIGHTBRINGER = "NIGHTBRINGER"
    CANNONEER = "CANNONEER"
    REDEEMED = "REDEEMED"



class GameManager():
    def __init__(self, players):
        self.players = players
        self.stage = 1
        self.champion_pool = self.create_champion_pool()

    def create_champion_pool(self):
        champion_pool = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
        }

        # TIER 1: 29 of each champ
        for c in [GRAGAS, KHAZIX, KLED, ZIGGS, POPPY, UDYR, OLAF, SENNA, LEONA, VLADIMIR, AATROX, KALISTA]:
            for i in range(29):
                champion_pool[1].append(Champion(c['id'], c['name'], 1, c['cost'], c['traits']))

        return champion_pool

    def distribute_stage_income(self):
        for player in self.players:
            # TODO: income calculations
            player.gold += 10

    def check_game_over(self):
        alive_players = 0
        for player in self.players:
            if not player.is_eliminated:
                alive_players += 1

        if alive_players <= 1:
            return True
        else:
            return False

    def roll_players_shop(self, player):
        shop = []

        players_odds = SET_DATA["ROLL_ODDS"][player.level]

        # First roll rarity, then roll a champion in that rarity
        for i in range(5):
           champ_level = random.choices([1, 2, 3, 4, 5], players_odds)
           champ = random.choice(self.champion_pool[champ_level[0]])
           shop.append(champ)

        player.shop = shop

    def roll_all_players_shops(self):
        for player in self.players:
            self.roll_players_shop(player)

    def simulate_combat_step(self):
        # TODO: actual matchmaking and detect winners
        for player in self.players:
            win = random.randint(0,1) == 1
            if not win:
                player.health -= 10
                
            player.ready = False

    def purchase_hero_at_shop_index(self, player, index):
        # TODO
        return

    # action - int - action integer
    def execute_agent_action(self, player, action):
        print("EXECUTING AGENT ACTION", player.id, action)
        if action == ACTIONS_MAP["BUY_SHOP_POS_1"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["BUY_SHOP_POS_2"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["BUY_SHOP_POS_3"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["BUY_SHOP_POS_4"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["BUY_SHOP_POS_5"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["SELL_BENCH_POS_1"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["SELL_BENCH_POS_2"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["SELL_BENCH_POS_3"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["SELL_BENCH_POS_4"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["SELL_BENCH_POS_5"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["SELL_BENCH_POS_6"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["SELL_BENCH_POS_7"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["SELL_BENCH_POS_8"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["SELL_BENCH_POS_9"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["SELL_CHAMPION_POS_1"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["SELL_CHAMPION_POS_2"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["SELL_CHAMPION_POS_3"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["SELL_CHAMPION_POS_4"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["SELL_CHAMPION_POS_5"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["SELL_CHAMPION_POS_6"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["SELL_CHAMPION_POS_7"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["SELL_CHAMPION_POS_8"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["SELL_CHAMPION_POS_9"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["BOARD_1_TO_BENCH"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["BOARD_2_TO_BENCH"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["BOARD_3_TO_BENCH"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["BOARD_4_TO_BENCH"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["BOARD_5_TO_BENCH"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["BOARD_6_TO_BENCH"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["BOARD_7_TO_BENCH"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["BOARD_8_TO_BENCH"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["BOARD_9_TO_BENCH"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["REROLL"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["BUY_EXP"]:
            print("need to implement", action)
        elif action == ACTIONS_MAP["READY_NEXT_STAGE"]:
            print("SETTING PLAYER TO READY")
            player.ready = True


        else:
            print("Unrecognized action:", action)

class Player():
    def __init__(self, id):
        self.id = id
        self.gold = 0
        self.level = 1
        self.experience = 0
        self.shop = [None]*5
        self.board = [None]*9
        self.bench = [None]*9
        self.health = 100
        self.ready = False

    @property
    def is_eliminated(self):
        return self.health <= 0
    

class Champion():
    def __init__(self, id, name, level, cost, traits):
        self.id = id
        self.level = level
        self.name = name
        self.cost = cost
        self.traits = traits

GRAGAS = {
    "id": 1,
    "name": "Gragas",
    "traits": [Traits.DAWNBRINGER, Traits.BRAWLER],
    "cost": 1
}

KHAZIX = {
    "id": 2,
    "name": "Khazix",
    "traits": [Traits.DAWNBRINGER, Traits.ASSASSIN],
    "cost": 1
}

KLED = {
    "id": 3,
    "name": "Kled",
    "traits": [Traits.HELLION, Traits.CAVALIER],
    "cost": 1
}

ZIGGS = {
    "id": 4,
    "name": "Ziggs",
    "traits": [Traits.HELLION, Traits.SPELLWEAVER],
    "cost": 1
}

POPPY = {
    "id": 5,
    "name": "Poppy",
    "traits": [Traits.HELLION, Traits.KNIGHT],
    "cost": 1
}

UDYR = {
    "id": 6,
    "name": "Udyr",
    "traits": [Traits.DRACONIC, Traits.SKIRMISHER],
    "cost": 1
}

OLAF = {
    "id": 7,
    "name": "Olaf",
    "traits": [Traits.SENTINEL, Traits.SKIRMISHER],
    "cost": 1
}

SENNA = {
    "id": 8,
    "name": "Senna",
    "traits": [Traits.SENTINEL, Traits.CANNONEER],
    "cost": 1
}

LEONA = {
    "id": 9,
    "name": "Leona",
    "traits": [Traits.KNIGHT, Traits.REDEEMED],
    "cost": 1
}

VLADIMIR = {
    "id": 10,
    "name": "Vladimir",
    "traits": [Traits.NIGHTBRINGER, Traits.RENEWER],
    "cost": 1
}

AATROX = {
    "id": 11,
    "name": "Aatrox",
    "traits": [Traits.LEGIONNAIRE, Traits.REDEEMED],
    "cost": 1
}

KALISTA = {
    "id": 12,
    "name": "Kalista",
    "traits": [Traits.LEGIONNAIRE, Traits.ABOMINATION],
    "cost": 1
}