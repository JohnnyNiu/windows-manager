#!/usr/bin/env python

import os.path
import string
import subprocess
import sys
import logging

logger = logging.getLogger('windows-manager')
hdlr = logging.FileHandler('/var/tmp/windows-manager.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)


TO_ROTOATE_STR=sys.argv[1]

wmctrl_columns = {'id': 0, 'desktop': 1, 'wm_class': 2, 'host': 3, 'title': 4}
wmctrl_argument = ['wmctrl', '-l', '-x']

proc = subprocess.Popen(wmctrl_argument, stdout=subprocess.PIPE, shell=False)
(out, err) = proc.communicate()
all_windows_str_array =  string.split(out, '\n')

to_rotate_win_ids = []

def get_current_win_id():
    proc = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE, shell=False)
    (out,err) = proc.communicate()
    hex_id = string.split(out)[4][2:]
    #different id format between wmctrl and xprop: eg: 0x03a00041 vs 0x3a00041
    return '0x' + hex_id.zfill(8)

for i, window_str in enumerate(all_windows_str_array):
    if window_str == '':
        continue

    window_data = string.split(window_str, maxsplit=4)
    win_id = window_data[wmctrl_columns['id']]
    win_desktop = window_data[wmctrl_columns['desktop']]
    win_class = window_data[wmctrl_columns['wm_class']]
    win_title = window_data[wmctrl_columns['title']]

    if TO_ROTOATE_STR in win_class:
        to_rotate_win_ids.append(win_id)

next_win_id = ''

if len(to_rotate_win_ids)>1:
    current_win_id = get_current_win_id()
    print "current win id: "+ current_win_id
    print to_rotate_win_ids
    if(current_win_id in to_rotate_win_ids):
        index = to_rotate_win_ids.index(current_win_id)
        if index == len(to_rotate_win_ids) - 1:
            next_win_id = to_rotate_win_ids[0]
        else:
            next_win_id = to_rotate_win_ids[index+1]
    else:
        next_win_id = to_rotate_win_ids[0]

if next_win_id !='':
    print("going to active: ", next_win_id)
    subprocess.call(['wmctrl', '-ia', next_win_id])