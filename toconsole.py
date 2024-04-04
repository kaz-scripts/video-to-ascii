import cv2
import os
import tqdm
import ffmpeg
import os
import time
import sys
import subprocess


videofile = input("video path:")
cap = cv2.VideoCapture(videofile)
f = [0,0,0]
now = time.time()
if cap.isOpened():
    os.makedirs('frames' ,exist_ok=True)
    base_path = os.path.join('frames')
    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    n = 0
    for i in tqdm.tqdm(range(frames)):
        if not os.path.isfile('./frames/'+str(n)+'.jpg'):
            ret, frame = cap.read()
            if ret:
                cv2.imwrite('./frames/'+str(n)+'.jpg', frame)
                n += 1
n = 0

while(True):
#for i in tqdm.tqdm(range(60)):
    n = int((time.time() - now) * cv2.VideoCapture(videofile).get(cv2.CAP_PROP_FPS))
    img = cv2.imread('./frames/'+str(n-1)+'.jpg')
    if type(img) == type(None):
        break
    h, w = img.shape[:2]
    width = 52
    height = round(h * (width / w))
    img = cv2.resize(img, dsize=(width, height))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #colorset = "鬱鑑驚襲籠艦顧議競護願鏡顔講謝績厳縮優親頭館線横談歌園語遠雲森強教夏校草音雨体学花気貝糸左右玉月四王円女火下山口三十乙丁人ニゝ　"
    colorset = "　ゝニ人丁乙十三口山下火女円王四月玉右左糸貝気花学体雨音草校夏教強森雲遠語園歌談横線館頭親優縮厳績謝講顔鏡願護競議顧艦籠襲驚鑑鬱"
    output = ""
    for gray2 in gray:
        for dark in gray2:
            output += colorset[dark // 4] * 2
        output += "\n"
    f[0]+=1
    subprocess.call('cls', shell=True)
    print(output+f"\nFPS:{f[2]}",flush=True)
    if time.time() - f[1] >= 1:
        f[2] = f[0]
        f[0] = 0
        f[1] = time.time()