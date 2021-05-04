
import argparse,sys,json
from termcolor import colored
import subprocess
import os
import argparse,sys,json
from termcolor import colored
import subprocess
import datetime


class warna():
	"""docstring for warna"""
	def red(self,str):
		return colored(str, "red")
	def blue(self,str):
		return colored(str, "blue")
	def green(self,str):
		return colored(str, "green")
	def yellow(self,str):
		return colored(str, "yellow")


def save(text, names):
	s = open(names, "a")
	s.write(text+"\n")

	return s

def create_dir(dir):
	try:
		linux = 'mkdir '+dir
		windows = 'makedirs '+dir
		os.makedirs([dir, dir][os.name == 'nt'])
	except:
		pass

def validator(aws_access_key_id ,aws_secret_access_key ,default_region,folder):
	limit = False
	cus = warna()
	date = datetime.datetime.now().strftime('%Y-%m-%d')
	raw = "{}|{}|{}".format(aws_access_key_id,aws_secret_access_key,default_region)
	try:
		print(cus.blue("[+] ============================ [+]"))
		print(cus.yellow("[+] Setup aws aws_access_key_id : {}".format(aws_access_key_id)))
		subprocess.call('aws configure set aws_access_key_id {}'.format(aws_access_key_id),shell=True)

		subprocess.call('aws configure set aws_secret_access_key  {}'.format(aws_secret_access_key),shell=True)
		print(cus.yellow("[+] Setup aws aws_secret_access_key : {}".format(aws_secret_access_key)))
		subprocess.call('aws configure set default.region  {}'.format(default_region),shell=True)
		print(cus.yellow("[+] Setup aws Region : {}".format(default_region)))

		aw = subprocess.check_output('aws service-quotas list-service-quotas --service-code ec2 --query "Quotas[*].{QuotaName:QuotaName,Value:Value}" --max-items 6', shell=True).decode()
		try:
			parsing = json.loads(aw)
			try:
				if parsing:
					print(cus.green("[+] aws_access_key_id : {}".format(aws_access_key_id)))
					print(cus.green("[+] aws_secret_access_key : {}".format(aws_secret_access_key)))
					print(cus.green("[+] Region : {}".format(default_region)))
					wekuk = '\naws_access_key_id : '+aws_access_key_id+'\naws_secret_access_key : '+aws_secret_access_key+'\nRegion : '+default_region+'\nServices :'
					save(wekuk, folder+"result.txt")
					service = []
					data = parsing[3]
					if "All P Spot Instance Requests" in data['QuotaName']:
						lim = data['Value']
						if lim == 0.0:
							status = "[+] Service Status :  BAD , Limit :  {}".format(lim)
							print(cus.red(status))
						else:
							status = "[+] Service Status :  GOOD , Limit :  {}".format(lim)
							print(cus.green(status))
					else:
						status = "[+] Service Status :  BAD , Limit : {}".format(lim)
						print(cus.red(status))
					save(status,folder+"result.txt")
					print(cus.blue("[+] ============================ [+]"))
					save(raw,folder+'raw_live.txt')
				else:
					print(cus.red("[-] ============================ [-]"))
					print(cus.red("[-] aws_access_key_id : {}".format(aws_access_key_id)))
					print(cus.red("[-] aws_secret_access_key : {}".format(aws_secret_access_key)))
					print(cus.red("[-] Region : {}".format(default_region)))
					print(cus.red("[-] Status : Die"))
					print(cus.red("[-] ============================ [-]"))
					wekuk = ' aws_access_key_id : '+aws_access_key_id+'\n aws_secret_access_key : '+aws_secret_access_key+'\n Region : '+default_region+'\n '
					save(wekuk, folder+'aws_secret_bad_result.txt')
					save(raw,folder+'raw_bad.txt')
			except Exception as e:
				print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
				pass
		except Exception as e:
			pass
	except Exception as e:
		print(cus.red("[-] ============================ [-]"))
		print(cus.red("[-] aws_access_key_id : {}".format(aws_access_key_id)))
		print(cus.red("[-] aws_secret_access_key : {}".format(aws_secret_access_key)))
		print(cus.red("[-] Region : {}".format(default_region)))
		print(cus.red("[-] Status : Die"))
		print(cus.red("[-] ============================ [-]"))
		aw = ' aws_access_key_id : '+aws_access_key_id+'\n aws_secret_access_key : '+aws_secret_access_key+'\n Region : '+default_region+'\n '
		save(aw, folder+'aws_secret_bad_result.txt')
		pass


def main():

	try:
		cus = warna()
		listnya = input(cus.yellow("[+] Input your Aws Key List : "))
		folder = input(" Put Your Folder Save : ")
		folders = str(folder)
		if '/' or '\\' not in folders:
			folders = str(folder)+'/'
		create_dir(folders)
		#print (folder)
		#exit(1)
		if listnya:
			try:
				with open(listnya, 'r') as op:
					for x in op:
						if len(x.rstrip().split('|')) == 3:
							extraxt = x.rstrip().split('|')
							aws_access_key_id = extraxt[0]
							aws_secret_access_key = extraxt[1]
							aws_region = extraxt[2]
							validator(aws_access_key_id,aws_secret_access_key,aws_region,folders)
						else:
							save(x, folders+"unknow-result.txt")
						
			except IOError as e:
				raise e
			pass

	except Exception as e:
		raise e



if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt  as e:
		print("[!] Exit Program....")
		sys.exit()
		pass
