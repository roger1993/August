# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 10:35:03 2017

@author: Santiago
"""

import odeParser
import graphParser

graphDict = graphParser.parser_main().dict

workDataDict = odeParser.odeParser()

for key,value in workDataDict.items():
    print(key,value)

reactionComponents = [initParameters.split('=')[0] for initParameters in workDataDict[2]['begin init']]
print(reactionComponents)

opinionDict = {i:reactionComponents[i] for i in range(len(reactionComponents))}

for key,value in opinionDict.items():
    print(key,value)

#Here we can include a step in which we send this opinions to the graph opinion generator so we
#can no which of the possible several opinions has been chosen by the user

begin_initial = dict()
initlist = []

for key,value in graphDict.items():
    if value.get_opinion() == 1:
        initlist.append(['y' + str(key),'=','1'])
        initlist.append(['m' + str(key),'=','0'])
        initlist.append(['n' + str(key),'=','0'])
    if value.get_opinion() == 0:
        initlist.append(['y' + str(key),'=','0'])
        initlist.append(['m' + str(key),'=','1'])
        initlist.append(['n' + str(key),'=','0'])
    if value.get_opinion() == -1:
        initlist.append(['y' + str(key),'=','0'])
        initlist.append(['m' + str(key),'=','0'])
        initlist.append(['n' + str(key),'=','1'])  
begin_initial['begin init'] = initlist

workDataDict[2] = begin_initial

begin_reaction = dict()

from itertools import product, permutations
def eq_writer(equation,idFrom,idTo):
    a = list(permutations([idFrom, idTo], 2))
    permutes = list(product(*[a,a]))
    res = []
    for i in range(4):
        res.append(' '.join(equation).replace('yes', 'y{}').\
            replace('no', 'n{}').replace('maybe', 'm{}').\
            format(permutes[i][0][0], permutes[i][0][1],
                   permutes[i][1][0], permutes[i][1][1]).\
            split())
    return res

from collections import deque
    
curr_node = graphDict.popitem()[1]
eq_list = workDataDict[3]['begin reactions']
waiting_list = deque([])
eq_list_new = []
while True:
    curr_node.visiting()
    for node in curr_node.get_friends():
        if not node.is_visited():
            for i in range(len(eq_list)):
                eq_list_new += eq_writer(eq_list[i], curr_node.get_uid(), node.get_uid())
            waiting_list.append(node)
    try:
        curr_node = waiting_list.popleft()
    except:
        break

workDataDict[3]['begin reactions'] = eq_list_new

odeParser.odeWriter(workDataDict)


     
