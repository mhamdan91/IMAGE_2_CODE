
# auto tabs
lines
dic = ["#", "def", "for", "while", "elif", "if", "else","class"]
non_tab = ["elif", "else"]
special = False
for i, line in enumerate (lines):
	for e in dic:
		if line. contains  {e):
			rest = False
			cleaned = ""
			for ch in line:
				if ch in e or rest:
					cleaned+= ch
					rest = True
			lines[i] = cleaned
			
	for j in range(tabs[i]):
		lines[i] = "\t" + lines[i]