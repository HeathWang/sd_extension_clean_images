import modules.scripts as scripts
import gradio as gr
from pathlib import Path
import os
from datetime import datetime

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
    del_cnt = 0
    now = datetime.now()

    if category == 1:
        del_cnt = del_cnt + delete_image('outputs/txt2img-images')
        del_cnt = del_cnt + delete_image('outputs/txt2img-grids')
        process_logs = process_logs + now.strftime("%Y-%m-%d %H:%M:%S") + "-> done clean text to image..." + "total delete:{}\n".format(del_cnt)
    elif category == 2:
        del_cnt = del_cnt + delete_image('outputs/img2img-images')
        del_cnt = del_cnt + delete_image('outputs/img2img-grids')
        process_logs = process_logs + now.strftime("%Y-%m-%d %H:%M:%S") + "-> done clean image to image..." + "total delete:{}\n".format(del_cnt)
    elif category == 3:
        del_cnt = del_cnt + delete_image('outputs/txt2img-images')
        del_cnt = del_cnt + delete_image('outputs/txt2img-grids')
        del_cnt = del_cnt + delete_image('outputs/img2img-images')
        del_cnt = del_cnt + delete_image('outputs/img2img-grids')
        del_cnt = del_cnt + delete_image('outputs/extras-images')
        process_logs = process_logs + now.strftime("%Y-%m-%d %H:%M:%S") + "-> done clean all images..." + "total delete:{}\n".format(del_cnt)
    return process_logs

def clean_all():
    return base_clean_action(3)

def delete_image(input_path):
    sum = 0
    folder_path = os.path.join(ROOT_DIR, input_path)
    if not os.path.isdir(folder_path):
        print(f"Warning: {folder_path} is not a directory.")
    else:
    
        for f in os.listdir(folder_path):
            file_path = os.path.join(folder_path, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
                sum += 1

    return sum

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        txt_3 = gr.Textbox(value="", label="Logs", lines=3)

        btn_textImage = gr.Button(value="Clean Text To Image Output")
        btn_textImage.click(clean_text_to_images, outputs=[txt_3])

        btn_imageImage = gr.Button(value="Clean Image To Image Output")
        btn_imageImage.click(clean_image_to_images, outputs=[txt_3])

        btn_all = gr.Button(value="Clean ALL Output")
        btn_all.click(clean_all, outputs=[txt_3])
        return [(ui_component, "Clean Output Images", "Clean Output Images")]

script_callbacks.on_ui_tabs(on_ui_tabs)