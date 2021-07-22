#!/usr/bin/env python3

import nuimo, soco

controller_manager = None
sonos_zone_list = list(soco.discover())

class termcolors:
    BOLD = '\033[1m'
    ENDC = '\033[0m'

class ControllerPrintListener(nuimo.ControllerListener):
    """
    An implementation of ``ControllerListener`` that prints each event.
    """
    def __init__(self, controller):
        self.controller = controller

    def started_connecting(self):
        self.print("connecting...")

    def connect_succeeded(self):
        self.print("connected.")
        
        '''
        [insert intro logo for Sonos]
        '''
        matrix = nuimo.LedMatrix(
            "*       *"
            " *     * "
            "  *   *  "
            "   * *   "
            "    *    "
            "   * *   "
            "  *   *  "
            " *     * "
            "*       *"
        )
        self.controller.display_matrix(matrix)

    def connect_failed(self, error):
        self.print("connect failed: " + str(error))

    def started_disconnecting(self):
        self.print("disconnecting...")

    def disconnect_succeeded(self):
        self.print("disconnected.")

    def received_gesture_event(self, event):
        if event.gesture == nuimo.Gesture.ROTATION:
            handle_event(event)
        #self.print("did send gesture event " + str(event))

    def print(self, string):
        print("Nuimo controller " + termcolors.BOLD + self.controller.mac_address + termcolors.ENDC + " " + string)


class ControllerTestListener(ControllerPrintListener):
    def __init__(self, controller, auto_reconnect=False):
        super().__init__(controller)
        self.auto_reconnect = auto_reconnect

    def connect_failed(self, error):
        super().connect_failed(error)
        controller_manager.stop()
        sys.exit(0)

    def disconnect_succeeded(self):
        super().disconnect_succeeded()

        if self.auto_reconnect:
            # Reconnect as soon as Nuimo was disconnected
            print("Disconnected, reconnecting...")
            self.controller.connect()
        else:
            controller_manager.stop()
            sys.exit(0)

    def received_gesture_event(self, event):
        super().received_gesture_event(event)
        self.controller.display_matrix(nuimo.LedMatrix(
            "*        "
            " *       "
            "  *      "
            "   *     "
            "    *    "
            "     *   "
            "      *  "
            "       * "
            "        *"))

def handle_event(event):
    for zone in sonos_zone_list:
        vol = zone.volume
        if (vol == 100 and event.value > 0) or (vol == 0 and event.value < 0) or abs(event.value/50) < 1:
            break #don't send -- volume level will stay the same, so avoid latency
        else:
            if vol + event.value/50 > 85:
                break #set max vol of 85 to avoid blowing out my ears while testing
            zone.volume += event.value/50
            print("Volume: " + str(vol + event.value//50) + " [" + zone.player_name + "]")
        #print("Rotated " + str(event.value) + ", Volume adjusted volume by " +str(event.value/50))

def main():
    controller_manager = nuimo.ControllerManager(adapter_name='hci0')
    controller = nuimo.Controller(mac_address='c1:4c:09:45:fd:c0', manager=controller_manager)
    controller.listener = ControllerTestListener(controller=controller, auto_reconnect=True)
    controller.connect()

    for sonos_zone in sonos_zone_list:
        print("Sonos speaker " + termcolors.BOLD + sonos_zone.player_name + termcolors.ENDC + " identified.")
    
    print("Terminate with Ctrl+C")
    try:
        controller_manager.run()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
