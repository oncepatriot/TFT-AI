from gym.envs.registration import register

register(
    id='TeamfightTactics-v0',
    entry_point='teamfighttactics.envs:TeamfightTacticsEnv',
)
