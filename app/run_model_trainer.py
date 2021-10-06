import tft_fight_predictor.training.model_trainer as model_trainer
from environments.teamfighttactics.teamfighttactics.envs.game_engine import Player
from environments.teamfighttactics.teamfighttactics.envs.game_utils import create_and_save_game_state_one_hot_encoder

from tft_fight_predictor.teamfight_predictor import TftFightPredictor


create_and_save_game_state_one_hot_encoder()
model_trainer.read_training_data_and_build_model()

# p1 = Player(0)
# p2 = Player(1)
# prediction = TftFightPredictor().predict_tft_fight(p1, p2)
# print(prediction)