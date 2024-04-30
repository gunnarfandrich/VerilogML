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


# Function definitions
def Avg(lst):
    if len(lst) == 0:
        return 0
    else:
        return round(sum(lst) / len(lst))


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
 
            if "module " in line:
                moduleName = line.split(" ")[1]
                moduleName = moduleName.split("(")[0]
                print(moduleName)
            
            # ignore everything until the actual code begins
            if "always @" in line:
                go = 1
                
                if lineCount:
                    sequentialStateList.append(lineCount)
                
                lineCount = 0
            
            if go == 1:
                # count lines for average number of sequential operations
                lineCount = lineCount + 1
            
                # Types of arithmetic operations.
                for i in arithmeticOperatorsBasic:
                    if i in line:
                        if not "//" in line and not "for" in line and not "if" in line and not "module" in line and not "/*" in line and not "*/" in line:
                            # add i to operatorDict and increment its value
                            operatorDict[i] = operatorDict.get(i,0) + 1
                                            
                # Number of conditional blocks
                for i in conditionalOperators:
                    if i in line:
                        if not "//" in line:                          
                            # add i to conditionalDict and increment its value
                            conditionalDict[i] = conditionalDict.get(i,0) + 1


    # DEBUG
    #print("Average Number of Sequential States: ", Avg(sequentialStateList))
    #print("Type and Number of Arithmetic Operations: ", operatorDict)
    #print("Type and Number of Conditional Blocks: ", conditionalDict, "\n")
    # END DEBUG
    

    dfTest = (pd.DataFrame.from_dict(orient='index', columns=[fileName.split(".")[0]], data=operatorDict)).T
    dfTest1 = (pd.DataFrame.from_dict(orient='index', columns=[fileName.split(".")[0]], data=conditionalDict)).T
    
    # concatenate dataframe with operator and conditional data
    df_merged = pd.concat([dfTest, dfTest1], axis=1)

    # append number of sequential states to dataframe
    df_merged['Seq. States'] = Avg(sequentialStateList)
    
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

    # manually run the power script... you can hardcode values in as seen below if necessary... The power value calculated will be printed to the terminal
    print(get_power.caleScript(
                               script="dc_power.tcl",
                               home_dir="~/Desktop/VerilogML/",
                               design_dir="~/Desktop/VerilogML/ip-cores/debug/",
                               design_path="ip-cores/debug/",
                               design_name="fulladd"))
    
    
if name == "-d" or name == "--d" or name == "-directory":
    directory = sys.argv[2]
    
    cwd = os.getcwd()
    
    #create empty dataframe for storage
    df = pd.DataFrame()
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1] in supportedExtensions:

                # get module name and a dataframe of the current design to be analyzed                
                moduleName, tempDf = getFeatures(os.path.join(root, file), file)
		
                # DEBUG
                #print("Current Design Dir:" , os.path.join(cwd,root))
                #print("Current Design Path: " , os.path.join(root,file))
                #print("Current Design Name: " , moduleName)
                # END DEBUG

                # format to integers for pretty viewing
                tempDf = tempDf.apply(np.int64)


                # add power value
                tempDf['Dynamic Power (W)'] = get_power.caleScript(
                                                               script="dc_power.tcl",
                                                               home_dir=cwd,
                                                               design_dir=os.path.join(cwd,root),
                                                               design_path=os.path.join(root, file),
                                                               design_name=moduleName)


                # concatenate dataframes
                df = pd.concat([df, tempDf])

                # replace NaN with zeroes
                df = df.replace(np.nan, 0)
                
                print(df)
    
    #print(df)
