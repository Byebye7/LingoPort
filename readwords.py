with open('wordlist.txt','r') as f:
	file = f.readlines()

words = []
for line in file:
	a = line.strip().split("\t")
	for word in a:
		words.append(word.lower())
words.sort()

with open('words.txt','w') as out:
	for word in words:
		out.writelines(word + '\n')

