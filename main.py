import whisper
import pyaudio
import os
import wave


MODEL_TYPE = "base"
SESSION_FILE = "transcription_output.txt"


def record_voice(duration=5, chunk_file="audio.wav"):
    data_size = 1024
    format_audio = pyaudio.paInt16
    channels = 1
    test_rate = 16000

    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=format_audio,
                        channels=channels,
                        rate=test_rate,
                        input=True,
                        frames_per_buffer=data_size)

        print(f" listening....Please Speak ({duration}) ", end="", flush=True)
        frames = []

        for _ in range(0, int(test_rate / data_size * duration)):
            data = stream.read(data_size)
            frames.append(data)

        stream.stop_stream()
        stream.close()

        # save raw audio data
        with wave.open(chunk_file, 'wb') as audio_format:
            audio_format.setnchannels(channels)
            audio_format.setsampwidth(p.get_sample_size(format_audio))
            audio_format.setframerate(test_rate)
            audio_format.writeframes(b''.join(frames))

    except Exception as e:
        print(f"Error recording: {e} ")
    finally:
        p.terminate()  # close PyAudio to avoid crashing


def audio_transcription(model, audio_path):
    # check file exists
    if not os.path.exists(audio_path):
        return ""

    # run model
    result = model.transcribe(audio_path, fp16=False)

    # Return text part
    return result["text"].strip()


def save_file(text, filename):
    with open(filename, "a") as f:
        f.write(text + "\n")


def main():
    print(f" wait a moment'{MODEL_TYPE}'")
    try:
        model = whisper.load_model(MODEL_TYPE)
    except Exception as e:
        print("Error while load the model")
        print(e)
        return

    print(f" audio translation text will save on : {SESSION_FILE}")
    print(" Ctrl + c to stop")

    # main program loop
    try:
        while True:
            record_voice(5, "audio.wav")  # record

            text = audio_transcription(model, "audio.wav")  # transcribe

            # for save
            if len(text) > 0:
                print(f"\n Result : {text}")
                save_file(text, SESSION_FILE)
            else:
                print(".", end="", flush=True)

    except KeyboardInterrupt:
        print("\n Stop")

        # if os.path.exists("audio.wav"):
        # os.remove("audio.wav")


if __name__ == "__main__":
    main()
