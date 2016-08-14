#!/usr/bin/env python3

import json
import sys
import time
import threading
import mlogger as log
from commander import *
from urllib import request, parse
from qqrobot import QQClient, QQHandler
from threading import Thread

class MsgHandler(QQHandler):
    def on_group_message(self, gid, uin, msg):
        group = self.get_group_info(gid)
        user = group['members'][uin]
        log.r(group['name'], user['nick'] + '@' + str(gid) + ': ' + msg, cmdr=c)

if __name__=='__main__':
    class QQCmd(Command):
        # def do_echo(self, *args):
        #     '''echo - Just echos all arguments'''
        #     return ' '.join(args)
        # def do_raise(self, *args):
        #     raise Exception('Some Error')
        def do_send(self, *args):
            qqcli.send_group_message(int(args[0]), args[1])
            log.s(qqcli.get_group_info(int(args[0]))['name'], qqcli.get_self_info()['nick'] + '@' + args[0] + ': ' + args[1], cmdr=c)
        
    c=Commander('QQ For Command Line 0.01', cmd_cb=QQCmd())

    qqcli = QQClient(c)
    msghd = MsgHandler()
    qqcli.load_veri(sys.argv[1])
    qqcli.login(get_info=False)
    qqcli.add_handler(msghd)
    qqcli.listen()
    
    #Test asynch output -  e.g. comming from different thread
    #import time
    #def run():
    #    while True:
    #        time.sleep(1)
    #        c.output('Tick', 'green')
    #t=Thread(target=run)
    #t.daemon=True
    #t.start()
    
    #start main loop
    c.loop()
