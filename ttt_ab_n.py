#!/usr/bin/env pythonself.n
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 22:52:28 2021

@author: dell-ubuntu

player 1's symbol=X
player 2's symbol=O

for nXn board using random picking of first n-1 moves
"""


from pade.acl.aid import AID
from pade.acl.messages import ACLMessage
from pade.core.agent import Agent
#from pade.behaviours.protocols import Behaviours
from pade.misc.utility import start_loop,display_message,call_later
import random
import numpy as np

class Tic_tac_toe(Agent):
    def __init__(self,aid,c,n):
        super().__init__(aid=aid)
        self.player1=c[0]
        self.player2=c[1]
        print("starting both agents")
        print("initialized")
        self.player_list1=[]
        self.player_list2=[]
        self.turn=random.randint(1,2)
        self.moves=0;
        self.board=[]
        self.n=n
        for i in range(n):
            b=[]
            for i in range(n):
                b.append("_")
            self.board.append(b)
        self.board=np.array(self.board)
        call_later(1,self.send_message)
        
    def printBoard(self):
        for i in range(self.n):
            for j in range(self.n):
                print(self.board[i][j],end=" ")
            print()
                
    def test_valid_move(self,move):
        if(self.board[int((move-1)/self.n)][(move-1)%self.n]=="_"):
            return True;
        else: return False;
        
        
    def testwin(self,player):
        st=[]
        if(player==1):
           st=["X"]*self.n
        else: 
           st=["O"]*self.n
        win=False
        #test in rows for specified string 
        for i in range(self.n):
            if(all(self.board[i]==st)):# test for ith row 
                win=True
            if([self.board[j][i] for j in range(self.n)]==st):#test for ith column
                win=True
        #test for columns
        if([self.board[i][i] for i in range(self.n)]==st):
            win=True
        if([self.board[i][self.n-1-i] for i in range(self.n)]==st):
            win=True
            
        if(win==True):
            self.printBoard()
            if(player==1):
                print(self.player1.aid.localname+" has won!!!!")
            else: print(self.player2.aid.localname+" has won!!!!")
        return win
        
        
    def react(self,message):
        super().react(message)
        win=False
        move=message.content
        if(self.test_valid_move(move)==True):
            if(self.turn==1):
                
                i=int((move-1)/self.n)
                j=(move-1)%self.n
                self.board[i][j]="X"
                self.turn=2
                win=self.testwin(1)
            else:
                self.board[int((move-1)/self.n)][(move-1)%self.n]="O"
                self.turn=1
                win=self.testwin(2)
            self.moves+=1
        print(self.board)
        if(win==False and self.moves<self.n*self.n):
            call_later(1,self.send_message)
        elif(win==False and self.moves==self.n*self.n):
            print("Match draw!!!!!!!")
            self.printBoard()
            
    def send_message(self):
        self.printBoard()
        display_message(self.aid.localname,"Player{} turn!!!!".format(self.turn))
        message=ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        if(self.turn==1):
            message.add_receiver(self.player1.aid)
        else:
            message.add_receiver(self.player2.aid)
        self.agentInstance.table[message.receivers[0].localname]=message.receivers[0]
        ml=[]
        ml.append("Player{} turn!!!!".format(self.turn))
        #if player is a computer then first element in list will be his list and at 2 it will be opponents list
        if(message.receivers[0].localname.__contains__("Computer1")):
            ml.append(self.board)
            ml.append("X")
            ml.append(self.n)
        elif(message.receivers[0].localname.__contains__("Computer2")):
            ml.append(self.board)
            ml.append("O")
            ml.append(self.n)
        message.set_content(ml)
        self.send(message)
        
    #def turn():
        

class PlayingAgent(Agent):
    mymoves=[]
    def __init__(self,aid):
        super().__init__(aid=aid)
        self.moves=0
    
    def testwin(self,board,playersymbol):
        st=[playersymbol]*self.n
        win=False
        #test in rows for specified string 
        for i in range(self.n):
            if(all(board[i]==st)):# test for ith row 
                win=True
            if([board[j][i] for j in range(self.n)]==st):#test for ith column
                win=True
        if([board[i][i] for i in range(self.n)]==st):
            win=True
        if([board[i][self.n-1-i] for i in range(self.n)]==st):
            win=True
            
        """if(win==True):
            self.printBoard()
            if(player==1):
                print(self.player1.aid.localname+" has won!!!!")
            else: print(self.player2.aid.localname+" has won!!!!")"""
        return win
    def play_my_move(self,board,mysymbol,ply,pcount):
        opsymbol=""
        if(mysymbol=="O"):
            opsymbol="X"
        else:
            opsymbol="O"
        #allposiblities=[]
        move_possible=False
        mvalue=0 #value for current node
        if ply=="max":
            mvalue=-2  #initialization for max ply in tic tac toe only self.n values are there -1,0,1 
            #so i put -1 in place of -inf 
        else: mvalue=2  #initialization for min ply i.e. its upper bound in place of inf i choosen 1
        mmove=-1    #move for current value
        abtest=False #alpha-beta prunning test variable initially no pruning required hence False
        i=0
        j=0
        for i in range(self.n):
            for j in range(self.n):
                #for each position in board
                if(board[i][j]=="_"):
                    #if already not filled
                    move_possible=True
                    b=np.copy(board)
                    #fill it and test further
                    if(ply=="max"):
                        #if max ply fill with my symbol
                        b[i][j]=mysymbol
                        mywin=self.testwin(b,mysymbol)
                        #test for my winnig after this move
                        if(mywin==True):
                            #if won myvalue is 1 as I won
                            mvalue=1
                            mmove=i*self.n+j
                        else:
                            #if I do not win then play further
                            move_value=self.play_my_move(b,mysymbol,"min",mvalue)
                            #if value of mychild is better then me update my value(mvalue)
                            if(mvalue<move_value[1]):
                                mvalue=move_value[1]
                                mmove=i*self.n+j
                        if(mvalue>=pcount):
                            #if myvalue is greater than parent value then do no check for other moves possible
                            #as this is max ply which will always result in value myval or greater than myval
                            #where as parent need less or this so no need to go further
                            abtest=True
                            #allposiblities.append([i*self.n+j,move_value[1]])
                    else:
                        #if min ply fill with opponent symbol
                        b[i][j]=opsymbol
                        opwin=self.testwin(b,opsymbol)
                        #test for opponent's winnig after this move
                        if(opwin==True):
                            #if opponent won make mvalue as -1 as I lost
                            mvalue=-1
                            mmove=i*self.n+j
                            #allposiblities.append([i*self.n+j,-1])
                        else:
                            #if opp do not win then play further as next move is mine so max ply
                            move_value=self.play_my_move(b,mysymbol,"max",mvalue)
                            #if value of anymove is worst then me update my value(mvalue)
                            if(mvalue>move_value[1]):
                                mvalue=move_value[1]
                                mmove=i*self.n+j
                        if(mvalue<=pcount):
                            #if myvalue is less than parent value then do no check for other moves possible
                            #as this is min ply which will always result in value myval or less than myval
                            #where as parent need more or this so no need to go further
                            abtest=True
                    if abtest==True:
                        #as ab test has satisfied so do not explore more so make loop variable at their max
                        break
            if abtest==True:
                break
        
        #if no move available then 
        if(move_possible==False):
            if(self.testwin(board,mysymbol)==True):
                #return value 1 if I won
                return [-1,1];
            elif(self.testwin(board,opsymbol)==True):
                #return value -1 if opponent won
                return [-1,-1];
            else:#return 0 if draw
                return [-1,0];
        else: #return my value
            return[mmove,mvalue]
        """if(ply=="max"):
            #extract all the values to get minimum
            values=[allposiblities[i][1] for i in range(len(allposiblities))]
            i=values.index(max(values))            
            return allposiblities[i]
        else:
            values=[allposiblities[i][1] for i in range(len(allposiblities))]
            i=values.index(min(values))            
            return allposiblities[i]"""
    
    def send_mymove(self,msg):
        print("choosing my move")
        board=msg[1]
        mysymbol=msg[2]
        self.n=msg[3]
        move=[]
        print("got board ")
        if(self.moves<=self.n-2):
            empty=[]
            for i in range(self.n):
                for j in range(self.n):
                    if board[i][j]=="_":
                        empty.append(i*self.n+j)
            move.append(random.choice(empty))
            self.moves+=1
        else:
            move=self.play_my_move(board,mysymbol,"max",1)
        mymove=move[0]+1
        message=ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.add_receiver(self.reciever)
        self.agentInstance.table[self.reciever.localname]=message.receivers[0]
        message.set_content(mymove)
        self.send(message)
        
    def react(self,message):
        super().react(message)
        info=message.content
        self.reciever=message.sender
        call_later(1,self.send_mymove,info)
        
class humanAgent(Agent):
    def __init__(self,aid):
        super().__init__(aid=aid)
        

    def send_mymove(self):
        move=int(input("Enter your move:"))
        message=ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.add_receiver(self.reciever)
        self.agentInstance.table[self.reciever.localname]=message.receivers[0]
        message.set_content(move)
        self.send(message)
        
    def react(self,message):
        super().react(message)
        self.reciever=message.sender
        call_later(1,self.send_mymove)

if __name__=="__main__":
    n=int(input("Enter size for board"))
    print("choose your game:")
    print("1)agent vs agent")
    print("2)agent vs human")
    print("3)human vs human")
    c=int(input("Enter your choice"))
    agent=[]
    if(c>=1 and c<=3):
        player1=1;
        player2=1;
        if(c==1):
            player1=PlayingAgent(AID(name='player1_Computer1{}@localhost:{}'.format(20010,20010)))
        else:
            player1=humanAgent(AID(name='player1_{}@localhost:{}'.format(20010,20010)))
        if(c==3):
            player2=humanAgent(AID(name='player1_{}@localhost:{}'.format(20020,20020)))
        else:
            player2=PlayingAgent(AID(name='player1_Computer2{}@localhost:{}'.format(20020,20020)))
        agent.append(player1)
        agent.append(player2)
        agent_name = 'tic_tac_toe_agent_{}@localhost:{}'.format(20000,20000)
        agent.append(Tic_tac_toe(AID(name=agent_name),agent[0:2],n))
        start_loop(agent)
    else: print("wrong choice")
        
    