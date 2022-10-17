class RXGate( Operation ):
    """
    Rotation along x axis.
    """
    def __init__( self, id:str, pars:List[float]=None ):
        """
        
        args:
            id: the ID of the operation.
            qubit: store the information to build pulse
            pars: a list of parameters to build pulse
                pars[0] = theta

        """
        theta = self.pars[0]
        super().__init__( id, [theta,0] )
        self.channel_type = "rfm"
        #self._pars = pars
    @property
    def pars( self ):
        """
        pars[0] = theta\n
        """
        return self._pars
        
    @pars.setter
    def pars( self, value ):
        self._pars = value

    def to_pulse( self, qubit:PhysicalQubit )->Pulse:
        theta = self.pars[0]
        rxy = RXYOperation("rxy",[theta,0])
        rxy.duration = self.duration
        rxy.t0 = self.t0
        pulse = rxy.to_pulse( qubit )
        return pulse

class XGate( Operation ):
    """
    Pauli-X gate.
    """
    def __init__( self, id:str ):
        super().__init__( id, [pi,0] )
        self.channel_type = "rfm"

    @property
    def pars( self ):
        """
        Don't need any parameter
        """
        return self._pars
        
    @pars.setter
    def pars( self, value ):
        self._pars = value


    def to_pulse( self, qubit:PhysicalQubit )->Pulse:
        rxy = RXYOperation("rxy",[pi,0])
        rxy.duration = self.duration
        rxy.t0 = self.t0
        pulse = rxy.to_pulse( qubit )
        return pulse