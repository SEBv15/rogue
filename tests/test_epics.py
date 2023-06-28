#!/usr/bin/env python3
#-----------------------------------------------------------------------------
# This file is part of the rogue software platform. It is subject to
# the license terms in the LICENSE.txt file found in the top-level directory
# of this distribution and at:
#    https://confluence.slac.stanford.edu/display/ppareg/LICENSE.html.
# No part of the rogue software platform, including this file, may be
# copied, modified, propagated, or distributed except according to the terms
# contained in the LICENSE.txt file.
#-----------------------------------------------------------------------------

import pyrogue
import time
import pyrogue.protocols.epicsV4
from p4p.client.thread import Context

epics_prefix='test_ioc'

class myDevice(pyrogue.Device):
    def __init__(self, name="myDevice", description='My device', **kargs):
        super().__init__(name=name, description=description, **kargs)

        self.add(pyrogue.LocalVariable(
            name='var',
            value=0,
            mode='RW'))

        self.add(pyrogue.LocalVariable(
            name='var_float',
            value=0.0,
            mode='RW'))

class LocalRoot(pyrogue.Root):
    def __init__(self):
        pyrogue.Root.__init__(self, name='LocalRoot', description='Local root')
        my_device=myDevice()
        self.add(my_device)

class LocalRootWithEpics(LocalRoot):
    def __init__(self, use_map=False):
        LocalRoot.__init__(self)

        if use_map:
            # PV map
            pv_map = {
                'LocalRoot.myDevice.var'       : epics_prefix+':LocalRoot:myDevice:var',
                'LocalRoot.myDevice.var_float' : epics_prefix+':LocalRoot:myDevice:var_float',
            }
        else:
            pv_map=None

        self.epics = pyrogue.protocols.epicsV4.EpicsPvServer(
            base      = epics_prefix,
            root      = self,
            pvMap     = pv_map,
            incGroups = None,
            excGroups = None,
        )
        self.addProtocol(self.epics)

def test_local_root():
    """
    Test Epics Server
    """
    # Test both autogeneration and mapping of PV names
    pv_map_states = [False, True]

    # setup the P4P client
    # https://mdavidsaver.github.io/p4p/client.html#usage
    print( Context.providers() )
    ctxt = Context('pva')

    for s in pv_map_states:
        with LocalRootWithEpics(use_map=s) as root:
            time.sleep(1)

            # Device EPICS PV name prefix
            device_epics_prefix=epics_prefix+':LocalRoot:myDevice'

            # Test dump method
            root.epics.dump()

            # Test list method
            root.epics.list()
            time.sleep(1)

            # Test RW a variable holding an scalar value
            pv_name=device_epics_prefix+':var'
            test_value=314
            ctxt.put(pv_name, test_value)
            time.sleep(1)
            test_result=ctxt.get(pv_name)
            if test_result != test_value:
                raise AssertionError('pv_name={}: test_value={}; test_result={}'.format(pv_name, test_value, test_result))

            # Test RW a variable holding a float value
            pv_name=device_epics_prefix+':var_float'
            test_value=5.67
            ctxt.put(pv_name, test_value)
            time.sleep(1)
            test_result=round(ctxt.get(pv_name),2)
            if test_result != test_value:
                raise AssertionError('pvStates={} pv_name={}: test_value={}; test_result={}'.format(s, pv_name, test_value, test_result))

        # Allow epics client to reset
        time.sleep(5)

if __name__ == "__main__":
    test_local_root()
