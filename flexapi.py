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
            if ep["type"] == "sql":
                data = process_sql(ep)
            
            if ep.has_key("return"):
                if ep["return"] == "json":
                    # print str(data)
                    js = json.dumps(data, cls=BetterEncoder, sort_keys=True, indent=4)
                    if ep.has_key("prefix"):
                        js = ep["prefix"] + js
                    if ep.has_key("suffix"):
                        js += ep["suffix"]
    
                    return js
                elif ep["return"] == "format":
                    """Use row_template and perform python 'format'. on each row."""
                    try:
                        iterator = iter(data)
                    except TypeError:
                        # data is not iterable, just return it
                        return str(data)
                    else:
                        # data is a rowset
                        txt = ""
                        for row in data:
                            # the elements in the row may be a dict, or a tuple
                            # only a dict will have 'itervalues'
                            try:
                                fields = row.itervalues()
                            except AttributeError:
                                fields = iter(row)
    
                            # turn the fields into a list so we can use them as format arguments
                            outlist = []
                            fieldlist = []
                            for field in fields:
                                fieldlist.append(field)
    
                            print tuple(fieldlist)                            
                            if ep.has_key("row_template"):
                                if ep["row_template"]:
                                    print ep["row_template"]
                                    outlist.append(ep["row_template"].format(*fieldlist))
                                else:
                                    print "Format return type requires a 'row_template'."
                            else:
                                print "Format return type requires a 'row_template'."
                           
                            txt += "".join(outlist)
    
                        if ep.has_key("prefix"):
                            txt = ep["prefix"] + txt
                        if ep.has_key("suffix"):
                            txt += ep["suffix"]
                        
                        return txt
                elif ep["return"] == "text":
                    """Kinda strange, but just concatenate the whole dataset into text. No formatting."""
                    try:
                        iterator = iter(data)
                    except TypeError:
                        # data is not iterable, just return it
                        return str(data)
                    else:
                        # data is a rowset
                        txt = ""
                        for row in data:
                            # the elements in the row may be a dict, or a tuple
                            # only a dict will have 'itervalues'
                            try:
                                fields = row.itervalues()
                            except AttributeError:
                                fields = iter(row)
    
                            outlist = []
                            for field in fields:
                                outlist.append(field)
                                
                            txt += "".join(outlist)
    
                        if ep.has_key("prefix"):
                            txt = ep["prefix"] + txt
                        if ep.has_key("suffix"):
                            txt += ep["suffix"]
                        
                        return txt
                                
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
                    
    return result
    
def mysql_exec(ds, ep):
    try:
        import pymysql

        server = ds["server"]
        port = (int(ds["port"]) if ds["port"] else 3306)
        uid = ds["uid"]
        pwd = ds["pwd"]
        database = ds["database"]
        sql = ep["code"] # would do variable replacement first
        
        print "Executing on [%s\%s]\n%s" % (ds["server"], ds["database"], ep["code"])

        conn = pymysql.connect(host=server, port=int(port), 
            user=uid, passwd=pwd, db=database)
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

        return result
        
    except Exception, ex:
        raise Exception(ex)
    finally:
        if conn.socket:
            conn.close()

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