import json
from datetime import datetime
from huggingface_hub import list_models, model_info

# Get 5 text-generation models
models = list_models(filter="text-generation", limit=5)

results = []  # store all model data

for model in models:
    info = model_info(model.modelId)
    # Convert the info object to a dictionary
    data = {
        "modelId": model.modelId,
        "downloads": info.downloads,
        "likes": info.likes,
        "lastModified": info.lastModified,
        # "files": [s.rfilename for s in info.siblings],  # optional, lists repo files
    }
    results.append(data)

# Print as pretty JSON
def default_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

print(json.dumps(results, indent=2, default=default_encoder))
