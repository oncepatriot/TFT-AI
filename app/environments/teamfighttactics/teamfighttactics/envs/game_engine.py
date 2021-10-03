import random
from . import game_utils
import numpy as np
import os
import sys
import math
sys.path.insert(1, os.path.join(sys.path[0], '...'))
from tft_fight_predictor.teamfight_predictor import TftFightPredictor


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

class GameManager():
    def __init__(self, players):
        self.players = players
        self.stage = 1
        self.round = 1
        self.champion_pool = self.create_champion_pool()
        self.fight_predictor = TftFightPredictor()
        self.placements = []

    def create_champion_pool(self):
        champion_pool = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
        }

        # TIER 1: 29 of each champ
        for champ in game_utils.get_cost_x_champions(1):
            for i in range(29):
                champion_pool[1].append(Champion(champ['championId'], champ['name'], 1, champ['cost'], champ['traits']))

        for champ in game_utils.get_cost_x_champions(2):
            for i in range(22):
                champion_pool[2].append(Champion(champ['championId'], champ['name'], 1, champ['cost'], champ['traits']))
        
        for champ in game_utils.get_cost_x_champions(3):
            for i in range(18):
                champion_pool[3].append(Champion(champ['championId'], champ['name'], 1, champ['cost'], champ['traits']))
                
        for champ in game_utils.get_cost_x_champions(4):
            for i in range(12):
                champion_pool[4].append(Champion(champ['championId'], champ['name'], 1, champ['cost'], champ['traits']))
        
        for champ in game_utils.get_cost_x_champions(5):
            for i in range(10):
                champion_pool[5].append(Champion(champ['championId'], champ['name'], 1, champ['cost'], champ['traits']))

        return champion_pool

    def increment_stage_round(self):
        if self.stage == 1:
            if self.round == 3:
                self.stage += 1
                self.round = 1
            else:
                self.round += 1

        else:
            if self.round == 6:
                self.stage += 1
                self.round = 1
            else:
                self.round += 1

        # Each player receives 2 exp at end of round
        for player in self.players:
            player.add_exp(2)

    def distribute_income(self):
        if self.stage == 1:
            for player in self.players: 
                player.gold += 3
        else:
            for player in self.players:
                player.gold += player.income

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

        # TODO: player can't roll units they have 3 star of

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
        if self.is_creep_round:
            for player in self.players:
                player.ready = True
            return
        
        alive_players= [player.id for player in self.players if not player.is_eliminated]
        random.shuffle(alive_players)
        mm_pairs = [alive_players[i:i + 2] for i in range(0, len(alive_players), 2)] # create pairs

        # TODO: If odd number of players, will need to create a ghost...
        for pair in mm_pairs:
            player_one = self.players[pair[0]]
            player_two = self.players[pair[1]]
            print(player_one.id, player_two.id)

            p1_win_probability, p2_win_probability = self.fight_predictor.predict_tft_fight(
                player_one,
                player_two
            )

            if p1_win_probability > .5:
                winner_probability = p1_win_probability
                winner = player_one
                loser = player_two
            else:
                winner_probability = p2_win_probability
                winner = player_one
                loser = player_two

            winner.update_streak(True)
            winner.gold += 1
            loser.update_streak(False)
            loser.health -= self.stage_damage

            # Approximate number of units lost by. Examples:
            # .8 * 4 units on board = 3.2 = 3 unit loss
            # .5 * 4 units on board = 2 unit loss
            # .8 * 8 units on board = 6.4 = 6 unit loss
            # .5 * 8 units on board = 4 = 4 unit loss
            units_lost_by = math.floor(winner_probability * winner.num_units_on_board) - random.randint(0,1)
            loser.health -= min(1, self.get_damage_for_x_unit_loss(units_lost_by))

            if loser.is_eliminated:
                self.placements.insert(0,loser)

            player_one.ready = False
            player_two.ready = False

    def purchase_champion_at_shop_index(self, player, shop_index):
        # TODO: Player can buy champ if bench is full but buying will
        # upgrade the champion
        if player.bench_is_full:
            raise Exception("Tried to buy champ with full bench")

        players_shop = player.shop
        champion = players_shop[shop_index]

        if player.gold >= champion.cost:
            # Puchase the hero: 
            # deduct gold, add to players bench, and remove from champion pool
            player.gold = player.gold - champion.cost
            player.shop[shop_index] = None
            player.add_champion_to_bench(champion)
            self.remove_champion_from_pool(champion)
            self.maybe_upgrade_champions_for_player(player, champion)
        else:
            raise Exception("tried to buy champ couldnt afford")

        return

    def remove_champion_from_pool(self, champion):
        for i, champ in enumerate(self.champion_pool[champion.cost]):
            if champ.id == champion.id:
                del self.champion_pool[champion.cost][i]
                return

        raise Exception("Did not found champ in pool to remove!")

    def maybe_upgrade_champions_for_player(self, player, champion):
        bench = player.bench
        board = player.board

        num_champs = 0
        bench_locations = []
        board_locations = []
        for index, c in enumerate(bench):
            if c and champion.is_same_level_and_champ(c):
                num_champs += 1
                bench_locations.append(index)

        for index, c in enumerate(board):
            if c and champion.is_same_level_and_champ(c):
                num_champs += 1
                board_locations.append(index)

        if num_champs == 3:
            print("Upgrading champion for player:", player, champion.id)
            for b in bench_locations:
                player.bench[b] = None
            for b in board_locations:
                player.board[b] = None

            upgraded_champ = Champion(champion.id, champion.name, champion.level + 1, champion.cost, champion.traits)
            player.add_champion_to_bench(upgraded_champ)
            self.maybe_upgrade_champions_for_player(player, champion) # Check again for double upgrade

        else:
            return

    def sell_champion_at_bench_index(self, player, bench_index):
        champion = player.bench[bench_index]
        if champion:
            player.bench[bench_index] = None
            player.gold += champion.sell_value
            self.champion_pool[champion.cost] += champion.champions_to_return_to_pool_when_sold # add units back to pool
        else:
            raise Exception("tried to sell hero at bench index where none existed", player.id)

    def sell_champion_at_board_index(self, player, board_index):
        champion = player.board[board_index]
        if champion:
            player.board[board_index] = None
            player.gold += champion.sell_value
            self.champion_pool[champion.cost] += champion.champions_to_return_to_pool_when_sold # add units back to pool
        else:
            raise Exception("tried to sell hero at board index where none existed", player.id)

    def place_champion_from_bench_to_board(self, player, bench_index):
        # TODO: swapping requires an empty board/bench slot
        champion = player.bench[bench_index]
        player.bench[bench_index] = None
        player.add_champion_to_board(champion)

    def place_champion_from_board_to_bench(self, player, board_index):
        # TODO: swapping requires an empty bench/bench slot
        champion = player.board[board_index]
        player.board[board_index] = None
        player.add_champion_to_bench(champion)

    # action - int - action integer
    def execute_agent_action(self, player, action):
        if action == ACTIONS_MAP["BUY_SHOP_POS_1"]:
            self.purchase_champion_at_shop_index(player,0)

        elif action == ACTIONS_MAP["BUY_SHOP_POS_2"]:
            self.purchase_champion_at_shop_index(player,1)

        elif action == ACTIONS_MAP["BUY_SHOP_POS_3"]:
            self.purchase_champion_at_shop_index(player,2)

        elif action == ACTIONS_MAP["BUY_SHOP_POS_4"]:
            self.purchase_champion_at_shop_index(player,3)

        elif action == ACTIONS_MAP["BUY_SHOP_POS_5"]:
            self.purchase_champion_at_shop_index(player,4)        

        elif action == ACTIONS_MAP["SELL_BENCH_POS_1"]:
            self.sell_champion_at_bench_index(player, 0)

        elif action == ACTIONS_MAP["SELL_BENCH_POS_2"]:
            self.sell_champion_at_bench_index(player, 1)

        elif action == ACTIONS_MAP["SELL_BENCH_POS_3"]:
            self.sell_champion_at_bench_index(player, 2)

        elif action == ACTIONS_MAP["SELL_BENCH_POS_4"]:
            self.sell_champion_at_bench_index(player, 3)

        elif action == ACTIONS_MAP["SELL_BENCH_POS_5"]:
            self.sell_champion_at_bench_index(player, 4)

        elif action == ACTIONS_MAP["SELL_BENCH_POS_6"]:
            self.sell_champion_at_bench_index(player, 5)  

        elif action == ACTIONS_MAP["SELL_BENCH_POS_7"]:
            self.sell_champion_at_bench_index(player, 6)

        elif action == ACTIONS_MAP["SELL_BENCH_POS_8"]:
            self.sell_champion_at_bench_index(player, 7)

        elif action == ACTIONS_MAP["SELL_BENCH_POS_9"]:
            self.sell_champion_at_bench_index(player, 8)

        elif action == ACTIONS_MAP["SELL_CHAMPION_POS_1"]:
            self.sell_champion_at_board_index(player, 0)

        elif action == ACTIONS_MAP["SELL_CHAMPION_POS_2"]:
            self.sell_champion_at_board_index(player, 1)

        elif action == ACTIONS_MAP["SELL_CHAMPION_POS_3"]:
            self.sell_champion_at_board_index(player, 2)

        elif action == ACTIONS_MAP["SELL_CHAMPION_POS_4"]:
            self.sell_champion_at_board_index(player, 3)

        elif action == ACTIONS_MAP["SELL_CHAMPION_POS_5"]:
            self.sell_champion_at_board_index(player, 4)

        elif action == ACTIONS_MAP["SELL_CHAMPION_POS_6"]:
            self.sell_champion_at_board_index(player, 5)

        elif action == ACTIONS_MAP["SELL_CHAMPION_POS_7"]:
            self.sell_champion_at_board_index(player, 6)

        elif action == ACTIONS_MAP["SELL_CHAMPION_POS_8"]:
            self.sell_champion_at_board_index(player, 7)

        elif action == ACTIONS_MAP["SELL_CHAMPION_POS_9"]:
            self.sell_champion_at_board_index(player, 8)

        elif action == ACTIONS_MAP["BENCH_1_TO_BOARD"]:
            self.place_champion_from_bench_to_board(player, 0)

        elif action == ACTIONS_MAP["BENCH_2_TO_BOARD"]:
            self.place_champion_from_bench_to_board(player, 1)

        elif action == ACTIONS_MAP["BENCH_3_TO_BOARD"]:
            self.place_champion_from_bench_to_board(player, 2)

        elif action == ACTIONS_MAP["BENCH_4_TO_BOARD"]:
            self.place_champion_from_bench_to_board(player, 3)

        elif action == ACTIONS_MAP["BENCH_5_TO_BOARD"]:
            self.place_champion_from_bench_to_board(player, 4)

        elif action == ACTIONS_MAP["BENCH_6_TO_BOARD"]:
            self.place_champion_from_bench_to_board(player, 5)

        elif action == ACTIONS_MAP["BENCH_7_TO_BOARD"]:
            self.place_champion_from_bench_to_board(player, 6)

        elif action == ACTIONS_MAP["BENCH_8_TO_BOARD"]:
            self.place_champion_from_bench_to_board(player, 7)

        elif action == ACTIONS_MAP["BENCH_9_TO_BOARD"]:
            self.place_champion_from_bench_to_board(player, 8)

        elif action == ACTIONS_MAP["BOARD_1_TO_BENCH"]:
            self.place_champion_from_board_to_bench(player, 0)

        elif action == ACTIONS_MAP["BOARD_2_TO_BENCH"]:
            self.place_champion_from_board_to_bench(player, 1)

        elif action == ACTIONS_MAP["BOARD_3_TO_BENCH"]:
            self.place_champion_from_board_to_bench(player, 2)

        elif action == ACTIONS_MAP["BOARD_4_TO_BENCH"]:
            self.place_champion_from_board_to_bench(player, 3)

        elif action == ACTIONS_MAP["BOARD_5_TO_BENCH"]:
            self.place_champion_from_board_to_bench(player, 4)

        elif action == ACTIONS_MAP["BOARD_6_TO_BENCH"]:
            self.place_champion_from_board_to_bench(player,5)

        elif action == ACTIONS_MAP["BOARD_7_TO_BENCH"]:
            self.place_champion_from_board_to_bench(player,6)   

        elif action == ACTIONS_MAP["BOARD_8_TO_BENCH"]:
            self.place_champion_from_board_to_bench(player,7)

        elif action == ACTIONS_MAP["BOARD_9_TO_BENCH"]:
            self.place_champion_from_board_to_bench(player,8)

        elif action == ACTIONS_MAP["REROLL"]:
            self.roll_players_shop(player)

        elif action == ACTIONS_MAP["BUY_EXP"]:
            player.buy_exp()

        elif action == ACTIONS_MAP["READY_NEXT_STAGE"]:
            player.ready = True

        else:
            print("Unrecognized action:", action)

    @property
    def is_all_players_ready(self):
        return all([True if player.ready else False for player in self.players])

    @property
    def is_creep_round(self):
        if self.stage == 1 and self.round in [1,2,3]:
            return True
        
        elif self.round == 6:
            return True
        
        return False

    @property
    def stage_damage(self):
        stage_to_damage = [0,0,2,3,5,8,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15]
        return stage_to_damage[self.stage-1]
    
    def get_damage_for_x_unit_loss(self, num_units):
        x_unit_lost_damage = [0, 2, 4, 6, 8, 10, 11, 12, 13, 14, 15]
        return x_unit_lost_damage[num_units]

    def print_board_state(self):
        print("====================")
        print("Game State")
        print("====================")
        print(f"Stage: {self.stage}-{self.round}")
        print("====================")
        for player in self.players:
            player.print_player()
            print("--------------------")

