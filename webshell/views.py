
# Create your views here.
import json

from channels.generic.websocket import WebsocketConsumer

from webshell.utils import K8SStreamThread, K8SApiTools


class SSHConsumer(WebsocketConsumer):

    def connect(self):
        self.name = self.scope["url_route"]["kwargs"]
        print('xxxx', self.scope)

        # kube exec
        self.stream = K8SApiTools(rw=True).create_attatch_pod_exec_stream()
        kub_stream = K8SStreamThread(self, self.stream)
        kub_stream.start()
        self.accept()

    def disconnect(self, close_code):
        self.stream.write_stdin('exit\r')

    def receive(self, text_data):
        text_data = json.loads(text_data)
        op = text_data.get('op')
        data = text_data.get('data')
        if op == 'stdin':
            self.stream.write_stdin(data)
        elif op == 'resize':
            rows = data.get("cols")
            cols = data.get("rows")
            self.stream.write_channel(4, json.dumps({"Height": int(rows), "Width": int(cols)}))
