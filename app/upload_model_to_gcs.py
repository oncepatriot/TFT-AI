import utils.google_cloud_storage as gcs

gcs.upload_model_to_gcs('zoo/teamfighttactics/base.zip')


try:
    gcs.upload_best_model_to_gcs('zoo/teamfighttactics/tmp/best_model.zip')
except Exception:
    print("No best model to upload")


gcs.upload_to_bucket('logs', 'tft_models', 'logs')