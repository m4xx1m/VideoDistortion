from datetime import datetime
from time import sleep
import os
import cv2
import sys
import shutil

code_start = datetime.now()

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0]))) # changing dir to dir with main.py

if os.path.exists('IM') or os.path.exists('IM'):
    print('Output folders ("IM" or "DONE" already exist on folder with script')
    answdel = input('\nDelete this folders? (distorting can work with bugs) [Y/n] ')
    if not answdel or answdel == 'Y' or answdel == 'y':
        if os.path.exists('IM'):
            try:
                shutil.rmtree('IM')
            except:
                print(f'Error deleting path "IM"')
                exit()

        if os.path.exists('DONE'):
            try:
                shutil.rmtree('DONE')
            except:
                print(f'Error deleting path "DONE"')
                exit()

res = input('Please enter render resolution (stock 640x360): ')

video_name = input('Please enter video name (from folder with script or enter path to video): ').replace('~', os.getenv("HOME"))

sansw = input('Are you need to trim video [Y/n] ')

if not sansw or sansw == 'Y' or sansw == 'y':
    ss = input('Trim Start [Only integer (Seconds)] ')
    t = input('Trim duration (video diration = diration from Start + (your value)) [Only integer (Seconds)] [recommend >3 secs] ')
    if not ss.isdigit() or not t.isdigit():
        print('Only integer')
        exit()
    ffmpeg_time_param = f'-ss {ss} -t {t}'
else:
    ffmpeg_time_param = ''
print()

if not res:
    res = '640x360'

if not os.path.exists(video_name):
    print('Video name is incorrect')
    exit()

if 'IM' not in os.listdir():
    os.system('mkdir IM')

if 'DONE' not in os.listdir():
    os.system('mkdir DONE')

fps = cv2.VideoCapture(video_name).get(cv2.CAP_PROP_FPS) # getting FPS

os.system(f'ffmpeg -hide_banner -y {ffmpeg_time_param} -i {video_name} -s {res} -q:v 1 "IM/%d.jpg"') # video cutting
print()
os.system(f'ffmpeg -hide_banner -y {ffmpeg_time_param} -i {video_name} sound.mp3') # getting sound from video

IM = os.listdir('IM') # getting images from dir

print()

for i in range(len(IM)):
    start = datetime.now() # time for distorting one frame
    image = IM[i] 
    prc = i / (len(IM) / 100) # procent of progress
    os.system(f"convert IM/{image} -liquid-rescale 40x40%! -resize 1920x1080 DONE/{image}") # distorting
    print(f'\rDistorting frame {image} [{int(prc)}%] | One frame: {(datetime.now() - start).microseconds / 1000} ms',
          end='', flush=True)

print()

os.system(f'ffmpeg -y -hide_banner -r {fps} {ffmpeg_time_param} -i "DONE/%d.jpg" -i sound.mp3 -s {res} -c:v libx264 -preset fast -strict -2 -map 0:v:0 -map 1:0 out.mp4')

process_time = (datetime.now() - code_start).seconds
process_mins = int(str((process_time) / 60).split(".")[0])
process_seconds = process_time - (60 * process_mins)

print(f'Processing took {process_mins} min {process_seconds} seconds')
