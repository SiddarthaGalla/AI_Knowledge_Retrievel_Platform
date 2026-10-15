_model = None


def _get_embedding_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def create_embeddings(texts):
    model = _get_embedding_model()
    return model.encode(texts).tolist()