import weasyprint as wp

class TestClass(object):
	def foo(self):
		print('hi')


wp.TC = TestClass