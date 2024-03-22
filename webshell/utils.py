from threading import Thread

import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
from kubernetes.stream.ws_client import WSClient


TEST_128 = {
    "K8S_HOST": "https://api-server-128.youkun.cn:9443",
    "K8S_ADMIN_TOKEN": "xxxx",
    "K8S_TOKEN": "xxxxx",
    "K8S_TOKEN_READ": "xxxxx",
}


class K8SStreamThread(Thread):
    def __init__(self, websocket, container_stream):
        Thread.__init__(self)
        self.websocket = websocket
        self.stream = container_stream

    def run(self):
        while self.stream.is_open():
            if self.stream.peek_stdout():
                stdout = self.stream.read_stdout()
                self.websocket.send(stdout)
            elif self.stream.peek_stderr():
                stderr = self.stream.read_stderr()
                self.websocket.send(stderr)
        else:
            self.websocket.close()


class K8SApiTools(Thread):
    def __init__(self, rw: bool = False, admin: bool = False, cluster: str = "152"):
        self.admin = admin
        self.cluster = cluster
        self.rw = rw
        self.configuration = None
        cluster_info = TEST_128
        if admin:
            K8S_TOKEN = cluster_info.get("K8S_ADMIN_TOKEN", "")
        elif rw:
            K8S_TOKEN = cluster_info.get("K8S_TOKEN", "")
        else:
            K8S_TOKEN = cluster_info.get("K8S_TOKEN_READ", "")
        self.api_key = {"authorization": "Bearer " + K8S_TOKEN}
        self.api_host = cluster_info.get("K8S_HOST", "")
        self.verify_ssl = False
        # 初始化 Configuration
        self.k8s_configure()

    def k8s_configure(self):
        self.configuration = kubernetes.client.Configuration()
        self.configuration.api_key = self.api_key
        self.configuration.verify_ssl = self.verify_ssl
        self.configuration.host = self.api_host
        self.configuration.assert_hostname = False  # type: ignore
        # return self.configuration

    def get_core_api(self) -> kubernetes.client.CoreV1Api:
        with kubernetes.client.ApiClient(self.configuration) as api_client:
            core_api = None
            try:
                core_api = kubernetes.client.CoreV1Api(api_client)
            except ApiException as err:
                raise ApiException()
            return core_api

    def create_attatch_pod_exec_stream(
        self,
        namespace: str = "dcp",
        pod_name: str = "app-guard-admin-api-7cc7b8f97f-hzlw9",
        container: str = "app-guard-admin-api",
    ) -> WSClient:
        core_api = self.get_core_api()

        resp = None
        try:
            resp = core_api.read_namespaced_pod(name=pod_name, namespace=namespace)
        except ApiException as err:
            raise ValueError(str(err))

        try:
            exec_command = [
                "/bin/sh",
                "-c",
                # 'export LINES=30; export COLUMNS=80; '
                "TERM=xterm-256color; export TERM; [ -x /bin/bash ] "
                "&& ([ -x /usr/bin/script ] "
                '&& /usr/bin/script -q -c "/bin/bash" /dev/null || exec /bin/bash) '
                "|| exec /bin/sh",
            ]
            resp = stream(
                core_api.connect_get_namespaced_pod_exec,
                pod_name,
                namespace,
                container=container,
                command=exec_command,
                stderr=True,
                stdin=True,
                stdout=True,
                tty=True,
                _preload_content=False,
            )
        except ApiException as err:
            raise InterruptedError(str(err))
        return resp
