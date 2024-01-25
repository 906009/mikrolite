from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import routeros_api

class MainMenu(Screen):
    pass

class Authorization(Screen):
    pass

class Manager(ScreenManager):
    pass

class MikroLiteApp(MDApp):

    def connector(self):
        prtv = self.root.get_screen('Authorization').ids.portv.text
        if prtv != 0:
            host = self.root.get_screen('Authorization').ids.ip_dns.text
            prt = int(self.root.get_screen('Authorization').ids.portv.text)
            usr = self.root.get_screen('Authorization').ids.user.text
            pwr = self.root.get_screen('Authorization').ids.passwordv.text
            connection = routeros_api.RouterOsApiPool(host, username=usr,password=pwr, port=prt,use_ssl=False, ssl_verify=False, ssl_verify_hostname=False,ssl_context=None, plaintext_login=True)
            api = connection.get_api()
    def build(self):
        sm = Manager()
        sm.add_widget(Authorization(name='Authorization'))
        sm.add_widget(MainMenu(name='MainMenu'))
        sm.current = 'Authorization'
        self.theme_cls.theme_style = "Dark"  # Light
        self.theme_cls.primary_palette = "LightBlue"  # BlueGray
        return sm
        #return Builder.load_file('mikrolite.kv')

if __name__ == "__main__":
    MikroLiteApp().run()