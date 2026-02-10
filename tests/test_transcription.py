import os
import sys
import pytest
import whisper
from numba.core.cgutils import printf

present_dir = os.path.dirname(os.path.abspath(__file__))
locate_dir = os.path.dirname(present_dir)
sys.path.append(locate_dir)

from main import audio_transcription


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
    expected_word = "test"
    assert expected_word in text, f"transcription failed' {expected_word}' "
    print(f"test success! the model received:' {text}'")

