import re

# token is a sequence of alphanumeric characters
# store each token into list
# cuz we can igore the capitalization 
# so each time add the token we lower the word 
# Time Complexity is O(n^2)
def tokenize(TextFilePath):
    try:
        f = open(TextFilePath, 'r')
        token_list = []
        for line in f:
            for word in map(lambda x:x.lower(), re.findall(r"[a-zA-Z0-9_]+", line)):
            	token_list.append(word)
        f.close()
        return token_list
    except:
        print("Error for opeing the file")
# token list as a prameter 
# compute the word frequencies 
# assgin to a new dict, return dict (the dict contain each value and key)
# Time Complexity is O(n^2)
def computeWordFrequencies(*Token_List):
	length = len(token_list)
	wordFreq = {}
	for i in range(length):
		word = token_list[i]
		j = i
		count = 0
		while j < length:
			if(word == token_list[j]):
				count += 1
				j+=1
			else:
				j+=1
		if word not in wordFreq:
			wordFreq.update({word:count})
	return wordFreq

# Time Complexity is O(n)
def printsWordFreq(**Token_List):
	a = sorted(Token_List.items(), key=lambda x: x[1], reverse=True)
	for keys,values in a:
		print("<token>", keys,"<",values,">")


# the main function below 
file_name = input("type the File Path: ")
token_list = tokenize(file_name)
wordFreq_list = computeWordFrequencies(token_list)
printsWordFreq(**wordFreq_list)

