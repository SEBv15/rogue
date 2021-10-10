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

# Comment added by rherbst for demonstration purposes.
import pyrogue as pr
import pyrogue.interfaces.simulation
import numpy as np

#rogue.Logging.setLevel(rogue.Logging.Warning)
#import logging
#logger = logging.getLogger('pyrogue')
#logger.setLevel(logging.DEBUG)

class ListDevice(pr.Device):

    # Last comment added by rherbst for demonstration.
    def __init__(
            self,
            name             = 'ListDevice',
            description      = 'List Device Test',
            **kwargs):

        super().__init__(
            name        = name,
            description = description,
            **kwargs)

        ##############################
        # Variables
        ##############################

        self.add(pr.RemoteVariable(
            name         = 'UInt32List',
            offset       = 0x0000,
            bitSize      = 32 * 32,
            bitOffset    = 0x0000,
            base         = pr.UInt,
            mode         = 'RW',
            disp         = '{}',
            numValues    = 32,
            valueBits    = 32,
            valueStride  = 32
        ))

        self.add(pr.RemoteVariable(
            name         = 'Int32List',
            offset       = 0x0800,
            bitSize      = 32 * 32,
            bitOffset    = 0x0000,
            base         = pr.Int,
            mode         = 'RW',
            disp         = '{}',
            numValues    = 32,
            valueBits    = 32,
            valueStride  = 32
        ))

        self.add(pr.RemoteVariable(
            name         = 'UInt48List',
            offset       = 0x1000,
            bitSize      = 48 * 32,
            bitOffset    = 0x0000,
            base         = pr.UInt,
            mode         = 'RW',
            disp         = '{}',
            numValues    = 32,
            valueBits    = 48,
            valueStride  = 48
        ))

        self.add(pr.RemoteVariable(
            name         = 'FloatList',
            offset       = 0x2000,
            bitSize      = 32 * 32,
            bitOffset    = 0x0000,
            base         = pr.Float,
            mode         = 'RW',
            disp         = '{}',
            numValues    = 32,
            valueBits    = 32,
            valueStride  = 32
        ))

        self.add(pr.RemoteVariable(
            name         = 'DoubleList',
            offset       = 0x3000,
            bitSize      = 64 * 32,
            bitOffset    = 0x0000,
            base         = pr.Double,
            mode         = 'RW',
            disp         = '{}',
            numValues    = 32,
            valueBits    = 64,
            valueStride  = 64
        ))

        self.add(pr.RemoteVariable(
            name         = 'UInt16List',
            offset       = 0x4000,
            bitSize      = 16 * 32,
            bitOffset    = 0x0000,
            base         = pr.UInt,
            mode         = 'RW',
            disp         = '{}',
            numValues    = 32,
            valueBits    = 16,
            valueStride  = 16
        ))

        self.add(pr.RemoteVariable(
            name         = 'UInt21List',
            offset       = 0x5000,
            bitSize      = 32 * 32,
            bitOffset    = 0x0000,
            base         = pr.UInt,
            mode         = 'RW',
            disp         = '{}',
            numValues    = 32,
            valueBits    = 21,
            valueStride  = 32
        ))

        self.add(pr.RemoteVariable(
            name         = 'BoolList',
            offset       = 0x6000,
            bitSize      = 32,
            bitOffset    = 0x0000,
            base         = pr.Bool,
            mode         = 'RW',
            disp         = '{}',
            numValues    = 32,
            valueBits    = 1,
            valueStride  = 1
        ))

class DummyTree(pr.Root):

    def __init__(self):
        pr.Root.__init__(self,
                         name='dummyTree',
                         description="Dummy tree for example",
                         timeout=2.0,
                         pollEn=False)
                         #serverPort=None)

        # Use a memory space emulator
        sim = pr.interfaces.simulation.MemEmulate()
        self.addInterface(sim)

        self.add(ListDevice(
            offset     = 0,
            memBase    = sim
        ))

