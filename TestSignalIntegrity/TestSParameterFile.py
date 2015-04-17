import unittest
import SignalIntegrity as si
import math
import os
from TestHelpers import *

class TestSParameterFile(unittest.TestCase,SParameterCompareHelper):
    def testSParameterFileFourPort(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        sf=si.sp.File('TestDut.s4p')
        #f=[i*100e6 for i in range(201)]
        #sf.Resample(f)
        #sf.WriteToFile('TestDut.s4p')
        f=sf.f()
        """
        import matplotlib.pyplot as plt
        for r in range(4):
            for c in range(4):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(4,4,r*4+c+1)
                plt.plot(f,y)
        plt.show()
        """
        # this is to test reading and writing, but also to ensure that
        # WriteToFile is always executed and covered
        sf.WriteToFile('TestDutCmp.s4p')
        sf2=si.sp.File('TestDutCmp.s4p')
        os.remove('TestDutCmp.s4p')
        self.assertTrue(self.SParametersAreEqual(sf2,sf,0.001),self.id()+'result not same')
    def testSParameterFileFourPortHzMA(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        sf=si.sp.File('TestDut.s4p')
        f=sf.f()
        """
        import matplotlib.pyplot as plt
        for r in range(4):
            for c in range(4):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(4,4,r*4+c+1)
                plt.plot(f,y)
        plt.show()
        """
        # this is to test reading and writing, but also to ensure that
        # WriteToFile is always executed and covered
        sf.WriteToFile('TestDutCmp.s4p','Hz MA')
        sf2=si.sp.File('TestDutCmp.s4p')
        os.remove('TestDutCmp.s4p')
        self.assertTrue(self.SParametersAreEqual(sf2,sf,0.001),self.id()+'result not same')
    def testSParameterFileFourPortKHzRI(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        sf=si.sp.File('TestDut.s4p')
        f=sf.f()
        """
        import matplotlib.pyplot as plt
        for r in range(4):
            for c in range(4):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(4,4,r*4+c+1)
                plt.plot(f,y)
        plt.show()
        """
        # this is to test reading and writing, but also to ensure that
        # WriteToFile is always executed and covered
        sf.WriteToFile('TestDutCmp.s4p','KHz RI')
        sf2=si.sp.File('TestDutCmp.s4p')
        os.remove('TestDutCmp.s4p')
        self.assertTrue(self.SParametersAreEqual(sf2,sf,0.001),self.id()+'result not same')
    def testSParameterFileFourPortMHzDB(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        sf=si.sp.File('TestDut.s4p')
        f=sf.f()
        """
        import matplotlib.pyplot as plt
        for r in range(4):
            for c in range(4):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(4,4,r*4+c+1)
                plt.plot(f,y)
        plt.show()
        """
        # this is to test reading and writing, but also to ensure that
        # WriteToFile is always executed and covered
        sf.WriteToFile('TestDutCmp.s4p','MHz DB')
        sf2=si.sp.File('TestDutCmp.s4p')
        os.remove('TestDutCmp.s4p')
        self.assertTrue(self.SParametersAreEqual(sf2,sf,0.001),self.id()+'result not same')
    def testSParameterFileFourPortGHzMA(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        sf=si.sp.File('TestDut.s4p')
        f=sf.f()
        """
        import matplotlib.pyplot as plt
        for r in range(4):
            for c in range(4):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(4,4,r*4+c+1)
                plt.plot(f,y)
        plt.show()
        """
        # this is to test reading and writing, but also to ensure that
        # WriteToFile is always executed and covered
        sf.WriteToFile('TestDutCmp.s4p','GHz MA')
        sf2=si.sp.File('TestDutCmp.s4p')
        os.remove('TestDutCmp.s4p')
        self.assertTrue(self.SParametersAreEqual(sf2,sf,0.001),self.id()+'result not same')
    def testSParameterFileFourPortNon50Write(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        sf=si.sp.File('TestDut.s4p')
        f=sf.f()
        """
        import matplotlib.pyplot as plt
        for r in range(4):
            for c in range(4):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(4,4,r*4+c+1)
                plt.plot(f,y)
        plt.show()
        """
        # this is to test reading and writing, but also to ensure that
        # WriteToFile is always executed and covered
        sf.WriteToFile('TestDutCmp.s4p','r 40')
        sf2=si.sp.File('TestDutCmp.s4p')
        os.remove('TestDutCmp.s4p')
        self.assertTrue(self.SParametersAreEqual(sf2,sf,0.001),self.id()+'result not same')
    def testSParameterFileFourPortNon50Read(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        sf=si.sp.File('TestDut.s4p',Z0=40)
        f=sf.f()
        """
        import matplotlib.pyplot as plt
        for r in range(4):
            for c in range(4):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(4,4,r*4+c+1)
                plt.plot(f,y)
        plt.show()
        """
        # this is to test reading and writing, but also to ensure that
        # WriteToFile is always executed and covered
        sf.WriteToFile('TestDutCmp.s4p')
        sf2=si.sp.File('TestDutCmp.s4p',Z0=40)
        os.remove('TestDutCmp.s4p')
        self.assertTrue(self.SParametersAreEqual(sf2,sf,0.001),self.id()+'result not same')
    def testSParameterFileFourPortNoSRead(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        sf=si.sp.File('TestDut.s4p')
        sf.m_sToken='Z' #switch the internal token to Z parameters to make them faulty
        sf.WriteToFile('TestDutCmp.s4p')
        sf2=si.sp.File('TestDutCmp.s4p')
        os.remove('TestDutCmp.s4p')
        self.assertTrue(len(sf2)==0,self.id()+'result not same')
    def testSParameterFileFourPortNonExistant(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        sf=si.sp.File('TestDutcmp.s4p')
        self.assertTrue(len(sf)==0,self.id()+'result not same')
    def testSParameterFileTwoPort(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        sf=si.sp.File('cable.s2p')
        f=sf.f()
        #f=[i*100e6 for i in range(201)]
        #sf2=sf
        #sf2.Resample(f)
        #sf2.WriteToFile('cable2.s2p')
        """
        import matplotlib.pyplot as plt
        for r in range(4):
            for c in range(4):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(4,4,r*4+c+1)
                plt.plot(f,y)
        plt.show()
        """
        # this is to test reading and writing, but also to ensure that
        # WriteToFile is always executed and covered
        sf.WriteToFile('cableCmp.s2p')
        sf2=si.sp.File('cableCmp.s2p')
        os.remove('cableCmp.s2p')
        self.assertTrue(self.SParametersAreEqual(sf2,sf,0.001),self.id()+'result not same')
    def testRLC(self):
        L1=1e-15
        C1=1e-9
        L2=1e-15
        freq=[100e6*(i+1) for i in range(100)]
        spc=[]
        spc.append(('L1',[si.dev.SeriesZ(1j*2.*math.pi*f*L1) for f in freq]))
        spc.append(('C1',[si.dev.SeriesZ(1./(1j*2.*math.pi*C1*f)) for f in freq]))
        spc.append(('L2',[si.dev.SeriesZ(1j*2.*math.pi*f*L2) for f in freq]))
        SD=si.sd.SystemDescription()
        SD.AddDevice('L1',2)
        SD.AddDevice('L2',2)
        SD.AddDevice('C1',2)
        SD.AddDevice('G',1,si.dev.Ground())
        SD.AddPort('L1',1,1)
        SD.AddPort('L2',2,2)
        SD.ConnectDevicePort('L1',2,'L2',1)
        SD.ConnectDevicePort('L1',2,'C1',1)
        SD.ConnectDevicePort('C1',2,'G',1)
        result=[]
        for n in range(len(freq)):
            for d in range(len(spc)):
                SD[SD.IndexOfDevice(spc[d][0])].pSParameters=spc[d][1][n]
            result.append(si.sd.SystemSParametersNumeric(SD).SParameters())
        sf=si.sp.SParameters(freq,result)
        fileName='_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p'
        if not os.path.exists(fileName):
            sf.WriteToFile('_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p')
            self.assertTrue(False,fileName + 'does not exist')
        regression = si.sp.File(fileName)
        self.assertTrue(self.SParametersAreEqual(sf,regression,0.001),self.id()+'result not same')
        """
        import matplotlib.pyplot as plt
        f=sf.f()
        for r in range(2):
            for c in range(2):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(2,2,r*2+c+1)
                plt.plot(f,y)
        plt.show()
        """
    def testRLC2(self):
        L1=1e-15
        C1=1e-9
        L2=1e-15
        freq=[100e6*(i+1) for i in range(100)]
        spc=[]
        spc.append(('L1',si.p.dev.SeriesLf(freq,L1)))
        spc.append(('C1',si.p.dev.SeriesCf(freq,C1)))
        spc.append(('L2',si.p.dev.SeriesLf(freq,L2)))
        SD=si.sd.SystemDescription()
        SD.AddDevice('L1',2)
        SD.AddDevice('L2',2)
        SD.AddDevice('C1',2)
        SD.AddDevice('G',1,si.dev.Ground())
        SD.AddPort('L1',1,1)
        SD.AddPort('L2',2,2)
        SD.ConnectDevicePort('L1',2,'L2',1)
        SD.ConnectDevicePort('L1',2,'C1',1)
        SD.ConnectDevicePort('C1',2,'G',1)
        result=[]
        for n in range(len(freq)):
            for d in range(len(spc)):
                SD[SD.IndexOfDevice(spc[d][0])].pSParameters=spc[d][1][n]
            result.append(si.sd.SystemSParametersNumeric(SD).SParameters())
        sf=si.sp.SParameters(freq,result)
        fileName='_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p'
        if not os.path.exists(fileName):
            sf.WriteToFile('_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p')
            self.assertTrue(False,fileName + 'does not exist')
        regression = si.sp.File(fileName)
        self.assertTrue(self.SParametersAreEqual(sf,regression,0.001),self.id()+'result not same')
        """
        import matplotlib.pyplot as plt
        f=sf.f()
        for r in range(2):
            for c in range(2):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(2,2,r*2+c+1)
                plt.plot(f,y)
        plt.show()
        """
    def testRes(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        newf=[100e6*n for n in range(100)]
        sf=si.sp.ResampledSParameters(si.sp.File('TestDut.s4p'),[1e9*n for n in range(10)])
        sf2=si.sp.ResampledSParameters(si.sp.ResampledSParameters(si.sp.File('TestDut.s4p'),[1e9*n for n in range(10)]),newf,truncate=False)
        if not os.path.exists('Test1.s4p'):
            sf.WriteToFile('Test1.s4p')
            self.assertTrue(False,'Test1.s4p' + ' does not exist')
        if not os.path.exists('Test2.s4p'):
            sf2.WriteToFile('Test2.s4p')
            self.assertTrue(False,'Test2.s4p' + ' does not exist')
        regression = si.sp.File('Test1.s4p')
        self.assertTrue(self.SParametersAreEqual(sf,regression,0.001),self.id()+'first result not same')
        regression = si.sp.File('Test2.s4p')
        self.assertTrue(self.SParametersAreEqual(sf2,regression,0.001),self.id()+'second result not same')
        """
        import matplotlib.pyplot as plt
        f=sf.f()
        f2=sf2.f()
        for r in range(4):
            for c in range(4):
                responseVector=sf.Response(r+1,c+1)
                responseVector2=sf2.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                y2=[20*math.log(abs(resp),10) for resp in responseVector2]
                plt.subplot(4,4,r*4+c+1)
                plt.plot(f,y)
                plt.plot(f2,y2)
        plt.show()
        """
    def testRLC3(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        L1=1e-15
        C1=1e-9
        L2=1e-15
        freq=[100e6*(i+1) for i in range(100)]
        spc=[]
        spc.append(('L1',si.p.dev.SeriesLf(freq,L1)))
        spc.append(('C1',si.p.dev.SeriesCf(freq,C1)))
        spc.append(('L2',si.p.dev.SeriesLf(freq,L2)))
        spc.append(('D1',si.sp.ResampledSParameters(si.sp.File('TestDut.s4p'),freq)))
        SD=si.sd.SystemDescription()
        SD.AddDevice('D1',4)
        SD.AddDevice('L1',2)
        SD.AddDevice('L2',2)
        SD.AddDevice('C1',2)
        SD.AddDevice('G',1,si.dev.Ground())
        SD.AddPort('D1',1,1)
        SD.AddPort('D1',2,2)
        SD.AddPort('D1',3,3)
        SD.ConnectDevicePort('L1',2,'L2',1)
        SD.ConnectDevicePort('L1',2,'C1',1)
        SD.ConnectDevicePort('C1',2,'G',1)
        SD.ConnectDevicePort('D1',4,'L1',1)
        SD.AddPort('L2',2,4)
        result=[]
        for n in range(len(freq)):
            for d in range(len(spc)):
                SD[SD.IndexOfDevice(spc[d][0])].pSParameters=spc[d][1][n]
            result.append(si.sd.SystemSParametersNumeric(SD).SParameters())
        sf=si.sp.SParameters(freq,result)
        fileName='_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p'
        if not os.path.exists(fileName):
            sf.WriteToFile('_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p')
            self.assertTrue(False,fileName + 'does not exist')
        regression = si.sp.File(fileName)
        self.assertTrue(self.SParametersAreEqual(sf,regression,0.001),self.id()+'result not same')
        """
        import matplotlib.pyplot as plt
        f=sf.f()
        for r in range(2):
            for c in range(2):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(2,2,r*2+c+1)
                plt.plot(f,y)
        plt.show()
        """
    def testRLC4(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        freq=[100e6*(i+1) for i in range(100)]
        parser=si.p.SystemSParametersNumericParser(freq)
        parser.AddLine('device L1 2 L 1e-15')
        parser.AddLine('device C1 2 C 1e-9')
        parser.AddLine('device L2 2 L 1e-15')
        parser.AddLine('device D1 4 file TestDut.s4p')
        parser.AddLine('device G 1 ground')
        parser.AddLine('port 1 D1 1 2 D1 2 3 D1 3 4 L2 2')
        #parser.AddLine('port 2 D1 2')
        #parser.AddLine('port 3 D1 3')
        parser.AddLine('connect L1 2 L2 1 C1 1')
        parser.AddLine('connect C1 2 G 1')
        parser.AddLine('connect D1 4 L1 1')
        #parser.AddLine('port 4 L2 2')
        sf=si.sp.SParameters(freq,parser.SParameters())
        fileName='_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p'
        if not os.path.exists(fileName):
            sf.WriteToFile('_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p')
            self.assertTrue(False,fileName + 'does not exist')
        regression = si.sp.File(fileName)
        regression = si.sp.File('_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p')
        self.assertTrue(self.SParametersAreEqual(sf,regression,0.001),self.id()+'result not same')
        """
        import matplotlib.pyplot as plt
        f=sf.f()
        for r in range(2):
            for c in range(2):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(2,2,r*2+c+1)
                plt.plot(f,y)
        plt.show()
        """
    def testRLC5(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        freq=[100e6*(i+1) for i in range(100)]
        parser=si.p.SystemSParametersNumericParser(freq,'%Lleft 1e-15 %Cshunt 1e-9 %Lright 1e-15')
        parser.AddLine('var %Lleft x %Cshunt x %Lright x')
        parser.AddLine('device L1 2 L %Lleft')
        parser.AddLine('device C1 2 C %Cshunt')
        parser.AddLine('device L2 2 L %Lright')
        parser.AddLine('device D1 4 file TestDut.s4p')
        parser.AddLine('device G 1 ground')
        parser.AddLine('port 1 D1 1 2 D1 2 3 D1 3 4 L2 2')
        #parser.AddLine('port 2 D1 2')
        #parser.AddLine('port 3 D1 3')
        parser.AddLine('connect L1 2 L2 1 C1 1')
        parser.AddLine('connect C1 2 G 1')
        parser.AddLine('connect D1 4 L1 1')
        #parser.AddLine('port 4 L2 2')
        sf=si.sp.SParameters(freq,parser.SParameters())
        fileName='_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p'
        if not os.path.exists(fileName):
            sf.WriteToFile('_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p')
            self.assertTrue(False,fileName + 'does not exist')
        regression = si.sp.File(fileName)
        self.assertTrue(self.SParametersAreEqual(sf,regression,0.001),self.id()+'result not same')
        """
        import matplotlib.pyplot as plt
        f=sf.f()
        for r in range(2):
            for c in range(2):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(2,2,r*2+c+1)
                plt.plot(f,y)
        plt.show()
        """
    def testRLC6(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        freq=[100e6*(i+1) for i in range(100)]
        if not os.path.exists('rlc.txt'):
            parser=si.p.SystemDescriptionParser(freq)
            parser.AddLine('var Ll x Cs x Lr x')
            parser.AddLine('device L1 2 L Ll')
            parser.AddLine('device C1 2 C Cs')
            parser.AddLine('device L2 2 L Lr')
            parser.AddLine('device G 1 ground')
            parser.AddLine('connect L1 2 L2 1 C1 1')
            parser.AddLine('connect C1 2 G 1')
            parser.AddLine('port 1 L1 1')
            parser.AddLine('port 2 L2 2')
            parser.WriteToFile('rlc.txt')
        if not os.path.exists('r.txt'):
            parser=si.p.SystemDescriptionParser(freq)
            parser.AddLine('var Rs 50')
            parser.AddLine('device D1 2 R Rs')
            parser.AddLine('port 1 D1 1 2 D1 2')
            parser.WriteToFile('r.txt')
        parser=si.p.SystemSParametersNumericParser(freq)
        parser.AddLine('device RLC 2 subcircuit rlc.txt Ll 1e-15 Cs 1e-9 Lr 1e-15')
        parser.AddLine('device R1 2 subcircuit r.txt')
        parser.AddLine('device D1 4 file TestDut.s4p')
        parser.AddLine('port 1 D1 1 2 D1 2 3 D1 3 4 RLC 2')
        parser.AddLine('connect D1 4 R1 1')
        parser.AddLine('connect R1 2 RLC 1')
        #parser.AddLine('port 4 L2 2')
        sf=si.sp.SParameters(freq,parser.SParameters())
        fileName='_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p'
        if not os.path.exists(fileName):
            sf.WriteToFile('_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p')
            self.assertTrue(False,fileName + 'does not exist')
        regression = si.sp.File(fileName)
        self.assertTrue(self.SParametersAreEqual(sf,regression,0.001),self.id()+'result not same')
        """
        import matplotlib.pyplot as plt
        f=sf.f()
        for r in range(2):
            for c in range(2):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(2,2,r*2+c+1)
                plt.plot(f,y)
        plt.show()
        """
    def testRes2(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        freq=[100e6*(i+1) for i in range(10)]
        parser=si.p.SystemSParametersNumericParser(freq)
        parser.AddLine('device R1 2 R 0.001')
        parser.AddLine('port 1 R1 1 2 R1 2')
        sf=si.sp.SParameters(freq,parser.SParameters())
        fileName='_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p'
        if not os.path.exists(fileName):
            sf.WriteToFile('_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p')
            self.assertTrue(False,fileName + 'does not exist')
        regression = si.sp.File(fileName)
        self.assertTrue(self.SParametersAreEqual(sf,regression,0.001),self.id()+'result not same')
        """
        import matplotlib.pyplot as plt
        f=sf.f()
        for r in range(2):
            for c in range(2):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(2,2,r*2+c+1)
                plt.plot(f,y)
        plt.show()
        """
    def testS2P(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        freq=[0.1e9*i for i in range(201)]
        parser=si.p.SystemSParametersNumericParser(freq)
        parser.AddLine('device D1 2 file cable.s2p')
        parser.AddLine('port 1 D1 1 2 D1 2')
        sf=si.sp.SParameters(freq,parser.SParameters())
        fileName='_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p'
        if not os.path.exists(fileName):
            sf.WriteToFile('_'.join(self.id().split('.'))+'.s'+str(sf.m_P)+'p')
            self.assertTrue(False,fileName + 'does not exist')
        regression = si.sp.File(fileName)
        self.assertTrue(self.SParametersAreEqual(sf,regression,0.001),self.id()+'result not same')
        """
        import matplotlib.pyplot as plt
        f=sf.f()
        for r in range(2):
            for c in range(2):
                responseVector=sf.Response(r+1,c+1)
                y=[20*math.log(abs(resp),10) for resp in responseVector]
                plt.subplot(2,2,r*2+c+1)
                plt.plot(f,y)
        plt.show()
        """
    def testAreEqual(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        firstFileRead = si.sp.File('TestDut.s4p')
        secondFileRead = si.sp.File('TestDut.s4p')
        self.assertTrue(self.SParametersAreEqual(firstFileRead,secondFileRead,0.001),'same file read is not equal')
    def testDeembed(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        freq=[0.1e9*i for i in range(201)]
        parser=si.p.SystemSParametersNumericParser(freq)
        parser.AddLine('device D1 2 file cable.s2p')
        parser.AddLine('device D2 2 file cable.s2p')
        parser.AddLine('port 1 D1 1 2 D2 2')
        parser.AddLine('connect D1 2 D2 1')
        system=si.sp.SParameters(freq,parser.SParameters())
        systemSParametersFileName='_'.join(self.id().split('.'))+'.s'+str(system.m_P)+'p'
        if not os.path.exists(systemSParametersFileName):
            system.WriteToFile(systemSParametersFileName)
        del parser
        parser = si.p.DeembedderNumericParser(freq)
        parser.AddLine('device D1 2 file cable.s2p')
        parser.AddLine('device ? 2')
        parser.AddLine('port 1 D1 1 2 ? 2')
        parser.AddLine('connect D1 2 ? 1')
        parser.AddLine('system file '+systemSParametersFileName)
        de=si.sp.SParameters(freq,parser.Deembed())
        os.remove(systemSParametersFileName)
        self.assertTrue(self.SParametersAreEqual(de,si.sp.ResampledSParameters(si.sp.File('cable.s2p'),freq),0.00001),self.id()+'result not same')
    def testDeembed2(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        freq=[0.1e9*i for i in range(201)]
        parser=si.p.SystemSParametersNumericParser(freq)
        parser.AddLine('device D1 2 file cable.s2p')
        parser.AddLine('device D2 2 file cable.s2p')
        parser.AddLine('port 1 D1 1 2 D2 2')
        parser.AddLine('connect D1 2 D2 1')
        system=si.sp.SParameters(freq,parser.SParameters())
        systemSParametersFileName='_'.join(self.id().split('.'))+'.s'+str(system.m_P)+'p'
        if not os.path.exists(systemSParametersFileName):
            system.WriteToFile(systemSParametersFileName)
        del parser
        parser = si.p.DeembedderNumericParser(freq)
        parser.AddLine('device D1 2 file cable.s2p')
        parser.AddLine('device ? 2')
        parser.AddLine('port 1 D1 1 2 ? 2')
        parser.AddLine('connect D1 2 ? 1')
        parser.AddLine('system file '+systemSParametersFileName)
        de=si.sp.SParameters(freq,parser.Deembed(system))
        self.assertTrue(self.SParametersAreEqual(de,si.sp.ResampledSParameters(si.sp.File('cable.s2p'),freq),0.00001),self.id()+'result not same')
        os.remove(systemSParametersFileName)

if __name__ == '__main__':
    unittest.main()
