#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Title      : PyRogue PyDM data plugin
#-----------------------------------------------------------------------------
# File       : pyrogue/pydm/data_plugins/rogue_plugin.py
# Created    : 2019-09-18
#-----------------------------------------------------------------------------
# This file is part of the rogue software platform. It is subject to 
# the license terms in the LICENSE.txt file found in the top-level directory 
# of this distribution and at: 
#    https://confluence.slac.stanford.edu/display/ppareg/LICENSE.html. 
# No part of the rogue software platform, including this file, may be 
# copied, modified, propagated, or distributed except according to the terms 
# contained in the LICENSE.txt file.
#-----------------------------------------------------------------------------
import logging
import numpy as np
import os

from pydm.data_plugins.plugin import PyDMPlugin, PyDMConnection
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication
from pydm import utilities

import pyrogue
from pyrogue.interfaces import VirtualClient


logger = logging.getLogger(__name__)

AlarmToInt = {'None':0, 'Good':0, 'AlarmMinor':1, 'AlarmMajor':2}

def parseAddress(address):
    # "rogue://index/<path>/<disp>"
    # or
    # "rogue://host:port/<path>/<disp>"
    envList = os.getenv('ROGUE_SERVERS')

    if envList is None:
        alist = ['localhost:9099']
    else:
        alist = envList.split(',')

    if address[0:8] == 'rogue://':
        address = address[8:]

    data = address.split("/")

    if ":" in data[0]:
        data_server = data[0].split(":")
    else:
        data_server = alist[int(data[0])].split(":")

    host = data_server[0]
    port = int(data_server[1])
    path = data[1]
    disp = (len(data) > 2) and (data[2] == 'True')

    return (host,port,path,disp)


class RogueConnection(PyDMConnection):

    def __init__(self, channel, address, protocol=None, parent=None):
        super(RogueConnection, self).__init__(channel, address, protocol, parent)

        #print("Adding connection channel={}, address={}".format(channel,address))

        self.app = QApplication.instance()

        self._host, self._port, self._path, self._disp = parseAddress(address)

        self._cmd  = False
        self._int  = False
        self._node = None
        self._enum = None

        if utilities.is_pydm_app():
            self._client = pyrogue.interfaces.VirtualClient(self._host, self._port)
            self._node   = self._client.root.getNode(self._path)
            self.add_listener(channel)
            print("New rogue channel: {}".format(channel))
            self.connection_state_signal.emit(True)

        if self._node is not None and not self._node.isinstance(pyrogue.Device):

            # Command
            if self._node.isinstance(pyrogue.BaseCommand):
                self.write_access_signal.emit(True)
                self._cmd = True
            else:
                self.write_access_signal.emit(self._node.mode=='RW')

            self._node.addListener(self._updateVariable)

            if self._node.units is not None:
                self.unit_signal.emit(self._node.units)

            if self._node.minimum is not None and self._node.maximum is not None:
                self.upper_ctrl_limit_signal.emit(self._node.maximum)
                self.lower_ctrl_limit_signal.emit(self._node.minimum)

            if self._node.disp == 'enum' and self._node.enum is not None and self._node.mode != 'RO':
                self._enum = list(self._node.enum.values())
                self.enum_strings_signal.emit(tuple(self._enum))

            elif 'Int' in self._node.typeStr or self._node.typeStr == 'int':
                self._int = True

            self.prec_signal.emit(self._node.precision)

            self._updateVariable(self._node.path,self._node.getVariableValue(read=False))


    def _updateVariable(self,path,varValue):
        if self._disp:
            self.new_value_signal[str].emit(varValue.valueDisp)
        elif self._enum is not None:
            self.new_value_signal[int].emit(self._enum.index(varValue.valueDisp))
        else:
            self.new_value_signal[type(varValue.value)].emit(varValue.value)

        self.new_severity_signal.emit(AlarmToInt[varValue.severity])


    @pyqtSlot(int)
    @pyqtSlot(float)
    @pyqtSlot(str)
    @pyqtSlot(np.ndarray)
    def put_value(self, new_value):
        if self._node is None:
            return
        try:

            if self._enum is not None:
                val = self._enum[new_value]
            elif self._int:
                val = int(new_value)
            else:
                val = new_value

            if self._cmd:
                self._node.__call__(val)
            else:
                self._node.setDisp(val)
        except:
            logger.error("Unable to put %s to %s.  Exception: %s", new_val, self.address, str(e))


    def add_listener(self, channel):
        super(RogueConnection, self).add_listener(channel)

        # If the channel is used for writing to PVs, hook it up to the 'put' methods.
        if channel.value_signal is not None:
            try:
                channel.value_signal[str].connect(self.put_value, Qt.QueuedConnection)
            except KeyError:
                pass
            try:
                channel.value_signal[int].connect(self.put_value, Qt.QueuedConnection)
            except KeyError:
                pass
            try:
                channel.value_signal[float].connect(self.put_value, Qt.QueuedConnection)
            except KeyError:
                pass
            try:
                channel.value_signal[np.ndarray].connect(self.put_value, Qt.QueuedConnection)
            except KeyError:
                pass

    def remove_listener(self, channel, destroying):
        #if channel.value_signal is not None:
        #    #try:
        #    #    channel.value_signal[str].disconnect(self.put_value)
        #    #except KeyError:
        #    #    pass
        #    try:
        #        channel.value_signal[int].disconnect(self.put_value)
        #    except KeyError:
        #        pass
        #    try:
        #        channel.value_signal[float].disconnect(self.put_value)
        #    except KeyError:
        #        pass
        #    try:
        #        channel.value_signal[np.ndarray].disconnect(self.put_value)
        #    except KeyError:
        #        pass

        #super(RogueConnection, self).remove_listener(channel)
        pass

    def close(self):
        pass

class RoguePlugin(PyDMPlugin):
    protocol = "rogue"
    connection_class = RogueConnection

