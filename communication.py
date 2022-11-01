import serial
import time


class Move():
    def __init__(self):
        # Open grbl serial port, 'COM13' will need replaced with the corresponding RPi port
        self.s = serial.Serial('COM13', 115200)
        # Wake up grbl
        self.s.write(str.encode('\r\n\r\n'))
        time.sleep(2)   # Wait for grbl to initialize
        self.s.flushInput()  # Flush startup text in serial input

    def draw(self):
        f = ["draw\n", "S1000M03\n", "draw + z\n", "G04P2\n",
             "draw\n", "flipper\n", "M05\n", "flipper + y\n"]
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
    def place(self, coord, dealer=False, frate=400):
        if dealer:
            f = ["flipper\n", "M03\n", "flipper + z\n", "G04P2\n", "flipper\n"]
        else:
            f = ["flip\n", "unflip\n", "flipped\n", "M03\n",
                 "flipped + z\n", "G04P2\n", "flipped\n"]
        d0 = f"G01X{coord[0]}Y{coord[1]}Z0F{frate}\n"
        d1 = "M05\n"
        d2 = "draw\n"
        f.extend([d0, d1, d2])

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
    def discard(self, stack, frate=400):
        for c in stack:
            f = [f"G01X{c[0]}Y{c[1]}Z0F{frate}\n"]
            von = "S1000M03\n"
            d1 = f"G01X{c[0]}Y{c[1]}Z1F30\nG04P2\n"
            d2 = "discard\nM05"
            f.extend([f, von, d1, f, d2])
            for line in f:
                l = line.strip()  # Strip all EOL characters for consistency
                print('Sending: ' + l)
                self.s.write(str.encode(l + '\n'))  # Send g-code block to grbl
                grbl_out = self.s.readline()  # Wait for grbl response with carriage return
                print(' : ' + bytes.decode(grbl_out.strip()))
            print('Stream Complete')

    def setG(self):
        f = ["$1=255", "$100=200", "$101=200",
             "$102=100", "$120=20", "$121=20", "$122=4"]
        # Stream g-code to grbl
        for line in f:
            l = line.strip()  # Strip all EOL characters for consistency
            print('Sending: ' + l)
            self.s.write(str.encode(l + '\n'))  # Send g-code block to grbl
            grbl_out = self.s.readline()  # Wait for grbl response with carriage return
            print(' : ' + bytes.decode(grbl_out.strip()))
        print('Stream Complete')
