# agrimitra-core

Set the following env vars in the .env dir:
```
GOOGLE_CLOUD_PROJECT="<project-name>"
GOOGLE_CLOUD_LOCATION="us-central1"
BQ_COMPUTE_PROJECT_ID="<project-name>"
BQ_DATA_PROJECT_ID="<project-name>"
BQ_DATASET_ID="<dataset_id>"
```

To run locally please set the .agnimitra/.env environment files as well.
Each of the rag, shopping , weather_forecast and datascience agent require their environment variables and API keys to be set up seperately as well


Then run the following:
use adk run agnimitra
or adk web to access the agent after filling up the environment variables

One can then continue to run the agri-mitra core agent!
