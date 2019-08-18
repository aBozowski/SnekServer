# SnekServer  
  
Web Server with rapid implementation of new pages and handlers.  
  
Python 3.7.3, standard libraries only.
  
Useful for small utilities or faking an API.  
  
## Configuration  
  
Edit the dictionary in config.py
  
## Creating new modules  
  
Create a new directory in the /modules directory named after the module.  
Inside the new directory, create a new script named after the module, and an empty \_\_init\_\_.py.
  
Nesting modules is supported.  
You can add new modules while the server is running. However, after the first time a request for a module is handled, you will need to restart the server for the changes to take effect.  
  
The script can implement any of the following methods for handling requests:  

```python  
def ROUTER_do_GET(self):  
def ROUTER_do_POST(self): 
def ROUTER_do_PUT(self):  
def ROUTER_do_PATCH(self): 
def ROUTER_do_DELETE(self):  
```  

See the home module for an example

Use self.ROUTER_ methods defined in Router.py to read request data and send responses.  
 
## Run  
  
To start the server:
```bash
python snekserver.py
```
  
The modules you implement will be available at http://\<HOST\>:\<PORT\>/\<new module name\>/  
