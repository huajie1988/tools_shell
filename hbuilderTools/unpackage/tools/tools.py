#-*- coding: UTF-8 -*- 
import sys,os,json,traceback,time,re

reload(sys)
sys.setdefaultencoding('utf-8') #设置Python的默认编码为 utf-8

################################################################

class Tools(object):

	path="";
	name="";
	environment="";
	version="";
	tplfolder="";
	modulefolder="";
	globalmodulefolder="";
	globalcssfolder="";
	viewfolder="";
	modules="";

	"""docstring for Tools"""
	def __init__(self):
		super(Tools, self).__init__()
		config = self.__getConfig()
		for k in config.keys():
			self.__setattr__(k,config[k])
#---------------------------------------------------------------
	def __setattr__(self, name, value):
		object.__setattr__(self, name, value)		
#---------------------------------------------------------------
	def create(self):
		
		self.__createModule()
		print "OK"

#---------------------------------------------------------------
	def update(self):
		self.__updateModule()
		print "OK"
#---------------------------------------------------------------
	def __readFile(self,file):
		fileObj = open(file)
		error=""
		try:
			fileText = fileObj.read()
		except Exception, e:
			error=e.message		
		finally:
			fileObj.close()
			error+=traceback.format_exc()
			self.__writeError(error)
		return fileText
#---------------------------------------------------------------
	def __writeError(self,error_msg):
		""""""
		content="\n=============================ERROR  INFO========================================\n"
		content+="\n time:"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"\n error message:"+error_msg+"\n"
		content+="\n================================================================================\n"
		self.__writeFile('error.log',content,'a+')
#---------------------------------------------------------------
	def __writeFile(self,file_path,content,type="w"):
		""""""
		file_object = open(file_path, type)
		file_object.write(content)
		file_object.close() 				
#---------------------------------------------------------------
	def __getConfig(self):
		path = os.path.dirname(__file__)
		config = self.__readFile(path+'/setting.json')
		config = json.loads(config)		
		return config
#---------------------------------------------------------------
	def __createModule(self):
		content=self.__readFile(self.path+"/"+self.tplfolder+"/init.js")
		layout=self.__readFile(self.path+"/"+self.tplfolder+"/layout.html")
		
		for k,v in self.modules.items():
			if not os.path.exists(self.path+"/"+self.tplfolder+"/"+k):
				self.__createDir(self.path+"/"+self.tplfolder+"/"+k)
			# print self.path+"/"+self.tplfolder+"/"+k
			# sys.exit()
			if(v.has_key('global')):
				js_file=self.path+"/"+self.globalmodulefolder+"/"+k+".js"
				if not os.path.exists(js_file):
					self.__writeFile(js_file,content)
			else:
				js_file_path=self.path+"/"+self.modulefolder+"/"+k
				if not os.path.exists(js_file_path):
					self.__createDir(js_file_path)
				js_file=js_file_path+"/"+k+".js"
				if not os.path.exists(js_file):
					self.__writeFile(js_file,content)
			css_tpls = re.search('{%csspath%}(.*?){%endcsspath%}', layout)
			layout_tmp=self.__replaceTpl(layout,self.path+"/"+self.globalcssfolder,css_tpls,self.globalcssfolder)

			js_tpls = re.search('{%jspath%}(.*?){%endjspath%}', layout_tmp)
			layout_tmp=self.__replaceTpl(layout_tmp,self.path+"/"+self.globalmodulefolder,js_tpls,self.globalmodulefolder)
			
			if(not v.has_key('global')):
				self_js_tpls = re.search('{%selfjspath%}(.*?){%endselfjspath%}', layout_tmp)
				layout_tmp=self.__replaceTpl(layout_tmp,js_file_path,self_js_tpls,self.modulefolder+"/"+k)
			else:
				layout_tmp= layout_tmp.replace('{%selfjspath%}<script src="{%path%}"></script>{%endselfjspath%}','')		
			
			if not os.path.exists(self.path+"/"+self.viewfolder+"/"+k+".html"):
				self.__writeFile(self.path+"/"+self.viewfolder+"/"+k+".html",layout_tmp)
#---------------------------------------------------------------

	def __createDir(self,path):
		os.makedirs(path)

#---------------------------------------------------------------
		
	def __replaceTpl(self,layout,path,css_tpls,rep_path):
		for parent,dirnames,filenames in os.walk(path):
			file=''
			for filename in filenames:
				css_tpl=css_tpls.group(1)
				if((self.environment=='min' or self.environment=='prod')):
					if not(filename.find('.min.')>0 or filename.find('.prod.')>0):
						continue
					else:
						file+=css_tpl.replace('{%path%}',rep_path+'/'+filename)+"\n"
				else:
					if (filename.find('.min.')>0 or filename.find('.prod.')>0):
						continue
					else:
						file+=css_tpl.replace('{%path%}',rep_path+'/'+filename)+"\n"					

			return layout.replace(css_tpls.group(0),file)

#---------------------------------------------------------------

	def __updateModule(self):
		for k,v in self.modules.items():
			view=self.__readFile(self.path+"/"+self.viewfolder+"/"+k+".html")
			
			if(v.has_key('tpl')):
				tpl_arr=v['tpl'].strip().strip(',').split(',')
				for tpl in tpl_arr:
					
					if tpl[0:1] == '.':
						tpl_file=self.path+"/"+self.tplfolder+"/"+k+"/"+tpl+".html";
					else:
						tpl_file=self.path+"/"+self.tplfolder+"/"+tpl+".html";
					
					if os.path.exists(tpl_file):
						tpl_str=self.__readFile(tpl_file)
						view=view.replace('{%'+os.path.basename(tpl)+'%}',tpl_str)

				
				self.__writeFile(self.path+"/"+self.viewfolder+"/"+k+".html",view)


#---------------------------------------------------------------

	d={
		'create':create,
		'1':create,
		'update':update,
		'2':update,
	}

	def run(self):
		self.__help()
		choice=raw_input("please please input a commend: ")
		""""""
		error=""
		try:
			self.d.get(choice)(self)
		except Exception, e:
			error=e.message        
		finally:
			if(error.strip()!=""):
				self.run()
				error+=traceback.format_exc()
				self.__writeError(error)		

	def __help(self):
		print "=============================="
		print "*       Hbuilder Tools       *"
		print "*    please input commend    *"
		print "*           1.create         *"
		print "*           2.update         *"
		print "=============================="

################################################################

def main():
	t=Tools()
	t.run()

if __name__ == '__main__':
    main()

