from datetime import datetime

class DataProcesser(object):
	"""docstring for DataProcesser"""
	def __init__(self):
		self.record_file = None

		# function
		self.methodlist = {}
		self.methodlist['help'] = self.on_help
		self.methodlist['startRec'] = self.on_startRec
		self.methodlist['stopRec'] = self.on_stopRec
		self.methodlist['screen'] = self.on_screen

	def process(self, data):
		# print('DataProcesser:', data)
		bin_spos =  data.find('"bin":')
		bin_data = None
		if bin_spos != -1:
			# have binary data
			bin_epos= data.find('}--end--')
			bin_data = data[bin_spos+6:bin_epos]
			data = data[:bin_spos-1] + '}'

		dictdata = eval(data)
		method = dictdata['method']
		param = dictdata['param']
		print('type',type(method),type(param))

		return self.methodlist[method](param,bin_data)

	def issupport(self, name):
		for i in self.methodlist:
			if i == name and self.methodlist[i] != None:
				return True

		return False

	def on_help(self, list_data,bin_data):
	    result = 'Support Command:  '

	    for i in range(len(list_data)):
	        result += '%s  ' % list_data[i]
	        if i == 6 or i == 13 or i == 20:
	            result += '\n'

	    result += '\n'
	    return result

	def set_recfilename(self, filename):
		self.record_file = open(filename,'w')
		print('create file:',self.record_file)

	def on_startRec(self, list_data,bin_data):
		result = ''
		for i in list_data:
			result += '%s\n' % i

		if self.record_file != None:
			self.record_file.write(result)

		return result

	def on_stopRec(self, list_data,bin_data):
		print 'close file '
		self.record_file.close()
		self.record_file = None

	def on_screen(self, list_data,bin_data):
		now = datetime.today()
		# print 'bin_data:',bin_data
		filename = "%s-%s-%s.bmp" % (now.hour,now.minute,now.second)
		f = open(filename,'wb')
		f.write(bin_data)
		f.close()
		return "OK BMP,size:%d" % len(bin_data)
