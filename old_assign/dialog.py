#!/usr/bin/python3.4
# This program runs a dialog between two agents, which must be defined
# elsewhere as separate modules.

# import Shrink3 as agentA
# import Hearnone as agentB
import bwg2 as agentA
import dtyfung as agentB


f = open('sampleConversation.txt','w')

N_TURNS = 10
turn = 0
f.write(str(turn)+"A: "+agentA.agentName() + ': ' + agentA.introduce()+"\n")
f.write(str(turn)+"B: "+agentB.agentName() + ': ' + agentB.introduce()+"\n")
remark = agentB.introduce() #"Good morning" #
for i in range(N_TURNS):
    turn += 1
    remark = str(agentA.respond(remark))
    f.write(str(turn)+"A: "+agentA.agentName() + ': ' + remark+"\n")
    remark = agentB.respond(remark)
    f.write(str(turn)+"B: "+agentB.agentName() + ': ' + remark+"\n")
