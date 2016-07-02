#encoding=utf-8

import sys
import urllib2
import urllib
import json
import time
import traceback

reload(sys)
sys.setdefaultencoding('utf-8') #设置Python的默认编码为 utf-8

class Translate(object):
	"""docstring for Translate"""

	error=''
	source_file_path=''
	target_file_path=''
	error_log_path=''
	trans_url=''
	tmp_short_urls=[]
	def __init__(self):
		super(Translate, self).__init__()
		config_json=self.readFile('config.json')
		config_obj = json.loads(config_json)
		self.source_file_path=config_obj['SOURCE_FILE_PATH']
		self.target_file_path=config_obj['TARGET_FILE_PATH']
		self.error_log_path=config_obj['ERROR_LOG_PATH']
		self.trans_url=config_obj['TANSLATE_URL']
	# def readFile(self):
	# 	data = sys.argv[1:]
	# 	if not sys.stdin.isatty():
	# 		data.append(sys.stdin.read())

	# 	if data[0]=='':
	# 		print "The Source File is empty"
	# 		sys.exit(-1)

	# 	return data[0].split()

	def readFile(self,file_path):
		file = open(file_path)
		file_text=''
		try:
			file_text = file.read()
		except Exception, e:
			self.error=e.message
			self.writeLog(self.error) 
			sys.exit(-1)
		finally:
			file.close()
			return file_text

	def getShortURL(self,urls):
		short_urls=[]
		line=1
		for url in urls:
			trans_url = self.trans_url
			data = urllib.urlencode({'url':url})
			req = urllib2.Request(trans_url,data)
			response = urllib2.urlopen(req)
			res = response.read()
			res_json=json.loads(res)
			if res_json['status']>=0:
				short_urls.append(res_json['tinyurl'])
			else:
				err='Translate Fail: Line '+str(line)+' URL '+url+'  error code '+str(res_json['status'])+' error msg '+res_json['err_msg']
				self.writeLog(err) 
				short_urls.append(url)
			line+=1
			self.tmp_short_urls=short_urls
			print str(float(line)/len(urls)*100)+"%\n"
		return short_urls

	def run(self):
		try:
			source_urls=self.readFile(self.source_file_path)

			if source_urls=='':
				print 'The source file is empty'
				sys.exit(-1)
			source_urls=source_urls.split()
			short_urls=self.getShortURL(source_urls)
			self.writeFile(self.target_file_path,"\n".join(short_urls))
			print "Translate finish !"
		except Exception, e:
			self.error=e.message+traceback.format_exc()
			self.writeLog(self.error) 
			sys.exit(-1)
	
	def writeFile(self,file_path,text,mode='w'):
		file_object = open(file_path, mode)
		file_object.write(text)
		file_object.close()

	#----------------------------------------------------------------------
	def writeLog(self,error_msg):
		""""""
		content="\n=============================ERROR  INFO========================================\n"
		content+="\n time:"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"\n error message:"+error_msg+"\n"
		content+="\n================================================================================\n"
		self.writeFile(self.error_log_path,content,'a+')

	def writeCrash(self):
		self.writeFile(self.target_file_path,"\n".join(self.tmp_short_urls))




if __name__ == '__main__':
	t=Translate()
	try:
		t.run()
	except KeyboardInterrupt:
		t.writeCrash()
	