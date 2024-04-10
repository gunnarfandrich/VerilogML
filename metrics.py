# Python Script to extract features from a given python file or directory
# March 9 2024, By: Gunnar Fandrich
# Last Updated: March 9, 2024

#import pyverilog
import sys

helpMessage = "Pass the file or directory name to be evaluated following the name of the python file!"

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
    
    
    
    
# Function definitions
def Avg(lst):
    return round(sum(lst) / len(lst))


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


# initialize empty dictionaries to store counts of each target feature
operatorDict = {}
conditionalDict = {}
sequentialStateList = []

# FLAGS
go = 0

# COUNTERS
lineCount = 0

# check each line for the desired operators

with open(name) as fp:
    for line in fp:
        #print(line)
        
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
                        
            
            # Number of conditional blocks
            for i in conditionalOperators:
                if i in line:
                    if not "//" in line:
                        #print(line)
                        #print(i)
                        
                        # add i to conditionalDict and increment its value
                        conditionalDict[i] = conditionalDict.get(i,0) + 1
                        
                        
                        


# Get average number of sequential states
#for i in range(len(sequentialStateList)):
#    print(sequentialStateList[i])

averageSequentialStates = Avg(sequentialStateList)




print("Average Number of Sequential States: ", averageSequentialStates)
print("Type and Number of Arithmetic Operations: ", operatorDict)
print("Type and Number of Conditional Blocks: ", conditionalDict)