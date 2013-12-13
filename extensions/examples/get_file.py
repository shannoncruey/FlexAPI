"""
    Will read a file from the filesystem and return it.  Useful for serving log files from an application
    that doesn't offer log access.
"""
import os

def execute(ep, args):
    # we're expecting the name of the file as a querystring argument.
    # but for security we've hardcoded the containing path
    
    f = args.get("filename")
    if not f:
        return "Requires a 'filename' argument."
    
    fn = os.path.join("/", "var", "log", f)
    with open(fn, 'r') as f_in:
        if not f_in:
            print("Unable to open file [%s]." % fn)
        data = f_in.read()
        return data