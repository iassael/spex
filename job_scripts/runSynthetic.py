from bo.demos.testSynthetic import testBranin, testHart3
import numpy as np
import re, os, sys, getopt


def getPath(subfolder):
	lpath = re.sub(r'runSynthetic.pyc?', subfolder, \
    	os.path.abspath(__file__))
	return lpath

def main(argv):                         
	name = ''; serial= ''; arrayid = ''
	
	try:
		opts, args = getopt.getopt(argv,"hn:s:a:", \
			["name=", "serial=", "arrayid="])
	except getopt.GetoptError:
		print 'runSynthetic.py -n <name> -s <serial> -a <arrayid>' 
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'runSynthetic.py -n <name> -s <serial> -a <arrayid>' 
			sys.exit()
		elif opt in ("-n", "--name"):
			name = arg
		elif opt in ("-s", "--serial"):
			serial = arg
		elif opt in ("-a", "--arrayid"):
			arrayid = arg

	if name == '' or serial == '' or arrayid == '':
		print 'runSynthetic.py -n <name> -s <serial> -a <arrayid>' 
		return

	if name == 'branin':
		result = testBranin(numIter=149)
	elif name == 'hart3':
		result = testHart3(numIter=149)
	else:
		print 'Not valid name given.'

	path = getPath('out-{}-{}/'.format(name, serial))

	try:
	    os.stat(path)
	except:
	    os.mkdir(path) 

	np.save('{}pybo-result-{}-{}'.format(path, name, arrayid), result)

if __name__ == '__main__':
	main(sys.argv[1:])