import gym
import numpy as np
import config
from stable_baselines import logger
from .game_engine import *
from .game_utils import PlayerEncoder

class TeamfightTacticsEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose = False, manual = False):
        super(TeamfightTacticsEnv, self).__init__()
        self.name = 'teamfighttactics'
        self.manual = manual        
        self.n_players = 8

        # Vector of all actions available to an agent
        self.action_space = gym.spaces.Discrete(len(ACTIONS_MAP.keys()))

        # Observation space - One hot encoded player state
        self.observation_space = gym.spaces.Box(low=-1, high=1, shape=(7711,), dtype=np.float32) 

        # self.players is defined in base class
        self.current_player_num = 0
        self.verbose = verbose

        # Game state initialized on reset()
        self.game_manager = None
        self.champion_pool = []

        self.player_encoder = PlayerEncoder()


    @property
    def observation(self):
        """The `observation` function returns a numpy array 
        that can be fed as input to the PPO policy network. It should 
        return a numeric representation of the current game state, 
        from the perspective of the current player, where each element
        of the array is in the range `[-1,1]`.
        """
        player = self.current_player
        obs = self.player_encoder.get_player_observation(player)
        return obs

        # return np.zeros(7081)

    def step(self, action):
        """The `step` method accepts an `action` from the current active player and performs the
        necessary steps to update the game environment. It should also it should 
        update the `current_player_num` to the next player, and check to see if 
        an end state of the game has been reached.

        Arguments:
            action - int - Action integer that maps to an action in the action space
        """
        done = False
        reward = [0.0] * self.n_players
        
        if self.legal_actions[action] == 0:
            # Maybe penalize illegal actions?: 
            pass
        else:
            try:
                self.game_manager.execute_agent_action(self.current_player, action)
            except Exception as e:
                print("ERROR EXECUTING ACTION", e)
                self.game_manager.print_board_state()
                raise Exception("Error executing game action")

        # If not a ready action
        if action != 43:
            self.current_player.actions_since_last_ready += 1
        # Force player to ready if they took 25 non ready actions
        if self.current_player.actions_since_last_ready > 35:
            self.current_player.ready = True
            self.current_player.actions_since_last_ready = 0

        # IF ALL PLAYERS ARE READY:
        # Calculate "combat math" based on all players current boards.
        # Matchmake players against one another, subtract healths
        # Eliminate dead players
        # End game if last player standing
        if self.game_manager.is_all_players_ready:
            self.game_manager.simulate_combat_step()
            self.game_manager.print_board_state()
            if self.game_manager.check_game_over():
                print("==========")
                print("GAME OVER")
                print("FINAL BOARD STATE:")
                self.game_manager.print_board_state()
                print("==========")
                print("FINAL PLACEMENTS:")
                print([player.id for player in self.game_manager.placements])
                done = True

                # Distribute rewards based on placement
                for place, player in enumerate(self.game_manager.placements):
                    print(place, player.id)
                    place_to_reward = [15,13,10,2,-6,-10,-13,-15]
                    reward[player.id] = place_to_reward[place]

                print("REWARDS:", reward)

            else:
                self.game_manager.distribute_income()
                self.game_manager.roll_all_players_shops()
                self.game_manager.increment_stage_round()

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