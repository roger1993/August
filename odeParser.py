# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 23:14:45 2017

@author: Santiago Romagosa Arjona
"""

def odeParser(infile = 'YesOrNo.ode'):
    with open(infile,'r') as infile:
        
                
        beginFlags = ['begin model','begin parameters','begin init','begin reactions','simulateODE']
        endFlags = ['end model','end parameters','end init','end reactions']
    
        #Here all the input file data necessary for making the calculations over the graph are going to be saved, and also not saved in the outFileData,until is processed
        """
        {index:{
            beginFlag:list of data lines
         }
        }
        """
        workData = {i:{beginFlags[i]:[]} for i in range(len(beginFlags))}
    
        readData = False
        data = []
    
        #Key of workData dict to keep the appearance order of the different parser code blocks
        index = 0    
        for line in infile:

            line = line.strip()                

            lineWordList = line.split()
            
            twoFirstWords = ' '.join(lineWordList[:2])
    
            #Read model name
            if(twoFirstWords == beginFlags[0]):
                workData[index][beginFlags[0]].extend(lineWordList[2:])
                index+=1
            #Read parameters
            if(twoFirstWords==endFlags[1]):
                readData = False
                workData[index][beginFlags[1]].extend(data)
                data = [] 
                index+=1
            if(readData and index==1):
                if('//' in line):
                    if(line.index('//')!=0):
                        indexLimit = line.index('//')
                        data.append(line[:indexLimit])
                else:
                    data.append(line)
            if(twoFirstWords == beginFlags[1]):
                readData = True
                
            #Read init
            if(twoFirstWords==endFlags[2]):
                readData = False
                workData[index][beginFlags[2]].extend(data)
                data = [] 
                index+=1
            if(readData and index==2):
                if('//' in line):
                    if(line.index('//')!=0):
                        indexLimit = line.index('//')
                        data.append(line[:indexLimit])
                else:
                    data.append(line)
            if(twoFirstWords == beginFlags[2]):
                readData = True
                
            #Read reactions            
            if(twoFirstWords==endFlags[3]):
                readData = False
                workData[index][beginFlags[3]].extend(data)
                data = []   
                index+=1
            if(readData and index==3):
                if('//' in line):
                    if(line.index('//')!=0):
                        indexLimit = line.index('//')
                        data.append(line[:indexLimit])
                else:
                    data.append(line)
            if(twoFirstWords == beginFlags[3]):
                readData = True
                
            if(beginFlags[4] in line):
                workData[index][beginFlags[4]] = line
                
    return workData
     
    
    
def odeWriter(workData,outfile = 'YesOrNoParser.ode'):  
    
    beginFlags = ['begin model','begin parameters','begin init','begin reactions','simulateODE']
    endFlags = ['end model','end parameters','end init','end reactions']
    endFlagDict = {beginFlags[i]:endFlags[i] for i in range(len(beginFlags)) if i<len(endFlags)}
    finalOutfileLine = '' 

    with open(outfile,'w') as outfile:
        for indexOrder in workData.keys():
            beginFlag = beginFlags[indexOrder]
            if(indexOrder==0):
                finalOutfileLine = endFlagDict[beginFlag]
                print(beginFlag+' '+workData[indexOrder][beginFlag][0],file=outfile)   

            elif(indexOrder!=4):
                print(beginFlag,file=outfile)  
                for line in workData[indexOrder][beginFlag]:
                    print(line,file=outfile)                
                print(endFlagDict[beginFlag],file=outfile)

            else:
               print(workData[indexOrder][beginFlag],file=outfile)
        
        print(finalOutfileLine,file=outfile)


            
                
        
        


