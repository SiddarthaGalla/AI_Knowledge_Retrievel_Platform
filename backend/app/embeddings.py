_model = None
_backend = None


def _get_embedding_model():
    global _model, _backend
    if _model is None:
        try:
            from fastembed import TextEmbedding
            _model = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
            _backend = "fastembed"
        except Exception:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer("all-MiniLM-L6-v2")
            _backend = "sentence_transformers"
    return _model


def create_embeddings(texts):
    model = _get_embedding_model()
    if _backend == "fastembed":
        return [e.tolist() for e in model.embed(texts)]
    return model.encode(texts).tolist()