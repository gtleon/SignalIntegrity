"""
 produces system descriptions from netlists
"""
# Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
# Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
# All Rights Reserved.
#
# Explicit license in accompanying README.txt file.  If you don't have that file
# or do not agree to the terms in that file, then you are not licensed to use
# this material whatsoever.
 
from SignalIntegrity.Parsers.ParserFile import ParserFile
from SignalIntegrity.Parsers.ParserArgs import ParserArgs

class SystemDescriptionParser(ParserFile,ParserArgs):
    """Parses netlists and produces system descriptions.

    These are instances of class SystemDescription.

    This class provides a mechanism for producing system descriptions from netlists
    rather than by scripting the adding of devices, ports, device connections, etc.
    """
    def __init__(self,f=None,args=None):
        """Constructor

        frequencies may be provided at construction time (or not for symbolic solutions).

        @param f (optional) list of frequencies
        @param args (optional) string arguments for the circuit.

        Arguments are provided on a line as pairs of names and values separated by a space.
        """
        self.m_sd = None
        self.m_f=f
        self.m_lines=[]
        self.m_addThru = False
        self.AssignArguments(args)
    def SystemDescription(self):
        """calculates and gets the system description
        @return instance of class SystemDescription
        @remark It will calculate it, if needed.
        """
        if self.m_sd is None: self._ProcessLines()
        return self.m_sd
    def AddLine(self,line):
        """adds a single line of a netlist
        @param line string line of a netlist
        """
        self.m_sd = None
        if len(line) == 0: return
        self.m_lines.append(line)
        return self
    def AddLines(self,lines):
        """adds a list of lines of a netlist
        @param lines list of strings representing lines of a netlist
        """
        self.m_sd = None
        for line in lines:
            self.AddLine(line)
        return self
    def _ProcessLine(self,line,exclusionList):
        """processes the lines of a netlist

        Lines that can be processed at this level are processed and lines that
        are unknown are place in a list of unknown lines for upstream processing.  This
        enables derived classes to benefit from what this class knows how to process and
        to simply add specific functionality.  As a simple example, a derived simulator class
        needs to add output probes, and this simple system description class knows nothing of
        this.

        netlist lines that are handled at this level are:
        - 'device' - addition of devices.
        - 'connect' - handles device connections.
        - 'port' - adds system ports for s-parameter calculation.

        @param exclusionList list of strings representing commands to exclude.  These are either
        commands that are removed from the functionality (i.e. it would not be write to add a system
        port in a simulation), or commands that are withheld until further processing at a later time
        to enforce the order that commands are handled in.  For example, we like the netlist to be agnostic
        about the order of devices listed and device connections, but we cannot connect device ports until
        a device has been declared.
        """
        # pragma: silent exclude
        from Devices.DeviceParser import DeviceParser
        from SignalIntegrity.Helpers.LineSplitter import LineSplitter
        # pragma: include
        lineList=self.ReplaceArgs(LineSplitter(line))
        if len(lineList) == 0: # pragma: no cover
            return
        if self.ProcessVariables(lineList):
            return
        elif lineList[0] in exclusionList:
            self.m_ul.append(line)
        elif lineList[0] == 'device':
            argList = lineList[3:]
            if [lineList[2]]+argList in self.m_spcl:
                dev = DeviceParser(self.m_f,int(lineList[2]),None)
                dev.m_spf = self.m_spc[self.m_spcl.index([lineList[2]]+argList)][1]
            else:
                dev=DeviceParser(self.m_f,int(lineList[2]),argList)
            self.m_sd.AddDevice(lineList[1],int(lineList[2]),dev.m_sp)
            if not dev.m_spf is None:
                self.m_spc.append((lineList[1],dev.m_spf))
                self.m_spcl.append([lineList[2]]+argList)
        elif lineList[0] == 'connect':
            for i in range(3,len(lineList),2):
                self.m_sd.ConnectDevicePort(lineList[1],int(lineList[2]),
                    lineList[i],int(lineList[i+1]))
        elif lineList[0] == 'port':
            for i in range((len(lineList)-1)/3):
                self.m_sd.AddPort(lineList[i*3+2],int(lineList[i*3+3]),
                    int(lineList[i*3+1]),self.m_addThru)
        else: self.m_ul.append(line)
    def _ProcessLines(self,exclusionList=[]):
        """processes all of the lines in a netlist
        @see _ProcessLine() for explanation of parameters and functionality.
        """
        # pragma: silent exclude
        from SignalIntegrity.SystemDescriptions import SystemDescription
        # pragma: include
        self.m_sd=SystemDescription()
        self.m_spc=[]; self.m_spcl=[]; self.m_ul=[]
        for line in self.m_lines: self._ProcessLine(line,exclusionList)
        return self