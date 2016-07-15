from pointer import create_or_connect


import numpy as np

def a_function():
  time = create_or_connect('time', 'time1')
  mem = create_or_connect('memory', 'mem1')
  mem.start("vector") ; time.start("vector")
  toto = np.random.rand(10000000)
  time.stop("vector") ; mem.stop("vector")

  mem.start("matrix") ; time.start("matrix")
  tutu = np.random.rand(20000,10000)
  time.stop("matrix") ; mem.stop("matrix")
