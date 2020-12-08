from datetime import datetime
from time import sleep
import os
import sys
import shutil

code_start = datetime.now()

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

if os.path.exists('IM') or os.path.exists('IM'):
    print('Output folders ("IM" or "DONE" already exist on folder with script')
    answdel = input('\nDelete this folders? (distorting can work with bugs) [Y/n]')
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
video_name = input('Please enter video name (from folder with script or enter FULL path): ')
sansw = input('Are you need to trim video [Y/n]')
if not sansw or sansw == 'Y' or sansw == 'y':
    ss = input('Trim Start [Only integer (Seconds)]')
    t = input('Trim duration (from Start to ...) [Only integer (Seconds)]')
    if not ss.isdigit() or not t.isdigit():
        print('CYKA ONLY INTEGER')
        exit()
    ffmpeg_time_param = f'-ss {ss} -t {t}'
else:
    ffmpeg_time_param = ''
print()

if not res:
    print('resolution is incorrect! Using 640x360')
    res = '640x360'

if not os.path.exists(video_name):
    print('Video name is incorrect')
    exit()

if 'IM' not in os.listdir():
    os.system('mkdir IM')

if 'DONE' not in os.listdir():
    os.system('mkdir DONE')

sleep(1)

os.system(f'ffmpeg -hide_banner -y {ffmpeg_time_param} -i {video_name} -s {res} -q:v 1 "IM/%d.jpg"')
os.system(f'ffmpeg -hide_banner -y {ffmpeg_time_param} -i {video_name} sound.mp3')

IM = os.listdir('IM')

print()

for i in range(len(IM)):
    start = datetime.now()
    image = IM[i]
    prc = i / (len(IM) / 100)
    os.system(f"convert IM/{image} -liquid-rescale 40x40%! -resize 1920x1080 DONE/{image}")
    print(f'\rDistorting frame {image} [{int(prc)}%] | One frame: {(datetime.now() - start).microseconds / 1000} ms',
          end='', flush=True)

print()

os.system(f'ffmpeg -y -hide_banner -r 30 {ffmpeg_time_param} -i "DONE/%d.jpg" -i sound.mp3 -s {res} -c:v libx264'
          f' -preset fast -strict -2 -map 0:v:0 -map 1:0 out.mp4')

process_time = (datetime.now() - code_start).seconds
process_mins = int(str((process_time) / 60).split(".")[0])
process_seconds = process_time - (60 * process_mins)

print(f'Processing took {process_mins} min {process_seconds} seconds')
