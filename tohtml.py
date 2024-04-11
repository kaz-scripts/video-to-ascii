import cv2
import os
import tqdm
import ffmpeg

videofile = input("video path:")
cap = cv2.VideoCapture(videofile)

if cap.isOpened():
    os.makedirs('frames' ,exist_ok=True)
    base_path = os.path.join('frames')
    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    for i in tqdm.tqdm(range(frames)):
        if not os.path.isfile('./frames/'+str(i)+'.jpg'):
            ret, frame = cap.read()
            if ret:
                cv2.imwrite('./frames/'+str(i)+'.jpg', frame)

if os.path.isfile("./output.html"):
    os.remove("./output.html")
if not os.path.isfile("bgm.mp3"):
    stream = ffmpeg.input(videofile)
    stream = ffmpeg.output(stream,"bgm.mp3")
    ffmpeg.run(stream)

def scale_to_width(img, width):
    h, w = img.shape[:2]
    height = round(h * (width / w))
    dst = cv2.resize(img, dsize=(width, height))

    return dst

with open("output.html", "a", encoding='UTF-8') as f:
    print('<html><head><title>made by wakka</title><meta charset="utf-8"><style>#ascii { font-size: 0.8vmin;word-break:keep-all;text-align: center;white-space: nowrap;}</style><style>.button {border: 0;line-height: 2.5;padding: 0 20px;font-size: 1rem;text-align: center;color: #fff;text-shadow: 1px 1px 1px #000;border-radius: 10px;background-color: rgba(220, 0, 0, 1);background-image: linear-gradient(to top left,rgba(0, 0, 0, .2),rgba(0, 0, 0, .2) 30%,rgba(0, 0, 0, 0));box-shadow: inset 2px 2px 3px rgba(255, 255, 255, .6),inset -2px -2px 3px rgba(0, 0, 0, .6);}.button:hover {background-color: rgba(255, 0, 0, 1);}.button:active {box-shadow: inset -2px -2px 3px rgba(255, 255, 255, .6),inset 2px 2px 3px rgba(0, 0, 0, .6);}</style><div id="ascii"></div>',file=f)
    print('<script async>function Click(){',file=f)
    print('(async () => {',file=f)
    print('let ad = new Audio("./bgm.mp3");ad.volume = 0.3;const sleep = (s) => new Promise(resolve => setTimeout(resolve, s));',file=f)
    print('var elem = document.getElementById("ascii");',file=f)
    print('let fps = '+str(cv2.VideoCapture(videofile).get(cv2.CAP_PROP_FPS))+';let lag = 2;fps = 1000/fps;',file=f)
    print('var list = [\'',file=f,end='')

for i in tqdm.tqdm(range(frames)):
#for i in tqdm.tqdm(range(60)):
    n += 1
    img = scale_to_width(cv2.imread('./frames/'+str(n-1)+'.jpg'),96)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    colorset = "鬱鑑驚襲籠艦顧議競護願鏡顔講謝績厳縮優親頭館線横談歌園語遠雲森強教夏校草音雨体学花気貝糸左右玉月四王円女火下山口三十乙丁人ニゝ　"
    output = ""
    for gray2 in gray:
        for dark in gray2:
            output += colorset[dark // 4] * 2
        output += "\\n"
    with open("output.html", "a", encoding='UTF-8') as f:
        print(output+"','",file=f,end='')

with open("output.html", "a", encoding='UTF-8') as f:
        print(output+"',''];",file=f,end='\n')
        print('let n = list.length;var start = new Date();var now = 0;ad.play();while(now+1<=n){await sleep(fps/lag);now = Math.floor((new Date().getTime() - start.getTime())/fps);',file=f)
        print('if(list[now] != undefined){',file=f)
        print("elem.innerText = list[now-1]+'\\n'+'frame:'+(now+1)+'/'+n;",file=f)
        print('}}})()}</script><button class="button" type="button" onclick="Click();" autofocus>実行！！！</button></head></html>',file=f)