from huggingface_hub import list_models, model_info

# List 5 text-generation models
models = list_models(filter="text-generation", limit=5)

for model in models:
    info = model_info(model.modelId)
    print(f"\nModel: {model.modelId}")
    print(f"  Downloads: {info.downloads}")
    print(f"  Likes: {info.likes}")
    print(f"  Last Modified: {info.lastModified}")
