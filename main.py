from kivy.clock import mainthread
from kivymd.uix.button import MDTextButton
from kivymd.uix.card import MDCard
import http.client as ht
from chat import Exchange
import webbrowser
from threading import Thread
import re
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.app import MDApp
from kivymd.uix.progressbar.progressbar import MDProgressBar
from PIL import Image
from kivymd.uix.label import MDLabel
from multiprocessing import Process, Pipe, freeze_support
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.widget import MDWidget
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.filemanager import MDFileManager
from database import check_user_pw, registration, get_user_data, all_users, get_ip, new_project
from kivy.config import Config
from avatar_crop import prepare_ava
import socket

Builder.load_file("apps.kv")
Builder.load_file("hello.kv")
Builder.load_file("regist.kv")
Builder.load_file("prof_set.kv")
Builder.load_file("apps_contain.kv")
Builder.load_file("chat_connection.kv")
Builder.load_file("chat_search.kv")
Builder.load_file("rooms.kv")
Builder.load_file("chat.kv")
Builder.load_file("project.kv")
Builder.load_file("project_creation.kv")

EMAIL_re = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
EMAIL = 'dd'
NAME = 'ds'
STATUS = 'dfvf'
app = 'd'
chat = 'f'
MSG = str
done = False
LINK_PROJ = 'htttps'
PROJ_NAME = 'proj'
progr = 0


def get_MSG(ch):
    global parent_conn, done
    while not done:
        try:
            msg = parent_conn.recv()
            ch.cout(msg)
        except Exception:
            done = True

class MD3Card(MDCard, RectangularElevationBehavior):
    pass
    
class Proj_Creation(MDBoxLayout):
    def yandex(self):
        webbrowser.open('https://disk.yandex.ru/client/disk')

    def start_project(self):
        global NAME, PROJ_NAME, LINK_PROJ, progr

        acc = Account()

        self.remove_widget(self.children[0])

        link = self.ids.link.text
        proj = self.ids.name_proj.text
        new_project(NAME, link, proj)
        LINK_PROJ = link
        PROJ_NAME = proj

        acc.ids.new_proj.text = 'Удалить проект'
        but = MDTextButton(text=PROJ_NAME)

        acc.ids.enter_proj = but
        acc.ids.container.add_widget(but)
        but.font_size = 25
        but.pos_hint = {"center_x": .5}
        but.color = 'blue'
        but.on_release = acc.open_proj_progress

        bar = MDProgressBar(value=progr, size_hint_y=0.01, color=(0, 1, 0, .5))
        acc.ids.container.add_widget(bar)
        acc.ids.container.padding = [0, 10, 0, 450]
        acc.ids.bar = bar
        self.add_widget(acc)


class Progress(MDBoxLayout):
    def prog_init(self, start=False):
        global progr
        progress = {"one": self.ids.one, "two": self.ids.two, "three": self.ids.three, "four": self.ids.four,
                    "five": self.ids.five}
        count = 0
        if start:
            load = open('progress.txt', mode='r', encoding='utf8')
            stats = load.readlines()
            for value in stats:
                progress[value[:-1]].active = True
            load.close()

        save = open('progress.txt', mode='w', encoding='utf8')
        for key, value in progress.items():
            if value.active:
                count += 1
                save.write(f"{key}\n")
        count *= 10 * 2
        progr = count
        save.close()
        self.ids.progress.value = count

    def cancel(self):
        global app, PROJ_NAME, progr
        app.ids.acc.remove_widget(app.ids.acc.children[0])

        acc = Account()
        acc.ids.new_proj.text = 'Удалить проект'
        but = MDTextButton(text=PROJ_NAME, font_size=32)

        acc.ids.enter_proj = but
        acc.ids.container.add_widget(but)
        but.font_size = 28
        but.pos_hint = {"center_x": .5}
        but.color = 'blue'
        but.on_release = acc.open_proj_progress

        bar = MDProgressBar(value=progr, size_hint_y=0.01, color=(0, 1, 0, .5))
        acc.ids.container.add_widget(bar)
        acc.ids.container.padding = [0, 10, 0, 450]
        acc.ids.bar = bar
        app.ids.acc.add_widget(acc)

    def open_project(self):
        global LINK_PROJ
        webbrowser.open(LINK_PROJ)


