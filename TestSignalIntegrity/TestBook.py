import unittest
import os
from cStringIO import StringIO
import sys
import SignalIntegrity as si
from TestHelpers import *

class Test(unittest.TestCase,RoutineWriterTesterHelper):
    def __init__(self, methodName='runTest'):
        RoutineWriterTesterHelper.__init__(self)
        unittest.TestCase.__init__(self,methodName)
    def CheckSymbolicResult(self,selfid,symbolic,Text):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        fileName = '_'.join(selfid.split('.')) + '.tex'
        if not os.path.exists(fileName):
            symbolic.WriteToFile(fileName)
            self.assertTrue(False, fileName + ' not found')
        regression=''
        with open(fileName, 'rU') as regressionFile:
            for line in regressionFile:
                regression = regression + line
        comparison = symbolic.Get()
        self.assertTrue(regression == comparison,Text + ' incorrect')
    def testBook(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        parser = si.p.SystemDescriptionParser()
        parser.m_addThru = False
        parser.AddLine('device L 2')
        parser.AddLine('device R 2')
        parser.AddLine('port 1 L 1')
        parser.AddLine('port 2 R 2')
        parser.AddLine('connect L 2 R 1')
        # parser.WriteToFile('book.txt')
        sd = si.sd.SystemSParameters(parser.SystemDescription())
        n = sd.NodeVector()
        W = sd.WeightsMatrix()
        m = sd.StimulusVector()
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        print ('{0:' + str(5 * len(n)) + '}').format('Weights Matrix'),
        print '| {0:4}'.format('n'),
        print '| {0:4} |'.format('m')
        print '----------------------------------------------'
        for r in range(len(n)):
            for c in range(len(sd.NodeVector())):
                print '{0:4}'.format(str(W[r][c])),
            print ' | {0:4}'.format(n[r]),
            print '| {0:4} |'.format(m[r])
        print '----------------------------------------------'
        print '\\left[ \\identity - ' + si.helper.Matrix2LaTeX(W) +\
        '\\right] \\cdot '+ si.helper.Matrix2LaTeX([[i] for i in n]) +\
        ' = '+ si.helper.Matrix2LaTeX([[i] for i in m])
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        sys.stdout = old_stdout
        fileName = '_'.join(self.id().split('.')) + '.txt'
        if not os.path.exists(fileName):
            resultFile = open(fileName, 'w')
            resultFile.write(mystdout.getvalue())
            resultFile.close()
            self.assertTrue(False, fileName + ' not found')
        regressionFile = open(fileName, 'rU')
        regression = regressionFile.read()
        regressionFile.close()
        self.assertTrue(regression == mystdout.getvalue(), 'Book Example 1 incorrect')
    def testSystemDescriptionExample(self):
        sd = si.sd.SystemDescription()
        sd.AddDevice('L', 2)  # add two-port left device
        sd.AddDevice('R', 2)  # add two-port right device
        sd.AddPort('L', 1, 1)  # add a port at port 1 of left device
        sd.AddPort('R', 2, 2)  # add a port at port 2 of right device
        sd.ConnectDevicePort('L', 2, 'R', 1)  # connect the other ports
        # exclude
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        # include
        sd.Print()  # print the system description
        spc = si.sd.SystemSParameters(sd)
        n = spc.NodeVector()  # get the node vector
        m = spc.StimulusVector()  # get the stimulus vector
        W = spc.WeightsMatrix()  # get the weights matrix
        # print out the vectors and matrices
        print ('{0:' + str(5 * len(n)) + '}').format('Weights Matrix'),
        print '| {0:4}'.format('n'),
        print '| {0:4} |'.format('m')
        print '----------------------------------------------'
        for r in range(len(W)):
            for c in range(len(W[r])):
                print '{0:4}'.format(str(W[r][c])),
            print ' | {0:4}'.format(n[r]),
            print '| {0:4} |'.format(m[r])
        print '----------------------------------------------'
        # exclude
        sys.stdout = old_stdout
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        fileName = '_'.join(self.id().split('.')) + '.txt'
        if not os.path.exists(fileName):
            resultFile = open(fileName, 'w')
            resultFile.write(mystdout.getvalue())
            resultFile.close()
            self.assertTrue(False, fileName + ' not found')
        regressionFile = open(fileName, 'rU')
        regression = regressionFile.read()
        regressionFile.close()
        self.assertTrue(regression == mystdout.getvalue(), 'Book Example System Description incorrect')
    def testSymbolicExample(self):
        symbolic = si.sd.Symbolic()
        symbolic.DocStart()
        symbolic._AddEq('\\mathbf{S}='+symbolic._LaTeXMatrix(si.sy.SeriesZ('Z')))
        symbolic.DocEnd()
        symbolic.WriteToFile('Symbolic.tex')
        # exclude
        symbolic.Clear()
        symbolic._AddEq('\\mathbf{S}='+symbolic._LaTeXMatrix(si.sy.SeriesZ('Z')))
        symbolic.Emit()
        self.CheckSymbolicResult(self.id(),symbolic,'Symbolic Example')
    def testSystemDescriptionSymbolicExample(self):
        sd = si.sd.SystemDescription()
        sd.AddDevice('L', 2)  # add two-port left device
        sd.AddDevice('R', 2)  # add two-port right device
        sd.AddPort('L', 1, 1)  # add a port at port 1 of left device
        sd.AddPort('R', 2, 2)  # add a port at port 2 of right device
        sd.ConnectDevicePort('L', 2, 'R', 1)  # connect the other ports
        ssps = si.sd.SystemSParametersSymbolic(sd)
        ssps.LaTeXSystemEquation().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),ssps,'Book Example System Description Symbolic')
    def testSymbolicMethods(self):
        sdp = si.p.SystemDescriptionParser()
        #sdp.AddLines(['device L 2','device R 2','device M 2','device G 1 ground','port 1 L 1 2 R 2',
        #   'connect L 2 R 1 M 1','connect G 1 M 2'])
        sdp.AddLines(['device L 2','device R 2','port 1 L 1 2 R 2','connect L 2 R 1'])
        spc = si.sd.SystemSParameters(sdp.SystemDescription())
        symbolic=si.sd.SystemSParametersSymbolic(spc)
        symbolic.Clear().LaTeXSystemEquation()
        self.CheckSymbolicResult('LaTeXSystemEquation',symbolic,'LaTeXSystemEquation')
        symbolic.Clear().LaTeXSolution(solvetype='direct')
        self.CheckSymbolicResult('LaTeXDirectSolution',symbolic,'LaTeXDirectSolution')
        symbolic.Clear().LaTeXSolution(size='big')
        self.CheckSymbolicResult('LaTeXBlockSolutionBig',symbolic,'LaTeXBlockSolutionBig')
        symbolic.Clear().LaTeXSolution(size='biggest')
        self.CheckSymbolicResult('LaTeXBlockSolutionBiggest',symbolic,'LaTeXBlockSolutionBiggest')
        symbolic.Clear().LaTeXSolution()
        self.CheckSymbolicResult('LaTeXBlockSolution',symbolic,'LaTeXBlockSolution')
    def testSymbolicSolutionExample1(self):
        sd = si.sd.SystemDescription()
        sd.AddDevice('S', 2)  # add two-port left device
        sd.AddDevice('\\Gamma t', 1)  # add a termination
        sd.AddPort('S', 1, 1)  # add a port at port 1 of left device
        sd.ConnectDevicePort('S', 2, '\\Gamma t', 1)  # connect the other ports
        spc = si.sd.SystemSParameters(sd)
        symbolic=si.sd.SystemSParametersSymbolic(spc)
        symbolic.LaTeXSystemEquation()
        symbolic.LaTeXSolution(solvetype='direct')
        symbolic.LaTeXSolution(solvetype='block').Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Solution 1')
    def testSymbolicSolutionParserExample1(self):
        sdp = si.p.SystemDescriptionParser()
        sdp.AddLines(['device S 2','device \\{\\Gamma\\}t 1','port 1 S 1','connect S 2 \\{\\Gamma\\}t 1'])
        sdp.WriteToFile('SymbolicSolution1.txt',False)
        spc = si.sd.SystemSParameters(sdp.SystemDescription())
        symbolic=si.sd.SystemSParametersSymbolic(spc)
        symbolic.LaTeXSystemEquation()
        symbolic.LaTeXSolution(solvetype='direct')
        symbolic.LaTeXSolution(solvetype='block').Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Solution 1 Parser')
    def testSymbolicSolutionParserFileExample1(self):
        sdp = si.p.SystemDescriptionParser().File('SymbolicSolution1.txt')
        spc = si.sd.SystemSParameters(sdp.SystemDescription())
        symbolic=si.sd.SystemSParametersSymbolic(spc)
        symbolic.LaTeXSystemEquation()
        symbolic.LaTeXSolution(solvetype='direct')
        symbolic.LaTeXSolution(solvetype='block').Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Solution 1 Parser File')
    def testSymbolicSolutionExample2(self):
        sd = si.sd.SystemDescription()
        sd.AddDevice('L', 2)  # add two-port left device
        sd.AddDevice('R', 2)  # add two-port right device
        sd.AddPort('L', 1, 1)  # add a port at port 1 of left device
        sd.AddPort('R', 2, 2)  # add a port at port 2 of right device
        sd.ConnectDevicePort('L', 2, 'R', 1)  # connect the other ports
        spc = si.sd.SystemSParameters(sd)
        symbolic=si.sd.SystemSParametersSymbolic(spc)
        symbolic.LaTeXSystemEquation()
        symbolic.LaTeXSolution(solvetype='direct')
        symbolic.LaTeXSolution(solvetype='block').Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Solution 2')
    def testSymbolicSolutionParserExample2(self):
        sdp = si.p.SystemDescriptionParser()
        sdp.AddLines(['device L 2','device R 2','port 1 L 1 2 R 2','connect L 2 R 1'])
        sdp.WriteToFile('SymbolicSolution2.txt',False)
        spc = si.sd.SystemSParameters(sdp.SystemDescription())
        symbolic=si.sd.SystemSParametersSymbolic(spc)
        symbolic.LaTeXSystemEquation()
        symbolic.LaTeXSolution(solvetype='direct')
        symbolic.LaTeXSolution(solvetype='block').Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Solution 2 Parser')
    def testSymbolicSolutionParserFileExample2(self):
        sdp = si.p.SystemDescriptionParser().File('SymbolicSolution2.txt')
        spc = si.sd.SystemSParameters(sdp.SystemDescription())
        symbolic=si.sd.SystemSParametersSymbolic(spc)
        symbolic.LaTeXSystemEquation()
        symbolic.LaTeXSolution(solvetype='direct')
        symbolic.LaTeXSolution(solvetype='block').Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Solution 2 Parser File')
    def testSymbolicSolutionExample3(self):
        sd = si.sd.SystemDescription()
        sd.AddDevice('L', 2)  # add two-port left device
        sd.AddDevice('R', 2)  # add two-port right device
        sd.AddDevice('M', 2)  # add two-port middle device
        sd.AddDevice('G', 1, [[-1]]) # add a ground
        sd.AddPort('L', 1, 1)  # add a port at port 1 of left device
        sd.AddPort('R', 2, 2)  # add a port at port 2 of right device
        sd.ConnectDevicePort('L', 2, 'R', 1)  # connect the other ports
        sd.ConnectDevicePort('L', 2, 'M', 1)
        sd.ConnectDevicePort('G', 1, 'M', 2)
        spc = si.sd.SystemSParameters(sd)
        symbolic=si.sd.SystemSParametersSymbolic(spc,size='small')
        symbolic.LaTeXSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Solution 3')
    def testSymbolicSolutionParserExample3(self):
        sdp = si.p.SystemDescriptionParser()
        sdp.AddLines(['device L 2','device R 2','device M 2','device G 1 ground','port 1 L 1 2 R 2',
            'connect L 2 R 1 M 1','connect G 1 M 2'])
        # exclude
        sdp.WriteToFile('SymbolicSolution3.txt',False)
        # include
        spc = si.sd.SystemSParameters(sdp.SystemDescription())
        symbolic=si.sd.SystemSParametersSymbolic(spc,size='small')
        symbolic.LaTeXSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Solution 3 Parser')
    def testSymbolicSolutionParserFileExample3(self):
        sdp = si.p.SystemDescriptionParser().File('SymbolicSolution3.txt')
        spc = si.sd.SystemSParameters(sdp.SystemDescription())
        symbolic=si.sd.SystemSParametersSymbolic(spc,size='small')
        symbolic.LaTeXSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Solution 3 Parser File')
    def testSymbolicDeembeddingExample1(self):
        d=si.sd.Deembedder()
        d.AddDevice('D',2)
        d.AddUnknown('Su',1)
        d.ConnectDevicePort('D',2,'Su',1)
        d.AddPort('D',1,1)
        symbolic=si.sd.DeembedderSymbolic(d,size='small')
        symbolic.SymbolicSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Deembedding Solution 1')
    def testSymbolicDeembeddingThruExample1(self):
        d=si.sd.Deembedder()
        d.AddDevice('D',2)
        d.AddUnknown('Su',1)
        d.ConnectDevicePort('D',2,'Su',1)
        d.AddPort('D',1,1,True)
        symbolic=si.sd.DeembedderSymbolic(d,size='small')
        symbolic.SymbolicSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Deembedding Solution 1 Thru')
    def testSymbolicDeembeddingParserExample1(self):
        dp=si.p.DeembedderParser()
        dp.AddLines(['device D 2','unknown Su 1','port 1 D 1','connect D 2 Su 1'])
        dp.WriteToFile('SymbolicDeembedding1.txt',False)
        spc = si.sd.Deembedder(dp.SystemDescription())
        symbolic=si.sd.DeembedderSymbolic(spc,size='small')
        symbolic.SymbolicSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Deembedding Solution 1 Parser')
    def testSymbolicDeembeddingParserFileExample1(self):
        dp=si.p.DeembedderParser().File('SymbolicDeembedding1.txt')
        spc = si.sd.Deembedder(dp.SystemDescription())
        symbolic=si.sd.DeembedderSymbolic(spc,size='small')
        symbolic.SymbolicSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Deembedding Solution 1 Parser File')
    def testSymbolicDeembeddingExample2(self):
        d=si.sd.Deembedder()
        d.AddDevice('L',2)
        d.AddUnknown('Su',2)
        d.AddDevice('R',2)
        d.AddPort('L',1,1)
        d.AddPort('R',1,2)
        d.ConnectDevicePort('L',2,'Su',1)
        d.ConnectDevicePort('R',2,'Su',2)
        symbolic=si.sd.DeembedderSymbolic(d,size='small')
        symbolic.SymbolicSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Deembedding Solution 2')
    def testSymbolicDeembeddingParserExample2(self):
        dp=si.p.DeembedderParser()
        dp.AddLines(['device L 2','unknown Su 2','device R 2',
            'port 1 L 1 2 R 1','connect L 2 Su 1','connect R 2 Su 2'])
        # exclude
        dp.WriteToFile('SymbolicDeembedding2.txt',False)
        # include
        spc = si.sd.Deembedder(dp.SystemDescription())
        symbolic=si.sd.DeembedderSymbolic(spc,size='small')
        symbolic.SymbolicSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Deembedding Solution 2 Parser')
    def testSymbolicDeembeddingParserFileExample2(self):
        dp=si.p.DeembedderParser().File('SymbolicDeembedding2.txt')
        spc = si.sd.Deembedder(dp.SystemDescription())
        symbolic=si.sd.DeembedderSymbolic(spc,size='small')
        symbolic.SymbolicSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Deembedding Solution 2 Parser File')
    def testSymbolicDeembeddingExample3(self):
        d=si.sd.Deembedder()
        d.AddDevice('L',2)
        d.AddUnknown('Su',2)
        d.AddPort('L',1,1)
        d.AddPort('Su',2,2,True)
        d.ConnectDevicePort('L',2,'Su',1)
        symbolic=si.sd.DeembedderSymbolic(d,size='small')
        symbolic.SymbolicSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Deembedding Solution 3')
    def testSymbolicDeembeddingThruExample3(self):
        d=si.sd.Deembedder()
        d.AddDevice('L',2)
        d.AddUnknown('Su',2)
        d.AddPort('L',1,1,True)
        d.AddPort('Su',2,2,True)
        d.ConnectDevicePort('L',2,'Su',1)
        symbolic=si.sd.DeembedderSymbolic(d,size='small')
        symbolic.SymbolicSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Deembedding 3 Thru incorrect')
    def testSymbolicDeembeddingParserExample3(self):
        dp=si.p.DeembedderParser()
        dp.AddLines(['device L 2','unknown Su 2','port 1 L 1 2 Su 2','connect L 2 Su 1'])
        dp.WriteToFile('SymbolicDeembedding3.txt',False)
        spc = si.sd.Deembedder(dp.SystemDescription())
        symbolic=si.sd.DeembedderSymbolic(spc,size='small')
        symbolic.SymbolicSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Deembedding Solution 3 Parser')
    def testSymbolicDeembeddingParserFileExample3(self):
        dp=si.p.DeembedderParser().File('SymbolicDeembedding3.txt')
        spc = si.sd.Deembedder(dp.SystemDescription())
        symbolic=si.sd.DeembedderSymbolic(spc,size='small')
        symbolic.SymbolicSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Deembedding Solution 3 Parser File')
    def testSymbolicDeembeddingExample4(self):
        d=si.sd.Deembedder()
        d.AddDevice('F',4)
        d.AddUnknown('?1',1)
        d.AddUnknown('?2',1)
        d.AddPort('F',1,1)
        d.AddPort('F',2,2)
        d.ConnectDevicePort('F',3,'?1',1)
        d.ConnectDevicePort('F',4,'?2',1)
        symbolic=si.sd.DeembedderSymbolic(d,size='small')
        symbolic.SymbolicSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Deembedding Solution 4')
    def testSymbolicDeembeddingParserExample4(self):
        dp=si.p.DeembedderParser()
        dp.AddLines(['device F 4','unknown ?1 1','unknown ?2 1','port 1 F 1 2 F 2',
            'connect F 3 ?1 1','connect F 4 ?2 1'])
        dp.WriteToFile('SymbolicDeembedding4.txt',False)
        spc = si.sd.Deembedder(dp.SystemDescription())
        symbolic=si.sd.DeembedderSymbolic(spc,size='small')
        symbolic.SymbolicSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Deembedding Solution 4 Parser')
    def testSymbolicDeembeddingParserFileExample4(self):
        dp=si.p.DeembedderParser().File('SymbolicDeembedding4.txt')
        spc = si.sd.Deembedder(dp.SystemDescription())
        symbolic=si.sd.DeembedderSymbolic(spc,size='small')
        symbolic.SymbolicSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Deembedding Solution 4 Parser File')
    def testSymbolicDeembeddingExample5(self):
        d=si.sd.Deembedder()
        d.AddDevice('D1',2)
        d.AddDevice('D2',2)
        d.AddDevice('D3',2)
        d.AddUnknown('Su',2)
        d.AddPort('D1',1,1)
        d.AddPort('D2',1,2)
        d.ConnectDevicePort('D1',2,'Su',1)
        d.ConnectDevicePort('D2',2,'D3',1)
        d.ConnectDevicePort('D3',2,'Su',2)
        symbolic=si.sd.DeembedderSymbolic(d,size='small')
        symbolic.SymbolicSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Deembedding Solution 5')
    def testSymbolicDeembeddingParserExample5(self):
        dp=si.p.DeembedderParser()
        dp.AddLines(['device D1 2','device D2 2','device D3 2',
            'unknown Su 2','port 1 D1 1 2 D2 1',
            'connect D1 2 Su 1','connect D2 2 D3 1',
            'connect D3 2 Su 2'])
        dp.WriteToFile('SymbolicDeembedding5.txt',False)
        spc = si.sd.Deembedder(dp.SystemDescription())
        symbolic=si.sd.DeembedderSymbolic(spc,size='small')
        symbolic.SymbolicSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Deembedding Solution 5 Parser')
    def testSymbolicDeembeddingParserFileExample5(self):
        dp=si.p.DeembedderParser().File('SymbolicDeembedding5.txt')
        spc = si.sd.Deembedder(dp.SystemDescription())
        symbolic=si.sd.DeembedderSymbolic(spc,size='small')
        symbolic.SymbolicSolution().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),symbolic,'Book Example Symbolic Deembedding Solution 5 Parser File')
    def testSymbolicVirtualProbeExample1(self):
        sd=si.sd.SystemDescription()
        sd.AddDevice('T',1)
        sd.AddDevice('C',2)
        sd.AddDevice('R',1)
        sd.ConnectDevicePort('T',1,'C',1)
        sd.ConnectDevicePort('C',2,'R',1)
        sd.AssignM('T',1,'m1')
        vp=si.sd.VirtualProbe(sd)
        vp.pMeasurementList = [('T',1)]
        vp.pOutputList = [('R',1)]
        svp=si.sd.VirtualProbeSymbolic(vp,size='small')
        svp.LaTeXEquations().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),svp,'Book Example Symbolic Virtual Probe 1')
    def testSymbolicVirtualProbeParserExample1(self):
        vpp=si.p.VirtualProbeParser()
        vpp.AddLines(['device T 1','device C 2','device R 1','connect T 1 C 1','connect C 2 R 1',
            'stim m1 T 1','meas T 1','output R 1'])
        vpp.WriteToFile('VirtualProbe1.txt',False)
        vp=si.sd.VirtualProbe(vpp.SystemDescription())
        svp=si.sd.VirtualProbeSymbolic(vp,size='small')
        svp.LaTeXEquations().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),svp,'Book Example Symbolic Virtual Probe 1 Parser')
    def testSymbolicVirtualProbeParserFileExample1(self):
        vpp=si.p.VirtualProbeParser().File('VirtualProbe1.txt')
        vp=si.sd.VirtualProbe(vpp.SystemDescription())
        svp=si.sd.VirtualProbeSymbolic(vp,size='small')
        svp.LaTeXEquations().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),svp,'Book Example Symbolic Virtual Probe 1 Parser File')
    def testSymbolicVirtualProbeExample2(self):
        sd=si.sd.SystemDescription()
        sd.AddDevice('T',2)
        sd.AddDevice('C',4)
        sd.AddDevice('R',2)
        sd.ConnectDevicePort('T',1,'C',1)
        sd.ConnectDevicePort('T',2,'C',2)
        sd.ConnectDevicePort('C',3,'R',1)
        sd.ConnectDevicePort('C',4,'R',2)
        sd.AssignM('T',1,'m1')
        sd.AssignM('T',2,'m2')
        vp=si.sd.VirtualProbe(sd)
        vp.pMeasurementList = [('T',1),('T',2)]
        vp.pOutputList = [('R',1),('R',2)]
        svp=si.sd.VirtualProbeSymbolic(vp,size='small')
        svp.LaTeXEquations().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),svp,'Book Example Symbolic Virtual Probe 2')
    def testSymbolicVirtualProbeParserExample2(self):
        vpp=si.p.VirtualProbeParser()
        vpp.AddLines(['device T 2','device C 4','device R 2','connect T 1 C 1','connect T 2 C 2',
            'connect C 3 R 1','connect C 4 R 2','stim m1 T 1','stim m2 T 2','meas T 1 T 2','output R 1 R 2'])
        vpp.WriteToFile('VirtualProbe2.txt',False)
        vp=si.sd.VirtualProbe(vpp.SystemDescription())
        svp=si.sd.VirtualProbeSymbolic(vp,size='small')
        svp.LaTeXEquations().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),svp,'Book Example Symbolic Virtual Probe 2 Parser')
    def testSymbolicVirtualProbeParserFileExample2(self):
        vpp=si.p.VirtualProbeParser().File('VirtualProbe2.txt')
        vp=si.sd.VirtualProbe(vpp.SystemDescription())
        svp=si.sd.VirtualProbeSymbolic(vp,size='small')
        svp.LaTeXEquations().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),svp,'Book Example Symbolic Virtual Probe 2 Parser File')
    def testSymbolicVirtualProbeExample3(self):
        sd=si.sd.SystemDescription()
        sd.AddDevice('T',2)
        sd.AddDevice('C',4)
        sd.AddDevice('R',2)
        sd.ConnectDevicePort('T',1,'C',1)
        sd.ConnectDevicePort('T',2,'C',2)
        sd.ConnectDevicePort('C',3,'R',1)
        sd.ConnectDevicePort('C',4,'R',2)
        sd.AssignM('T',1,'m1')
        sd.AssignM('T',2,'m2')
        vp=si.sd.VirtualProbe(sd)
        vp.pMeasurementList = [('T',1),('T',2)]
        vp.pOutputList = [('R',1),('R',2)]
        vp.pStimDef = [[1],[-1]]
        svp=si.sd.VirtualProbeSymbolic(vp,size='small')
        svp.LaTeXEquations().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),svp,'Book Example Symbolic Virtual Probe 3')
    def testSymbolicVirtualProbeParserExample3(self):
        vpp=si.p.VirtualProbeParser()
        vpp.AddLines(['device T 2','device C 4','device R 2','connect T 1 C 1',
            'connect T 2 C 2','connect C 3 R 1','connect C 4 R 2','stim m1 T 1',
            'stim m2 T 2','meas T 1 T 2','output R 1 R 2','stimdef [[1],[-1]]'])
        vpp.WriteToFile('VirtualProbe3.txt',False)
        vp=si.sd.VirtualProbe(vpp.SystemDescription())
        svp=si.sd.VirtualProbeSymbolic(vp,size='small')
        svp.LaTeXEquations().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),svp,'Book Example Symbolic Virtual Probe 3 Parser')
    def testSymbolicVirtualProbeParserFileExample3(self):
        vpp=si.p.VirtualProbeParser().File('VirtualProbe3.txt')
        vp=si.sd.VirtualProbe(vpp.SystemDescription())
        svp=si.sd.VirtualProbeSymbolic(vp,size='small')
        svp.LaTeXEquations().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),svp,'Book Example Symbolic Virtual Probe 3 Parser File')
    def testSymbolicVirtualProbeExample4(self):
        sd=si.sd.SystemDescription()
        sd.AddDevice('T',2)
        sd.AddDevice('MM1',4,si.dev.MixedModeConverter())
        sd.AddDevice('MM2',4,si.dev.MixedModeConverter())
        sd.AddDevice('C',4)
        sd.AddDevice('R',2)
        sd.ConnectDevicePort('T',1,'MM1',1)
        sd.ConnectDevicePort('T',2,'MM1',2)
        sd.ConnectDevicePort('MM1',3,'MM2',3)
        sd.ConnectDevicePort('MM1',4,'MM2',4)
        sd.ConnectDevicePort('MM2',1,'C',1)
        sd.ConnectDevicePort('MM2',2,'C',2)
        sd.ConnectDevicePort('C',3,'R',1)
        sd.ConnectDevicePort('C',4,'R',2)
        sd.AssignM('T',1,'m1')
        sd.AssignM('T',2,'m2')
        vp=si.sd.VirtualProbe(sd)
        vp.pMeasurementList = [('MM1',3)]
        vp.pOutputList = [('R',1),('R',2)]
        vp.pStimDef = [[1],[-1]]
        svp=si.sd.VirtualProbeSymbolic(vp,size='small')
        svp.LaTeXTransferMatrix().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),svp,'Book Example Symbolic Virtual Probe 4')
    def testSymbolicVirtualProbeParserExample4(self):
        vpp=si.p.VirtualProbeParser()
        vpp.AddLines(['device T 2','device MM1 4 mixedmode','device MM2 4 mixedmode','device C 4',
            'device R 2','connect T 1 MM1 1','connect T 2 MM1 2','connect MM1 3 MM2 3','connect MM1 4 MM2 4',
            'connect MM2 1 C 1','connect MM2 2 C 2',
            'connect C 3 R 1','connect C 4 R 2','stim m1 T 1 m2 T 2','meas MM1 3','output R 1 R 2',
            'stimdef [[1],[-1]]'])
        vpp.WriteToFile('VirtualProbe4.txt',False)
        vp=si.sd.VirtualProbe(vpp.SystemDescription())
        svp=si.sd.VirtualProbeSymbolic(vp,size='small')
        svp.LaTeXTransferMatrix().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),svp,'Book Example Symbolic Virtual Probe 4 Parser')
    def testSymbolicVirtualProbeParserFileExample4(self):
        vpp=si.p.VirtualProbeParser().File('VirtualProbe4.txt')
        vp=si.sd.VirtualProbe(vpp.SystemDescription())
        svp=si.sd.VirtualProbeSymbolic(vp,size='small')
        svp.LaTeXTransferMatrix().Emit()
        # exclude
        self.CheckSymbolicResult(self.id(),svp,'Book Example Symbolic Virtual Probe 4 Parser File')
    def testSymbolicSolutionExample1Code(self):
        self.WriteCode('TestBook.py','testSymbolicSolutionExample1(self)',self.standardHeader)
    def testSymbolicSolutionParserExample2Code(self):
        self.WriteCode('TestBook.py','testSymbolicSolutionParserExample2(self)',self.standardHeader)
    def testSymbolicSolutionParserFileExample3Code(self):
        self.WriteCode('TestBook.py','testSymbolicSolutionParserFileExample3(self)',self.standardHeader)
    def testSystemDescriptionExampleCode(self):
        self.WriteCode('TestBook.py','testSystemDescriptionExample(self)',self.standardHeader)
    def testSymbolicExampleCode(self):
        self.WriteCode('TestBook.py','testSymbolicExample(self)',self.standardHeader)
    def testSystemDescriptionExampleSymbolicCode(self):
        self.WriteCode('TestBook.py','testSystemDescriptionSymbolicExample(self)',self.standardHeader)
    def testSymbolicDeembeddingExample1Code(self):
        self.WriteCode('TestBook.py','testSymbolicDeembeddingExample1(self)',self.standardHeader)
    def testSymbolicDeembeddingParserExample2Code(self):
        self.WriteCode('TestBook.py','testSymbolicDeembeddingParserExample2(self)',self.standardHeader)
    def testSymbolicDeembeddingParserFileExample3Code(self):
        self.WriteCode('TestBook.py','testSymbolicDeembeddingParserFileExample3(self)',self.standardHeader)
    def testSymbolicDeembeddingExample4Code(self):
        self.WriteCode('TestBook.py','testSymbolicDeembeddingExample4(self)',self.standardHeader)
    def testSymbolicDeembeddingExample5Code(self):
        self.WriteCode('TestBook.py','testSymbolicDeembeddingExample5(self)',self.standardHeader)
    def testSymbolicVirtualProbeExample1Code(self):
        self.WriteCode('TestBook.py','testSymbolicVirtualProbeExample1(self)',self.standardHeader)
    def testSymbolicVirtualProbeExample2Code(self):
        self.WriteCode('TestBook.py','testSymbolicVirtualProbeExample2(self)',self.standardHeader)
    def testSymbolicVirtualProbeParserFileExample3Code(self):
        self.WriteCode('TestBook.py','testSymbolicVirtualProbeParserExample3(self)',self.standardHeader)
    def testSymbolicVirtualProbeParserFileExample4Code(self):
        self.WriteCode('TestBook.py','testSymbolicVirtualProbeParserFileExample4(self)',self.standardHeader)

if __name__ == "__main__":
    unittest.main()
