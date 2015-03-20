input = open("hola.txt")
while 1:
	line = input.readline()
	if not line:
		break
	file = line.split()[0]
	print "wget http://libregeosocial.org/libregeosocial/apps/_gymkhana/templates/" + file
