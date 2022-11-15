import random, time
from deskapp.server import Server


class RadioStation:
    def __init__(self):
        self.server = Server()
        self.server.register_callback(self.callback)
        self.main()

    def callback(self, sess, message):
        username = sess.username
        if message.respawn:
            pass
        if message.dir_key:
            pass

    def main(self):
        self.server.start()
        while True:
            try:
                time.sleep(.5)
                self.server.update_publish(
                    'radio',
                    {'music': 'some song name.'}
                )
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(e)
        self.server.end_safely()


def main():
    RadioStation()

if __name__ == "__main__":
    main()