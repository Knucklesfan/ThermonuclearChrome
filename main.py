import signal
import time
import pychromecast
import threading

chromecasts, browser = pychromecast.get_chromecasts(tries=1, retry_wait=1, timeout=1)
thread_list = []

def handler(sig, frame):
    for cast in chromecasts:
        cast.quit_app()
    exit(0)




def chromecastHandler(cast):
    print ('Handling ' + str(cast.cast_info.friendly_name) + '\n')
    cast.wait()
    mc = cast.media_controller
    mc.play_media('https://ia601602.us.archive.org/11/items/Rick_Astley_Never_Gonna_Give_You_Up/Rick_Astley_Never_Gonna_Give_You_Up.mp4', 'video/mp4')
    mc.block_until_active()
    lasttime = float(0.0)
    duration = float(1.0)
    while True:
        time.sleep(0.1)
        mc.update_status()

        if cast.status.app_id !='CC1AD845': # default cast id btw
            cast.wait()
            mc = cast.media_controller
            mc.play_media(
                'https://ia601602.us.archive.org/11/items/Rick_Astley_Never_Gonna_Give_You_Up/Rick_Astley_Never_Gonna_Give_You_Up.mp4',
                'video/mp4', current_time=lasttime)
            mc.block_until_active()
        if mc.status.player_state == 'PLAYING':
            lasttime = float(mc.status.current_time)
        if(mc.status.duration != None):
            duration = mc.status.duration
        if mc.status.current_time > duration-1:
            cast.quit_app()
            break

services, browser = pychromecast.discovery.discover_chromecasts()
pychromecast.discovery.stop_discovery(browser)

stop_threads = False

for cast in chromecasts:
    thread = threading.Thread(target=chromecastHandler, args=(cast,))
    thread.daemon = True
    thread_list.append(thread)
    thread.start()

print("Handling Casts... Press CTRL-C")
signal.signal(signal.SIGINT, handler)
while True:
    time.sleep(0.0)