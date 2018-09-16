#! /usr/bin/python3

    # NAL Unit extractor
import binascii
import math

    # homemade bits
from config import *
from utils import *

"""
    In order to be streamed over a websocket, a h264 feed need to be 
    split into Network Abstraction Layer Units (NALU, NAL unit). In a 
    raw h264 stream, these NALU are delimited by 0x0001 bytes.
    This class efficiently parses the raw h264 feed into NALU and is 
    passed a callback function that pushes parsed NALUs into the 
    websocket.
    
    This is essentially a rewrite of the 'stream-split' nodejs library
    
    ByteArray Documentation : 
        https://docs.python.org/3/library/stdtypes.html#bytearray

    Author : Quentin Bouvet
"""
class StreamSplitter : 
    
    def __init__(self, separator, callback) : 
        
        self.buffersize = 1024*1024*2                           # Internal buffer space
        self.bufferflush = math.floor(self.buffersize * 0.1)    # safety margin within which the buffer is considered full
        self.buffer = bytearray(self.buffersize)
        
        self.offset = 0         # self.buffer is populated up to offset
        self.bodyoffset = 0     # If not 0, then there's a separator in self.buffer[0:bodyoffset]

        self.separator = separator
        self.callback=callback  # Callback function to call when data has been processed
    
    def ack(self, chunk) : 
        stamp("received "+str(len(chunk))+" bytes", name="streamsplitter")
    
    def write(self, chunk):
        debug("received "+str(len(chunk))+" bytes", name="streamsplitter")
        self.process(chunk)
        
    def process(self, chunk) :
        debug("processing "+str(len(chunk))+" bytes", name="streamsplitter")
        #
        # Make sure self.buffer has enough space, allocate new buffer if needed
        #
        if self.offset + len(chunk) > self.buffersize - self.bufferflush : 
                # compute and replace buffer length
            minimallength = self.buffersize - self.bodyoffset + len(chunk)
            if self.buffersize < minimallength : 
                print("[splitter] increasing buffer size")
                self.buffersize = minimallength
                # create temporary bufferr
            tmp = bytearray(self.buffersize)
                # Copy everything to a secondary buffer, except the nal splitter that is at [0:bodyoffset]
            tmp[0:] = self.buffer[self.bodyoffset:]
                # replace the primary buffer and update offset values
            self.buffer = tmp
            self.offset = self.offset - self.bodyoffset
            self.bodyoffset = 0
        #
        # Copy chunk data into local buffer
        #
        self.buffer[self.offset:] = chunk
        #
        # Loop over data 
        #
        i = self.offset + len(chunk)
        start, stop = (i, i)
        while True : 
            #
            # Define some scope (start,stop), search for separator within scope, break loop if not found
            #
            #start = max(self.bodyoffset, self.offset-len(self.separator))
            start = max(self.bodyoffset if self.bodyoffset else 0, self.offset-len(self.separator))
                # NOTE : i is the absolute position in buffer and not the relative position in buffer[start:stop] (as opposed to JS)
            i = self.buffer.find(self.separator, start, stop)
            if i == -1 : 
                break
            #
            # Generate / push / callback transformed output
            #
            nalunit = self.buffer[self.bodyoffset:i]
            #print("[Splitter] Found/pushing nal unit : "+str(len(nalunit))+" bytes")
            self.callback(bytes(self.separator + nalunit))
            #
            # Update offsets
            #
            self.bodyoffset = i + len(self.separator)
        self.offset = self.offset + len(chunk)

