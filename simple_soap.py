from spyne import Application, ServiceBase, rpc
from spyne.model.primitive import Unicode, Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import socket

class TestService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Unicode)
    def SayHello(self, name, count):
        return f"Hello {name}! " * count

    @rpc(Integer, Integer, _returns=Integer)
    def AddNumbers(self, a, b):
        return a + b

# Create application
application = Application([TestService],
    'test.service',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)

if __name__ == '__main__':
    port = 8000
    
    # Test if we can bind to the port
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', port))
        sock.close()
        print(f"✅ Port {port} is available")
    except OSError as e:
        print(f"❌ Cannot use port {port}: {e}")
        print("Trying port 8080...")
        port = 8080
    
    print(f"🚀 Starting SOAP service on http://localhost:{port}")
    print(f"📄 WSDL: http://localhost:{port}/?wsdl")
    
    try:
        server = make_server('0.0.0.0', port, wsgi_app)
        print(f"✅ Server started successfully!")
        print("⏹️  Press Ctrl+C to stop")
        server.serve_forever()
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