class Player():
    def __init__(self, id):
        self.id = id
        self.gold = 0
        self.level = 1
        self.exp = 0
        self.shop = [None]*5
        self.board = [None]*9
        self.bench = [None]*9
        self.health = 100
        self.ready = False
        self.items = [0]*9
        self.streak = 0 # negative is lose streak, positive is win streak

    def buy_exp(self):
        if self.gold < 4:
            raise Exception("Tried to buy exp without enough gold")
        elif self.level == 9:
            raise Exception("Tried to buy exp at level 9")
        else:
            self.gold -= 4
            self.add_exp(4)

    def add_exp(self, exp):
        self.exp = self.exp + exp
        if self.level == 1:
            self.level = 2
            self.exp = 0

        elif self.level == 2 and self.exp >= 2:
            self.level = 3
            self.exp = self.exp - 2

        elif self.level == 3 and self.exp >= 6:
            self.level = 4
            self.exp = self.exp - 6

        elif self.level == 4 and self.exp >= 10:
            self.level = 5
            self.exp = self.exp - 10

        elif self.level == 5 and self.exp >= 20:
            self.level = 6
            self.exp = self.exp - 20

        elif self.level == 6 and self.exp >= 36:
            self.level = 7
            self.exp = self.exp - 36

        elif self.level == 7 and self.exp >= 56:
            self.level = 8
            self.exp = self.exp - 56

        elif self.level == 8 and self.exp >= 80:
            self.level = 9
            self.exp = self.exp - 80

    def update_streak(self, is_win):
        if is_win:
            if self.streak <= 0:
                self.streak = 1
            else:
                self.streak += 1
        else:
            if self.streak >= 0:
                self.streak = -1
            else:
                self.streak -= 1

    def add_champion_to_bench(self, champion):
        for i, bench_occupant in enumerate(self.bench):
            if bench_occupant == None:
                self.bench[i] = champion
                return

    def add_champion_to_board(self, champion):
        for i, board_occupant in enumerate(self.board):
            if board_occupant == None:
                self.board[i] = champion
                return

    @property
    def bench_is_full(self):
        return (None not in self.bench)
    
    @property
    def board_is_full(self):
        champions_on_board = 0
        for c in self.board:
            if c == None:
                champions_on_board += 1

        if champions_on_board == self.level:
            return True
    
    @property
    def income(self):
        income = 5
        if abs(self.streak) == 5:
            income += 3
        elif abs(self.streak) == 4:
            income += 2
        elif abs(self.streak) > 1:
            income += 1

        # interest with max at 5
        income += min((self.gold // 10), 5)
        return income
    
    @property
    def is_eliminated(self):
        return self.health <= 0
    
    @property
    def num_units_on_board(self):
        return len([i for i in self.board if i])
    
    def print_player(self):
        print(f"Player: {self.id} | Level: {self.level} | Exp: {self.exp} | Health: {self.health} | Gold: {self.gold} | Streak: {self.streak}")
        print("Board:", [str(c) for c in self.board])
        print("Bench:", [str(c) for c in self.bench])
        print("Shop:", [str(c) for c in self.shop] )
        print(f"Ready: {self.ready}")


class Champion():
    def __init__(self, id, name, level, cost, traits):
        self.id = id
        self.level = level
        self.name = name
        self.cost = cost
        self.traits = traits
        self.items = [0] * 3 # array of item_ids (1532)

    def __str__(self):
        return f"Level {self.level} {self.id}"

    def is_same_level_and_champ(self, champ):
        return self.level == champ.level and self.id == champ.id

    @property
    def sell_value(self):
        if self.level > 1:
            return self.cost - 1
        else:
            return self.cost
    
    @property
    def champions_to_return_to_pool_when_sold(self):
        champions = []
        if self.level == 1:
            champions.append(Champion(self.id, self.name, 1, self.cost, self.traits))
        elif self.level == 2:
            for i in range(3):
                champions.append(Champion(self.id, self.name, 1, self.cost, self.traits))
        elif self.level == 3:
            for i in range(9):
                champions.append(Champion(self.id, self.name, 1, self.cost, self.traits))

        return champions



def is_action_legal(player, action):
    if player.is_eliminated:
        return False

    # Player puchasing champ must have a bench slot and enough gold. TODO:
    # technically they can buy if bench is full and buying champ levels champ up
    if action == ACTIONS_MAP["BUY_SHOP_POS_1"]:
        return (not player.bench_is_full and player.shop[0] != None and player.shop[0].cost <= player.gold)
    elif action == ACTIONS_MAP["BUY_SHOP_POS_2"]:
        return (not player.bench_is_full and player.shop[1] != None and player.shop[1].cost <= player.gold)
    elif action == ACTIONS_MAP["BUY_SHOP_POS_3"]:
        return (not player.bench_is_full and player.shop[2] != None and player.shop[2].cost <= player.gold)
    elif action == ACTIONS_MAP["BUY_SHOP_POS_4"]:
        return (not player.bench_is_full and player.shop[3] != None and player.shop[3].cost <= player.gold)
    elif action == ACTIONS_MAP["BUY_SHOP_POS_5"]:
        return (not player.bench_is_full and player.shop[4] != None and player.shop[4].cost <= player.gold)

    # Player can sell bench at position if it is not empty
    elif action == ACTIONS_MAP["SELL_BENCH_POS_1"]:
        return (player.bench[0] != None)
    elif action == ACTIONS_MAP["SELL_BENCH_POS_2"]:
        return (player.bench[1] != None)
    elif action == ACTIONS_MAP["SELL_BENCH_POS_3"]:
        return (player.bench[2] != None)
    elif action == ACTIONS_MAP["SELL_BENCH_POS_4"]:
        return (player.bench[3] != None)
    elif action == ACTIONS_MAP["SELL_BENCH_POS_5"]:
        return (player.bench[4] != None)
    elif action == ACTIONS_MAP["SELL_BENCH_POS_6"]:
        return (player.bench[5] != None)
    elif action == ACTIONS_MAP["SELL_BENCH_POS_7"]:
        return (player.bench[6] != None)
    elif action == ACTIONS_MAP["SELL_BENCH_POS_8"]:
        return (player.bench[7] != None)
    elif action == ACTIONS_MAP["SELL_BENCH_POS_9"]:
        return (player.bench[8] != None)

    # Player can sell champion at board position x if not empty
    elif action == ACTIONS_MAP["SELL_CHAMPION_POS_1"]:
        return (player.board[0] != None)
    elif action == ACTIONS_MAP["SELL_CHAMPION_POS_2"]:
        return (player.board[1] != None)
    elif action == ACTIONS_MAP["SELL_CHAMPION_POS_3"]:
        return (player.board[2] != None)
    elif action == ACTIONS_MAP["SELL_CHAMPION_POS_4"]:
        return (player.board[3] != None)
    elif action == ACTIONS_MAP["SELL_CHAMPION_POS_5"]:
        return (player.board[4] != None)
    elif action == ACTIONS_MAP["SELL_CHAMPION_POS_6"]:
        return (player.board[5] != None)
    elif action == ACTIONS_MAP["SELL_CHAMPION_POS_7"]:
        return (player.board[6] != None)
    elif action == ACTIONS_MAP["SELL_CHAMPION_POS_8"]:
        return (player.board[7] != None)
    elif action == ACTIONS_MAP["SELL_CHAMPION_POS_9"]:
        return (player.board[8] != None)

    # Can move champion on bench to board if board is not full
    # and the bench champion exists
    elif action == ACTIONS_MAP["BENCH_1_TO_BOARD"]:
        return (not player.board_is_full and player.bench[0] != None)
    elif action == ACTIONS_MAP["BENCH_2_TO_BOARD"]:
        return (not player.board_is_full and player.bench[1] != None)
    elif action == ACTIONS_MAP["BENCH_3_TO_BOARD"]:
        return (not player.board_is_full and player.bench[2] != None)
    elif action == ACTIONS_MAP["BENCH_4_TO_BOARD"]:
        return (not player.board_is_full and player.bench[3] != None)
    elif action == ACTIONS_MAP["BENCH_5_TO_BOARD"]:
        return (not player.board_is_full and player.bench[4] != None)
    elif action == ACTIONS_MAP["BENCH_6_TO_BOARD"]:
        return (not player.board_is_full and player.bench[5] != None)
    elif action == ACTIONS_MAP["BENCH_7_TO_BOARD"]:
        return (not player.board_is_full and player.bench[6] != None)
    elif action == ACTIONS_MAP["BENCH_8_TO_BOARD"]:
        return (not player.board_is_full and player.bench[7] != None)
    elif action == ACTIONS_MAP["BENCH_9_TO_BOARD"]:
        return (not player.board_is_full and player.bench[8] != None)

    # Can move champion on bench to board if bench is not full
    # and the board champion exists
    elif action == ACTIONS_MAP["BOARD_1_TO_BENCH"]:
        return (not player.bench_is_full and player.board[0] != None)
    elif action == ACTIONS_MAP["BOARD_2_TO_BENCH"]:
        return (not player.bench_is_full and player.board[1] != None)
    elif action == ACTIONS_MAP["BOARD_3_TO_BENCH"]:
        return (not player.bench_is_full and player.board[2] != None)
    elif action == ACTIONS_MAP["BOARD_4_TO_BENCH"]:
        return (not player.bench_is_full and player.board[3] != None)
    elif action == ACTIONS_MAP["BOARD_5_TO_BENCH"]:
        return (not player.bench_is_full and player.board[4] != None)
    elif action == ACTIONS_MAP["BOARD_6_TO_BENCH"]:
        return (not player.bench_is_full and player.board[5] != None)
    elif action == ACTIONS_MAP["BOARD_7_TO_BENCH"]:
        return (not player.bench_is_full and player.board[6] != None)
    elif action == ACTIONS_MAP["BOARD_8_TO_BENCH"]:
        return (not player.bench_is_full and player.board[7] != None)
    elif action == ACTIONS_MAP["BOARD_9_TO_BENCH"]:
        return (not player.bench_is_full and player.board[8] != None)

    elif action == ACTIONS_MAP["REROLL"]:
        return (player.gold >= 2)

    elif action == ACTIONS_MAP["BUY_EXP"]:
        return (player.gold >= 4 and player.level < 9)

    elif action == ACTIONS_MAP["READY_NEXT_STAGE"]:
        return (not player.ready)
    else:
        raise Exception("UNRECOGNIZED ACTION", action)