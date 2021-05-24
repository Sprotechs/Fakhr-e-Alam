import os
for file in os.listdir("uiFiles"):
	if '.ui' in file:
		os.system(f"pyuic5 uiFiles/{file} -o pyFiles/{file.replace('.','_')}.py")