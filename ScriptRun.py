
class DataProcesser(object):
	"""docstring for DataProcesser"""
	def __init__(self):
		self.record_file = None

		# function
		self.methodlist = {}
		self.methodlist['help'] = self.on_help
		self.methodlist['startRec'] = self.on_startRec
		self.methodlist['stopRec'] = self.on_stopRec

	def process(self, data):
		print('DataProcesser:', data)
		bin_spos =  data.find('"bin"')
		if bin_spos != -1:
			dictdata = eval(data[:bin_spos-1] + '}')
			bin_epos= data.find('}--end--')
			bin_data = data[bin_spos+6:bin_epos]
			# print 'bin_data:',bin_data
			f = open('test.bmp','w')
			f.write(bin_data)
			f.close()
			return "OK BMP"
		else:
			dictdata = eval(data)

		method = dictdata['method']
		param = dictdata['param']
		print('type',type(method),type(param))

		return self.methodlist[method](param)

	def issupport(self, name):
		for i in self.methodlist:
			if i == name and self.methodlist[i] != None:
				return True

		return False

	def on_help(self, list_data):
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

	def on_startRec(self, list_data):
		result = ''
		for i in list_data:
			result += '%s\n' % i

		if self.record_file != None:
			self.record_file.write(result)

		return result

	def on_stopRec(self, list_data):
		print 'close file '
		self.record_file.close()
		self.record_file = None

