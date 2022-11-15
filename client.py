import random, time
from deskapp import App, Module, callback
from deskapp.server import ClientSession


LoginID = random.random()
class Login(Module):
    name = 'Login'
    def __init__(self, app):
        super().__init__(app)
        self.classID = LoginID
        self.register_module()

        # GLOBAL LOGIN STUFFS.
        self.username = "Agent42"
        self.password = 'password42'
        self.hostname = 'localhost'
        self.client = False
        self.update = True
        self.index = 3
        self.scroll = 3

        self.print("finished loading login module.")

    def page(self, panel):
        panel.addstr(1,1,"Login to listen to other peoples Music or Your own!")
        self.scroll_elements = [
            f"Username: {self.username}",
            f"Password: {'*'*len(self.password)}",
            f"Host: {self.hostname}",
            "-  Login -",
            "-- Exit --"
        ]
        clear_to = self.index
        self.index = 3

        if self.update:
            self.update = False
            for i in range(clear_to-3):
                panel.addstr(3+i,1," "*(self.max_w-5))
            
        for index, element in enumerate(self.scroll_elements):
            color = self.frontend.chess_white if index is not self.scroll else self.frontend.color_rw
            panel.addstr(self.index, 4, element, color)
            self.index += 1
        
    def string_decider(self, string_input):
        super().string_decider(string_input)
        self.update = True
        if self.scroll == 0: self.username = string_input
        elif self.scroll == 1: self.password = string_input
        elif self.scroll == 2: self.hostname = string_input

    def end_safely(self):
        if self.client:
            self.client.end_safely()
            self.print("client ended safely")

    @callback(LoginID, 10)
    def on_enter(self, *args, **kwargs):
        if self.scroll == 3: self.login()
        elif self.scroll == 4: self.app.close()

    def login(self):
        self.print(f"Starting Login to '{self.hostname}'")
        self.client = ClientSession(SERVER_HOST=self.hostname,VERBOSE=False)
        self.client.connect()
        if not self.client.connected:
            self.print(f"can't connect to client.({self.hostname})")
            self.client = False
            return
        self.client.login(self.username,self.password)
        time.sleep(.1)
        if not self.client.logged_in:
            time.sleep(1)
            if not self.client.logged_in:
                self.print("login failed.")
                return
        self.print("Login successful.")
        self.app.data['client'] = {
            'host': self.hostname,
            'client': self.client
        }
        self.app.add_module(Radio)

    
RadioID = random.random()
class Radio(Module):
    name = 'Radio'
    def __init__(self, app):
        super().__init__(app)
        self.classID = RadioID
        self.register_module()
        self.game_setup()

    def game_setup(self):
        self.client = self.app.data['client']['client']
        self.client.add_sub('radio')
        self.print("Subbing to channel radio.")

    def page(self, panel):
        panel.addstr(1,1,"This is the Station!")
        idx = 2
        try:
            theRadio = self.client.data['radio']
            # for line in theMap:
            #     if idx >= self.max_h-1: break
            #     l = ['.' if x==0 else '&' for x in line]
            #     panel.addstr(idx, 2, ''.join(l))
            #     idx += 1
        
        except Exception as e:
            # self.print(e)
            pass



def main():
    app = App(
        modules=[Login],splash_screen=False,demo_mode=False,
        name='DeskRadio',title='DeskRadio',header='DeskRadio',
        v_split=.3,h_split=.2,autostart=False
        )
    app.start()


if __name__ == "__main__":
    main()
