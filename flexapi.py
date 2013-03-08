#!/usr/bin/env python

# Copyright 2012 Neal Shannon Cruey / Box198
#  
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  
#     http:# www.apache.org/licenses/LICENSE-2.0
#  
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import web
import os
import sys
import json
import decimal
import importlib

web_root = os.path.abspath(os.path.dirname(__file__))
lib_path = os.path.join(web_root, "lib")
sys.path.insert(0, lib_path)
sys.path.append(web_root)

# to avoid any path issues, "cd" to the web root.
os.chdir(web_root)
        
urls = (
    '/(.*)', 'endpoint'
)
app = web.application(urls, globals())

class endpoint:        
    def GET(self, endpoint):
        try:
            if not endpoint: 
                return "Endpoint not defined."
    
            # the endpoint definition is a json file
            filename = "%s/endpoints/%s.ep" % (web_root, endpoint)
            with open(filename, 'r') as f_in:
                endpoint_json = f_in.read()
            
            ep = json.loads(endpoint_json)
            
            print "Processing endpoint [%s]" % ep["name"]
            
            data = ""
            options = ep["options"] if ep.has_key("options") else {}
            
            if ep["type"] == "sql":
                data = process_sql(ep)
            elif ep["type"] == "nosql":
                data = process_nosql(ep)
            elif ep["type"] == "extension":
                data = process_extension(ep)
            else:
                return "Invalid Endpoint Type."
            
            if ep.has_key("return"):
                if ep["return"] == "json":
                    return return_json(data, ep)
                elif ep["return"] == "format":
                    """Use row_template and perform python 'format'. on each row."""
                    return return_format(data, ep, options)
                elif ep["return"] == "text":
                    return return_text(data)
                                
                elif ep["return"] == "csv":
                    """This can make use of the csv module, if I can 
                    figure out how to use it with variables instead of files.
                    
                    This was an attempt to do it manually before I discovered the csv module."""
                    """try:
                        iterator = iter(data)
                    except TypeError:
                        # data is not iterable, just return it
                        return str(data)
                    else:
                        # data is a rowset
                        for row in data:
                            # the elements in the row may be a dict, or a tuple
                            # only a dict will have 'itervalues'
                            try:
                                fields = row.itervalues()
                            except AttributeError:
                                fields = iter(row)
    
                            outlist = []
                            for field in fields:
                                outlist.append(field)"""
    
                            
                else:
                    return returnerror("Invalid 'return' format.")
            else:
                return returnerror("'return' format is required.")
            
        except Exception, ex:
            raise ex
            return ex.__str__()
            
def return_json(data, ep):
    # print str(data)
    js = json.dumps(data, cls=BetterEncoder, sort_keys=True, indent=4)
    if ep.has_key("prefix"):
        js = ep["prefix"] + js
    if ep.has_key("suffix"):
        js += ep["suffix"]
    
    return js

def return_text(data, ep):
    try:
        _ = iter(data)
    except TypeError:
        # data is not iterable, just return it
        return str(data)
    else:
        # data is a rowset
        output = ""
        for row in data:
            # the elements in the row may be a dict, or a tuple
            # only a dict will have 'itervalues'
            try:
                fields = row.itervalues()
            except AttributeError:
                fields = iter(row)

            outlist = []
            for field in fields:
                outlist.append(str(field))
                
            output += "".join(outlist)
            
        return output

def return_format(data, ep, options):
    """Use row_template and perform python 'format' on each row."""
    try:
        _ = iter(data)
    except TypeError:
        # data is not iterable, just return it
        return str(data)
    else:
        # data is a rowset
        outlist = []
        output = ""
        rownum = 0
        for row in data:
            if ep.has_key("row_template"):
                if ep["row_template"]:
                    rowstr = "".join(ep["row_template"])

                    # there are two format_types... index and replace...
                    # 'index' uses the python .format function, and looks for {0} notation
                    # 'replace' type uses the pythonish %s and %d tokens.
                    
                    # index is the default
                    fmt_type = "index"
                    if options.has_key("format_type"):
                        if options["format_type"] == "replace":
                            fmt_type = "replace"
                    
                    if fmt_type == "replace":
                        try:
                            # the token %# is a special replacement token, in the %s format style :-)
                            rowstr = rowstr.replace("{#}", str(rownum))
                            
                            # convert the row to a tuple
                            fieldlist = tuple(row)
                            outlist.append(rowstr % fieldlist)
                        except TypeError:
                            raise Exception("Format type 'replace' row_template must use every item in the result row.")
                        except Exception as ex:
                            raise Exception("Format type 'replace' row_template uses the %%s placeholder syntax.  Any literal percent signs should be doubled. The token %# is used for printing the row number. %s" % ex)
                    else:
                        # the token {#} is a special replacement token, in the {0} format style :-)
                        rowstr = rowstr.replace("{#}", str(rownum))

                        # the elements in the row may be a dict, list or tuple
                        # only a dict will have 'itervalues'
                        try:
                            _ = row.itervalues()
                            try:
                                # if it's a dict, we can replace using {key} syntax
                                print row
                                outlist.append(rowstr.format(**row))
                            except IndexError:
                                raise Exception("Results are a dictionary, the {key} syntax must be used in the row_template.")
                            except KeyError:
                                raise Exception("One or more keys do not exist on the result row.")
                        except AttributeError:
                            _ = iter(row)
                            try:
                                # if it's a list, we can replace using {0} syntax
                                outlist.append(rowstr.format(*row))
                            except IndexError:
                                raise Exception("The row_template is asking for more values than exist in the result row.")
                            except KeyError:
                                raise Exception("Results are a list, the {0} syntax must be used in the row_template.")
                            
