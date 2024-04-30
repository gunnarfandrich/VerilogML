# Python Script to extract features from a given python file or directory
# March 9 2024, By: Gunnar Fandrich
# Last Updated: March 9, 2024

#import pyverilog
import sys
import os
import pandas as pd
import numpy as np
import get_power


helpMessage = "Pass the file or directory name to be evaluated following the name of the python file!"

    
# Function definitions
def Avg(lst):
    if len(lst) == 0:
        return 0
    else:
        return round(sum(lst) / len(lst))


# Supported File Extensions
supportedExtensions = [
                        ".vhd",
                        ".v"
                        ]


# Dictionary definitions
arithmeticOperatorsBasic = [
                        "+",
                        "-",
                        "*",
                        "/",
                        "rem",
                        "mod",
                        "<",
                        "<=",
                        ">",
                        ">=",
                        "=",
                        "/="
                        ]

arithmeticOperatorsExtend1 = [
                        "sll",
                        "srl",
                        "rol",
                        "ror"
                        ]

arithmeticOperatorsExtend2 = [
                        "not",
                        "and",
                        "or",
                        "nand",
                        "nor",
                        "xor",
                        "xnor"
                        ]
                        
                        
conditionalOperators = [
                    "if",
                    "else",
                    "elif",
                    "case"
                    ]





# check each line for the desired operators
def getFeatures(name, fileName):

    moduleName = ""

    with open(name) as fp:
    
        # initialize empty dictionaries to store counts of each target feature
        operatorDict = {}
        conditionalDict = {}
        sequentialStateList = []

        

        # FLAGS
        go = 0

        # COUNTERS
        lineCount = 0
    
    
        for line in fp:
            #print(line)


 
            if "module " in line:
                moduleName = line.split(" ")[1]
                moduleName = moduleName.split("(")[0]
                print(moduleName)
            
            # ignore everything until the actual code begins
            if "always @" in line:
                go = 1
                
                if lineCount:
                    #print("CURRENT COUNT IS = ", lineCount)
                    sequentialStateList.append(lineCount)
                
                lineCount = 0
            
            if go == 1:
            
                # number of sequential states
                
                #print("line count =", lineCount)
                
                
                lineCount = lineCount + 1
            
                # Types of arithmetic operations.
                for i in arithmeticOperatorsBasic:
                    if i in line:
                        if not "//" in line and not "for" in line and not "if" in line and not "module" in line and not "/*" in line and not "*/" in line:
                            #print(line)
                            #print(i)
                            
                            # add i to operatorDict and increment its value
                            operatorDict[i] = operatorDict.get(i,0) + 1
                            
                            #print(operatorDict[i])
                    #else:
                    #    operatorDict[i] = 0
                
                # Number of conditional blocks
                for i in conditionalOperators:
                    if i in line:
                        if not "//" in line:
                            #print(line)
                            #print(i)
                            
                            # add i to conditionalDict and increment its value
                            conditionalDict[i] = conditionalDict.get(i,0) + 1
                    #else:
                    #    conditionalDict[i] = 0       
                            
                            


    # Get average number of sequential states
    #for i in range(len(sequentialStateList)):
    #    print(sequentialStateList[i])

    #averageSequentialStates = Avg(sequentialStateList)




    #print("Average Number of Sequential States: ", averageSequentialStates)
    #print("Type and Number of Arithmetic Operations: ", operatorDict)
    #print("Type and Number of Conditional Blocks: ", conditionalDict, "\n")
    
    
    dfTest = (pd.DataFrame.from_dict(orient='index', columns=[fileName.split(".")[0]], data=operatorDict)).T
    dfTest1 = (pd.DataFrame.from_dict(orient='index', columns=[fileName.split(".")[0]], data=conditionalDict)).T
    
    
    #print(dfTest)
    #print(dfTest1)
    
    df_merged = pd.concat([dfTest, dfTest1], axis=1)
    df_merged['Seq. States'] = Avg(sequentialStateList)
    
    
    #print(df_merged)
    
    return moduleName, df_merged
    
    
    
    
    
try:
    name = sys.argv[1]
except:
    print(helpMessage)
    print("Example: fileName.py myVerilog.v")
    print()
    sys.exit()

if name == "-?" or name == "-help" or name == "--help":
    print(helpMessage)
    print()
    sys.exit()

if name == "--debug":
    print("DEBUG ACTIVE")
    
    debugFile = sys.argv[2]

    print(get_power.caleScript(
                               script="dc_power.tcl",
                               home_dir="~/Desktop/VerilogML/",
                               design_dir="~/Desktop/VerilogML/ip-cores/debug/",
                               design_path="ip-cores/debug/",
                               design_name="fulladd"))
    
    
    
if name == "-d" or name == "--d" or name == "-directory":
    directory = sys.argv[2]
    
    #create empty dataframe for storage
    df = pd.DataFrame()
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1] in supportedExtensions:
                print("Current File: " + os.path.join(root, file))

                moduleName, tempDf = getFeatures(os.path.join(root, file), file)

                #print(file.split(".")[0])

                #print(moduleName)				

                print("Dir is:" , root)


                # add power value
                tempDf['Dynamic Power'] = get_power.caleScript(script="dc_power.tcl", home_dir="~/Desktop/VerilogML/", design_dir=root, design_path=os.path.join(root, file), design_name=moduleName)


                print(tempDf)

		# combine dataframe
                #df = pd.concat([df, getFeatures(os.path.join(root, file), file)[1]])
                
                df = pd.concat([df, tempDf])
                



                # replace NaN with zeroes
                df = df.replace(np.nan, 0)
                
                #print(df)

    
    #integers only in dataframe
    df = df.apply(np.int64)
    
    
    print(df)
