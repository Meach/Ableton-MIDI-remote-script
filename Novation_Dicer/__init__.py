#__init__.py

from Novation_Dicer import Novation_Dicer

def create_instance(c_instance):
    """ Creates and returns the Novation_Dicer script """
    return Novation_Dicer(c_instance)