import gradio as gr
import google.generativeai as genai
import PIL.Image
from io import BytesIO
import requests

def get_api():
    GOOGLE_API_KEY=''
    genai.configure(api_key=GOOGLE_API_KEY)


def generate_content(image_url, question, model_name):
    model = genai.GenerativeModel(model_name)

    # Download the image
    response = requests.get(image_url)
    image = PIL.Image.open(BytesIO(response.content))

    response = model.generate_content([question, image])
    return response.text

def main():
    get_api()

    # Get the list of models
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods and 'vision' in m.name]

    interface = gr.Interface(fn=generate_content, 
                             inputs=[gr.Textbox(lines=2, placeholder="Enter your image path here..."), gr.Textbox(lines=2, placeholder="Enter your question here..."), gr.Dropdown(choices=models, label="Model")], 
                             outputs=gr.Markdown())
    interface.launch()

if __name__ == "__main__":
    main()