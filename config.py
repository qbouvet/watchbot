#! /usr/bin/python3

import os

"""
    Configuration variables for the whole application

	Author : Quentin Bouvet
"""

    # Enable printing debug information
DEBUG = True

    # PIR sensor GPIO configuration
PIR_pin=11

    # Camera settings and file storage
dcim="/opt/dcim"
CAM_WARMUP_TIME=0.6
RES_PHOTO=(2592, 1944)
RES_VIDEO=(1296, 972) 
#RES_VIDEO=(640, 480) 
CAM_FPS = 12
CAM_QUALITY = 25

    # Telegram settings
TGTOKEN='674761733:AAHF_pBnumgdXRR1SKe6psQLi1cmWu_AAd0'

    # Webserver settings
PORT=8384
WS_PING_INTERVAL=5
WS_NB_PING_TIMEOUT=12
stream_separator = bytearray.fromhex('00000001')
STREAM_SEPARATOR = bytearray.fromhex('00000001')
STATIC_WEB_RESSOURCES = os.path.join(os.path.dirname(__file__), "static")

    # 
CAMERA_WRAPPER_BUFFER_SIZE = 1024 * 100