#                            except Exception as ex:
#                                raise Exception("Format type 'index' row_template uses the {0} or {key} placeholder syntax." \
#                                                  "  Any literal curly braces should be doubled." \
#                                                  " The token {#} is used for printing the row number. %s" % ex)
                else:
                    raise Exception("Format return type requires a 'row_template'.  Value cannot be empty.")
            else:
                raise Exception("Format return type requires a 'row_template'.  Value cannot be empty.")
                
            rownum += 1

        # might have a row separator which will go between each row
        joinwith = ""
        if options.has_key("row_separator"):
            joinwith = options["row_separator"]
        
        output += joinwith.join(outlist)
        
    return output

def returnerror(msg):
    return "{\"error\":\"%s\"}" % msg
            
def process_sql(ep):
    filename = "%s/datasources/%s.ds" % (web_root, ep["datasource"])
    with open(filename, 'r') as f_in:
        ds_json = f_in.read()
        
    ds = json.loads(ds_json)  
    
    result = None
    if ds["provider"] == "mysql":
        result = mysql_exec(ds, ep)
    if ds["provider"] == "mssql":
        result = mssql_exec(ds, ep)
                    
    return result
    
def mssql_exec(ds, ep):
    try:
        from pytds import dbapi

        server = ds["server"]
        port = (int(ds["port"]) if ds["port"] else 1433)
        uid = ds["uid"]
        pwd = ds["pwd"]
        database = ds["database"]
        sql = ep["code"]  # would do variable replacement first
        
        print "(sql server) Executing on [%s\%s]\n%s" % (ds["server"], ds["database"], ep["code"])

        conn = dbapi.connect(server=server, port=port, user=uid, password=pwd, database=database)
        
        
        if conn:
            # a select or an exec?
            method = "select"
            if ep.has_key("method"):
                method = ep["method"]
            
            if method == "select":
                conn.as_dict = True
                if ep.has_key("record_format"):
                    if ep["record_format"] == "list":
                        conn.as_dict = False

                c.execute(sql)
                result = c.fetchall()
                c.close()
            elif method == "exec":
                c = conn.cursor()
                c.execute(sql)
                conn.commit()
                result = {"result":"true"}
                c.close()
            else:
                result = {"result":"Invalid SQL method."}
        else:
            result = {"result":"Unable to establish connection to datasource."}

        return result

    except Exception as e:
        msg = "Could not connect to the database. Error message -> %s" % (e)
        raise Exception(msg)

def mysql_exec(ds, ep):
    try:
        import pymysql

        server = ds["server"]
        port = (int(ds["port"]) if ds["port"] else 3306)
        uid = ds["uid"]
        pwd = ds["pwd"]
        database = ds["database"]
        sql = ep["code"]  # would do variable replacement first
        
        print "(mysql) Executing on [%s\%s]\n%s" % (ds["server"], ds["database"], ep["code"])
        conn = pymysql.connect(host=server, port=int(port),
            user=uid, passwd=pwd, db=database)

        if conn:
            conn.autocommit(1)
        
            # a select or an exec?
            method = "select"
            if ep.has_key("method"):
                method = ep["method"]
            
            if method == "select":
                if ep.has_key("record_format"):
                    if ep["record_format"] == "list":
                        c = conn.cursor()
                    else:
                        c = conn.cursor(pymysql.cursors.DictCursor)
                else:
                    c = conn.cursor(pymysql.cursors.DictCursor)
    
                c.execute(sql)
                result = c.fetchall()
            elif method == "exec":
                c = conn.cursor()
                c.execute(sql)
                conn.commit()
                result = {"result":"true"}
            else:
                result = {"result":"Invalid SQL method."}
        else:
            result = {"result":"Unable to establish connection to datasource."}

        return result
        
    except Exception, ex:
        raise Exception(ex)
    finally:
        if conn and conn.socket:
            conn.close()

def process_extension(ep):
    extmodule = ep["extension"]
    
    try:
        mod = importlib.import_module(extmodule)
    except ImportError as ex:
        msg = "Extension module [%s] does not exist." % extmodule
        raise Exception(msg)

    if hasattr(mod, "execute"):
        method_to_call = getattr(mod, "execute", None)
        # we pass a pointer to the TaskEngine instance itself, so the command code has access to everything!
        # also pass in the logger, since it's global and not a TE property
        return method_to_call(ep, web.input())
    else:
        raise Exception("Extension module does not contain an 'execute' function.")
    
    
class BetterEncoder(json.JSONEncoder):
    def default(self, o):
        # decimals
        if isinstance(o, decimal.Decimal):
            return float(o)
        
        # date time
        if hasattr(o, 'isoformat'):
            return o.isoformat()
        else:
            return str(o)

        return super(BetterEncoder, self).default(o)


if __name__ == "__main__":
    # setting this to True shows exceptions to the client.
    web.config.debug = True
    app.run()
