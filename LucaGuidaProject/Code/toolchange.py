#Tools:
# 0:Pneumatic extruder 1
# 1:Pneumatic extruder 2
# 2:Pneumatic extruder 3

def toolchange_function():

#=====================================================================================
#Positions of the heads are declared (X, Y, Z)
#=====================================================================================
    global pos
    pos=[[0 for x in range(3)] for y in range(7)]
    pos[0]=[-190,-231,-10]
    pos[1]=[-153,-231,-10]
    pos[2]=[-116,-231,-10]
    pos[3]=[-351.5,-217,-10]
    pos[4]=[0,0,0]
    pos[5]=[0,0,0]
    pos[6]=[0,0,0]


#=====================================================================================
#Lists containing activation and deactivation lines for all heads
#=====================================================================================
#For any tool change, first lines are needed to deactivate the head
#that has been used (final[]), successive lines are needed to activate the head
#that will be used (initial[]).
    final=[[] for y in range(7)]
    initial=[[] for y in range(7)]


#=====================================================================================
#Head 0
#=====================================================================================
    initial[0]=["\n",
                ";Activate extruder T0 (Pneumatic extruder 1)",
                "M206 X{} Y{} Z{};         home offset from 0,0,0 to extruder T0 ".format(pos[0][0],pos[0][1],pos[0][2]),
                "T0;                            change extruder ",
                "M104 S185 T0;                  set temperature and do not wait for it to be reached ",
                "G1 X25 Y25; ",
                "M400;",
                "",
                ""]

    final[0]=["\n",
              ";Deactivate extruder T0",
              "M107;                           disable fan ",
              "M400;",
              "M104 S11 ;                      turn off temperature",
              "M206 X{} Y{} Z{};       home offset from extruder T0 to 0,0,0".format(-pos[0][0],-pos[0][1],-pos[0][2]),
              #"M501;                           reset EEprom settings ",
              "G91;",
              "G1 Z30;",
              "G90;"]


#=====================================================================================
#Head 1
#=====================================================================================
    initial[1]=["\n",
                ";Activate extruder T1 (Pneumatic extruder 2)",
                "M206 X{} Y{} Z{};         home offset from 0,0,0 to extruder T1 ".format(pos[1][0],pos[1][1],pos[1][2]),
                "T1;                            change extruder ",
                "M104 S185 T1;                  set temperature and do not wait for it to be reached ",
                "G1 X25 Y25; ",
                "M400;",
                "",
                ""]

    final[1]=["\n",
              ";Deactivate extruder T1",
              "M107;                           disable fan ",
              "M400;",
              "M104 S11 ;                      turn off temperature",
              "M501;                           reset EEprom settings ",
              "G91;",
              "G1 Z30;",
              "G90;"]


#=====================================================================================
#Head 2
#=====================================================================================
    initial[2]=["\n",
                ";Activate extruder T2 (Pneumatic extruder 3)",
                "M206 X{} Y{} Z{};         home offset from 0,0,0 to extruder T2 ".format(pos[2][0],pos[2][1],pos[2][2]),
                "T2;                            change extruder ",
                "M104 S185 T2;                  set temperature and do not wait for it to be reached ",
                "G1 X25 Y25; ",
                "M400;",
                "",
                ""]

    final[2]=["\n",
              ";Deactivate extruder T2",
              "M107;                           disable fan ",
              "M400;",
              "M104 S11 ;                      turn off temperature",
              "M501;                           reset EEprom settings ",
              "G91;",
              "G1 Z30;",
              "G90;"]


#=====================================================================================
#Head 3
#=====================================================================================
    initial[3]=[";"]

    final[3]=["M104 S11"]


#=====================================================================================
#Head 4
#=====================================================================================
    initial[4]=["\n",
                ";Activate extruder T5 (Piston extruder)",
                "M206 X{} Y{} Z{};         home offset from 0,0,0 to extruder T5 ".format(pos[5][0],pos[5][1],pos[5][2]),
                "T2;",
                "G1 X25 Y25; ",
                "G92 E0;",
                "G91;",
                "G1 E40;",
                "G90;",
                "M400;",
                "G91;",
                "G1 Z-30;",
                "G90;",
                "T3;",
                "M17 E2;",
                "",
                ""]

    final[4]=["M400;",
              "T2;",
              "G92 E0;",
              "G91;",
              "G1 Z30 E-40;",
              "G90;"]


#=====================================================================================
#Array creation
#=====================================================================================
# The strings needed for tool change will be inserted into an array.

# The commands needed for the tool change depend both on the tool used before the
#change and on the tool that will be used after the change.

# The array has two dimensions:     x:tool that has been used before the tool change (T')
#                                   y:tool that will be  used after the tool change (T'')
#                                   cell [x][y]: String needed to change tool from T' to T''

    tool_change = [[[] for x in range(7)] for y in range(7)]

    for i in range (7):
        for j in range (7):
            for k in range(len(final[i])):
                tool_change[i][j].append(final[i][k])
            for l in range(len(initial[j])):
                tool_change[i][j].append(initial[j][l])


#=====================================================================================
#Head activation list
#=====================================================================================
#At the beginning of the print, no head is active
#To activate a new head, no other head has to be deactivated
#A list containing activation sequences only is created
    head_activation = [[] for x in range(7)]

    for i in range (7):
            for k in range(len(initial[i])):
                head_activation[i].append(initial[i][k])

    return[tool_change, head_activation, pos]
