import os

def caleScript(script, home_dir, design_path, design_name, design_dir):
	
        # Example of each variable for debugging or manual calling of script
        #script = "dc_power.tcl"
	#home_dir = "~/Desktop/VerilogML/"
	#design_dir = "~/Desktop/VerilogML/ip-cores"
	#design_name = "s38584"


        # Execute TCL script with Synopsis Design Compiler
	os.system("HOME_DIRECTORY="+home_dir+" DESIGN_DIRECTORY="+design_dir+" DESIGN_NAME="+design_name+" dc_shell-t -f "+script)

	adj_num = 0.0

	# create temporary directory to store .rpt files
	if not os.path.exists('./cache/'):
		os.makedirs('./cache/')


        # Open .rpt file and extact Total Dynamic Power
	with open('./cache/' + design_name + '_power.rpt', 'r') as f:

		adj_num = 0.0
		for line in f:
		    if "Total Dynamic Power" in line:
		        line = line.lstrip("Total Dynamic Power =")
		        line = line.split("(")
		        line = line[0]
		        line = line.split(" ")
		        num = float(line[0])
		        unit = line[1]
		        if(unit== "W"):
		            adj_num = num
		        elif(unit== "dW"):
		            adj_num = num * 1e-1
		        elif(unit== "cW"):
		            adj_num = num * 1e-2
		        elif(unit== "mW"):
		            adj_num = num * 1e-3
		        elif(unit== "uW"):
		            adj_num = num * 1e-6
		        elif(unit== "nW"):
		            adj_num = num * 1e-9
		        elif(unit== "pW"):
		            adj_num = num * 1e-12
		        elif(unit== "fW"):
		            adj_num = num * 1e-15
		        else:
		            print("unknown unit")
		            quit()
		        break

	# return power value with units
	return adj_num
		                
