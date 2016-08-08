import inspect

#stacks
ds = [] #data stack
cs = [] #call stack
vws = [] #variable work stack
dws = [] #dictionary work stack
iws = [] #if work stack
lws = [] #loop work stack
nws = [] #name work stack

dict = {
	"+": lambda : (ds.append(int(ds.pop()) + int(ds.pop()))) if len(ds) > 1 else error("stack underflow"),
	"-": lambda : (ds.append(int(ds.pop(-2)) - int(ds.pop()))) if len(ds) > 1 else error("stack underflow"),
	"*": lambda : (ds.append(int(ds.pop()) * int(ds.pop()))) if len(ds) > 1 else error("stack underflow"),
	"/": lambda : (ds.append(int(ds.pop(-2)) / int(ds.pop()))) if len(ds) > 1 else error("stack underflow"),
	"<": lambda : (ds.append(-1) if int(ds.pop(-2)) < int(ds.pop()) else ds.append(0)) if len(ds) > 1 else error("stack underflow"),
	">": lambda : (ds.append(-1) if int(ds.pop(-2)) > int(ds.pop()) else ds.append(0)) if len(ds) > 1 else error("stack underflow"),
	"=": lambda : (ds.append(-1) if int(ds.pop()) == int(ds.pop()) else ds.append(0)) if len(ds) > 1 else error("stack underflow"),
	".": lambda : print_tos() if len(ds) > 0 else error("stack underflow"),
	"depth": lambda : ds.append(len(ds)),
	":": lambda : handle_add_to_dict(),
	"create": lambda : handle_create(),
	",": lambda : allot_single() if len(nws) > 0 else error("name work stack underflow"),
	"allot": lambda : allot_area() if len(nws) > 0 else error("name work stack underflow"),
	"@": lambda : ds.append(vws[int(ds.pop())]) if len(ds) > 0 else error("stack underflow"),
	"!": lambda : set_var() if len(ds) > 1 else error("stack underflow"),
	"does>": lambda : handle_does() if len(nws) > 0 else error("name work stack underflow"),
	"begin": lambda : handle_begin(),
	"again": lambda : handle_again() if len(lws) > 0 else error("loop work stack underflow"),
	"until": lambda : handle_until() if len(lws) > 0 else error("loop work stack underflow"),
	"if": lambda : handle_if(),
	"else": lambda : handle_else() if len(iws) > 0 else error("if work stack underflow"),
	"then": lambda : handle_then() if len(iws) > 0 else error("if work stack underflow"),
	"drop": lambda : ds.pop() if len(ds) > 0 else error("stack underflow"),
	"swap": lambda : ds.insert(-1, int(ds.pop())) if len(ds) > 1 else error("stack underflow"),
	"words": lambda : print_words(),
	"see": lambda : print_word(),
	"dup": lambda :	ds.append(ds[-1]) if len(ds) > 0 else error("stack underflow"),
	"file": lambda : get_file_name(),
	"run": lambda : run_file() if len(nws) > 0 else error("name work stack underflow"),
	"save": lambda : save_file() if len(nws) > 0 else error("name work stack underflow") }

#global counters and flags
ip = 0 #instruction pointer
vi = 0 #variable index
adding_word = 0
adding_var = False
reading_file_name = False
var_name = ""
add_to_dict = False
error_occured = False
printing_word = False
execution_allowed = True
debugging = False

def debug(msg):
	if debugging == True:
		print "debug: " + str(msg)

def error(msg):
	global error_occured 
	error_occured = True
	print "error, " + msg

def get_file_name():
	global reading_file_name
	reading_file_name = True

def run_file():
	global ip
	file_name = nws.pop()
	ip += 1
	print "reading file " + file_name
	try:
		file = open(file_name, 'r')
		for line in file:
			#print ">> " + line[:-1]
			read_line(line)	
		print "done, running read file"
		ip -= 1
	except IOError:
		error("invalid file: " + file_name)

def save_file():
	global ip
	file_name = nws.pop()
	print "writing file " + file_name
	ip -= 2
	cs.pop(ip)
	cs.pop(ip)
	cs.pop(ip)
	try:
		file = open(file_name, 'w')
		for word in cs:
			file.write(word + "\n")
		print "done"
	except IOError:
		error("invalid file: " + file_name)

