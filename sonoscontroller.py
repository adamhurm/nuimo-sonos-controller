import soco
from nuimo import GestureEvent, Gesture

zone_list = list(soco.discover())

def handle_event(event):
    if event.gesture == Gesture.ROTATION:
        for zone in zone_list:
            zone.volume += event.value/50
            print("Volume: " + str(zone.volume) + " [" + zone.player_name + "]")
        #print("Rotated " + str(event.value) + ", Volume adjusted volume by " +str(event.value/50))
