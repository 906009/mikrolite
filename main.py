from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
import routeros_api
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
    def logout(self):
        self.sm.current = 'Authorization'
        self.connection.disconnect()
    def local_ip(self):
        ip = self.root.get_screen('Local').ids.ipv4_local_ip.text
        index = str(ip.get()).rfind(".")
        block = ip[:int(index)] + '.0/24'
        raw_ip = ip[:int(index)]
        time = self.root.get_screen('Local').ids.ipv4_local_time.text
        res = self.api.get_resource('/system/script')
        res.add(name='MikroLite_local_ip_changer', source='do command={:foreach id in=[/interface bridge find] do={/interface bridge remove $id}; /interface bridge add name=bridge};do command={:foreach id in=[/interface bridge port find] do={/interface bridge port set $id bridge=bridge}} ;do command={/ip address remove [find interface=bridge1];/ip address remove [find interface=bridge];/ip address add address=' + block + ' interface=bridge};do command={/ip pool remove [find name=default-dhcp];/ip pool remove [find name=dhcp];/ip pool add name=dhcp ranges=' + raw_ip + '.10-' + raw_ip + '.254};do command={/ip dhcp-server remove [find interface=bridge1];/ip dhcp-server add name=dhcp interface=bridge address-pool=dhcp lease-time=' + time + '};do command={:foreach id in [/ip dhcp-server network find] do { /ip dhcp-server network remove $id;};/ip dhcp-server network add address=' + block + ' gateway=' + ip + ' dns-server=' + ip +'}')
        index = str(res.get()).find("MikroLite_local_ip_changer")
        if index > 1:
            script_to_run = res.get(name="MikroLite_local_ip_changer")[0]
            self.api.get_binary_resource('/').call('system/script/run', {"number": script_to_run["id"].encode("utf-8")})
        else:
            res.add(name='MikroLite_local_ip_changer', source='do command={:foreach id in=[/interface bridge find] do={/interface bridge remove $id}; /interface bridge add name=bridge};do command={:foreach id in=[/interface bridge port find] do={/interface bridge port set $id bridge=bridge}} ;do command={/ip address remove [find interface=bridge1];/ip address remove [find interface=bridge];/ip address add address=' + block + ' interface=bridge};do command={/ip pool remove [find name=default-dhcp];/ip pool remove [find name=dhcp];/ip pool add name=dhcp ranges=' + raw_ip + '.10-' + raw_ip + '.254};do command={/ip dhcp-server remove [find interface=bridge1];/ip dhcp-server add name=dhcp interface=bridge address-pool=dhcp lease-time=' + time + '};do command={:foreach id in [/ip dhcp-server network find] do { /ip dhcp-server network remove $id;};/ip dhcp-server network add address=' + block + ' gateway=' + ip + ' dns-server=' + ip + '}')
            script_to_run = res.get(name="MikroLite_local_ip_changer")[0]
            self.api.get_binary_resource('/').call('system/script/run', {"number": script_to_run["id"].encode("utf-8")})
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
    def resour(self):
        #Lease-time
        res = self.api.get_resource('/ip/dhcp-server')
        index = str(res.get()).find("id")
        if index > 1:
            index = str(res.get()).find("lease-time")
            b = 0
            while b < len(str(res.get())):
                if str(res.get())[b] == "'":
                    break
                else:
                    b = b + 1
            stroka = str(res.get())[index + 15:b]
            index = str(res.get()).find("d")
            if index > 0:
                day = stroka[:int(index)] + 'd'
            else:
                day = '0d'
            index = str(res.get()).find("h")
            if index > 0:
                hours = stroka[int(index) - 2:int(index)]
            else:
                hours = '00'
            index = str(res.get()).find("m")
            if index > 0:
                minuts = stroka[int(index) - 2:int(index)]
            else:
                minuts = '00'
            index = str(res.get()).find("s")
            if index > 0:
                second = stroka[int(index)- 2:int(index)]
            else:
                second = '00'
            stroka = day + hours + ':' +minuts + ':' + second
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
        #Получение модели
        index = str(res.get()).find("board-name")
        a = index + 14
        while a < len(str(res.get())):
            if str(res.get())[a] == "'":
                break
            else:
                a = a + 1
        self.root.get_screen('MainMenu').ids.model.text = 'Модель:\n'+(str(res.get())[index + 14:a])
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