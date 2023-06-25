import modules.scripts as scripts
import gradio as gr
from pathlib import Path
import os

from modules import script_callbacks

process_logs = ""
# Webui root path
ROOT_DIR = Path().absolute()

def clean_text_to_images():
    return base_clean_action(1)

def clean_image_to_images():
    return base_clean_action(2)

def base_clean_action(category):
    global process_logs
    
    if category == 1:
        process_logs = process_logs + "done clean text to image...\n"
        delete_image('outputs/txt2img-images')
        delete_image('outputs/txt2img-grids')
    return process_logs

def clean_all():
    pass

def delete_image(input_path):
    # /kaggle/working/stable-diffusion-webui/outputs/txt2img-images
    # /kaggle/working/stable-diffusion-webui/outputs/txt2img-grids
    # /kaggle/working/stable-diffusion-webui/outputs/img2img-grids
    # /kaggle/working/stable-diffusion-webui/outputs/img2img-images
    # /kaggle/working/stable-diffusion-webui/outputs/extras-images
    folder_path = os.path.join(ROOT_DIR, input_path)
    if not os.path.isdir(folder_path):
        print(f"Warning: {folder_path} is not a directory.")
        continue
    
    for f in os.listdir(folder_path):
        file_path = os.path.join(folder_path, f)
        if os.path.isfile(file_path):
            os.remove(file_path)



def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        txt_3 = gr.Textbox(value="", label="Logs", lines=3)

        btn_textImage = gr.Button(value="Text To Image")
        btn_textImage.click(clean_text_to_images, outputs=[txt_3])

        btn_imageImage = gr.Button(value="Image To Image")
        btn_imageImage.click(clean_image_to_images, outputs=[txt_3])

        btn_all = gr.Button(value="ALL")
        btn_all.click(clean_all, outputs=[txt_3])
        return [(ui_component, "sd_extension_clean_images", "sd_extension_clean_images")]

script_callbacks.on_ui_tabs(on_ui_tabs)
