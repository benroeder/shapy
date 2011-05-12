import unittest
import socket
from shapy.framework.netlink.constants import *
from shapy.framework.netlink.message import *
from shapy.framework.netlink.tc import *
from shapy.framework.netlink.connection import Connection

from tests.mixins import TeardownMixin

class TestQdisc(unittest.TestCase, TeardownMixin):
    def setUp(self):
        self.if_index = 1   # lo
        self.conn = Connection()
        try:
            self.delete_root_qdisc()
        except OSError:
            pass
    
    def test_add_pfifo_qdisc(self):
        handle = 0x1 << 16 # | 0x1   # major:minor
        tcm = tcmsg(socket.AF_UNSPEC, self.if_index, handle, TC_H_ROOT, 0,
                   [Attr(TCA_KIND, 'pfifo\0')])
        
        msg = Message(type=RTM_NEWQDISC,
                      flags=NLM_F_EXCL | NLM_F_CREATE | NLM_F_REQUEST | NLM_F_ACK,
                      service_template=tcm)

        self.conn.send(msg)
    
        response = self.conn.recv()
        print response
        
        print self.delete_root_qdisc()
        
    def test_add_htb_qdisc(self):
        from shapy.framework.netlink.htb import HTBQdiscAttr
        handle = 0x1 << 16 # | 0x1   # major:minor
        tcm = tcmsg(socket.AF_UNSPEC, self.if_index, handle, TC_H_ROOT, 0,
                   [Attr(TCA_KIND, 'htb\0'), HTBQdiscAttr(defcls=0x1ff)])
        
        msg = Message(type=RTM_NEWQDISC,
                      flags=NLM_F_EXCL | NLM_F_CREATE | NLM_F_REQUEST | NLM_F_ACK,
                      service_template=tcm)
        
        self.conn.send(msg)
        print self.conn.recv()
        
        print self.delete_root_qdisc()
        