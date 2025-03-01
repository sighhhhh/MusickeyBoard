import time

from pyo import *

server = Server().boot()
server.start()


a = Sine(mul=0.01).out()
server.gui(locals())


time.sleep(2)


server.shutdown()