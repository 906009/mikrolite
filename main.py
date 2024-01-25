from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
import routeros_api
from kivymd.uix.menu import MDDropdownMenu
class MainMenu(Screen):
    pass
class Authorization(Screen):
    pass
class Internet(Screen):
    pass
class Local(Screen):
    pass
class Forward(Screen):
    pass
class Static(Screen):
    pass
class PPPoE(Screen):
    pass
class VPN(Screen):
    pass
class Other(Screen):
    pass
class Update(Screen):
    pass
class wifi(Screen):
    pass
class Manager(ScreenManager):
    pass
class MikroLiteApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.setup)
    def setup(self, *args):
        menu_items = [{"text": f"{i}","viewclass": "OneLineListItem","on_release": lambda x=f"{i}": self.menu_callback(x)} for i in range(1,14)]
        self.two = MDDropdownMenu(caller=self.root.get_screen('wifi').ids.wifi24_channel, items=menu_items, width_mult=4)
        menu_items = [{"text": f"{i}", "viewclass": "OneLineListItem","on_release": lambda x=f"{i}": self.menu_callback(x)} for i in range(36,148,4)]+[{"text": f"{i}", "viewclass": "OneLineListItem","on_release": lambda x=f"{i}": self.menu_callback(x)} for i in range(149,169,4)]
        self.five = MDDropdownMenu(caller=self.root.get_screen('wifi').ids.wifi5_channel, items=menu_items, width_mult=4)
    def menu_callback(self, text_item):
        print(text_item)
        if int(text_item) < 16:
            x = int(text_item)
            self.chastota_24.text = 2407 + 5 * x
        if int(text_item) > 16 and int(text_item) < 170:
            x = int(text_item)
            self.chastota_5.text = 5000 + 5 * x
    def standart(self):
        self.connection = routeros_api.RouterOsApiPool('192.168.88.1', username='Danil_64', password='66236623', port=8728, use_ssl=False,
                                                       ssl_verify=False, ssl_verify_hostname=False, ssl_context=None,
                                                       plaintext_login=True)
        self.api = self.connection.get_api()
        return self.api
    def connector(self):
        host = self.root.get_screen('Authorization').ids.ip_dns.text
        usr = self.root.get_screen('Authorization').ids.user.text
        pwr = self.root.get_screen('Authorization').ids.passwordv.text
        self.connection = routeros_api.RouterOsApiPool(host, username=usr, password=pwr, port=8728, use_ssl=False,
                                                       ssl_verify=False, ssl_verify_hostname=False, ssl_context=None,
                                                       plaintext_login=True)
        self.api = self.connection.get_api()
        return self.api, self.connection
    def static(self):
        address = self.root.get_screen('Static').ids.static_address.text
        gateway = self.root.get_screen('Static').ids.static_gateway.text
        res = self.api.get_resource('/system/script')
        index = str(res.get()).find("MikroLite_static")
        if index > 1:
            script_to_run = res.get(name="MikroLite_static")[0]
            self.api.get_binary_resource('/').call('system/script/run', {"number": script_to_run["id"].encode("utf-8")})
        else:
            res.add(name='MikroLite_static', source=":do command={/ip/address set [find interface=ether1] address="+address+"} on-error={/ip/address add interface=ether1 address="+address+"};:do command={/ip/route remove [find gateway="+gateway+"]};:do command={/ip/route add gateway="+gateway+" dst-address=0.0.0.0/0};:do command={/system script remove MikroLite_static}")
            script_to_run = res.get(name="MikroLite_static")[0]
            self.api.get_binary_resource('/').call('system/script/run', {"number": script_to_run["id"].encode("utf-8")})
    def static_remove(self):
        pass
    def twowifivkl(self):
        res = self.api.get_resource('/interface/wireless')
        index = str(res.get()).find("'default-name': 'wlan1'")
        if index > 0:
            index = str(res.get()).find("}")
            stroka = str(res.get())[:index]
            index = str(stroka).find("id")
            a = index + 6
            while a < len(str(stroka)):
                if str(stroka)[a] == "'":
                    break
                else:
                    a = a + 1
            idis = str(stroka)[index + 6:a]
            index = str(stroka).find("disabled': 'false'")
            if index > 0:
                res.set(id=idis, enabled='true')
                self.root.get_screen('wifi').ids.wifi_24.text = 'Вкл'
            else:
                res.set(id=idis, disabled='false')
                self.root.get_screen('wifi').ids.wifi_24.text = 'Выкл'
    def twowidth(self):
        width = self.root.get_screen('wifi').ids.wifi_24_XX.text
        if str(width).find("20/40") > 1:
            self.root.get_screen('wifi').ids.wifi_24_XX.text = '20mhz'
        elif str(width).find("20") > 1:
            self.root.get_screen('wifi').ids.wifi_24_XX.text = '20/40mhz-XX'
    def fivewidth(self):
        width = self.root.get_screen('wifi').ids.wifi_5_XX.text
        if str(width).find("20/40/80") > 1:
            self.root.get_screen('wifi').ids.wifi_5_XX.text = '20mhz'
        elif str(width).find("20/40") > 1:
            self.root.get_screen('wifi').ids.wifi_5_XX.text = '20/40/80mhz-XXXX'
        elif str(width).find("20") > 1:
            self.root.get_screen('wifi').ids.wifi_5_XX.text = '20/40mhz-XX'
    def twowifi(self):
        ssid = self.root.get_screen('wifi').ids.wifi24_ssid.text
        width = self.root.get_screen('wifi').wifi_24_XX.text
        res = self.api.get_resource('/system/script')
        index = str(res.get()).find("MikroLite_wifi_24")
        if index > 0:
            script_to_run = res.get(name="MikroLite_wifi_24")[0]
            self.api.get_binary_resource('/').call('system/script/run', {"number": script_to_run["id"].encode("utf-8")})
            self.sm.current = 'Authorization'
            self.connection.disconnect()
        else:
            res.add(name='MikroLite_wifi_24', source=":do command={/interface wireless set [find default-name=wlan1] ssid="+ssid+" channel-width="+width+" frequency="+self.chastota_24+" mode=ap-bridge band=2ghz-b/g/n country=no_country_set installation=indoor wmm-support=enabled frequency-mode=superchannel hw-protection-mode=rts-cts hw-retries=15 adaptive-noise-immunity=ap-and-client-mode};/system script remove MikroLite_wifi_24}")
            script_to_run = res.get(name="MikroLite_wifi_24")[0]
            self.api.get_binary_resource('/').call('system/script/run', {"number": script_to_run["id"].encode("utf-8")})
            self.sm.current = 'Authorization'
            self.connection.disconnect()
    def fivewifi(self):
        ssid = self.root.get_screen('wifi').ids.wifi5_ssid.text
        width = self.root.get_screen('wifi').wifi_5_XX.text
        res = self.api.get_resource('/system/script')
        index = str(res.get()).find("MikroLite_wifi_5")
        if index > 0:
            script_to_run = res.get(name="MikroLite_wifi_5")[0]
            self.api.get_binary_resource('/').call('system/script/run', {"number": script_to_run["id"].encode("utf-8")})
            self.sm.current = 'Authorization'
            self.connection.disconnect()
        else:
            res.add(name='MikroLite_wifi_5', source=":do command={/interface wireless set [find default-name=wlan2] ssid="+ssid+" channel-width="+width+" frequency="+self.chastota_5+" mode=ap-bridge band=5ghz-a/n/ac country=no_country_set installation=indoor wmm-support=enabled frequency-mode=superchannel hw-protection-mode=rts-cts hw-retries=15 adaptive-noise-immunity=ap-and-client-mode};/system script remove MikroLite_wifi_5}")
            script_to_run = res.get(name="MikroLite_wifi_5")[0]
            self.api.get_binary_resource('/').call('system/script/run', {"number": script_to_run["id"].encode("utf-8")})
            self.sm.current = 'Authorization'
            self.connection.disconnect()
    def fivewifivkl(self):
        res = self.api.get_resource('/interface/wireless')
        index = str(res.get()).rfind("'default-name': 'wlan2'")
        if index > 0:
            index = str(res.get()).find("{")
            stroka = str(res.get())[index:]
            index = str(stroka).find("id")
            a = index + 6
            while a < len(str(stroka)):
                if str(stroka)[a] == "'":
                    break
                else:
                    a = a + 1
            idis = str(stroka)[index + 6:a]
            index = str(stroka).find("disabled': 'false'")
            if index > 0:
                res.set(id=idis, disabled='true')
                self.root.get_screen('wifi').ids.wifi_5.text = 'Вкл'
            else:
                res.set(id=idis, disabled='false')
                self.root.get_screen('wifi').ids.wifi_5.text = 'Выкл'
    def wifisecurity(self):
        password = self.root.get_screen('wifi').ids.wifi_password.text
        res = self.api.get_resource('/interface/wireless/security-profiles')
        index = str(res.get()).find("default")
        if index > 1:
            a = index
            while a > 1:
                if str(res.get())[a] == "id":
                    break
                else:
                    a = a - 1
            b = a + 8
            while b < len(str(res.get())):
                if str(res.get())[b] == "'":
                    break
                else:
                    b = b + 1
            idis = str(res.get())[a + 8:b]
            while b < len(str(res.get())):
                if str(res.get())[b] == "}":
                    break
                else:
                    b = b + 1
            stroka = str(res.get())[a + 1:b]
            print(stroka)
            index = str(stroka).find("id")
            b = index + 6
            while b < len(str(stroka)):
                if str(stroka)[b] == "'":
                    break
                else:
                    b = b + 1
            idis = str(stroka)[index + 6:b]
            res.set(id=idis, authentication_types='wpa-psk,wpa2-psk', wpa_pre_shared_key=password, wpa2_pre_shared_key=password)
    def logout(self):
        self.sm.current = 'Authorization'
        self.connection.disconnect()
    def ntp(self):
        res = self.api.get_resource('/system/ntp/client')
        res.set(enabled='true')
        ntp = self.root.get_screen('Local').ids.local_ntp.text
        res.set(servers=ntp)
    def ntp_srv(self):
        res = self.api.get_resource('/system/ntp/server')
        index = str(res.get()).find("'enabled': 'true'")
        if index > 0:
            res.set(enabled='false', broadcast='false', multicast='false', manycast='false')
            self.root.get_screen('Local').ids.local_ntp_srv.text = 'Вкл'
        else:
            res.set(enabled='true', broadcast='true', multicast='true', manycast='true')
            self.root.get_screen('Local').ids.local_ntp_srv.text = 'Выкл'
    def doh(self):
        res = self.api.get_resource('/ip/dns')
        index = str(res.get()).find("ordns")
        if index > 0:
            res.set(use_doh_server='')
            self.root.get_screen('Local').ids.local_doh.text = 'Вкл'
        else:
            res.set(use_doh_server='https://ordns.he.net/dns-query', verify_doh_cert='false')
            self.root.get_screen('Local').ids.local_doh.text = 'Выкл'
    def local_dns(self):
        dns = self.root.get_screen('Local').ids.local_dns.text
        res = self.api.get_resource('/ip/dns')
        res.set(servers=dns)
    def perehvat_dns(self):
        res = self.api.get_resource('/ip/firewall/nat')
        index = str(res.get()).find("MikroLite_dns_interception")
        if index > 0:
            qw = str(res.get())[:index]
            qw = qw.rfind('id')
            index = str(res.get()).rfind("MikroLite_dns_interception")
            qe = str(res.get())[:index]
            qe = qe.rfind('id')
            res.remove(id=qw)
            res.remove(id=qe)
            self.root.get_screen('Local').ids.local_perehvat.text = 'Вкл'
        else:
            res.add(chain='dstnat', protocol='tcp', dst_port='53', in_interface_list='LAN', action='redirect', to_ports='53', comment='MikroLite_dns_interception')
            res.add(chain='dstnat', protocol='udp', dst_port='53', in_interface_list='LAN', action='redirect', to_ports='53', comment='MikroLite_dns_interception')
            self.root.get_screen('Local').ids.local_perehvat.text = 'Выкл'
    def local_time(self):
        time = self.root.get_screen('Local').ids.ipv4_local_time.text
        res = self.api.get_resource('/ip/dhcp-server')
        index = str(res.get()).find("id")
        if index > 0:
            a = index + 7
            while a < len(str(res.get())):
                if str(res.get())[a] == "'":
                    break
                else:
                    a = a + 1
            idis = str(res)[index + 7:a]
            res.set(id=idis, lease_time=time)
    def local_ip(self):
        ip = self.root.get_screen('Local').ids.ipv4_local_ip.text
        index = str(ip.get()).rfind(".")
        block = ip[:int(index)] + '.0/24'
        raw_ip = ip[:int(index)]
        time = self.root.get_screen('Local').ids.ipv4_local_time.text
        res = self.api.get_resource('/system/script')
        res.add(name='MikroLite_local_ip_changer', source='do command={:foreach id in=[/interface bridge find] do={/interface bridge remove $id}; /interface bridge add name=bridge};do command={:foreach id in=[/interface bridge port find] do={/interface bridge port set $id bridge=bridge}} ;do command={/ip address remove [find interface=bridge1];/ip address remove [find interface=bridge];/ip address add address=' + block + ' interface=bridge};do command={/ip pool remove [find name=default-dhcp];/ip pool remove [find name=dhcp];/ip pool add name=dhcp ranges=' + raw_ip + '.10-' + raw_ip + '.254};do command={/ip dhcp-server remove [find interface=bridge1];/ip dhcp-server add name=dhcp interface=bridge address-pool=dhcp lease-time=' + time + '};do command={:foreach id in [/ip dhcp-server network find] do { /ip dhcp-server network remove $id;};/ip dhcp-server network add address=' + block + ' gateway=' + ip + ' dns-server=' + ip +';/system script remove MikroLite_local_ip_changer}')
        index = str(res.get()).find("MikroLite_local_ip_changer")
        if index > 1:
            script_to_run = res.get(name="MikroLite_local_ip_changer")[0]
            self.api.get_binary_resource('/').call('system/script/run', {"number": script_to_run["id"].encode("utf-8")})
            self.sm.current = 'Authorization'
            self.connection.disconnect()
        else:
            res.add(name='MikroLite_local_ip_changer', source='do command={:foreach id in=[/interface bridge find] do={/interface bridge remove $id}; /interface bridge add name=bridge};do command={:foreach id in=[/interface bridge port find] do={/interface bridge port set $id bridge=bridge}} ;do command={/ip address remove [find interface=bridge1];/ip address remove [find interface=bridge];/ip address add address=' + block + ' interface=bridge};do command={/ip pool remove [find name=default-dhcp];/ip pool remove [find name=dhcp];/ip pool add name=dhcp ranges=' + raw_ip + '.10-' + raw_ip + '.254};do command={/ip dhcp-server remove [find interface=bridge1];/ip dhcp-server add name=dhcp interface=bridge address-pool=dhcp lease-time=' + time + '};do command={:foreach id in [/ip dhcp-server network find] do { /ip dhcp-server network remove $id;};/ip dhcp-server network add address=' + block + ' gateway=' + ip + ' dns-server=' + ip + ';/system script remove MikroLite_local_ip_changer}')
            script_to_run = res.get(name="MikroLite_local_ip_changer")[0]
            self.api.get_binary_resource('/').call('system/script/run', {"number": script_to_run["id"].encode("utf-8")})
            self.sm.current = 'Authorization'
            self.connection.disconnect()
    def firewall(self):
        res = self.api.get_resource('/ip/firewall/filter')
        index = str(res.get()).find("id")
        if index > 1:
            #Deleter
            res = self.api.get_resource('/ip/firewall/filter')
            index = str(res.get()).find("id")
            index1 = index
            a = 0
            while a > 1:
                res = self.api.get_resource('/ip/firewall/filter')
                index1 = str(res.get()).find("id")
                a = index1 + 6
                while a < len(str(res.get())):
                    if str(res.get())[a] == "'":
                        break
                    else:
                        a = a + 1
                idis = str(res.get())[index + 6:a]
            res = self.api.get_resource('/system/script')
            res.add(name='MikroLite_firewall_del',source=':foreach id in [/ip firewall filter find] do {/ip firewall filter remove $id};/system script remove MikroLite_firewall_del')
            index = str(res.get()).find("MikroLite_firewall_del")
            if index > 1:
                script_to_run = res.get(name="MikroLite_firewall_del")[0]
                self.api.get_binary_resource('/').call('system/script/run', {"number": script_to_run["id"].encode("utf-8")})
            else:
                res.add(name='MikroLite_firewall_del', source=':foreach id in [/ip firewall filter find] do {/ip firewall filter remove $id};/system script remove MikroLite_firewall_del')
                script_to_run = res.get(name="MikroLite_firewall_del")[0]
                self.api.get_binary_resource('/').call('system/script/run', {"number": script_to_run["id"].encode("utf-8")})
            res = self.api.get_resource('/ip/settings')
            res.set(tcp_syncookies='yes')
            self.root.get_screen('Internet').ids.firewall.text = 'Вкл'
        else:
            res = self.api.get_resource('/ip/settings')
            res.set(tcp_syncookies='yes')
            res = self.api.get_resource('/ip/firewall/filter')
            res.add(action='accept', chain='input', protocol='icmp')
            res.add(chain='input', protocol='tcp', action='tarpit', src_address_list='blacklist')
            res.add(chain='input', action='drop', src_address_list='blacklist')
            res.add(action='accept', chain='input', connection_state='established,related', comment="established,related")
            res.add(chain='input', in_interface_list='WAN', protocol='udp', dst_port='53', action='add-dst-to-address-list', address_list='blacklist', address_list_timeout='1d')
            res.add(chain='input', in_interface_list='WAN', protocol='tcp', dst_port='53', action='add-dst-to-address-list', address_list='blacklist', address_list_timeout='1d')
            res.add(chain='input', action='accept', dst_address ='127.0.0.1')
            res.add(chain='input', action='accept', src_address_type='local', dst_address_type='local')
            res.add(action='drop', chain='input', in_interface_list='WAN')
            self.root.get_screen('Internet').ids.firewall.text = 'Выкл'
    def prioritet(self):
        route_priority = self.root.get_screen('Internet').ids.isp_dhcp_def.text
        if route_priority > '0':
            res = self.api.get_resource('/ip/dhcp-client')
            index = str(res.get()).find("id")
            if index > 1:
                res.set(interface='ether1', default_route_distance=route_priority, disabled='no')
        route_priority = self.root.get_screen('Internet').ids.isp_lte_def.text
        res = self.api.get_resource('/interface/lte/apn')
        index = str(res.get()).find("id")
        if index > 1:
            a = index + 6
            while a < len(str(res.get())):
                if str(res.get())[a] == "'":
                    break
                else:
                    a = a + 1
            idis = str(res.get())[index + 6:a]
            if route_priority > '0':
                res = self.api.get_resource('/interface/lte/apn')
                index = str(res.get()).find("id")
                if index > 1:
                    res.set(id=idis, default_route_distance=route_priority, disabled='no')
            else:
                res = self.api.get_resource('/interface/lte/apn')
                index = str(res.get()).find("id")
                if index > 1:
                    res.set(id=idis, default_route_distance=2, disabled='no')
    def autoisp(self):
        #Опора
        res = self.api.get_resource('/ip/dhcp-client')
        index = str(res.get()).find("id")
        if index > 1:
            a = index + 6
            while a < len(str(res.get())):
                if str(res.get())[a] == "'":
                    break
                else:
                    a = a + 1
            idis = str(res.get())[index + 6:a]
        if index > 1:
            index = str(res.get()).find("default-route-distance")
            a = index + 26
            while a < len(str(res.get())):
                if str(res.get())[a] == "'":
                    break
                else:
                    a = a + 1
            self.root.get_screen('Internet').ids.isp_dhcp_def.text = str(res.get())[index + 26:a]
        res = self.api.get_resource('/ip/dhcp-client')
        index = str(res.get()).find("id")
        if index > 1:
            res = self.api.get_resource('/ip/dhcp-client')
            index = str(res.get()).find("id")
            if index > 1:
                a = index + 6
                while a < len(str(res.get())):
                    if str(res.get())[a] == "'":
                        break
                    else:
                        a = a + 1
                idis = str(res.get())[index + 6:a]
            if index > 1:
                res.remove(id=idis)
        else:
            res = self.api.get_resource('/ip/dhcp-client')
            index = str(res.get()).find("id")
            if index < 1:
                route_priority = self.root.get_screen('Internet').ids.isp_dhcp_def.text
                if str(route_priority) == '':
                    route_priority = '1'
                res.add(interface='ether1', default_route_distance=route_priority, disabled='no')
    def resour_wifi(self):

    def resour(self):

        #wifi пароль
        res = self.api.get_resource('/interface/wireless/security-profiles')
        index = str(res.get()).find("default")
        if index > 1:
            a = index
            while a > 1:
                if str(res.get())[a] == "id":
                    break
                else:
                    a = a - 1
            b = a + 8
            while b < len(str(res.get())):
                if str(res.get())[b] == "}":
                    break
                else:
                    b = b + 1
            stroka = str(res.get())[a+1:b]
            index = str(stroka).find("wpa-pre-shared-key")
            a = index + 22
            while a < len(str(stroka)):
                if str(stroka)[a] == "'":
                    break
                else:
                    a = a + 1
            wpa = (str(stroka)[index + 22:a])
            index = str(stroka).find("wpa2-pre-shared-key")
            a = index + 23
            while a < len(str(stroka)):
                if str(stroka)[a] == "'":
                    break
                else:
                    a = a + 1
            wpa2 = (str(stroka)[index + 23:a])
            if wpa == wpa2:
                self.root.get_screen('wifi').ids.wifi_password.text = wpa
            elif wpa > wpa2:
                self.root.get_screen('wifi').ids.wifi_password.text = wpa
            else:
                self.root.get_screen('wifi').ids.wifi_password.text = wpa2
        #Получение модели
        res = self.api.get_resource('/system/resource')
        index = str(res.get()).find("board-name")
        a = index + 14
        while a < len(str(res.get())):
            if str(res.get())[a] == "'":
                break
            else:
                a = a + 1
        model = (str(res.get())[index + 14:a])
        self.root.get_screen('MainMenu').ids.model.text = 'Модель:\n'+(str(res.get())[index + 14:a])
        if model == 'x86':
            res = self.api.get_resource('/ip/cloud')
        else:
            res = self.api.get_resource('/ip/cloud')
            res.set(ddns_enabled='yes')
        #WiFi 2.4Ghz
        res = self.api.get_resource('/interface/wireless')
        index = str(res.get()).find("'default-name': 'wlan1'")
        if index > 0:
            self.root.get_screen('wifi').ids.wifi_24_have.text = 'Имеется'
            index = str(res.get()).find("'disabled': 'false'")
            if index > 0:
                self.root.get_screen('wifi').ids.wifi_24.text = 'Выкл'
            index = str(res.get()).find("'ssid")
            if index > 0:
                a = index + 9
                while a < len(str(res.get())):
                    if str(res.get())[a] == "'":
                        break
                    else:
                        a = a + 1
                self.root.get_screen('wifi').ids.wifi24_ssid.text = str(res.get())[index + 9:a]
            index = str(res.get()).find("frequency'")
            if index > 0:
                a = index + 13
                while a < len(str(res.get())):
                    if str(res.get())[a] == "'":
                        break
                    else:
                        a = a + 1
                channel = int(str(res.get())[index + 13:a], base=10)
                if channel == 2412:
                    self.root.get_screen('wifi').ids.wifi24_channel.text = '1'
                elif channel == 2417:
                    self.root.get_screen('wifi').ids.wifi24_channel.text = '2'
                elif channel == 2422:
                    self.root.get_screen('wifi').ids.wifi24_channel.text = '3'
                elif channel == 2427:
                    self.root.get_screen('wifi').ids.wifi24_channel.text = '4'
                elif channel == 2432:
                    self.root.get_screen('wifi').ids.wifi24_channel.text = '5'
                elif channel == 2437:
                    self.root.get_screen('wifi').ids.wifi24_channel.text = '6'
                elif channel == 2442:
                    self.root.get_screen('wifi').ids.wifi24_channel.text = '7'
                elif channel == 2447:
                    self.root.get_screen('wifi').ids.wifi24_channel.text = '8'
                elif channel == 2452:
                    self.root.get_screen('wifi').ids.wifi24_channel.text = '9'
                elif channel == 2457:
                    self.root.get_screen('wifi').ids.wifi24_channel.text = '10'
                elif channel == 2462:
                    self.root.get_screen('wifi').ids.wifi24_channel.text = '11'
                elif channel == 2467:
                    self.root.get_screen('wifi').ids.wifi24_channel.text = '12'
                elif channel == 2472:
                    self.root.get_screen('wifi').ids.wifi24_channel.text = '13'
                else:
                    self.root.get_screen('wifi').ids.wifi24_channel.text = 'Другая'
            index = str(res.get()).find("channel-width'")
            if index > 0:
                a = index + 17
                while a < len(str(res.get())):
                    if str(res.get())[a] == "'":
                        break
                    else:
                        a = a + 1
                self.root.get_screen('wifi').ids.wifi_24_XX.text = str(res.get())[index + 17:a]
        # WiFi 5Ghz
        res = self.api.get_resource('/interface/wireless')
        index = str(res.get()).rfind("'default-name': 'wlan2'")
        index1 = str(res.get()).rfind("about")
        if index > 0 and index1 < 1:
            self.root.get_screen('wifi').ids.wifi_5_have.text = 'Имеется'
            index = str(res.get()).rfind("'disabled': 'false'")
            if index > 0:
                self.root.get_screen('wifi').ids.wifi_5.text = 'Выкл'
            index = str(res.get()).rfind("'ssid")
            if index > 0:
                a = index + 9
                while a < len(str(res.get())):
                    if str(res.get())[a] == "'":
                        break
                    else:
                        a = a + 1
                self.root.get_screen('wifi').ids.wifi5_ssid.text = str(res.get())[index + 9:a]
            index = str(res.get()).rfind("'frequency'")
            if index > 0:
                a = index + 14
                while a < len(str(res.get())):
                    if str(res.get())[a] == "'":
                        break
                    else:
                        a = a + 1
                channel = int(str(res.get())[index + 14:a], base=10)
                if channel == 5180:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '36'
                elif channel == 5200:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '40'
                elif channel == 5220:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '44'
                elif channel == 5240:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '48'
                elif channel == 5260:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '52'
                elif channel == 5280:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '56'
                elif channel == 5300:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '60'
                elif channel == 5320:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '64'
                elif channel == 5340:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '68'
                elif channel == 5360:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '72'
                elif channel == 5380:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '76'
                elif channel == 5400:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '80'
                elif channel == 5420:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '84'
                elif channel == 5440:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '88'
                elif channel == 5460:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '92'
                elif channel == 5480:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '96'
                elif channel == 5500:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '100'
                elif channel == 5520:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '104'
                elif channel == 5540:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '108'
                elif channel == 5560:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '112'
                elif channel == 5580:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '116'
                elif channel == 5600:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '120'
                elif channel == 5620:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '124'
                elif channel == 5640:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '128'
                elif channel == 5660:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '132'
                elif channel == 5680:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '136'
                elif channel == 5700:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '140'
                elif channel == 5720:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '144'
                elif channel == 5745:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '149'
                elif channel == 5765:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '153'
                elif channel == 5785:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '157'
                elif channel == 5805:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '161'
                elif channel == 5825:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = '165'
                else:
                    self.root.get_screen('wifi').ids.wifi5_channel.text = 'Другое'
            index = str(res.get()).rfind("channel-width'")
            if index > 0:
                a = index + 17
                while a < len(str(res.get())):
                    if str(res.get())[a] == "'":
                        break
                    else:
                        a = a + 1
                self.root.get_screen('wifi').ids.wifi_5_XX.text = str(res.get())[index + 17:a]
        #Сервер NTP
        res = self.api.get_resource('/system/ntp/server')
        index = str(res.get()).find("'enabled': 'true'")
        if index > 0:
            self.root.get_screen('Local').ids.local_ntp_srv.text = 'Выкл'
        else:
            self.root.get_screen('Local').ids.local_ntp_srv.text = 'Вкл'
        #Получение NTP серверов
        res = self.api.get_resource('/system/ntp/client')
        res.set(enabled='true')
        index = str(res.get()).find("servers")
        stroka = str(res.get())[index + 8:]
        a = index + 11
        while a < len(str(res.get())):
            if str(res.get())[a] == "'":
                break
            else:
                a = a + 1
        if stroka != "''":
            self.root.get_screen('Local').ids.local_ntp.text = str(res.get())[index + 11:a]
        #Получение DoH
        res = self.api.get_resource('/ip/dns')
        res.set(allow_remote_requests='true')
        index = str(res.get()).find("ordns")
        if index > 0:
            self.root.get_screen('Local').ids.local_doh.text = 'Выкл'
        #Получение dns серверов
        res = self.api.get_resource('/ip/dns')
        index = str(res.get()).find("servers")
        a = index + 11
        while a < len(str(res.get())):
            if str(res.get())[a] == "'":
                break
            else:
                a = a + 1
        self.root.get_screen('Local').ids.local_dns.text = str(res.get())[index + 11:a]
        #Перехват dns запросов
        res = self.api.get_resource('/ip/firewall/nat')
        index = str(res.get()).find("MikroLite_dns_interception")
        if index > 0:
            self.root.get_screen('Local').ids.local_perehvat.text = 'Выкл'
        #Lease-time
        res = self.api.get_resource('/ip/dhcp-server')
        index = str(res.get()).find("id")
        if index > 1:
            index = str(res.get()).find("lease-time")
            b = index + 15
            while b < len(str(res.get())):
                if str(res.get())[b] == "'":
                    break
                else:
                    b = b + 1
            stroka = str(res.get())[index + 14:b]
            index = str(stroka).find("d")
            if index > 0:
                day = stroka[:int(index)] + 'd'
            else:
                day = '0d'
            index = str(stroka).find("h")
            if index > 0:
                hours = stroka[int(index) - 2:int(index)]
            else:
                hours = '00'
            index = str(stroka).find("m")
            if index > 0:
                minuts = stroka[int(index) - 2:int(index)]
            else:
                minuts = '00'
            index = str(stroka).find("s")
            if index > 0:
                second = stroka[int(index) - 2:int(index)]
            else:
                second = '00'
            stroka = day + hours + ':' + minuts + ':' + second
            self.root.get_screen('Local').ids.ipv4_local_time.text = stroka
        #Local Ip
        res = self.api.get_resource('/ip/address')
        index = str(res.get()).find("bridge")
        if index > 1:
            a = index
            while a > 1:
                if str(res.get())[a] == "id":
                    break
                else:
                    a = a - 1
            b = a + 8
            while b < len(str(res.get())):
                if str(res.get())[b] == "'":
                    break
                else:
                    b = b + 1
            idis = str(res.get())[a + 8:b]
            while b < len(str(res.get())):
                if str(res.get())[b] == "}":
                    break
                else:
                    b = b + 1
            stroka = str(res.get())[a+1:b]
            index = stroka.find("address")
            b = index + 11
            while b < len(stroka):
                if stroka[b] == "/":
                    break
                else:
                    b = b + 1
            self.root.get_screen('Local').ids.ipv4_local_ip.text = stroka[index + 11:b]
        #DHCP_client
        res = self.api.get_resource('/ip/dhcp-client')
        index = str(res.get()).find("id")
        if index > 1:
            a = index + 6
            while a < len(str(res.get())):
                if str(res.get())[a] == "'":
                    break
                else:
                    a = a + 1
            idis = str(res.get())[index + 6:a]
        if index > 1:
            index = str(res.get()).find("default-route-distance")
            a = index + 26
            while a < len(str(res.get())):
                if str(res.get())[a] == "'":
                    break
                else:
                    a = a + 1
            self.root.get_screen('Internet').ids.isp_dhcp_def.text = str(res.get())[index + 26:a]
        res = self.api.get_resource('/ip/dhcp-client')
        index = str(res.get()).find("id")
        if index > 1:
            self.root.get_screen('Internet').ids.isp_dhcp_button.text = 'Выкл'
        else:
            self.root.get_screen('Internet').ids.isp_dhcp_button.text = 'Вкл'
        #LTE
        a = 1
        if model == 'hAP lite':
            a = 0
        elif model == 'hEX lite':
            a = 0
        elif model == 'LDF':
            a = 0
        elif model == 'SXTsq Lite':
            a = 0
        elif model == 'hAP mini':
            a = 0
        elif model == 'cAP lite':
            a = 0
        elif model == 'wAP':
            a = 0
        elif model == 'wsAP':
            a = 0
        elif model == 'cAP ac':
            a = 0
        elif model == 'cAP XL ac':
            a = 0
        elif model == 'Audience':
            a = 0
        if a == 1:
            res = self.api.get_resource('/interface/lte/apn')
            index = str(res.get()).find("id")
            if index > 1:
                index = str(res.get()).find("default-route-distance")
                a = index + 26
                while a < len(str(res.get())):
                    if str(res.get())[a] == "'":
                        break
                    else:
                        a = a + 1
                self.root.get_screen('Internet').ids.isp_lte_def.text = str(res.get())[index + 26:a]
        else:
            self.root.get_screen('Internet').ids.vsegda_activno.text = 'Не имеется'
        #Firewall
        res = self.api.get_resource('/ip/firewall/filter')
        index1 = str(res.get()).find("defconf: drop invalid")
        if index1 > 1:
            self.root.get_screen('Internet').ids.firewall.text = 'Удалить заводской\nfirewall'
        res = self.api.get_resource('/ip/firewall/filter')
        index = str(res.get()).find("id")
        if index > 1:
            if index1 < 1:
                self.root.get_screen('Internet').ids.firewall.text = 'Выкл'
        else:
            self.root.get_screen('Internet').ids.firewall.text = 'Вкл'
        #Опора ####################################################################################################################
        res = self.api.get_resource('/system/resource')
        #Версия ОС
        index = str(res.get()).find("version")
        a = index + 14
        while a < len(str(res.get())):
            if str(res.get())[a] == "'":
                break
            else:
                a = a + 1
        self.root.get_screen('MainMenu').ids.resource.text = 'Версия RouterOS:\n'+(str(res.get())[index+11:a])
        #Получение загрузки CPU
        index = str(res.get()).find("cpu-load")
        a = index + 12
        while a < len(str(res.get())):
            if str(res.get())[a] == "'":
                break
            else:
                a = a + 1
        self.root.get_screen('MainMenu').ids.loadcpu.text = 'Загрузка CPU:\n'+(str(res.get())[index + 12:a])+'%'
        #Определение ip или NAT
        res = self.api.get_resource('/ip/cloud')
        index = str(res.get()).find("Router is behind a NAT")
        if index > 1:
            index = str(res.get()).find("public-address")
            a = index + 18
            while a < len(str(res.get())):
                if str(res.get())[a] == "'":
                    break
                else:
                    a = a + 1
            index1 = str(res.get()).find("ipv6")
            b = index1 + 8
            if index1 > 1:
                while b < len(str(res.get())):
                    if str(res.get())[b] == "'":
                        break
                    else:
                        b = b + 1
            if index1 > 1:
                self.root.get_screen('MainMenu').ids.ipnatdetector.text = 'Вы находитесь за NAT провайдера.\nДоступ извне по IPv4 невозможен.\nОбщий IPv4:\n' + (str(res.get())[index + 18:a]) + '\nВаш публичный IPv6:\n' + (str(res.get())[index1 + 8:b])
            else:
                self.root.get_screen('MainMenu').ids.ipnatdetector.text = 'Вы находитесь за NAT провайдера.\nДоступ извне по IPv4 невозможен.\nОбщий IPv4:\n'+(str(res.get())[index + 18:a])+'\nПубличный IPv6 не найден'
        else:
            index = str(res.get()).find("public-address")
            a = index + 18
            while a < len(str(res.get())):
                if str(res.get())[a] == "'":
                    break
                else:
                    a = a + 1
            index1 = str(res.get()).find("ipv6")
            b = index1 + 8
            if index1 > 1:
                while b < len(str(res.get())):
                    if str(res.get())[b] == "'":
                        break
                    else:
                        b = b + 1
            if index1 > 1:
                self.root.get_screen('MainMenu').ids.ipnatdetector.text = 'Ваш публичный IPv4:\n'+(str(res.get())[index + 18:a]) + (str(res.get())[index + 18:a]) + '\nВаш публичный IPv6:\n' + (str(res.get())[index1 + 8:b])
            else:
                self.root.get_screen('MainMenu').ids.ipnatdetector.text = 'Ваш публичный IPv4:\n'+(str(res.get())[index + 18:a])+'\nПубличный IPv6 не найден'
    def build(self):
        self.sm = Manager()
        self.sm.add_widget(Authorization(name='Authorization'))
        self.sm.add_widget(MainMenu(name='MainMenu'))
        self.sm.add_widget(Internet(name='Internet'))
        self.sm.add_widget(Local(name='Local'))
        self.sm.add_widget(Forward(name='Forward'))
        self.sm.add_widget(Static(name='Static'))
        self.sm.add_widget(PPPoE(name='PPPoE'))
        self.sm.add_widget(Other(name='Other'))
        self.sm.add_widget(wifi(name='wifi'))
        self.sm.add_widget(VPN(name='VPN'))
        self.sm.add_widget(Update(name='Update'))
        self.sm.current = 'Authorization'
        self.theme_cls.theme_style = "Light"  # Light Dark
        self.theme_cls.primary_palette = "LightBlue"  # BlueGray LightBlue
        return self.sm
if __name__ == "__main__":
    MikroLiteApp().run()
