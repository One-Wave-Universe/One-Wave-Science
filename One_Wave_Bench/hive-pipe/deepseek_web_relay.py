#!/usr/bin/env python3
"""Free DeepSeek web-session relay for One-Wave Brain Buddy."""
from __future__ import annotations
import argparse, json, os, re, threading, time, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

DEFAULT_BIND=os.environ.get("DEEPSEEK_WEB_RELAY_BIND","192.168.55.100")
DEFAULT_PORT=int(os.environ.get("DEEPSEEK_WEB_RELAY_PORT","3000"))
DEFAULT_PROFILE=Path(os.environ.get("DEEPSEEK_WEB_FIREFOX_PROFILE",str(Path.home()/".local/state/one-wave-deepseek-web/firefox-profile"))).expanduser()
FIREFOX=os.environ.get("DEEPSEEK_WEB_FIREFOX_BIN","/snap/firefox/current/usr/lib/firefox/firefox")
GECKO=os.environ.get("DEEPSEEK_WEB_GECKODRIVER","/snap/firefox/current/usr/lib/firefox/geckodriver")
ALLOWED={x.strip() for x in os.environ.get("DEEPSEEK_WEB_RELAY_ALLOWED_CLIENTS","127.0.0.1,192.168.55.1").split(",") if x.strip()}

PROTOCOL="""You are DeepSeek Brain Buddy behind a local browser relay.
You do not have direct shell access. The caller can execute only the listed tools.
If you need a tool, respond with ONLY one JSON object:
{"tool_call":{"name":"TOOL_NAME","arguments":{...}}}
Do not wrap it in Markdown or add explanation. After a tool result appears in
the transcript, request another tool or give the final answer normally.
Never claim a tool ran until its result is present. Use repository authority
before interpretation.
"""

def imports():
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    return webdriver,Keys,Options,Service,WebDriverWait

def tools_compact(tools):
    out=[]
    for item in tools or []:
        fn=item.get("function") if isinstance(item,dict) else None
        if isinstance(fn,dict):
            out.append({"name":fn.get("name"),"description":fn.get("description",""),"parameters":fn.get("parameters",{})})
    return out

def render(messages,tools):
    parts=[PROTOCOL,"AVAILABLE TOOLS:\n"+json.dumps(tools_compact(tools),ensure_ascii=False),"TRANSCRIPT:"]
    for msg in messages or []:
        if not isinstance(msg,dict): continue
        content=msg.get("content","")
        if isinstance(content,list): content=json.dumps(content,ensure_ascii=False)
        parts.append(f"{str(msg.get('role','unknown')).upper()}: {content}")
    parts.append("Respond to the last turn. Use exactly one tool_call JSON object if a tool is required; otherwise give the final answer.")
    return "\n\n".join(parts)

def parse_call(text):
    s=text.strip()
    m=re.fullmatch(r"```(?:json)?\s*(.*?)\s*```",s,re.S|re.I)
    if m: s=m.group(1).strip()
    try: obj=json.loads(s)
    except json.JSONDecodeError: return None
    call=obj.get("tool_call") if isinstance(obj,dict) else None
    if not isinstance(call,dict): return None
    name,args=call.get("name"),call.get("arguments",{})
    return (name,args) if isinstance(name,str) and name and isinstance(args,dict) else None

class Browser:
    def __init__(self,profile):
        webdriver,Keys,Options,Service,Wait=imports()
        self.Keys,self.Wait=Keys,Wait
        opts=Options(); opts.binary_location=FIREFOX; opts.add_argument("-headless"); opts.profile=str(profile)
        self.driver=webdriver.Firefox(options=opts,service=Service(GECKO))
        self.lock=threading.Lock()
    def close(self):
        try:self.driver.quit()
        except Exception:pass
    def ask(self,prompt,timeout=180):
        with self.lock:
            d=self.driver; d.get("https://chat.deepseek.com/")
            ta=self.Wait(d,45).until(lambda x:x.find_element("tag name","textarea"))
            before=len(d.find_elements("css selector",".ds-assistant-message-main-content"))
            ta.click(); ta.send_keys(prompt); ta.send_keys(self.Keys.ENTER)
            deadline=time.monotonic()+timeout; last=""; stable=None
            while time.monotonic()<deadline:
                items=d.find_elements("css selector",".ds-assistant-message-main-content")
                if len(items)>before:
                    cur=items[-1].text.strip()
                    if cur:
                        if cur==last:
                            stable=stable or time.monotonic()
                            if time.monotonic()-stable>=2:return cur
                        else:last,stable=cur,time.monotonic()
                time.sleep(.5)
            if last:return last
            raise RuntimeError("Timed out waiting for DeepSeek web response")

class Handler(BaseHTTPRequestHandler):
    server_version="OneWaveDeepSeekWebRelay/1"
    def log_message(self,fmt,*args): print(time.strftime("%FT%T"),self.client_address[0],fmt%args,flush=True)
    def allowed(self): return self.client_address[0] in ALLOWED
    def sendj(self,status,obj):
        raw=json.dumps(obj,ensure_ascii=False).encode()
        self.send_response(status); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        if not self.allowed(): return self.sendj(403,{"error":"client not allowed"})
        if self.path=="/health": return self.sendj(200,{"ok":True,"transport":"deepseek-free-web-firefox","bind":self.server.server_address[0],"allowed_clients":sorted(ALLOWEDI)})
        return self.sendj(404,{"error":"not found"})
    def do_POST(self):
        if not self.allowed(): return self.sendj(403,{"error":"client not allowed"})
        if self.path!="/v1/chat/completions": return self.sendj(404,{"error":"not found"})
        try:
            n=int(self.headers.get("Content-Length","0"))
            if n<=0 or n>1000000: raise ValueError("invalid request length")
            p=json.loads(self.rfile.read(n))
            text=self.server.browser.ask(render(p.get("messages",[]),p.get("tools",[])))
            call=parse_call(text); msg={"role":"assistant","content":"" if call else text}
            if call:
                name,args=call
                msg["tool_calls"]=[{"id":"web-"+uuid.uuid4().hex[:16],"type":"function","function":{"name":name,"arguments":json.dumps(args,separators=(",",":"))}}]
            return self.sendj(200,{"id":"webrelay-"+uuid.uuid4().hex,"object":"chat.completion","choices":[{"index":0,"message":msg,"finish_reason":"tool_calls" if call else "stop"}]})
        except Exception as e:return self.sendj(500,{"error":str(e)})

class Server(ThreadingHTTPServer):
    daemon_threads=True
    def __init__(self,addr,browser): super().__init__(addr,Handler); self.browser=browser

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--bind",default=DEFAUL_BIND); ap.add_argument("--port",type=int,default=DEFAULT_PORT); ap.add_argument("--profile",type=Path,default=DEFAULT_PROFILE); a=ap.parse_args()
    b=Browser(a.profile.expanduser()); s=Server((a.bind,a.port),b)
    print(json.dumps({"status":"DEEPSEEK_FREE_WEB_RELAY_READY","bind":a.bind,"port":a.port,"allowed_clients":sorted(ALLOWED)}),flush=True)
    try:s.serve_forever()
    finally:b.close(); s.server_close()
if __name__=="__main__":main()
