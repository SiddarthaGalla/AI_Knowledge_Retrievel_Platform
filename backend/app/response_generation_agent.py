import requests


def generate_response(query, retrieved_results):

    # =====================================================
    # RETRIEVED INFORMATION
    # =====================================================

    context_blocks = []
    for i, chunk in enumerate(retrieved_results):
        context_blocks.append(f"[Document Excerpt {i+1}]:\n{chunk.strip()}")

    context = "\n\n".join(context_blocks)

    # =====================================================
    # LLM PROMPT
    # =====================================================

    prompt = f"""You are a knowledgeable, document-grounded AI assistant.

Analyze the user's question carefully and provide a thorough, accurate, and well-structured answer using ONLY the facts present in the document excerpts below.

DOCUMENT EXCERPTS:
{context}

USER QUESTION:
{query}

INSTRUCTIONS:
1. Ground your answer strictly in the provided document excerpts.
2. Answer the question completely and directly. If the question asks for multiple details, requirements, or steps, explain all of them clearly.
3. Use clear bullet points where appropriate to make lists and multi-part answers easy to read.
4. Do not invent, assume, or speculate about anything not supported by the document excerpts.
5. If the document excerpts genuinely do not contain the answer, reply: "Information not found in the knowledge base."
6. Do not include conversational preambles (such as "Based on the text..." or "Sure!"). Provide the direct factual answer.

ANSWER:"""

    # =====================================================
    # CALL GROQ (FAST CLOUD) OR OLLAMA (LOCAL FALLBACK)
    # =====================================================

    from app.config import GROQ_API_KEY, GROQ_MODEL, OLLAMA_URL, OLLAMA_MODEL

    if GROQ_API_KEY:
        try:
            groq_response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": GROQ_MODEL,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a knowledgeable, document-grounded AI assistant. Follow all instructions strictly."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.0
                },
                timeout=30
            )
            if groq_response.status_code == 200:
                answer = groq_response.json()["choices"][0]["message"]["content"]
                return answer.strip()
            else:
                print(f"[Warning] Groq returned {groq_response.status_code}: {groq_response.text}. Falling back to Ollama.")
        except Exception as e:
            print(f"[Warning] Groq request failed: {e}. Falling back to Ollama.")

    # Fallback to local Ollama
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0
            }
        },
        timeout=90
    )

    response.raise_for_status()

    return response.json()["response"].strip()