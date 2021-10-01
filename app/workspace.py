import environments.teamfighttactics.teamfighttactics.envs.game_utils as game_utils
import environments.teamfighttactics.teamfighttactics.envs.game_engine as game_engine

gm = game_engine.GameManager([1,2,3,4,5,6,7,8])
gm.create_champion_pool()
print(gm.champion_pool[1][0])