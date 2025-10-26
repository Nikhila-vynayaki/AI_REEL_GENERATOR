from flask import Flask
import os
from text_to_audio import text_to_audio
import subprocess
import time

# app=Flask(__name__)
def text_to_speech(folder):
    with open(f"user_uploads/{folder}/desc.txt") as f:
        text=f.read()
    text_to_audio(text, folder)
    # text_to_audio(text,folder)

def reel_generator(folder):
    command=f'ffmpeg -f concat -safe 0 -i user_uploads/{folder}/input.txt -i user_uploads/{folder}/audio.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/{folder}.mp4'
    subprocess.run(command, shell=True, check=True)

if os.path.exists("generated_reels.txt") is False:
    with open("generated_reels.txt",'w') as f:
        pass

if __name__=="__main__":
    while True:
        
        folders = [
            folder for folder in os.listdir("user_uploads")
            if os.path.isdir(os.path.join("user_uploads", folder))
        ]
        if folders:
            print("Found folders:", folders)
        else:
            print("No folders found, waiting for user uploads...")

        print(folders)
        with open("generated_reels.txt",'r') as f:
            files=[line.strip() for line in f.readlines()]
        for folder in folders:
            if folder not in files:
                text_to_speech(folder)
                reel_generator(folder)
                with open("generated_reels.txt",'a') as f:
                    f.write(folder+"\n")
        time.sleep(10)