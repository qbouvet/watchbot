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
    # general
dcim="/opt/dcim"
CAM_WARMUP_TIME=0.2
    # Photo
RES_PHOTO=(1296, 972)
PHOTO_QUALITY = 25
    # Video
RES_VIDEO=(1296, 972) 
CAM_FPS = 12
CAM_QUALITY = 35

    # Telegram settings
TGTOKEN='674761733:AAHF_pBnumgdXRR1SKe6psQLi1cmWu_AAd0'
PHOTO_SEND_TIMEOUT=30

    # Webserver settings
PORT=8384
WS_PING_INTERVAL=5
WS_NB_PING_TIMEOUT=12
stream_separator = bytearray.fromhex('00000001')
STREAM_SEPARATOR = bytearray.fromhex('00000001')
STATIC_WEB_RESSOURCES = os.path.join(os.path.dirname(__file__), "static")

    # 
CAMERA_WRAPPER_BUFFER_SIZE = 1024 * 100
