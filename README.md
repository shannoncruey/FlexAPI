FlexAPI
=======

FlexAPI is a simple framework that allows you to quickly and easily create a REST API on a relational database.

DESCRIPTION
-----------
There are thousands of enterprise, custom, proprietary and legacy application out in the world today.  Many of these
applications are performing their purposes quite well, and will not be retired any time soon.  However, as 
the world marches forward, Application administrators are increasingly being tasked with creating new and
'modern' ways to interface with these legacy applications.

Enter FlexAPI!  Our goal is simple - to provide a robust,
stable and easy to configure REST API that can be easily hooked into an existing application.

API "endpoints" are defined in simple configuration files.  Endpoints can access different "datasources", also defined in configuration files.

FlexAPI could very easily evolve into a content delivery system, but this is *not the goal*.  However, since FlexAPI is built
on the Web.py framework, any web
developer could easily use FlexAPI along with tools such as jQuery to quickly create any type 
of end user experience.

FlexAPI is currently a very young project, but we hope it will rapidly evolve into the beta phase.


DEPENDENCIES:
------------
* The [web.py](http://webpy.org/) framework.
* [PyMySql](https://github.com/petehunt/PyMySQL/) for MySql access.
* [pytds](https://github.com/denisenkom/pytds) for MS SQL Server access.
* [cx_Oracle](http://cx-oracle.sourceforge.net/) for Oracle access.

TODO:
----
These are items on the short list:
* A Tutorial
* Request Authentication
* A single installer that includes all dependencies.