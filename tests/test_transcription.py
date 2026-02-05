import os
import sys
import pytest
import whisper

present_dir = os.path.dirname(os.path.abspath(__file__))
locate_dir = os.path.dirname(present_dir)
sys.path.append(locate_dir)

from main import audio_transcription

#test setup
@pytest.fixture(scope = "module")
def model():
    return whisper.load_model("tiny")   #load faster using tiny

#for test
def test_audio_transcription(model):
    present_dir = os.path.dirname(os.path.abspath(__file__))
    audio_path = os.path.join (present_dir, "test_audio.wav")

    #check for the file
    assert os.path.exists(audio_path), f"File missing!!!! :{audio_path}"

    #run function
    text_result = audio_transcription(model, audio_path)

    # show result
    assert isinstance(text_result, str)
    assert len(text_result) > 0   #must not be empty

    print(f"test success! the model received: '{text_result}'")
