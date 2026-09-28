import time
import subprocess

BROWSER_APP = "Google Chrome"
def send_key(key_code):
    script = f'''
    tell application "{BROWSER_APP}" to activate
    delay 0.1
    tell application "System Events" to key code {key_code}
    '''
    subprocess.run(["osascript", "-e", script])


def send_shift_key(letter):
    script = f'''
    tell application "{BROWSER_APP}" to activate
    delay 0.1
    tell application "System Events" to keystroke "{letter}" using {{shift down}}
    '''
    subprocess.run(["osascript", "-e", script])# change to "Safari" if that's what you use
last_gesture = None
last_action_time = 0
COOLDOWN = 1.0   # seconds between triggered actions


def classify(fingers):
    """Turn a [0,1,1,0,0]-style list into a gesture name."""
    if fingers == [0, 0, 0, 0, 0]:
        return "fist"
    if fingers == [0, 1, 1, 0, 0]:
        return "peace"
    if fingers == [0, 1, 0, 0, 0]:
        return "point"
    if fingers == [1, 1, 1, 1, 1]:
        return "open"
    return "unknown"


def set_mac_volume(pct):
    pct = max(0, min(100, int(pct)))
    subprocess.run(["osascript", "-e", f"set volume output volume {pct}"])


def set_play():
    send_key(49)   # spacebar


def set_pause():
    send_key(49)   # spacebar (YouTube uses space to toggle both ways)


def trigger(gesture):
    global last_gesture, last_action_time
    now = time.time()

    if gesture == last_gesture:
        return
    if now - last_action_time < COOLDOWN:
        return

    if gesture == "fist":
        print("Action: Play")
        set_play()
    elif gesture == "open":
        print("Action: Pause")
        set_pause()
    elif gesture == "peace":
        print("Action: Next video")
        send_shift_key("n")
    elif gesture == "point":
        print("Action: Previous video")
        send_shift_key("p")

    last_gesture = gesture
    last_action_time = now

last_volume_time = 0
VOLUME_INTERVAL = 0.15   # only update volume every 0.15 sec, not every frame

def update_volume_from_distance(distance, min_dist=25, max_dist=220):
    """Map a pixel distance to 0-100 volume and set it, throttled."""
    global last_volume_time
    now = time.time()
    if now - last_volume_time < VOLUME_INTERVAL:
        return None

    pct = (distance - min_dist) / (max_dist - min_dist) * 100
    pct = max(0, min(100, pct))
    set_mac_volume(pct)
    last_volume_time = now
    return pct