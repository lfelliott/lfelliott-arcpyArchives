import os.path, fnmatch
def listFiles(root, patterns = '*', recurse=1, return_folders = 0):
	pattern_list = patterns.split(';')
	class Bunch:
		def __init__(self, **kwds): self.__dict__.update(kwds)
	arg = Bunch(recurse=recurse, pattern_list = pattern_list, return_folders=return_folders, results=[])
	def visit(arg, dirname, files):
		for name in files:
			fullname = os.path.normpath(os.path.join(dirname, name))
			if arg.return_folders or os.path.isfile(fullname):
				for pattern in arg.pattern_list:
					if fnmatch.fnmatch(name, pattern):
						arg.results.append(fullname)
						break
		if not arg.recurse: files[:]=[]
	os.path.walk(root, visit, arg)
	return arg.results
files2 = listFiles(r'd:\\images\\', '*.jpg')
for name2 in files2: print name2