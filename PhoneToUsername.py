import string
import requests, json, secrets, uuid, binascii, time, random
import httpx, asyncio
from user_agent import generate_user_agent
from MedoSigner import Argus, Ladon, md5, Gorgon
import urllib

PROXY_INPUT = input("Enter Proxy (or press Enter to skip. Format: http://proxy): ").strip()
GLOBAL_PROXIES = {"http": PROXY_INPUT, "https": PROXY_INPUT} if PROXY_INPUT else None
HTTPX_PROXIES = PROXY_INPUT if PROXY_INPUT else None

def sign(params: str = "", payload: str = "", sec_device_id: str = "AadCFwpTyztA5j9L" + ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(9)), cookie: str = "", aid: int = 1233, license_id: int = 1611921764, sdk_version_str: str = 'v05.00.06-ov-android', sdk_version: int = 167775296, platform: int = 0, unix: int = int(round(time.time()))):
    params = urllib.parse.urlencode(params) if isinstance(params, dict) else params
    payload = urllib.parse.urlencode(payload) if isinstance(payload, dict) else (payload or "")
    x_ss_stub = md5(payload.encode('utf-8')).hexdigest() if payload != None else None
    return Gorgon(params, unix, payload, cookie).get_value() | {
        'content-length': str(len(payload)),
        'x-ss-stub': x_ss_stub.upper(),
        'x-ladon': Ladon.encrypt(int(unix), license_id, aid),
        'x-argus': Argus.get_sign(params, x_ss_stub, int(unix),
                platform=platform,
                aid=aid,
                license_id=license_id,
                sec_device_id=sec_device_id,
                sdk_version=sdk_version_str, 
                sdk_version_int=sdk_version
            )}