def set_var():
	i = ds.pop()
	vws[i] = int(ds.pop())

def handle_create():
	global adding_var
	adding_var = True

def add_var(name):
	global adding_var
	nws.append(name)
	adding_var = False

def allot_single():
	global vi
	global dict
	if len(nws) != 0:
		dict[nws.pop()] = str(vi)
	if len(ds) == 0:
		ds.append(0)
	vws.append(int(ds.pop()))
	vi += 1

def allot_area():
	global vi
	global dict
	size = ds.pop()
	if len(nws) != 0:
		dict[nws[-1]] = str(vi)
	for i in range(0, size):
		vws.append(0)
	vi += size

def handle_begin():
	lws.append(ip)

def handle_again():
	global ip
	ip = lws[-1]

def handle_until():
	if ds.pop() == -1:
		lws.pop()
	else:
		handle_again()

def handle_add_to_dict():
	global add_to_dict
	add_to_dict = True

def handle_if():
	global execution_allowed
	global iws
	condition = ds.pop()
	if condition == -1:
		iws.append(True)
		execution_allowed = True
	elif condition == 0:
		iws.append(False)
		execution_allowed = False
	else:
		error("unknown truth")

def handle_else():
	global execution_allowed
	if iws[-1] == True:
		execution_allowed = False
	else:
		execution_allowed = True

def handle_then():
	global execution_allowed
	execution_allowed = True
	iws.pop()

def print_tos():
	print str(ds.pop())

def print_words():
	print dict.keys()

def print_word(word = "dummy"):
	global printing_word
	if printing_word == False:
		printing_word = True
	else:
		if hasattr(dict[word], '__call__'):
			print inspect.getsource(dict[word])
		else:
			print dict[word]
		printing_word = False

def handle_does():
	global adding_word
	adding_word += 1
	dws.append(nws[-1])

def add_word(word):
	global adding_word
	global add_to_dict
	if word in dict:
		error("error, word already in dictionary: " + word)
	else: 
		dict[word] = ""
		dws.append(word)
		adding_word += 1
		add_to_dict = False

def add_to_word(word):
	global adding_word
	global dict
	if word == ";":
		dws.pop()
		adding_word -= 1
	else:
		dict[dws[-1]] = dict[dws[-1]] + " " + word

def expand_word(word):
	global ip
	i = 0
	cs.pop(ip)
	for expanded in dict[word].split():
		debug(dict[word])
		debug(expanded)
		cs.insert(ip + i, expanded)
		i += 1
	ip -= 1

def exec_word(word):
	global add_to_dict
	global execution_allowed	
	global error_occured 
	global ip
	global reading_file_name
	debug(word)
	if execution_allowed == False and word != "then" and word != "else":
		ip += 1
		return
	elif add_to_dict == True:
		add_word(word)
	elif printing_word == True:
		print_word(word)
	elif adding_word > 0:
		add_to_word(word)	
	elif adding_var == True:
		add_var(word) 
	elif reading_file_name == True:
		nws.append(word)
		reading_file_name = False
	elif word.isdigit() or (word[0] == "-" and word[1:].isdigit()):
		ds.append(int(word))
	elif word in dict:
		if hasattr(dict[word], '__call__'):
			dict[word]()
		else:
			expand_word(word)
	else:
		error("unknown word or context: " + word)
	ip += 1

def read_line(line):
	global error_occured 
	for word in line.split():
		cs.append(word)
	flush_call_stack()

def flush_call_stack():
	global ip
	while ip < len(cs):
		debug(cs[ip])
		debug(ds)
		exec_word(cs[ip])
		if error_occured == True:
			break

def main():
	global error_occured
	global ip
	cs.append("file")
	cs.append("default.dth")
	cs.append("run")
	flush_call_stack()
	while 1:
		input = raw_input(str(len(ds)) + " >> ")
		if input == "exit":
			debug(cs)
			debug(len(cs))
			debug(str(ip))
			break
		read_line(input)
		if error_occured == True:
			error_occured = False
			ip = len(cs)
		else:
			print " ok "

if __name__== "__main__":
	main()
