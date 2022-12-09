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

    def draw(self, c, frate=10000):
        zoff = -4.7 - (1.3*c/52)
        zoff = round(zoff, 1)
        f = ["$1=255", f"G1X125Y0Z0F{frate}", "G04P0", "S1000M03", "G04P0", f"G1X125Y0Z{zoff}F200", "G04P0", "G04P1", "G04P0",
             "G1X125Y0Z0F200", "G04P0", f"G1X0Y0Z0F{frate}", "G04P0", "G0X0Y0Z-4.5", "G04P0", "M05", "G04P0", "G04P2", "G04P0", "G0X0Y0Z0", "G04P0"]
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

    def place(self, coord2, coord1=[0, 0], frate=10000):
        coord1[1] = coord1[1]
        coord2[1] = coord2[1]
        f = [f"G01X{coord1[0]}Y{coord1[1]}Z0F{frate}", "S1000M03",
             f"G1X{coord1[0]}Y{coord1[1]}Z-6.0F200", "G04P1", f"G0X{coord1[0]}Y{coord1[1]}Z0",
             f"G01X{coord2[0]}Y{coord2[1]}Z0F{frate}", f"G0X{coord2[0]}Y{coord2[1]}Z-4.5",
             "M05", "G04P1", f"G0X{coord2[0]}Y{coord2[1]}Z0", f"G1X125Y0Z0F{frate}"]
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
            c[1] = c[1]
            f = [f"G01X{c[0]}Y{c[1]}Z0F{frate}", "S1000M03", f"G01X{c[0]}Y{c[1]}Z-6.0F200",
                 "G04P2", f"G01X{c[0]}Y{c[1]}Z0F200", "G0X250Y-12Z0", "M05", "G04P2"]
            for line in f:
                l = line.strip()  # Strip all EOL characters for consistency
                print('Sending: ' + l)
                self.s.write(str.encode(l + '\n'))  # Send g-code block to grbl
                grbl_out = self.s.readline()  # Wait for grbl response with carriage return
                print(' : ' + bytes.decode(grbl_out.strip()))
        l = "G0X0Y0Z0"
        print('Sending: ' + l)
        self.s.write(str.encode(l + '\n'))  # Send g-code block to grbl
        grbl_out = self.s.readline()  # Wait for grbl response with carriage return
        print(' : ' + bytes.decode(grbl_out.strip()))
        print('Stream Complete')

    def setG(self):
        f = ["$1=255", "$100=40", "$101=40",
             "$102=100", "$110=10000", "$111=10000", "$120=300", "$121=300", "$122=4"]
        # Stream g-code to grbl
        for line in f:
            l = line.strip()  # Strip all EOL characters for consistency
            print('Sending: ' + l)
            self.s.write(str.encode(l + '\n'))  # Send g-code block to grbl
            grbl_out = self.s.readline()  # Wait for grbl response with carriage return
            print(' : ' + bytes.decode(grbl_out.strip()))
        print('Stream Complete')