class App(MDWidget):
    def cancel(self):
        if self.ids.ch_cancel.text != 'Назад':
            self.ids.ch_cancel.text = 'Назад'
            self.ids.chat_bl.remove_widget(self.ids.chat_bl.children[0])
            self.ids.chat_bl.add_widget(Chat_search())
        else:
            self.ids.ch_cancel.text = 'Добавить'
            self.ids.chat_bl.remove_widget(self.ids.chat_bl.children[0])
            self.chat_build()

    def chat_build(self):
        rooms = Rooms()
        self.ids.chat_bl.add_widget(rooms)
        with open('connections', mode='r', encoding='utf8') as file:
            lines = file.readlines()
            for i in lines:
                if i[0].isalpha():
                    rooms.ids.box.add_widget(
                        MDExpansionPanel(
                            content=Content(),
                    panel_cls=MDExpansionPanelTwoLine(
                        text=i,
                        secondary_text="ученик"
                    )
                )
            )
    def open_link(self, ident):
        if ident == 'a':
            webbrowser.open('https://disk.yandex.ru/d/ZR0R8XJdvci3Pg')
        elif ident == 'b':
            webbrowser.open('https://disk.yandex.ru/d/GoIvcLBgG8wdhA')
        elif ident == 'c':
            webbrowser.open('https://disk.yandex.ru/d/LidtIB1tBfpoEQ')
        elif ident == 'd':
            webbrowser.open('https://disk.yandex.ru/d/YbcCuZfE9XqUVw')

class Peoples(MDWidget):
    pass


class Message(MDWidget):
    """"""


