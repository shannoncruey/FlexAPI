"""
    An extension module is very simple...
    
    You can have as many classes and functions as you like, it can be a complex as necesary.
    
    The file must contain a 'execute()' function, which will return the data to go to the client.
"""

def execute(ep, args):
    print ep
    print args
    return "woohoo"