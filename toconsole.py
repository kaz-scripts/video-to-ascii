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

# 文字アート用の文字セット
CHAR_SET = "　ゝニ人丁乙十三口山下火女円王四月玉右左糸貝気花学体雨音草校夏教強森雲遠語園歌談横線館頭親優縮厳績謝講顔鏡願護競議顧艦籠襲驚鑑鬱"
DEFAULT_WIDTH = 128  # デフォルトの幅
CHAR_DIVISION = 4    # 文字を選択する際の除算値

def play_audio(filename):
    """ビデオファイルから直接音声を再生する"""
    try:
        # 直接ビデオファイルから音声のみを再生
        subprocess.call(['ffplay', '-nodisp', '-autoexit', '-loglevel', 'error', '-i', filename])
    except Exception as e:
        print(f"{Fore.RED}音声再生エラー: {e}{Style.RESET_ALL}")

def convert_to_ascii_art(img, width=DEFAULT_WIDTH):
    """画像をカラー文字アートに変換する"""
    h, w = img.shape[:2]
    height = round(h * (width / w)) * 2
    img = cv2.resize(img, dsize=(width, height))
    
    output = ""
    for y in range(height):
        for x in range(width):
            # BGRからRGBに変換（OpenCVはBGR形式）
            b, g, r = img[y, x]
            
            # 明るさに基づいて文字を選択
            brightness = (int(r) + int(g) + int(b)) // 3
            char = CHAR_SET[brightness // CHAR_DIVISION]
            
            # ANSIエスケープシーケンスで色を設定
            output += f"\033[38;2;{r};{g};{b}m{char*2}"
        
        output += Style.RESET_ALL + "\n"
    
    return output

def calculate_fps(frame_count, last_time, fps):
    """FPSを計算して更新する"""
    if time.time() - last_time >= 1:
        current_fps = frame_count
        frame_count = 0
        last_time = time.time()
        return frame_count, last_time, current_fps
    return frame_count, last_time, fps

def process_video(videofile):
    frame_count, last_time_check, current_fps = 0, time.time(), 0
    audio_available = True  # デフォルトで音声ありと仮定

    # ビデオキャプチャを設定
    cap = cv2.VideoCapture(videofile)
    if not cap.isOpened():
        print(f"{Fore.RED}エラー: ビデオファイルを開けませんでした{Style.RESET_ALL}")
        return
        
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"{Fore.CYAN}ビデオ情報: {total_frames}フレーム, {fps}fps{Style.RESET_ALL}")
    
    # 音声と映像の同期準備
    audio_thread = None
    
    # パフォーマンス向上のためのバッファ設定
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
    
    # 直接ビデオファイルから音声を再生
    try:
        audio_thread = threading.Thread(target=play_audio, args=(videofile,))
        audio_thread.start()
    except Exception as e:
        print(f"{Fore.YELLOW}警告: 音声の再生に失敗しました: {e}{Style.RESET_ALL}")
        audio_available = False

    # 動画の本来のフレームレートに合わせた設定
    frame_duration = 1.0 / fps
    current_frame = 0
    start_time = time.time()
    last_display_time = start_time  # last_display_time変数を初期化
    display_count = 0

    # メインループ - リアルタイムフレーム処理
    while True:
        # 現在の時間に基づいて理想のフレーム位置を計算
        elapsed_time = time.time() - start_time
        ideal_frame = int(elapsed_time * fps)
        
        # フレームを読み込む
        ret, frame = cap.read()
        if not ret:
            break
            
        current_frame += 1
        
        # フレームスキップ処理: 大きく遅れている場合はスキップして追いつく
        if current_frame < ideal_frame - 1:
            continue
            
        # 理想的なフレーム表示タイミングを計算
        expected_time = start_time + (current_frame / fps)
        current_time = time.time()
        
        # 早すぎる場合は適切なタイミングまで待機
        if current_time < expected_time:
            sleep_time = expected_time - current_time
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        # 文字アートに変換
        ascii_art = convert_to_ascii_art(frame, DEFAULT_WIDTH)
        
        # 画面表示
        sys.stdout.write('\033[H')
        real_fps = 1.0 / max(0.001, current_time - last_display_time)
        position_info = f"フレーム: {current_frame}/{total_frames}"
        status_text = f"\nFPS:{int(real_fps)} 目標:{int(fps)}" + ("" if audio_available else f" {Fore.RED}[音声なし]{Style.RESET_ALL}")
        sys.stdout.write(ascii_art + status_text)
        
        # FPS計測の更新
        last_display_time = current_time
        
        # CPUリソースを少し解放
        time.sleep(0.001)

    # 後処理
    cap.release()
    if audio_thread and audio_thread.is_alive():
        audio_thread.join()

# メイン実行部分
videofile = input("video path:")
process_video(videofile)
