import soco
from nuimo import GestureEvent, Gesture

zone_list = list(soco.discover())

def handle_event(event):
    if event.gesture == Gesture.ROTATION:
        for zone in zone_list:
            if (zone.volume == 100 and event.value > 0) or (zone.volume == 0 and event.value < 0) or abs(event.value) < 1:
                break #don't send -- volume level will stay the same, so avoid latency
            else:
                if zone.volume + event.value/50 > 85:
                    break #set max vol of 85 to avoid blowing out my ears while testing
                zone.volume += event.value/50
                print("Volume: " + str(zone.volume) + " [" + zone.player_name + "]")
        #print("Rotated " + str(event.value) + ", Volume adjusted volume by " +str(event.value/50))
