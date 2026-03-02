import pytest
import whisper


# test setup
@pytest.fixture(scope="module")
def model():
    return whisper.load_model("base")


# for test
def test_audio_transcription(model):
    audio_path = "tests/test_audio.wav"

    result = model.transcribe(audio_path)
    text = result["text"].lower().strip()

    # result
    expected_word = "room"
    assert expected_word in text, f"transcription failed '{expected_word}' but got: '{text}'"
