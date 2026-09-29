#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,threading,time,uuid
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
DEFAULT_BIND=os.environ.get("GEMINI_WEB_RELAY_BIND","192.168.55.100")
DEFAULT_PORT=int(os.environ.get("GEMINI_WEB_RELAY_PORT","3001"))
DEFAULT_PROFILE=Path(os.environ.get("GEMINI_WEB_FIREFOX_PROFILE",str(Path.home()/".local/state/one-wave-gemini-web/firefox-profile"))).expanduser()
FIREFOX=os.environ.get("GEMINI_WEB_FIREFOX_BIN","/snap/firefox/current/usr/lib/firefox/firefox")
GECKO=os.environ.get("GEMINI_WEB_GECKODRIVER","/snap/firefox/current/usr/lib/firefox/geckodriver")
ALLOWED={x.strip() for x in os.environ.get("GEMINI_WEB_RELAY_ALLOWED_CLIENTS","127.0.0.1,192.168.55.1").split(",") if x.strip()}
PROTOCOL="""You are Gemini Brain Buddy behind a local browser relay.
You do not have direct shell access. Use only the listed tools.
For a tool, respond with ONLY one JSON object shaped as:
{"tool_call":{"name":"TOOL_NAME","arguments":{}}}
Never claim a tool ran until its result is present.
Reference canonical One-Wave files and I-06 metadata first. If external research
is needed, keep its provenance distinct and return it to the exact repo claim/test.
"""
def imports():
 from selenium import webdriver
 from selenium.webdriver.common.keys import Keys
 from selenium.webdriver.firefox.options import Options
 from selenium.webdriver.firefox.service import Service
 from selenium.webdriver.support.ui import WebDriverWait
 return webdriver,Keys,Options,Service,WebDriverWait
def compact(tools):
 out=[]
 for item in tools or []:
  fn=item.get("function") if isinstance(item,dict) else None
  if isinstance(fn,dict):out.append({"name":fn.get("name"),"description":fn.get("description",""),"parameters":fn.get("parameters",{})})
 return out
def render(messages,tools):
 parts=[PROTOCOL,"AVAILABLE TOOLS:\n"+json.dumps(compact(tools),ensure_ascii=False),"TRANSCRIPT:"]
 for msg in messages or []:
  if not isinstance(msg,dict):continue
  c=msg.get("content","")
  if isinstance(c,list):c=json.dumps(c,ensure_ascii=False)
  parts.append(f"{str(msg.get('role','unknown')).upper()}: {c}")
 parts.append("Use exactly one tool_call JSON object if a tool is required; otherwise give the final answer.")
 return "\n\n".join(parts)
def parse_call(text):
 try:o=json.loads(text.strip())
 except json.JSONDecodeError:return None
 c=o.get("tool_call") if isinstance(o,dict) else None
 if not isinstance(c,dict):return None
 n,a=c.get("name"),c.get("arguments",{})
 return (n,a) if isinstance(n,str) and n and isinstance(a,dict) else None
class Browser:
 def __init__(self,profile):
  webdriver,Keys,Options,Service,Wait=imports();self.Keys,self.Wait=Keys,Wait
  o=Options();o.binary_location=FIREFOX;o.add_argument("-headless");o.profile=str(profile)
  self.driver=webdriver.Firefox(options=o,service=Service(GECKO));self.lock=threading.Lock()
 def close(self):
  try:self.driver.quit()
  except Exception:pass
 def ask(self,prompt,timeout=180):
  with self.lock:
   d=self.driver;d.get("https://gemini.google.com/app")
   box=self.Wait(d,45).until(lambda x:x.find_element("css selector",'[contenteditable=true][aria-label="Enter a prompt for Gemini"]'))
   before=len(d.find_elements("css selector",".model-response-text"))
   box.click();box.send_keys(prompt);box.send_keys(self.Keys.ENTER)
   deadline=time.monotonic()+timeout;last="";stable=None
   while time.monotonic()<deadline:
    items=d.find_elements("css selector",".model-response-text")
    if len(items)>before:
     cur=items[-1].text.strip()
     if cur:
      if cur==last:
       stable=stable or time.monotonic()
       if time.monotonic()-stable>=2:return cur
      else:last,stable=cur,time.monotonic()
    time.sleep(.5)
   if last:return last
   raise RuntimeError("Timed out waiting for Gemini web response")
class Handler(BaseHTTPRequestHandler):
 def log_message(self,fmt,*args):print(time.strftime("%FT%T"),self.client_address[0],fmt%args,flush=True)
 def allowed(self):return self.client_address[0] in ALLOWED
 def sendj(self,status,obj):
  raw=json.dumps(obj,ensure_ascii=False).encode();self.send_response(status);self.send_header("Content-Type","application/json");self.send_header("Content-Length",str(len(raw)));self.end_headers();self.wfile.write(raw)
 def do_GET(self):
  if not self.allowed():return self.sendj(403,{"error":"client not allowed"})
  if self.path=="/health":return self.sendj(200,{"ok":True,"transport":"gemini-free-web-firefox","bind":self.server.server_address[0],"allowed_clients":sorted(ALLOWED)})
  return self.sendj(404,{"error":"not found"})
 def do_POST(self):
  if not self.allowed():return self.sendj(403,{"error":"client not allowed"})
  if self.path!="/v1/chat/completions":return self.sendj(404,{"error":"not found"})
  try:
   n=int(self.headers.get("Content-Length","0"));p=json.loads(self.rfile.read(n))
   text=self.server.browser.ask(render(p.get("messages",[]),p.get("tools",[])));call=parse_call(text);msg={"role":"assistant","content":"" if call else text}
   if call:
    name,args=call;msg["tool_calls"]=[{"id":"web-"+uuid.uuid4().hex[:16],"type":"function","function":{"name":name,"arguments":json.dumps(args,separators=(",",":"))}}]
   return self.sendj(200,{"choices":[{"index":0,"message":msg,"finish_reason":"tool_calls" if call else "stop"}]})
  except Exception as e:return self.sendj(500,{"error":str(e)})
class Server(ThreadingHTTPServer):
 daemon_threads=True
 def __init__(self,addr,browser):super().__init__(addr,Handler);self.browser=browser
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--bind",default=DEFAULT_BIND);ap.add_argument("--port",type=int,default=DEFAULT_PORT);ap.add_argument("--profile",type=Path,default=DEFAULT_PROFILE);a=ap.parse_args()
 b=Browser(a.profile.expanduser());s=Server((a.bind,a.port),b)
 print(json.dumps({"status":"GEMINI_FREE_WEB_RELAY_READY","bind":a.bind,"port":a.port}),flush=True)
 try:s.serve_forever()
 finally:b.close();s.server_close()
if __name__=="__main__":main()
