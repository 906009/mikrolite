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
        return self.api
    def autoisp(self, checkbox, value):
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
            self.root.get_screen('Internet').ids.dhcp_isp_switch.active = 'true'
        else:
            self.root.get_screen('Internet').ids.dhcp_isp_switch.active = 'false'
        res = self.api.get_resource('/ip/dhcp-client')
        index = str(res.get()).find("id")
        print(value)
        if value:
            res = self.api.get_resource('/ip/dhcp-client')
            index = str(res.get()).find("id")
            if index > 1:
                route_priority = self.root.get_screen('Internet').ids.isp_dhcp_def.text
                if int(route_priority) < 1:
                    route_priority = 1
                res.set(id=idis, interface='ether1', default_route_distance=route_priority, disabled='no')
                self.root.get_screen('Internet').ids.dhcp_isp_switch.active = 'true'
            else:
                route_priority = self.root.get_screen('Internet').ids.isp_dhcp_def.text
                if int(route_priority) < 1:
                    route_priority = 1
                print('Я тут')
                res.add(interface='ether1', default_route_distance=route_priority, disabled='no')
                self.root.get_screen('Internet').ids.dhcp_isp_switch.active = 'true'
        else:
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
                self.root.get_screen('Internet').ids.dhcp_isp_switch.active = 'false'
            else:
                self.root.get_screen('Internet').ids.dhcp_isp_switch.active = 'false'
    def resour(self):
        #Опора
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
                self.root.get_screen('MainMenu').ids.ipnatdetector.text = 'Вы находитесь за NAT провайдера.\nДоступ извне по ip невозможен.\nОбщий IPv4:\n' + (str(res.get())[index + 18:a]) + '\nВаш публичный IPv6:\n' + (str(res.get())[index1 + 8:b])
            else:
                self.root.get_screen('MainMenu').ids.ipnatdetector.text = 'Вы находитесь за NAT провайдера.\nДоступ извне по ip невозможен.\nОбщий IPv4:\n'+(str(res.get())[index + 18:a])+'\nПубличный IPv6 не найден'
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
        sm = Manager()
        sm.add_widget(Authorization(name='Authorization'))
        sm.add_widget(MainMenu(name='MainMenu'))
        sm.add_widget(Internet(name='Internet'))
        sm.add_widget(Local(name='Local'))
        sm.add_widget(Forward(name='Forward'))
        sm.add_widget(Other(name='Other'))
        sm.add_widget(VPN(name='VPN'))
        sm.add_widget(Update(name='Update'))
        sm.current = 'Authorization'
        self.theme_cls.theme_style = "Light"  # Light Dark
        self.theme_cls.primary_palette = "LightBlue"  # BlueGray LightBlue
        return sm
if __name__ == "__main__":
    MikroLiteApp().run()