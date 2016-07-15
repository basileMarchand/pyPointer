from pyPointer import create_or_connect

from example_2_dependy import a_function


a_function()


ptime = create_or_connect('time', 'time1')
pmem  = create_or_connect('memory', 'mem1')

ptime.resume()
pmem.resume()


