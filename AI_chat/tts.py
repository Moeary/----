import azure.cognitiveservices.speech as speechsdk

def speech_to_text(audio_filename):
    # Replace with your own subscription key and region identifier
    with open('azure_api.key', 'r') as file:
        speech_key = file.readline().strip()  # Read the first line
        service_region = file.readline().strip()  # Read the second line

    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region, speech_recognition_language='zh-CN')

    # Creates an audio configuration that points to an audio file.
    audio_input = speechsdk.AudioConfig(filename=audio_filename)

    # Creates a arecognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    # Starts speech recognition, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed.
    result = speech_recognizer.recognize_once()

    # Checks result.
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

def text_to_speech(text, output_audio_filename):
    # Replace with your own subscription key and region identifier
    with open('azure_api.key', 'r') as file:
        speech_key = file.readline().strip()  # Read the first line
        service_region = file.readline().strip()  # Read the second line

    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Creates an audio configuration that points to an audio file.
    audio_output = speechsdk.audio.AudioOutputConfig(filename=output_audio_filename)

    # Creates a speech synthesizer using the audio file as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

    # Set the speech synthesis language to Chinese.
    ssml_string = "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='zh-CN'><voice name='Microsoft Server Speech Text to Speech Voice (zh-CN, XiaoxiaoNeural)'>{}</voice></speak>".format(text)

    # Receives a text from console input and synthesizes it to the audio file.
    result = speech_synthesizer.speak_ssml_async(ssml_string).get()

    # Checks result.
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to [{}] for text [{}]".format(output_audio_filename, text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))


# Call the function
#speech_to_text('output.wav')
text_to_speech('我的梦想是', 'output.wav')