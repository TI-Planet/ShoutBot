import threading

class setInterval():
	def __init__(self, func, sec):
		try:
			def func_wrapper():
				self.t = threading.Timer(sec, func_wrapper)
				self.t.start()
				func()
			self.t = threading.Timer(sec, func_wrapper)
			self.t.start()
		finally:
			self.t.cancel()

