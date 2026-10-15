import re


def classify_query(query):
    query_str = (query or "").strip()
    query_lower = query_str.lower()
    clean_words = re.sub(r"[^\w\s]", "", query_lower).split()

    # Comparative queries
    comparative_markers = [
        "difference",
        "compare",
        "comparative",
        "versus",
        " vs ",
        "better",
        "distinguish",
        "comparison"
    ]

    # Procedural queries
    procedural_markers = [
        "how",
        "steps",
        "procedure",
        "process",
        "workflow",
        "instructions"
    ]

    if any(marker in query_lower for marker in comparative_markers):
        query_type = "comparative"
    elif any(marker in query_lower for marker in procedural_markers):
        query_type = "procedural"
    elif len(clean_words) < 2 or (
        len(clean_words) == 2
        and clean_words[0] in ["tell", "give", "show", "what"]
        and clean_words[1] in ["me", "this", "it", "more"]
    ):
        query_type = "ambiguous"
    else:
        # Natural queries, voice transcripts (which have no '?'), and statements default to factual
        query_type = "factual"

    return {
        "query": query,
        "query_type": query_type,
        "confidence": 0.9
    }