#encoding=utf-8
import time
import hashlib
import traceback
import sys

class Client(object):
	"""docstring for Client"""

	__start_timesteamp=0;
	__user_name="";
	__user_salt="";
	__PASSWORD_NUMS=8
	__MAPPING_NUMS=10
	__SLEEP_TIME=10
	__PERCENTAGE_WIDTH=2
	__MIN2SEC=60
	__PERCENTAGE=100
	__TIMESTEAMP_MID=5
	__TIMESTEAMP_END=10

	def __init__(self):
		# self.__start_timesteamp = time.mktime(time.strptime(time.strftime('%Y-%m-%d %H:%M:00'),'%Y-%m-%d %H:%M:%S'))
		self.__user_name="Huajie";
		self.__user_salt="Token";

	def __translate(self,pwd):
		tmp_pwd=''
		for x in xrange(0,self.__PASSWORD_NUMS):
			step=len(pwd)/self.__PASSWORD_NUMS
			index=step*x
			tmp_pwd+=self.mapping(pwd[index:index+1])
		return tmp_pwd

	def mapping(self,chr):
		return str(ord(chr)%self.__MAPPING_NUMS)

	def __calcPassword(self):
		self.__start_timesteamp = time.mktime(time.strptime(time.strftime('%Y-%m-%d %H:%M:00'),'%Y-%m-%d %H:%M:%S'))
		timesteamp=str(self.__start_timesteamp)[0:self.__TIMESTEAMP_END]
		has = hashlib.md5()
		password=self.__user_name+timesteamp[0:self.__TIMESTEAMP_MID]+self.__user_salt+timesteamp[self.__TIMESTEAMP_MID:self.__TIMESTEAMP_END]
		has.update(password)
		password=has.hexdigest()
		old_password=password
		password=self.__translate(password)
		return password

	def run(self):
		old_password=''
		progress_bar=''
		while True:
			progress_percentage=int((time.time()-self.__start_timesteamp)/self.__MIN2SEC*self.__PERCENTAGE)/self.__PERCENTAGE_WIDTH
			password=self.__calcPassword();
			if password!=old_password:
				old_password=password
				print("\n"+password)
			else:
				progress_bar = '#'*progress_percentage
				sys.stdout.write("process:"+str(progress_percentage*self.__PERCENTAGE_WIDTH)+"%   "+progress_bar+"\r")
				sys.stdout.flush()
			time.sleep(1);


if __name__ == '__main__':
	c=Client()
	try:
		c.run()
	except KeyboardInterrupt:
		print "\n bye"