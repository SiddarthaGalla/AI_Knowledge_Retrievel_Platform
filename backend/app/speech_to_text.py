from pathlib import Path

_whisper_model = None


def _get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        try:
            import av
            _orig_av_open = av.open

            def _compatible_av_open(*args, **kwargs):
                kwargs.pop("metadata_errors", None)
                return _orig_av_open(*args, **kwargs)

            av.open = _compatible_av_open
        except Exception:
            pass

        from faster_whisper import WhisperModel
        _whisper_model = WhisperModel(
            "tiny",
            device="cpu",
            compute_type="int8"
        )
    return _whisper_model


def transcribe_audio(audio_file):

    # Try Groq Whisper cloud first if API key is configured (Uses 0 MB server RAM!)
    try:
        from app.config import GROQ_API_KEY
        if GROQ_API_KEY:
            import requests
            with open(audio_file, "rb") as f:
                r = requests.post(
                    "https://api.groq.com/openai/v1/audio/transcriptions",
                    headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                    files={"file": (Path(audio_file).name, f, "audio/webm")},
                    data={"model": "whisper-large-v3-turbo", "language": "en"},
                    timeout=15
                )
            if r.status_code == 200:
                cloud_text = r.json().get("text", "").strip()
                if cloud_text:
                    return cloud_text
    except Exception as e:
        print(f"[Warning] Groq Whisper failed: {e}. Falling back to local Whisper.")

    # Local fallback (only loaded on-demand if Groq is unavailable)
    model = _get_whisper_model()
    segments, info = model.transcribe(
        audio_file,
        language="en",
        beam_size=1,
        best_of=1,
        temperature=0.0,
        vad_filter=True
    )

    text = ""
    for segment in segments:
        text += segment.text

    return text.strip()
