import serial
import time


class Move():
    def __init__(self):
        # Open grbl serial port, 'COM13' will need replaced with the corresponding RPi port
        # ls /dev/ttyACM*
        try:
            self.s = serial.Serial('/dev/ttyACM0', 115200)
        except FileNotFoundError:
            self.s = serial.Serial('/dev/ttyACM1', 115200)
        # Wake up grbl
        self.s.write(str.encode('\r\n\r\n'))
        time.sleep(2)   # Wait for grbl to initialize
        self.s.flushInput()  # Flush startup text in serial input

    def draw(self, c):
        zoff = -4.3 - (2.35*c/52)
        zoff = round(zoff, 2)
        f = ["G1X125Y0Z0F5000", "G04P0", "S1000M03", "G04P0", f"G1X125Y0Z{zoff}F100", "G04P0", "G04P2", "G04P0",
             "G1X125Y0Z0F200", "G04P0", "G1X0Y0Z0F5000", "G04P0", "G1X0Y0Z-4.5F200", "G04P0", "M05", "G04P0", "G04P2", "G04P0"]
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
    def place(self, coord2, coord1=[0, 0], dealer=False, frate=5000):
        f = [f"G01X{coord1[0]}Y{coord1[1]}Z0F{frate}\n", "G04P0", "M03\n", "G04P0",
             f"G1X{coord1[0]}Y{coord1[1]}Z-6.65F100\n", "G04P0", "G04P2\n", "G04P0", f"G01X{coord1[0]}Y{coord1[1]}Z0F{200}\n", "G04P0"]
#         if dealer:
#             f = ["G1X0Y0Z0F5000\n", "M03\n",
#                  "G1X0Y0Z-7.0F100\n", "G04P2\n", "G1X0Y0Z0F200\n"]
#         else:
#             f = ["G1X0Y0Z0F5000\n", "M03\n",
#                  "G1X0Y0Z-7.0F100\n", "G04P2\n", "G1X0Y0Z0F200\n"]
# #             f = ["flip\n", "unflip\n", "flipped\n", "M03\n",
# #                  "flipped + z\n", "G04P2\n", "flipped\n"]
        d0 = f"G01X{coord2[0]}Y{coord2[1]}Z0F{frate}\n"
        d1 = f"G01X{coord2[0]}Y{coord2[1]}Z-4.5F100\nM05\n"
        p1 = "G04P2\n"
        d2 = "G1X125Y0Z0F5000\n"
        f.extend([d0, d1, p1, d2])

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
    def discard(self, stack, frate=5000):
        for c in stack:
            f = [f"G01X{c[0]}Y{c[1]}Z0F{frate}\n", "S1000M03\n", f"G01X{c[0]}Y{c[1]}Z-6.65F100\n",
                 "G04P2\n", f"G01X{c[0]}Y{c[1]}Z0F{frate}\n", "G1X250Y0Z0\n", "M05\n", "G04P2\n", f"G01X0Y0Z0F{frate}"]
#             von = "S1000M03\n"
#             d1 = f"G01X{c[0]}Y{c[1]}Z-7.0F100\nG04P2\n"
#             d2 = "G1X250Y0Z0\nM05\nG04P2\n"
#             f.extend([von, d1, f, d2])
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
