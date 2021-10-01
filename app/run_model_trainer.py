import tft_fight_predictor.training.model_trainer as model_trainer

model_trainer.read_training_data_and_build_model()


prediction = model_trainer.TftFightPredictor().predict_tft_fight([
	"TFT5_Nautilus",89,0,0,1,
	"TFT5_Thresh",0,0,0,1,
	"TFT5_Nidalee",0,0,0,1,
	"TFT5_Jax",16,29,15,1,
	"TFT5_Rell",55,77,0,1,
	"TFT5_Galio",2099,2046,2011,1,
	"TFT5_Viego",45,0,0,2,
	"TFT5_Garen",34,33,1158,2,
	"None",0,0,0,0,

	"TFT5_Vayne",0,23,26,3,
	"TFT5_Hecarim",2055,25,0,3,
	"TFT5_Sejuani",0,0,0,3,
	"TFT5_Nautilus",0,0,0,2,
	"TFT5_Thresh",0,0,0,2,
	"TFT5_Ashe",17,79,17,2,
	"TFT5_Rell",34,44,4,1,
	"TFT5_Draven",0,0,0,1,
	"None",0,0,0,0
])
print(prediction)