class Chat(MDBoxLayout):
    def open_project(self):
        global LINK_PROJ
        webbrowser.open(LINK_PROJ)

    def cancel(self):
        global app, p1, mesages, done, parent_conn, sock
        done = True

        parent_conn.send('/quit')
        p1.done = True
        print('1')
        p1.join()
        print('2')

        print('3')
        parent_conn.close()

        child_conn.close()
        sock.close()


        app.ids.chat_bl.remove_widget(app.ids.chat_bl.children[0])
        app.chat_build()
        print(app.ids)

        bl = MDBoxLayout(id='bl_cancel', padding=[450, 0, 0, 30])
        app.ids.bl_cancel = bl
        but = MDTextButton(id='ch_cancel', text='Добавить')
        but.on_release = app.cancel
        app.ids.ch_cancel = but
        bl.add_widget(but)
        app.ids.chat.add_widget(bl)
        bl.size_hint_x = 1
        bl.size_hint_y = 0.2
        but.font_size = 32
        but.color = 'blue'


    def send(self):
        global MSG, parent_conn
        if not done:
            msg = self.ids.mess.text
            card = MD3Card()
            card.ids.recs.text = msg
            h = (len(card.ids.recs.text) // 30 + 1) * 20 + 40
            card.height = h
            card.ids.card.height = h
            self.ids.chat_lay.add_widget(MDCard(height=h))
            self.ids.chat_lay.add_widget(card)
            parent_conn.send(msg)
            print(card.ids.recs.height)

            self.ids.mess.text = ''

    @mainthread
    def cout(self, out):
        self.msg = MD3Card()
        h = (len(out) // 30 + 1) * 20 + 40
        self.msg.ids.recs.text = out
        self.msg.height = h
        self.msg.ids.card.height = h
        self.ids.chat_lay.add_widget(self.msg)
        self.ids.chat_lay.add_widget(MDCard(height=h))


class Content(MDBoxLayout):
    def connect(self):
        global app, sock, p1, mesages, done, PROJ_NAME
        app.ids.chat.remove_widget(app.ids.bl_cancel)
        app.ids.chat_bl.remove_widget(app.ids.chat_bl.children[0])
        chat = Chat()
        chat.ids.linker.text = PROJ_NAME
        app.ids.chat_bl.add_widget(chat)

        done = False
        proc()
        mesages = Thread(target=get_MSG, kwargs=dict(ch=chat))
        mesages.start()

class Rooms(MDScrollView):
    '''Custom content.'''


class Connections(OneLineIconListItem):
    icon = StringProperty()

    def on_add(self):
        file = open('connections', mode='a', encoding='utf8')
        file.write(f'{self.text}\n{get_ip(ip=None, name=self.text, update=False, connect=True)[0]}\n')
        file.close()


class Chat_search(MDScreen):
    users = all_users()

    def set_list_people(self, text=""):

        def add_elem(name):
            self.ids.rv.data.append(
                {
                    "viewclass": "Connections",
                    "icon": 'account-arrow-left',
                    "text": name,
                    "callback": lambda x: x,
                }
            )

        self.ids.rv.data = []
        for names in self.users:
            if text in names[1]:
                add_elem(names[1])


class Account(MDBoxLayout):

    def open_proj_progress(self):
        global LINK_PROJ, PROJ_NAME, app

        prog = Progress()
        prog.prog_init(start=True)
        prog.ids.link.text = PROJ_NAME
        app.ids.acc.remove_widget(app.ids.acc.children[0])
        app.ids.acc.add_widget(prog)

    def reset_prof(self):
        self.remove_widget(self.ids.prof)
        self.add_widget(Prof_set())

    def create_project(self):
        if self.ids.new_proj.text == 'Создать проект +':
            self.remove_widget(self.children[0])
            self.add_widget(Proj_Creation())
        else:
            self.ids.new_proj.text = 'Создать проект +'
            self.ids.container.remove_widget(self.ids.enter_proj)
            self.ids.container.remove_widget(self.ids.bar)


class Prof_set(MDBoxLayout):
    aim_path = ''

    def save(self):
        global PROJ_NAME, LINK_PROJ, progr
        im = Image.open('test_1.png')
        im.save('test.png')
        self.remove_widget(self.ids.bl)
        contain = Account()
        self.add_widget(contain)
        
        if (PROJ_NAME != None) and (PROJ_NAME != 'proj'):
        	contain.ids.new_proj.text = 'Удалить проект'
        	but = MDTextButton(text=PROJ_NAME)
        	
        	contain.ids.enter_proj = but
        	contain.ids.container.add_widget(but)
        	
        	but.font_size = 28
        	but.pos_hint = {"center_x": .5}
        	but.color = 'blue'
        	but.on_release = contain.open_proj_progress
        	
        	bar = MDProgressBar(value=progr, size_hint_y=0.01, color=(0, 1, 0, .5))
        	contain.ids.container.add_widget(bar)
        	contain.ids.container.padding = [0, 10, 0, 450]
        	contain.ids.bar = bar
        	
        

    def change_image(self):
        self.file_manager = MDFileManager(
            select_path=self.select_path,
            exit_manager=self.exit_manager,
            preview=True
        )
        self.open_file_manager()

    def select_path(self, path):
        print(path)
        prepare_ava(path)
        self.ids.ava_s.source = 'test_1.png'
        self.exit_manager()

    def open_file_manager(self):
        self.file_manager.show('/')

    def exit_manager(self):
        self.file_manager.close()


class Enter(MDWidget):

    def app(self):
        global EMAIL, NAME, STATUS, app, LINK_PROJ, PROJ_NAME, progr
        check_pw = check_user_pw(self.ids.email.text)
        print(check_pw)
        bl = self.ids.bl

        if (self.ids.pw.text == check_pw) and (self.ids.pw.text != ''):
            EMAIL = self.ids.email.text
            bl.remove_widget(self.ids.a1)
            bl.remove_widget(self.ids.a2)
            self.app = App()

            contain = Account()
            data = get_user_data(EMAIL)
            NAME = data[1]
            STATUS = data[0]
            contain.ids.name.text = f"ФИО:\n    {NAME}"
            contain.ids.st.text = f"Статус:\n    {STATUS}"

            s = ht.HTTPConnection("ifconfig.me")
            s.request("GET", "/ip")
            
            get_ip(ip=s.getresponse().read().decode('utf8'), name=NAME, update=True, connect=False)
           

            self.app.ids.acc.add_widget(contain)
            self.chat_build()
            app = self.app
            bl.add_widget(self.app)
            proj_inform = new_project(NAME,'','',True)
            if proj_inform['project']:
            	LINK_PROJ = proj_inform['project_link']
            	PROJ_NAME = proj_inform['project']
            	contain.ids.new_proj.text = 'Удалить проект'
            	but = MDTextButton(text=PROJ_NAME, font_size=32)
            	
            	contain.ids.enter_proj = but
            	contain.ids.container.add_widget(but)
            	
            	but.font_size = 28
            	but.pos_hint = {"center_x": .5}
            	but.color = 'blue'
            	but.on_release = contain.open_proj_progress
            	
            	bar = MDProgressBar(value=progr, size_hint_y=0.01, color=(0, 1, 0, .5))
            	contain.ids.container.add_widget(bar)
            	contain.ids.container.padding = [0, 10, 0, 450]
            	contain.ids.bar = bar
            	
            	 

    def chat_build(self):
        rooms = Rooms()
        self.app.ids.chat_bl.add_widget(rooms)
        with open('connections', mode='r', encoding='utf8') as file:
            lines = file.readlines()
            for i in lines:
                if i[0].isalpha():
                    rooms.ids.box.add_widget(
                        MDExpansionPanel(
                            content=Content(),
                    panel_cls=MDExpansionPanelTwoLine(
                        text=i,
                        secondary_text="ученик"
                    )
                )
            )

    def reg(self):
        bl = self.ids.bl
        bl.remove_widget(self.ids.a1)
        bl.remove_widget(self.ids.a2)
        bl.add_widget(Reg())


class Reg(MDWidget):
    name = ''
    password = ''
    re_pass = ''
    email_re = ''
    status = ''

    def cansel(self):
        bl = self.ids.bl
        bl.remove_widget(self.ids.a1)
        bl.remove_widget(self.ids.a2)
        bl.add_widget(Enter())

    def regist(self):
        if self.ids.pupil.active:
            self.status = 'ученик'
        elif self.ids.teach.active:
            self.status = 'учитель'

        self.name = self.ids.name.text
        self.email_re = self.ids.email_r.text
        self.password = self.ids.passw.text
        self.re_pass = self.ids.re_pass.text
        check_1 = check_user_pw(self.email_re)

        if not check_1:
            if re.fullmatch(EMAIL_re, self.email_re):
                if len(self.name) >= 3:
                    if (self.password == self.re_pass) and (self.password != ''):
                        registration(name=self.name, pw=self.password, email=self.email_re, status=self.status)
                        self.cansel()

class TestApp(MDApp):

    def build(self):
        global app

        self.app = App()
        

        return Enter()



mesages = Thread()

if __name__ == '__main__':
    def proc():
        global p1, sock, parent_conn, child_conn
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock = s
        p, c = Pipe()
        parent_conn = p
        child_conn = c
        reserv_chats = Exchange(sock=s, conn=c)
        p1 = reserv_chats
        reserv_chats.start()


    freeze_support()
    sock = ''
    parent_conn, child_conn = 'Pipe()', 'd'
    p1 = Process()

    TestApp().run()
