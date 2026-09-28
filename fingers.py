TIP_IDS = [4, 8, 12, 16, 20]

def get_fingers_up(landmarks):
    """Returns a list like [0,1,1,0,0] -> thumb down, index up, middle up, ring down, pinky down"""
    fingers = []

    # Thumb: compare tip x against the joint below it (thumb moves sideways, not up/down)
    if landmarks[TIP_IDS[0]].x < landmarks[TIP_IDS[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other four fingers: tip is "up" if it's above the joint two points below it
    for i in range(1, 5):
        if landmarks[TIP_IDS[i]].y < landmarks[TIP_IDS[i] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers