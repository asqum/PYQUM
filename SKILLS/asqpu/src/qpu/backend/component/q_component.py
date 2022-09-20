from typing import List
from abc import ABC


class QComponent( ABC ):
    """
    This class is used for record information of a Qubit-Cavity coupling system and operation method.
    """
    def __init__ ( self, qid:str ):

        self.id = qid
        #self._ports = []

    def __eq__( self, other )->str:
        if isinstance(other, QComponent):
            return self.id == other.id
        if isinstance(other, str):
            return self.id == other
        return False

