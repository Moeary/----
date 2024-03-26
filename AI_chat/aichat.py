import gradio as gr
import datetime
import os
import azure.cognitiveservices.speech as speechsdk
import google.generativeai as genai
import re

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms.ollama import Ollama

llm = Ollama(base_url="http://localhost:11434", model="gemma:2b",)

def generate_content(question):
    response = llm.invoke(question)
    print(response)
    return response

def get_api():
    with open('api.key', 'r') as file:
        GOOGLE_API_KEY = file.read().strip()
    genai.configure(api_key=GOOGLE_API_KEY)

def get_voices():
    with open('azure_api.key', 'r') as file:
        speech_key = file.readline().strip()  # Read the first line
        service_region = file.readline().strip()  # Read the second line

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    voices = speech_synthesizer.get_voices_async().get()
    voice_names = [voice.name for voice in voices.voices]
    return voice_names

def synthesize_speech(text, voice):
    with open('azure_api.key', 'r') as file:
        speech_key = file.readline().strip()  # Read the first line
        service_region = file.readline().strip()  # Read the second line
    
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    valid_text = re.sub(r'[\/:*?"<>|]', '', text[:20])  # Remove invalid filename characters
    output_audio_filename =valid_text + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".wav"
    
    # Check if the directory exists and create it if not
    os.makedirs(os.path.dirname(output_audio_filename), exist_ok=True)

    audio_output = speechsdk.audio.AudioOutputConfig(filename=output_audio_filename)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

    ssml_string = "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='zh-CN'><voice name='{}'>{}</voice></speak>".format(voice, text)
    result = speech_synthesizer.speak_ssml_async(ssml_string).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to [{}] for text [{}]".format(output_audio_filename, text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

    return text, gr.Audio(output_audio_filename)

def main():
    # get_api()

    # models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    models = "111"
    def process(question, model_name, voice):
        text = generate_content(question)
        return synthesize_speech(text, voice)

    iface = gr.Interface(fn=process, 
                         inputs=[gr.Textbox(lines=2, placeholder="Enter your question here..."),gr.Dropdown(choices=get_voices(), label="Voice")], 
                         outputs=["text", "audio"], 
                         title="AI对话机器人",
                         description="Enter some text and select a model and voice to synthesize speech.")
    iface.launch()

if __name__ == "__main__":
    main()