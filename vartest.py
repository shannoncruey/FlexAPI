#!/usr/bin/env python

import re

def replace_vars(input_string, collection, preserve_unmatched = False):
    # first, grab all literal sections
    literal_blocks = []
    p = re.compile("#LITERAL(.*)LITERAL#")
    matches = p.findall(input_string)
    for match in matches:
        literal_blocks.append(match.replace("#LITERAL(", "").replace(")LITERAL#", ""))
        input_string.replace(match, "~~##LITERALPLACEHOLDER##~~")
        

    # a holder for unmatched variables
    unmatched = []
    
    bail = 0
    while "[[" in input_string:
        begin_pos = input_string.rfind("[[")
        end_pos = input_string.find("]]", begin_pos)
        left_string = input_string[:begin_pos]
        right_string = input_string[end_pos + 2]
        
        varname = input_string[begin_pos + 2:end_pos]
        
        if varname:
            print "looking for %s ..." % varname
            replacement_value = lookup_var(varname, collection)
            if not replacement_value:
                if preserve_unmatched:
                    unmatched.append("[[%s]]" % varname)
                    replacement_value = "~~##UNMATCHED##~~"
        
            print "replacing >[[%s]]< with >%s<" % (varname, replacement_value)
            input_string = input_string.replace("[[%s]]" % varname, replacement_value)

        # safety bail
        bail += 1
        if bail > 10:
            print "Safety Bail!"
            break
        
    # unmark the "preserved" variables
    for um in unmatched:
        input_string = input_string.replace("~~##UNMATCHED##~~", um)
    
    p = re.compile("~~##LITERALPLACEHOLDER##~~")
    matches = p.findall(input_string)
    i=0
    for match in matches:
        input_string.replace(match, literal_blocks[i])
        i += 1

    return input_string

def lookup_var(varname, collection):
    if collection.has_key(varname):
        return collection[varname]
    
    return ""
    
vararray = {}
vararray["foo"] = "variable"

x = """
#LITERAL(first lit section)LITERAL#

this is a >[[foo]]<
>[[hort]]< is not

#LITERAL(last lit section)LITERAL#
"""

print replace_vars(x, vararray, True)

