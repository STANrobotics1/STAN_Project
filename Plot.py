import math
import sys
import random
import numpy as np
import serial
import time

# plates
# 1: bottom
# 2: left
# 3: right

PORT = "/dev/ttyACM0"
ser = serial.Serial(PORT, 9600)

class FakeData:

    def __init__(self):
        self.prev_fake_data = 500

    def get(self):
        self.prev_fake_data += random.randrange(-10, 11)
        return self.prev_fake_data

fakes = [FakeData(), FakeData(), FakeData()]

def get_readings():
#    global fakes
#    return [0] + map(lambda x: x.get(), fakes)
    return ser.readline().strip().split()

def reading_to_distance(x):
    if (x <= 0):
         return 0.0
    root = math.sqrt(x)
    return 1000/root

class Graph:
    
    def __init__(self):
        self.verbose = False
        self.distances = []
        # TODO: adjust this based on the time between inputs
        self.distances_max_len = 30 # 20
        self.prev_rms = 1
        self.seconds = time.time()
        
    # Finds the root mean square of the distances array.
    def rms(self):
        if len(self.distances) == 0:
            return None
        return math.sqrt(reduce(lambda a, b: a + b, \
                                [x**2 for x in self.distances]) \
                     / len(self.distances))
        
    # reading: a string representing a raw input value.
    def add_reading(self, reading):
        reading = int(reading)
        ser.flush()
        distance = reading_to_distance(reading)
        self.add_distance(distance)
        if (self.verbose):
            print int(distance), int(self.rms())

    # Adds a new distance reading to the distances array. If 
    # the array has more than the distances_max_len, remove 
    # its first element.
    def add_distance(self, distance):
        self.distances.append(distance)
        if len(self.distances) > self.distances_max_len:
            self.distances.pop(0)   

    def delta(self):
        # Note: I'm attempting to use time.clock() to make the return value 
        # proportional to time, so that fast readings won't cause really 
        # tiny deltas. -Michael
        rms = self.rms()
        seconds = time.time()
        ds = seconds - self.seconds
        
        diff = (rms - self.prev_rms) / self.prev_rms / ds
        self.prev_rms = rms
        self.seconds = seconds
        return diff
        


graph = Graph()
graph2 = Graph()
graph3 = Graph()

def direction(x):
    diff = 0.02
    if x < -diff:
        return '-'
    if x > diff:
        return '+'
    return '='

while True:
    try:
        cur_time, reading, reading2, reading3 = get_readings()
        graph.add_reading(reading)
        graph2.add_reading(reading2)
        graph3.add_reading(reading3)
        print "(%d, %d, %d)" % (graph.rms(), graph2.rms(), graph3.rms())
#        print "(%f, %f, %f)" % (graph.delta(), graph2.delta(), graph3.delta())
#        print (direction(graph.delta()) + direction(graph2.delta()) + direction(graph3.delta()))
    except ValueError as e:
        print "Error: ", str(e)
#    except BaseException as e:
#        print "Error: ", str(e)