class PhoneToUsernameTikTok:
   def __init__(self, number: str) -> None:
      self.number = number
      self.secret = secrets.token_hex(16)
      self.client = self.client_builder()
      self.xor_number = self.xor(self.number)
      self.params = self.__get_param()
      self.cookies = {"passport_csrf_token": self.secret, "passport_csrf_token_default": self.secret, "install_id": self.params["iid"]}
      
   def client_builder(self) -> httpx.AsyncClient:
       if HTTPX_PROXIES:
           return httpx.AsyncClient(http2=True, follow_redirects=True, proxy=HTTPX_PROXIES)
       return httpx.AsyncClient(http2=True, follow_redirects=True)
       
   def xor(self, string: str) -> str:
      return "".join([hex(ord(c) ^ 5)[2:] for c in string])
      
   def __get_param(self) -> dict:
       return {
        "request_tag_from": "h5",
        "fixed_mix_mode": "1",
        "mix_mode": "1",
        "account_param": self.xor_number,
        "scene": "1",
        "device_platform": "android",
        "os": "android",
        "ssmix": "a",
        "type": "3736",
        "_rticket": str(round(int(time.time()*1000))),
        "cdid": str(uuid.uuid4()),
        "channel": "googleplay",
        "aid": "1233",
        "app_name": "musical_ly",
        "version_code": "370805",
        "version_name": "37.8.5",
        "manifest_version_code": "2023708050",
        "update_version_code": "2023708050",
        "ab_version": "37.8.5",
        "resolution": "1600*900",
        "dpi": "240",
        "device_type": "SM-G998B",
        "device_brand": "samsung",
        "language": "en",
        "os_api": "28", 
        "os_version": "9",
        "ac": "wifi",
        "is_pad": "0",
        "current_region": "TW",
        "app_type": "normal",
        "sys_region": "US",
        "last_install_time": str(round(int(time.time()*1000))),
        "mcc_mnc": "46692",
        "timezone_name": "Asia/Baghdad",
        "carrier_region_v2": "466",
        "residence": "TW",
        "app_language": "en",
        "carrier_region": "TW",
        "timezone_offset": "10800",
        "host_abi": "arm64-v8a",
        "locale": "en-GB",
        "ac2": "wifi",
        "uoo": "1",
        "op_region": "TW",
        "build_number": "37.8.5",
        "region": "GB",
        "ts": str(round(int(time.time()))),
        "iid": str(random.randint(7400000000000000000, 7499999999999999999)),
        "device_id": str(random.randint(7400000000000000000, 7499999999999999999)),
        "openudid": str(uuid.uuid4().hex[:6]),
        "support_webview": "1",
        "okhttp_version": "4.2.210.6-tiktok",
        "use_store_region_cookie": "1",
        "app_version": "37.8.5"}

   def __get_token(self, email: str) -> str:
    headers = {
        'User-Agent': str(generate_user_agent()),
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'Referer': 'https://mail.tm/',
        'Origin': 'https://mail.tm',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Connection': 'keep-alive',
        'Priority': 'u=4',
    }
    json_data = {
        'address': email,
        'password': "NtroAtro", 
    }
    response = requests.post('https://api.mail.tm/token', headers=headers, json=json_data, proxies=GLOBAL_PROXIES)
    try:
        return response.json()["token"]
    except:
        return None

   async def __get_email(self) -> dict[str:str, str:str]:
    headers = {
        'User-Agent': str(generate_user_agent()),
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'Referer': 'https://mail.tm/',
        'Origin': 'https://mail.tm',
        'Sec-Fetch-Dest': 'empty',
        'Seccd-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Connection': 'keep-alive',
        'Priority': 'u=0',
    }
    json_data = {
        'address': "".join(random.choices(string.ascii_lowercase + string.digits, k=12)) + '@web-library.net',
        'password': 'NtroAtro',
    }
    response = requests.post('https://api.mail.tm/accounts', headers=headers, json=json_data, proxies=GLOBAL_PROXIES)
    try:
        return {"id": response.json()["id"], "email": response.json()["address"]}
    except:
        return {"id": None, "email": None}

   async def __get_inbox(self, email: str, token: str, id: str) -> httpx.Response.json:
       try:
           headers = {
                'User-Agent': str(generate_user_agent()),
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://mail.tm/',
                'Origin': 'https://mail.tm',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'authorization': 'Bearer ' + token,
                'Connection': 'keep-alive',
                'If-None-Match': '{}'.format(id),
                'Priority': 'u=0',
            }
           response = requests.get('https://api.mail.tm/messages', headers=headers, proxies=GLOBAL_PROXIES)
           return response.json()
       except json.JSONDecodeError as e:
            return e
    
   def __get_header(self, signature, parma: dict[str:str, str:str]) -> httpx.Headers:
      return {
        'User-Agent': "com.zhiliaoapp.musically/2023708050 (Linux; U; Android 9; en_" + parma["region"] + "; " + parma["device_type"] + "; Build/SP1A.210812.016;tt-ok/3.12.13.16)",
        'Accept': "application/json, text/plain, */*",
        'x-ss-stub': signature['x-ss-stub'],
        'x-tt-dm-status': "login=1;ct=1;rt=1",
        'x-ss-req-ticket': signature['x-ss-req-ticket'],
        'x-ladon': signature['x-ladon'],
        'x-khronos': parma["ts"], 
        'x-argus': signature['x-argus'],
        'x-gorgon': signature['x-gorgon'],
        'content-type': "application/x-www-form-urlencoded",
        'content-length': '0', 
        }
 
   async def __ticket_request(self) -> httpx.Response:
      for host in [
        "api16-normal-va.tiktokv.com",
        "api16-normal-c-alisg.tiktokv.com",
        "api16-normal-zr.tiktokv.com",
        "api31-normal-useast2a.tiktokv.com",
        "api16-normal-useast5.us.tiktokv.com",
        "api19-normal-useast8.us.tiktokv.com",
        "api31-normal-alisg.tiktokv.com",
        "api16-normal-c-tw.tiktokv.com",
        "api31-normal-zr.tiktokv.com",
        "api16-normal-no1a.tiktokv.eu",
        "api19-normal-ycru.tiktokv.com",
        "api16-normal.tiktokv.com",
        "api16-normal.ttapis.com",
        "api31-normal.tiktokv.com",
        "api22-normal.tiktokv.com",
        "api19-normal.tiktokv.com",
        "api-normal.tiktokv.com",
        "api21-normal.tiktokv.com",
        "api16-core.tiktokv.com",
        "api16-core-va.tiktokv.com",
        "api32-normal.tiktokv.com",
        "api33-normal.tiktokv.com"
    ]:
        try:
            signature = sign(params=self.params, payload="", aid=1233)
            response = await self.client.post("https://" + host + "/passport/account_lookup/mobile/", headers=self.__get_header(signature, self.params), params=self.params, cookies=self.cookies)
            # print(response.json())    
            if "'verify_center_decision_conf'" in response.text:
                return "Captch"
            if response.json()["data"] == None:
                return None
            return response
        except Exception as e:
            continue

   async def send_code(self) -> str:
      tmMail = await self.__get_email() 
      email = tmMail["email"]
      if email == None:
          return await self.send_code()
      
      id = tmMail["id"]
      token = self.__get_token(email=email)
      response_ticket = await self.__ticket_request() 
      if response_ticket == None:
          return "Phone Number Not found in TikTok"
      if response_ticket == "Captch":
          return await self.send_code()
      try:
          ticket = response_ticket.json()["data"]["accounts"][0]["passport_ticket"]
      except Exception as e:
        return await self.send_code()
          
      host = str(response_ticket.url).split("/passport/account_lookup/mobile/")[0].split("https://")[1]
      
      self.params.update({"not_login_ticket": ticket, "email": self.xor(email), "ts": str(round(int(time.time()))), "_rticket": str(round(int(time.time()*1000)))})
      signature = sign(params=self.params, payload="", aid=1233)
      
      response = await self.client.post("https://" + host + "/passport/email/send_code/", headers=self.__get_header(signature, self.params), params=self.params, cookies=self.cookies)
      if "email_ticket" in response.text:
          await asyncio.sleep(5)
          inbox = await self.__get_inbox(email=email, token=token, id=id)
          username = await self.__extraxt_username(inbox)
          return username
      else:
          return await self.send_code()
          
   async def __extraxt_username(self, inbox: httpx.Response.json) -> str:
       try:
            username = inbox["hydra:member"][0]["intro"].split("code Hi ")[1].split(",")[0]
            return username
       except Exception as e:
            return str(e)

if __name__ == "__main__":
    username = asyncio.run(PhoneToUsernameTikTok(input("Enter Phone Number with country key :")).send_code())
    if username == "Phone Number Not found in TikTok":
        print("Phone Number Not found in TikTok")
    else:
        print("username -> ", username)