import gradio as gr
import google.generativeai as genai

def get_api():
    GOOGLE_API_KEY=''
    genai.configure(api_key=GOOGLE_API_KEY)

def generate_content(question,model_name):
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(question)
    return response.text

def main():
    get_api()

    # Get the list of models
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]

    interface = gr.Interface(fn=generate_content, 
                             inputs=[gr.Textbox(lines=2, placeholder="Enter your question here..."),gr.Dropdown(choices=models, label="model")], 
                             outputs=gr.Markdown())
    interface.launch()

if __name__ == "__main__":
    main()