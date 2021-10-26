
---
<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

Install [Docker](https://github.com/davidADSP/SIMPLE/issues) and [Docker Compose](https://docs.docker.com/compose/install/) to make use of the `docker-compose.yml` file

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/davidADSP/SIMPLE.git
   cd SIMPLE
   ```
2. Build the image and 'up' the container.
   ```sh
   docker-compose up -d
   ```
3. Choose an environment to install in the container (`tictactoe`, `connect4`, `sushigo`, `geschenkt`, `butterfly`, and `flamme rouge` are currently implemented)
   ```sh
   bash ./scripts/install_env.sh sushigo
   ```

---
<!-- QUICKSTART -->
### Quickstart

#### `test.py` 

This entrypoint allows you to play against a trained AI, pit two AIs against eachother or play against a baseline random model.

For example, try the following command to play against a baseline random model in the Sushi Go environment.
   ```sh
   docker-compose exec app python3 test.py -d -g 1 -a base base human -e sushigo 
   ```

#### `train.py` 

This entrypoint allows you to start training the AI using selfplay PPO. The underlying PPO engine is from the [Stable Baselines](https://stable-baselines.readthedocs.io/en/master/) package.

For example, you can start training the agent to learn how to play SushiGo with the following command:
   ```sh
   docker-compose exec app python3 train.py -r -e sushigo 
   ```

After 30 or 40 iterations the process should have achieved above the default threshold score of 0.2 and will output a new `best_model.zip` to the `/zoo/sushigo` folder. 

Training runs until you kill the process manually (e.g. with Ctrl-C), so do that now.

You can now use the `test.py` entrypoint to play 100 games silently between the current `best_model.zip` and the random baselines model as follows:

  ```sh
  docker-compose exec app python3 test.py -g 100 -a best_model base base -e sushigo 
  ```

You should see that the best_model scores better than the two baseline model opponents. 
```sh
Played 100 games: {'best_model_btkce': 31.0, 'base_sajsi': -15.5, 'base_poqaj': -15.5}
```

You can continue training the agent by dropping the `-r` reset flag from the `train.py` entrypoint arguments - it will just pick up from where it left off.

   ```sh
   docker-compose exec app python3 train.py -e sushigo 
   ```

Congratulations, you've just completed one training cycle for the game Sushi Go! The PPO agent will now have to work out a way to beat the model it has just created...

---
<!-- TENSORBOARD -->
### Tensorboard

To monitor training, you can start Tensorboard with the following command:

  ```sh
  bash scripts/tensorboard.sh
  ```

Navigate to `localhost:6006` in a browser to view the output.

In the `/zoo/pretrained/` folder there is a pre-trained `/<game>/best_model.zip` for each game, that can be copied up a directory (e.g. to `/zoo/sushigo/best_model.zip`) if you want to test playing against a pre-trained agent right away.

---
<!-- CUSTOM ENVIRONMENTS -->
### Custom Environments

You can add a new environment by copying and editing an existing environment in the `/environments/` folder.

For the environment to work with the SIMPLE self-play wrapper, the class must contain the following methods (expanding on the standard methods from the OpenAI Gym framework):

`__init__`

In the initiation method, you need to define the usual `action_space` and `observation_space`, as well as two additional variables: 
  * `n_players` - the number of players in the game
  * `current_player_num` - an integer that tracks which player is currently active
   

`step`

The `step` method accepts an `action` from the current active player and performs the necessary steps to update the game environment. It should also it should update the `current_player_num` to the next player, and check to see if an end state of the game has been reached.


`reset`

The `reset` method is called to reset the game to the starting state, ready to accept the first action.


`render`

The `render` function is called to output a visual or human readable summary of the current game state to the log file.


`observation`

The `observation` function returns a numpy array that can be fed as input to the PPO policy network. It should return a numeric representation of the current game state, from the perspective of the current player, where each element of the array is in the range `[-1,1]`.


`legal_actions`

The `legal_actions` function returns a numpy vector of the same length as the action space, where 1 indicates that the action is valid and 0 indicates that the action is invalid.


Please refer to existing environments for examples of how to implement each method.

You will also need to add the environment to the two functions in `/utils/register.py` - follow the existing examples of environments for the structure.

---
<!-- Parallelisation -->
### Parallelisation

The training process can be parallelised using MPI across multiple cores.

For example to run 10 parallel threads that contribute games to the current iteration, you can simply run:

  ```sh
  docker-compose exec app mpirun -np 10 python3 train.py -e sushigo 
  ```


# SETUP

cd C:\Users\Samsung\Documents\GitHub\TFT-AI

docker-compose up -d
# install dependencies for env
bash ./scripts/install_env.sh teamfighttactics

SSH into container

docker exec -it selfplay bash
docker-compose exec app python3 run_data_scraper.py
docker-compose exec app python3 run_model_trainer.py
docker-compose exec app python3 test.py -e teamfighttactics
docker-compose exec app python3 train.py -e teamfighttactics

# The training process can be parallelised using MPI across multiple cores.
docker-compose exec app mpirun -np 10 python3 train.py -e teamfighttactics

bash ./scripts/install_env.sh teamfighttactics

# Single Core Basic Training
docker-compose exec app python3 train.py -e teamfighttactics

# TENSORBOARD
bash scripts/tensorboard.sh
Navigate tolocalhost:6006 

# Upload model to GCS
docker-compose exec -T app python3 upload_model_to_gcs.py


# GOOGLE COMPUTE ENGINE STUFF BELOW


# HOW TO RUN ON Google Compute engine
https://cloud.google.com/community/tutorials/docker-compose-on-container-optimized-os


# USING GIT TO PULL / PUSH TO REPOSITORY
git clone https://antoineblueberry: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@github.com/antoineblueberry/TFT-AI.git
docker run docker/compose:1.24.0 version
git pull origin master

Run rest of commands on link above

# TFT DEPENDENCY INSTALL AND RUN SCRIPTS
docker-compose up -d
docker-compose exec -T app pip3 install -e ./environments/teamfighttactics
docker-compose exec -T app pip3 install -r requirements.txt

docker-compose exec -T app python3 train.py -e teamfighttactics

docker-compose exec -T app mpirun --oversubscribe -np 6 python3 train.py -e teamfighttactics

docker-compose exec -T app mpirun -np 4 python3 train.py -e teamfighttactics



# EXPOSE TENSORBOARD
docker-compose exec -T -d app tensorboard --logdir ./logs

http://35.196.75.255:6006/ (external_ip:6006/)


# permission error? run this in all files
sudo chmod -R 777 . 


# Download logs
gsutil -m cp -R gs://tft_models/logs/ C:\Users\Samsung\Documents\GitHub\TFT-AI\app
gsutil -m cp -R gs://tft_models/logs/ C:\Users\Samsung\Documents\GitHub\TFT-AI\app

# SSH
gcloud compute ssh instance-1






# TODO
- Add Carousel
- Look into distributed training rllib: https://docs.ray.io/en/latest/rllib.html
- Prepare for set 6 - updating encoders, predictors, and observation space size
- Manual testing of actions - play a game loop manualy and see if state is updated correctly
- Improve performance of game engine/environment
- Develop overwolf app to gather data for real fight prediction


actions are legal at each step
Look into distributed training rllib: https://docs.ray.io/en/latest/rllib.html
