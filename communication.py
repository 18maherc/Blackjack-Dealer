import serial
import time


class Move():
    def __init__(self):
        # Open grbl serial port, 'COM13' will need replaced with the corresponding RPi port`
        self.s = serial.Serial('COM3', 115200)
        # Wake up grbl
        self.s.write(str.encode('\r\n\r\n'))
        time.sleep(2)   # Wait for grbl to initialize
        self.s.flushInput()  # Flush startup text in serial input

    def draw(self, c):
        zoff = -4.7 - (2*c/52)
        zoff = round(zoff,2)
        f = ["G1X125Y0Z0F5000", "G04P0", "S1000M03", "G04P0", f"G1X125Y0Z{zoff}F100", "G04P0", "G04P2", "G04P0",
             "G1X125Y0Z0F200", "G04P0", "G1X0Y0Z0F5000", "G04P0", "M05", "G04P0", "G04P2", "G04P0"]
        # Stream g-code to grbl
        for line in f:
            l = line.strip()  # Strip all EOL characters for consistency
            print('Sending: ' + l)
            self.s.write(str.encode(l + '\n'))  # Send g-code block to grbl
            grbl_out = self.s.readline()  # Wait for grbl response with carriage return
            print(' : ' + bytes.decode(grbl_out.strip()))
        print('Stream Complete')

    # s is the serial variable
    # coord is the location the card needs to be placed; a list consisting of 2 values [x,y]
    # dealer is only invoked on the deal -> no flipping
    # frate = feedrate, speed at which the move is executed
    def place(self, coord2, coord1=[0, 0], dealer=False, frate=10000):
        f = [f"G01X{coord1[0]}Y{coord1[1]}Z0F{frate}", "M03",
             f"G1X{coord1[0]}Y{coord1[1]}Z-6.7F100", "G04P2", f"G01X{coord1[0]}Y{coord1[1]}Z0F200"]
#         if dealer:
#             f = ["G1X0Y0Z0F5000", "M03",
#                  "G1X0Y0Z-6.7F100", "G04P2", "G1X0Y0Z0F200"]
#         else:
#             f = ["G1X0Y0Z0F5000", "M03",
#                  "G1X0Y0Z-6.7F100", "G04P2", "G1X0Y0Z0F200"]
# #             f = ["flip", "unflip", "flipped", "M03",
# #                  "flipped + z", "G04P2", "flipped"]
        d = [f"G01X{coord2[0]}Y{coord2[1]}Z0F{frate}", "M05", "G04P2", "G1X125Y0Z0F5000"]
        f.extend(d)

        # Stream g-code to grbl
        for line in f:
            l = line.strip()  # Strip all EOL characters for consistency
            print('Sending: ' + l)
            self.s.write(str.encode(l + '\n'))  # Send g-code block to grbl
            grbl_out = self.s.readline()  # Wait for grbl response with carriage return
            print(' : ' + bytes.decode(grbl_out.strip()))
        print('Stream Complete')

    # s is the serial variable
    # c is a stack of every location a card has been placed; each entry contains a list [x,y]
    def discard(self, stack, frate=10000):
        for c in stack:
            f = [f"G01X{c[0]}Y{c[1]}Z0F{frate}","S1000M03",f"G01X{c[0]}Y{c[1]}Z-6.7F100\n","G04P2",f"G01X{c[0]}Y{c[1]}Z0F200","G1X250Y0Z0\n","M05","G04P2"]
            for line in f:
                l = line.strip()  # Strip all EOL characters for consistency
                print('Sending: ' + l)
                self.s.write(str.encode(l + '\n'))  # Send g-code block to grbl
                grbl_out = self.s.readline()  # Wait for grbl response with carriage return
                print(' : ' + bytes.decode(grbl_out.strip()))
            print('Stream Complete')

    def setG(self):
        f = ["$1=255", "$100=40", "$101=40",
             "$102=100", "$110=5000", "$111=5000", "$120=100", "$121=100", "$122=4"]
        # Stream g-code to grbl
        for line in f:
            l = line.strip()  # Strip all EOL characters for consistency
            print('Sending: ' + l)
            self.s.write(str.encode(l + '\n'))  # Send g-code block to grbl
            grbl_out = self.s.readline()  # Wait for grbl response with carriage return
            print(' : ' + bytes.decode(grbl_out.strip()))
        print('Stream Complete')