def test_memory():

    UInt32ListARaw = [i for i in range(32)]
    Int32ListARaw  = [i for i in range(32)]
    UInt48ListARaw = [i for i in range(32)]
    FloatListARaw  = [i/2 for i in range(32)]
    DoubleListARaw = [i/2 for i in range(32)]
    UInt16ListARaw = [i for i in range(32)]
    UInt21ListARaw = [i for i in range(32)]
    BoolListARaw   = [i%2==0 for i in range(32)]

    UInt32ListA = np.array(UInt32ListARaw,np.uint32)
    Int32ListA  = np.array(Int32ListARaw,np.int32)
    UInt48ListA = np.array(UInt48ListARaw,np.uint64)
    FloatListA  = np.array(FloatListARaw,np.float32)
    DoubleListA = np.array(DoubleListARaw,np.float64)
    UInt16ListA = np.array(UInt16ListARaw,np.uint32)
    UInt21ListA = np.array(UInt21ListARaw,np.uint32)
    BoolListA   = np.array(BoolListARaw,bool)

    UInt32ListB = np.array([i+1 for i in range(32)],np.uint32)
    Int32ListB  = np.array([i+1 for i in range(32)],np.int32)
    UInt48ListB = np.array([i+1 for i in range(32)],np.uint64)
    FloatListB  = np.array([(i+1)/2 for i in range(32)],np.float32)
    DoubleListB = np.array([(i+1)/2 for i in range(32)],np.float64)
    UInt16ListB = np.array([i+1 for i in range(32)],np.uint32)
    UInt21ListB = np.array([i+1 for i in range(32)],np.uint32)
    BoolListB   = np.array([(i+1)%2==0 for i in range(32)],bool)

    with DummyTree() as root:

        root.ListDevice.UInt32List.set(UInt32ListARaw)
        root.ListDevice.Int32List.set(Int32ListARaw)
        root.ListDevice.UInt48List.set(UInt48ListARaw)
        root.ListDevice.FloatList.set(FloatListARaw)
        root.ListDevice.DoubleList.set(DoubleListARaw)
        root.ListDevice.UInt16List.set(UInt16ListARaw)
        root.ListDevice.UInt21List.set(UInt21ListARaw)
        root.ListDevice.BoolList.set(BoolListARaw)

        UInt32ListAA = root.ListDevice.UInt32List.get()
        Int32ListAA  = root.ListDevice.Int32List.get()
        UInt48ListAA = root.ListDevice.UInt48List.get()
        FloatListAA  = root.ListDevice.FloatList.get()
        DoubleListAA = root.ListDevice.DoubleList.get()
        UInt16ListAA = root.ListDevice.UInt16List.get()
        UInt21ListAA = root.ListDevice.UInt21List.get()
        BoolListAA   = root.ListDevice.BoolList.get()

        UInt32ListAB = np.array([0] * 32,np.uint32)
        Int32ListAB  = np.array([0] * 32,np.int32)
        UInt48ListAB = np.array([0] * 32,np.uint64)
        FloatListAB  = np.array([0] * 32,np.float32)
        DoubleListAB = np.array([0] * 32,np.float64)
        UInt16ListAB = np.array([0] * 32,np.uint32)
        UInt21ListAB = np.array([0] * 32,np.uint32)
        BoolListAB   = np.array([0] * 32,bool)

        for i in range(32):
            UInt32ListAB[i] = root.ListDevice.UInt32List.get(index=i)
            Int32ListAB[i]  = root.ListDevice.Int32List.get(index=i)
            UInt48ListAB[i] = root.ListDevice.UInt48List.get(index=i)
            FloatListAB[i]  = root.ListDevice.FloatList.get(index=i)
            DoubleListAB[i] = root.ListDevice.DoubleList.get(index=i)
            UInt16ListAB[i] = root.ListDevice.UInt16List.get(index=i)
            UInt21ListAB[i] = root.ListDevice.UInt21List.get(index=i)
            BoolListAB[i]   = root.ListDevice.BoolList.get(index=i)

        for i in range(32):
            if UInt32ListAA[i] != UInt32ListA[i]:
                raise AssertionError(f'Verification Failure for UInt32ListAA at position {i}')

            if Int32ListAA[i] != Int32ListA[i]:
                raise AssertionError(f'Verification Failure for Int32ListAA at position {i}')

            if UInt48ListAA[i] != UInt48ListA[i]:
                raise AssertionError(f'Verification Failure for UInt48ListAA at position {i}')

            if FloatListAA[i] != FloatListA[i]:
                raise AssertionError(f'Verification Failure for FloatListAA at position {i}')

            if DoubleListAA[i] != DoubleListA[i]:
                raise AssertionError(f'Verification Failure for DoubleListAA at position {i}')

            if UInt16ListAA[i] != UInt16ListA[i]:
                raise AssertionError(f'Verification Failure for UInt16ListAA at position {i}')

            if UInt21ListAA[i] != UInt21ListA[i]:
                raise AssertionError(f'Verification Failure for UInt21ListAA at position {i}')

            if BoolListAA[i] != BoolListA[i]:
                raise AssertionError(f'Verification Failure for BoolListAA at position {i}')

            if UInt32ListAB[i] != UInt32ListA[i]:
                raise AssertionError(f'Verification Failure for UInt32ListAB at position {i}')

            if UInt48ListAB[i] != UInt48ListA[i]:
                raise AssertionError(f'Verification Failure for UInt48ListAB at position {i}')

            if FloatListAB[i] != FloatListA[i]:
                raise AssertionError(f'Verification Failure for FloatListAB at position {i}')

            if DoubleListAB[i] != DoubleListA[i]:
                raise AssertionError(f'Verification Failure for DoubleListAB at position {i}')

            if UInt16ListAB[i] != UInt16ListA[i]:
                raise AssertionError(f'Verification Failure for UInt16ListAB at position {i}')

            if UInt21ListAB[i] != UInt21ListA[i]:
                raise AssertionError(f'Verification Failure for UInt21ListAB at position {i}')

            if BoolListAB[i] != BoolListA[i]:
                raise AssertionError(f'Verification Failure for BoolListAB at position {i}')

        for i in range(32):
            root.ListDevice.UInt32List.set(UInt32ListB[i],index=i)
            root.ListDevice.Int32List.set(Int32ListB[i],index=i)
            root.ListDevice.UInt48List.set(UInt48ListB[i],index=i)
            root.ListDevice.FloatList.set(FloatListB[i],index=i)
            root.ListDevice.DoubleList.set(DoubleListB[i],index=i)
            root.ListDevice.UInt16List.set(UInt16ListB[i],index=i)
            root.ListDevice.UInt21List.set(UInt21ListB[i],index=i)
            root.ListDevice.BoolList.set(BoolListB[i],index=i)

        UInt32ListBA = root.ListDevice.UInt32List.get()
        Int32ListBA  = root.ListDevice.Int32List.get()
        UInt48ListBA = root.ListDevice.UInt48List.get()
        FloatListBA  = root.ListDevice.FloatList.get()
        DoubleListBA = root.ListDevice.DoubleList.get()
        UInt16ListBA = root.ListDevice.UInt16List.get()
        UInt21ListBA = root.ListDevice.UInt21List.get()
        BoolListBA   = root.ListDevice.BoolList.get()

        UInt32ListBB = np.array([0] * 32,np.uint32)
        Int32ListBB  = np.array([0] * 32,np.int32)
        UInt48ListBB = np.array([0] * 32,np.uint64)
        FloatListBB  = np.array([0] * 32,np.float32)
        DoubleListBB = np.array([0] * 32,np.float64)
        UInt16ListBB = np.array([0] * 32,np.uint32)
        UInt21ListBB = np.array([0] * 32,np.uint32)
        BoolListBB   = np.array([0] * 32,bool)

        for i in range(32):
            UInt32ListBB[i] = root.ListDevice.UInt32List.get(index=i)
            Int32ListBB[i]  = root.ListDevice.Int32List.get(index=i)
            UInt48ListBB[i] = root.ListDevice.UInt48List.get(index=i)
            FloatListBB[i]  = root.ListDevice.FloatList.get(index=i)
            DoubleListBB[i] = root.ListDevice.DoubleList.get(index=i)
            UInt16ListBB[i] = root.ListDevice.UInt16List.get(index=i)
            UInt21ListBB[i] = root.ListDevice.UInt21List.get(index=i)
            BoolListBB[i]   = root.ListDevice.BoolList.get(index=i)

        for i in range(32):
            if UInt32ListBA[i] != UInt32ListB[i]:
                raise AssertionError(f'Verification Failure for UInt32ListBA at position {i}')

            if Int32ListBA[i] != Int32ListB[i]:
                raise AssertionError(f'Verification Failure for Int32ListBA at position {i}')

            if UInt48ListBA[i] != UInt48ListB[i]:
                raise AssertionError(f'Verification Failure for UInt48ListBA at position {i}')

            if FloatListBA[i] != FloatListB[i]:
                raise AssertionError(f'Verification Failure for FloatListBA at position {i}')

            if DoubleListBA[i] != DoubleListB[i]:
                raise AssertionError(f'Verification Failure for DoubleListBA at position {i}')

            if UInt16ListBA[i] != UInt16ListB[i]:
                raise AssertionError(f'Verification Failure for UInt16ListBA at position {i}')

            if UInt21ListBA[i] != UInt21ListB[i]:
                raise AssertionError(f'Verification Failure for UInt21ListBA at position {i}')

            if BoolListBA[i] != BoolListB[i]:
                raise AssertionError(f'Verification Failure for BoolListBA at position {i}')

            if UInt32ListBB[i] != UInt32ListB[i]:
                raise AssertionError(f'Verification Failure for UInt32ListBB at position {i}')

            if FloatListBB[i] != FloatListB[i]:
                raise AssertionError(f'Verification Failure for FloatListBB at position {i}')

            if DoubleListBB[i] != DoubleListB[i]:
                raise AssertionError(f'Verification Failure for DoubleListBB at position {i}')

            if UInt16ListBB[i] != UInt16ListB[i]:
                raise AssertionError(f'Verification Failure for UInt16ListBB at position {i}')

            if UInt21ListBB[i] != UInt21ListB[i]:
                raise AssertionError(f'Verification Failure for UInt21ListBB at position {i}')

            if BoolListBB[i] != BoolListB[i]:
                raise AssertionError(f'Verification Failure for BoolListBB at position {i}')

def run_gui():
    import pyrogue.pydm

    with DummyTree() as root:
        pyrogue.pydm.runPyDM(root=root,title='test123',sizeX=1000,sizeY=500)

if __name__ == "__main__":
    test_memory()
    #run_gui()

