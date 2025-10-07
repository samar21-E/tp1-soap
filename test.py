from spyne import Application, ServiceBase, rpc
from spyne.model.primitive import Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

class TestService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def Hello(ctx, name):
        return f"Hello {name} from SOAP service!"

application = Application([TestService],
    'test',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)

if __name__ == '__main__':
    print("Starting minimal SOAP service on http://localhost:8000")
    print("WSDL: http://localhost:8000/?wsdl")
    try:
        server = make_server('0.0.0.0', 8000, wsgi_app)
        print("Server started successfully! Press Ctrl+C to stop.")
        server.serve_forever()
    except Exception as e:
        print(f"Failed to start server: {e}")
