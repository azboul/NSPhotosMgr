from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

###### function list ############

# Check Connection
def IsConnect():
    return True

# Register a function under a different name
def adder_function(x,y):
    return x + y

# Register an instance; all the methods of the instance are
# published as XML-RPC methods (in this case, just 'mul').
class MyFuncs:
    def mul(self, x, y):
        return x * y
#################################

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

def Run():
    # Create server
    server = SimpleXMLRPCServer(("localhost", 8000),
                                requestHandler=RequestHandler)
    server.register_introspection_functions()

    # Register pow() function; this will use the value of
    # pow.__name__ as the name, which is just 'pow'.
    server.register_function(pow)
    server.register_function(adder_function, 'add')
    server.register_instance(MyFuncs())
    server.register_function(IsConnect, 'IsConnect')

    # Run the server's main loop
    server.serve_forever()

if __name__ == '__main__':
    Run()
