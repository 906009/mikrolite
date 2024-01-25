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
class VPN(Screen):
    pass
class Update(Screen):
    pass
class Manager(ScreenManager):
    pass
class MikroLiteApp(MDApp):

    def connector(self):
        host = self.root.get_screen('Authorization').ids.ip_dns.text
        usr = self.root.get_screen('Authorization').ids.user.text
        pwr = self.root.get_screen('Authorization').ids.passwordv.text
        self.connection = routeros_api.RouterOsApiPool(host, username=usr, password=pwr, port=8728, use_ssl=False,
                                                       ssl_verify=False, ssl_verify_hostname=False, ssl_context=None,
                                                       plaintext_login=True)
        self.api = self.connection.get_api()

        return self.api



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
            self.root.get_screen('MainMenu').ids.ipnatdetector.text = 'Вы находитесь за NAT провайдера.\nДоступ извне по ip невозможен.\nВаш публичный IPv4:\n'+(str(res.get())[index + 18:a])
        else:
            index = str(res.get()).find("public-address")
            a = index + 18
            while a < len(str(res.get())):
                if str(res.get())[a] == "'":
                    break
                else:
                    a = a + 1
            self.root.get_screen('MainMenu').ids.ipnatdetector.text = 'Ваш публичный IPv4:\n'+(str(res.get())[index + 18:a])

    def build(self):
        sm = Manager()
        sm.add_widget(Authorization(name='Authorization'))
        sm.add_widget(MainMenu(name='MainMenu'))
        sm.add_widget(Internet(name='Internet'))
        sm.add_widget(Local(name='Local'))
        sm.add_widget(VPN(name='VPN'))
        sm.add_widget(Update(name='Update'))
        sm.current = 'Authorization'
        self.theme_cls.theme_style = "Light"  # Light Dark
        self.theme_cls.primary_palette = "LightBlue"  # BlueGray LightBlue
        return sm
        #return Builder.load_file('mikrolite.kv')

if __name__ == "__main__":
    MikroLiteApp().run()