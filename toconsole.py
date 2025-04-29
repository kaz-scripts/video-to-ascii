import cv2
import os
import tqdm
import subprocess
import ffmpeg
import time
import sys
import threading
from colorama import init, Fore, Back, Style

init()

def play_audio(filename):
    subprocess.call(['ffplay', '-nodisp', '-autoexit', filename])

def process_video(videofile):
    cap = cv2.VideoCapture(videofile)
    f = [0, 0, 0]

    if cap.isOpened():
        os.makedirs('frames', exist_ok=True)
        base_path = os.path.join('frames')
        digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        for i in tqdm.tqdm(range(frames)):
            if not os.path.isfile('./frames/'+str(i)+'.jpg'):
                ret, frame = cap.read()
                if ret:
                    cv2.imwrite('./frames/'+str(i)+'.jpg', frame)

    if not os.path.isfile("bgm.mp3"):
        stream = ffmpeg.input(videofile)
        stream = ffmpeg.output(stream,"bgm.mp3")
        ffmpeg.run(stream)

    audio_thread = threading.Thread(target=play_audio, args=('bgm.mp3',))
    now = time.time()
    audio_thread.start()

    while True:
        n = int((time.time() - now) * cv2.VideoCapture(videofile).get(cv2.CAP_PROP_FPS))
        img = cv2.imread('./frames/'+str(n-1)+'.jpg')
        if img is None:
            break
        h, w = img.shape[:2]
        #width = 64
        width = 128
        height = round(h * (width / w)) * 2
        img = cv2.resize(img, dsize=(width, height))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        colorset = "　ゝニ人丁乙十三口山下火女円王四月玉右左糸貝気花学体雨音草校夏教強森雲遠語園歌談横線館頭親優縮厳績謝講顔鏡願護競議顧艦籠襲驚鑑鬱"
        output = ""
        for gray2 in gray:
            for dark in gray2:
                output += colorset[dark // 4] * 2
            output += "\n"
        f[0] += 1
        sys.stdout.write('\033[H')
        #sys.stdout.write('\033[J')
        sys.stdout.write(output+f"\nFPS:{f[2]}")
        if time.time() - f[1] >= 1:
            f[2] = f[0]
            f[0] = 0
            f[1] = time.time()

    audio_thread.join()

videofile = input("video path:")
process_video(videofile)
