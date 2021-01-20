import re
# Time Complexity is O(n^2)
def commonWords(TextFilePath1, TextFilePath2):
	try:
		f = open(TextFilePath1, 'r')
		token_list = []
		for line in f:
			for word in map(lambda x:x.lower(), re.findall(r"[a-zA-Z0-9_]+", line)):
				token_list.append(word)
		f.close()
	except:
		print("Error for opeing first file")
	try:
		f_2 = open(TextFilePath2, 'r')
		token_list2 = []
		for line in f_2:
			for word in map(lambda x:x.lower(), re.findall(r"[a-zA-Z0-9_]+", line)):
				token_list2.append(word)
		f_2.close()
	except:
		print("Error for opeing first file")

	x = set(token_list)
	y = set(token_list2)
	z = x.intersection(y)
	print(len(z))


file_name = input("type the File Path for first file: ")
file_name_2 = input("type the File Path for second file: ")
commonWords(file_name, file_name_2)
