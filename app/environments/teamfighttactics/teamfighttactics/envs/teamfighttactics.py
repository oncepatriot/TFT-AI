import gym
import numpy as np
import config
from stable_baselines import logger
from .game_engine import *
from .game_utils import get_champion_id_and_item_name_to_unique_id_map

class TeamfightTacticsEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose = False, manual = False):
        super(TeamfightTacticsEnv, self).__init__()
        self.name = 'teamfighttactics'
        self.manual = manual        
        self.n_players = 8

        # Vector of all actions available to an agent
        self.action_space = gym.spaces.Discrete(len(ACTIONS_MAP.keys())) # 44 for now...

        # Observation space:
        # 
        # 
        # 5 spots for gold, health, exp, levels, streak
        #
        # 5 spots for shop (champ_id)
        # 9 * 4 spots for bench (champ, item, item, item)
        # 9 * 4 spots for boards (champ, item, item, item) 
        self.observation_space = gym.spaces.Box(
            np.array([0, -100, 0, 0, -30] + [0]*77),   # 8s elements
            np.array([300, 100, 100, 9, 50] +  [1]*77) # 82 elements
        )

        self.champion_or_item_to_normalized_id = get_champion_id_and_item_name_to_unique_id_map()

        # self.players is defined in base class
        self.current_player_num = 0
        self.verbose = verbose

        # Game state initialized on reset()
        self.game_manager = None
        self.champion_pool = []


    @property
    def observation(self):
        """The `observation` function returns a numpy array 
        that can be fed as input to the PPO policy network. It should 
        return a numeric representation of the current game state, 
        from the perspective of the current player, where each element
        of the array is in the range `[-1,1]`.
        """
        player = self.current_player
        player_data = [[player.gold, player.health, player.exp, player.level, player.streak]]
        shop_data = [[c.champion_id if c else None for c in player.shop]]
        shop_data = [[self.champion_or_item_to_normalized_id[c] for c in s] for s in shop_data]

        bench_data = []
        for c in player.bench:
            if c == None:
                bench_data.append([None, None, None, None])
            else:
                bench_data.append([c.champion_id, c.items[0], c.items[1], c.items[2]])
        bench_data = [[self.champion_or_item_to_normalized_id[c] for c in b] for b in bench_data]

        board_data = []
        for c in player.board:
            if c == None:
                board_data.append([None, None, None, None])
            else:
                board_data.append([c.champion_id, c.items[0], c.items[1], c.items[2]])
        board_data = [[self.champion_or_item_to_normalized_id[c] for c in b] for b in board_data]

        obs = player_data + shop_data + bench_data + board_data
        # print(obs)
        result = np.concatenate(obs).flatten()
        # print(result)
        return result

    def step(self, action):
        """The `step` method accepts an `action` from the current active player and performs the
        necessary steps to update the game environment. It should also it should 
        update the `current_player_num` to the next player, and check to see if 
        an end state of the game has been reached.

        Arguments:
            action - int - Action integer that maps to an action in the action space
        """
        print(self.current_player_num, action)
        done = False
        reward = [0.0] * self.n_players
        

        # VALIDATE ACTIONS... Money to buy, If ready cant perform any actions.
        # punish taking actions that are invalid
        if self.legal_actions[action] == 0:
            reward = [1.0/(self.n_players-1)] * self.n_players
            reward[self.current_player_num] = -1
        else:
            try:
                if not self.current_player.is_eliminated:
                    self.game_manager.execute_agent_action(self.current_player, action)
            except Exception as e:
                print("ERROR EXECUTING ACTION", e)
                print(self.game_manager.print_board_state())
                raise Exception("Error executing game action")

            # IF ALL PLAYERS ARE READY:
            # Calculate "combat math" based on all players current boards.
            # Matchmake players against one another, subtract healths
            # Eliminate dead players
            # End game if last player standing
            if self.game_manager.is_all_players_ready:
                print("all players ready")
                self.game_manager.increment_stage_round()
                self.game_manager.simulate_combat_step()
                self.game_manager.distribute_income()
                self.game_manager.roll_all_players_shops()
                self.game_manager.print_board_state()


                # Distribute reward if a player has 4+ win streak
                for i, player in enumerate(self.players):
                    if player.streak >= 4:
                        reward[i] += .15


            if self.game_manager.check_game_over():
                print("==========")
                print("GAME OVER")
                print("FINAL BOARD STATE:")
                print(self.game_manager.print_board_state())
                print("==========")
                print("FINAL PLACEMENTS:")
                print(self.game_manager.placements)
                # Distribute rewards based on placement
                for place, player_id in enumerate(self.game_manager.placements):
                    place_to_reward = [10,6,4,2,-2,-4,-6,-8]
                    reward[player_id] = place_to_reward[place]

                print("REWARDS:", reward)
                done = True

        # Update current player to the next player
        self.current_player_num = (self.current_player_num + 1) % self.n_players

        self.done = done
        return self.observation, reward, done, {}

    def reset(self):
        """The `reset` method is called to reset the game to the starting state, 
        ready to accept the first action.
        """
        print("CALLED RESET")
        self.current_player_num = 0
        self.players = [
            Player(0),
            Player(1),
            Player(2),
            Player(3),
            Player(4),
            Player(5),
            Player(6),
            Player(7)
        ]
        self.game_manager = GameManager(self.players)
        self.game_manager.create_champion_pool()

        self.done = False

        logger.debug(f'\n\n---- NEW GAME ----')
        return self.observation

    def render(self, mode='human', close=False):
        """The `render` function is called to output a visual or human readable
         summary of the current game state to the log file.
        """
        # self.game_manager.print_board_state()
        return

    @property
    def legal_actions(self):
        """The `legal_actions` function returns a numpy vector of the 
        same length as the action space, where 1 indicates that the action is valid 
        and 0 indicates that the action is invalid.
        """
        legal_actions = np.zeros(self.action_space.n)

        for i in range(self.action_space.n):
            legal_actions[i] = (1 if is_action_legal(self.current_player, i) else 0)

        return legal_actions

    @property
    def current_player(self):
        return self.players[self.current_player_num]