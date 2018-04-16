stuff = {}

stuff["abstrac"] = "I don't like Marty"
stuff["title"] = "Die baby"

for key, value in stuff.items():
	if("Marty" in key or "Marty" in value):
		print("True")
	else:
		print("False")

