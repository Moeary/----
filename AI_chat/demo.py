import gradio as gr
import openai, subprocess
openai.api_key = ""

# messages = [{"role": "system", "content": '你是一名知识渊博，乐于助人的智能聊天机器人.你的任务是陪我聊天，请用简短的对话方式，每次回答不超过50个字！'}]
messages = [{"role": "system", "content": 'you are a chat bot'}]

def transcribe(audio):
    global messages

    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    messages.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response["choices"][0]["message"]
    messages.append(system_message)

    subprocess.call(["wsay", system_message['content']])

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript

ui = gr.Interface(
    fn=transcribe, 
    inputs=gr.Audio(type="filepath"), 
    outputs="text"
    ).launch()
ui.launch()