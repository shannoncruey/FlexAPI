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
stable and easy to configure REST API that can be easily hooked into existing application.

API "endpoints" are defined in simple JSON files.  Endpoints can access different "datasources", also defined in JSON files.

FlexAPI could very easily evolve into a content delivery system.  This is not the goal.  However, any web
developer could easily use FlexAPI along with "Web 2.0" tools such as jQuery to quickly create any type 
of user experience.

FlexAPI is currently a very young project, but we hope it will rapidly evolve into the beta phase.


DEPENDENCIES:
------------
* The [web.py](http://webpy.org/) framework.
* [PyMySql](https://github.com/petehunt/PyMySQL/) for MySql access.

TODO:
----
These are items on the short list:
* A Tutorial
* Request Authentication
* MS SQL Server support
* Oracle support
* A single installer that includes all dependencies.