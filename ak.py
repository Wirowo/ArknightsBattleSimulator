import mitmproxy.http

class AKRedirect:

    def __init__(self):
        print('Addon for Redirecting Arknight [EN] Loaded !')

    def request(self, flow: mitmproxy.http.HTTPFlow):
        # Manually making the client errors out to prevent sending modified data back to server
        if 'gs.arknights.global' in flow.request.pretty_host or 'android.bugly.qq.com' in flow.request.pretty_host:
            flow.request.host = "localhost"
            flow.request.scheme = 'http'


addons = [
    AKRedirect()
]
