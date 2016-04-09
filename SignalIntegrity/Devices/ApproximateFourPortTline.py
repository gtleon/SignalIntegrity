'''
 Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
 Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
 All Rights Reserved.

 Explicit license in accompanying README.txt file.  If you don't have that file
 or do not agree to the terms in that file, then you are not licensed to use
 this material whatsoever.
'''
from numpy import linalg

from SignalIntegrity.Conversions import S2T
from SignalIntegrity.Conversions import T2S

def ApproximateFourPortTLine(f, Rsp, Lsp, Csp, Gsp, Rsm, Lsm, Csm, Gsm, Lm, Cm, Gm, Z0, K):
    from SignalIntegrity.Devices import SeriesZ
    from SignalIntegrity.Devices import Mutual
    from SignalIntegrity.Devices import MixedModeConverter
    from SignalIntegrity.Devices import TerminationG
    from SignalIntegrity.Devices import SeriesG
    from SignalIntegrity.Devices import TerminationC
    from SignalIntegrity.Devices import SeriesC

    from SignalIntegrity.SystemDescriptions import SystemDescription
    from SignalIntegrity.SystemDescriptions import SystemSParametersNumeric
    D=SystemDescription()
    D.AddDevice('RP',2,SeriesZ(Rsp/K,Z0))
    D.AddDevice('T',4)
    D.AddDevice('CP',1)
    D.AddDevice('GP',1,TerminationG(Gsp/K,Z0))
    D.AddDevice('CM',2)
    D.AddDevice('GM',2,SeriesG(Gm/K,Z0))
    D.AddDevice('RN',2,SeriesZ(Rsm/K,Z0))
    D.AddDevice('CN',1)
    D.AddDevice('GN',1,TerminationG(Gsm/K,Z0))
    D.AddPort('RP',1,1)
    D.AddPort('RN',1,2)
    D.AddPort('GM',1,3)
    D.AddPort('GM',2,4)
    D.ConnectDevicePort('RP',2,'T',1)
    D.ConnectDevicePort('T',2,'CP',1)
    D.ConnectDevicePort('CP',1,'GP',1)
    D.ConnectDevicePort('RN',2,'T',3)
    D.ConnectDevicePort('T',4,'CN',1)
    D.ConnectDevicePort('CN',1,'GN',1)
    D.ConnectDevicePort('CM',1,'CP',1)
    D.ConnectDevicePort('CM',2,'CN',1)
    D.ConnectDevicePort('GM',1,'GP',1)
    D.ConnectDevicePort('GM',2,'GN',1)
    DMM=SystemDescription()
    DMM.AddDevice('MM1',4,MixedModeConverter())
    DMM.AddDevice('S',4)
    DMM.AddDevice('MM2',4,MixedModeConverter())
    DMM.AddPort('MM1',3,1)
    DMM.AddPort('MM2',3,2)
    DMM.AddPort('MM1',4,3)
    DMM.AddPort('MM2',4,4)
    DMM.ConnectDevicePort('MM1',1,'S',1)
    DMM.ConnectDevicePort('MM1',2,'S',2)
    DMM.ConnectDevicePort('MM2',1,'S',3)
    DMM.ConnectDevicePort('MM2',2,'S',4)
    Results=[]
    for fn in f:
        D.AssignSParameters('CP',TerminationC(Csp/K,fn,Z0))
        D.AssignSParameters('CN',TerminationC(Csm/K,fn,Z0))
        D.AssignSParameters('CM',SeriesC(Cm/K,fn,Z0))
        D.AssignSParameters('T',Mutual(Lsp/K,Lsm/K,Lm/K,fn,Z0))
        #return D
        R=SystemSParametersNumeric(D).SParameters()
        TR=S2T(R)
        TR=linalg.matrix_power(TR,K)
        R=T2S(TR)
        DMM.AssignSParameters('S',R)
        #return DMM
        R2=SystemSParametersNumeric(DMM).SParameters()
        Results.append(R2)
    return Results