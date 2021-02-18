# Copyright (c) 2021 Philipp Hochkamp
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import asyncio
import yaml
import json
from aiosmtpd.controller import Controller
import logging
import requests

class HttpHandler:
    def __init__(self, payload, headers, url):
        self.payload = payload
        self.headers = headers
        self.url = url

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        envelope.rcpt_tos.append(address)
        return '250 OK'
    async def handle_DATA(self, server, session, envelope):
        mess =  "New Mail:\n"
        for ln in envelope.content.decode('utf8', errors='replace').splitlines():
            mess += ln.strip()+'\n'
        print(mess)
        print(self.payload)
        pl = self.payload % mess
        pl = pl.replace('\n', '\\n')
        print(pl)
        r = requests.post(self.url, data=pl, headers=self.headers)
        print(r.text)
        return '250 Message accepted for delivery'

def main():
    with open(r'./config.yaml') as file:
        config = yaml.full_load(file)
    logging.basicConfig(level=logging.DEBUG)
    print(f"Starting HttpHandler with config {config}")
    controller = Controller(HttpHandler(payload=config["http"]["payload"], headers=config["http"]["headers"], url=config["http"]["url"]))
    controller.hostname = config["smtp"]["hostname"]
    controller.port = config["smtp"]["port"]
    controller.start()
    print(f"HttpHandler started  on {controller.hostname}:{controller.port}")
    loop = asyncio.get_event_loop()
    loop.run_forever()

if __name__ == '__main__':
    main()
