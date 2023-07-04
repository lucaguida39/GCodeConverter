def layerchange_function():
    from toolchange import toolchange_function
    import tempfile
    [tool_change, head_activation, pos]=toolchange_function()
    LedPos=[402, 232, -0.7]

#=====================================================================================
#Find the temporary file folder in which settings are stored
#=====================================================================================
    temp=tempfile.gettempdir()
    filename = temp + "/datagcodeconverter.txt"


#=====================================================================================
#Recover stored settings
#=====================================================================================
    file=open(filename)
    lines = file.readlines()
    folder_path = str(lines[0].strip())
    LedActive = bool(int(lines[1].strip()))
    if lines[2].strip()=="":
        LedTime=0
    if lines[2].strip()!="":
        LedTime = float(lines[2].strip())
    ExtraRun = bool(int(lines[3].strip()))
    ExtraBeforeLayerChangeDirection = str(lines[4].strip())
    if lines[5].strip()=="":
        ExtraBeforeLayerChange = 0
    if lines[5].strip()!="":
        ExtraBeforeLayerChange = str(lines[5].strip())


#=====================================================================================
#Generate lines retraction
#=====================================================================================
    Retraction_penumatic=[  "",
                            ";Retraction (Release pressure)",
                            "M106 S0;" ,
                            "M106 P3;",
                            ""]


#=====================================================================================
#Generate commands for extra run at layer change
#=====================================================================================
    ExtraString=";"
    if ExtraRun==True:
        if ExtraBeforeLayerChangeDirection=="Up":
            ExtraString="Y{}".format(ExtraBeforeLayerChange)
        if ExtraBeforeLayerChangeDirection=="Down":
            ExtraString="Y-{}".format(ExtraBeforeLayerChange)
        if ExtraBeforeLayerChangeDirection=="Right":
            ExtraString="X{}".format(ExtraBeforeLayerChange)
        if ExtraBeforeLayerChangeDirection=="Left":
            ExtraString="X-{}".format(ExtraBeforeLayerChange)


#=====================================================================================
#Generate lines for UV curing
#=====================================================================================
    if LedTime<=120:
        LedString=[ "M106 P4;",
                    "G4 S{};".format(LedTime),
                    "M107 P4;"]
#In order to prevent LEDs over heating, curing times longer than 120 seconds are
#divided into periods of 60 seconds alternated with 30 seconds of pause
    if LedTime>120:
        LedString=[]
        i=0
        n=int(LedTime/60)
        for i in range (n):
            NewStrings=[ "M106 P4;",
                        "G4 S60;",
                        "M107 P4;",
                        "G4 S30;"]
            for i in range(len(NewStrings)):
            	LedString.append(NewStrings[i])
        FinalString=[ "M106 P4;",
                    "G4 S{};".format(LedTime-60*n),
                    "M107 P4;"]
        for i in range(len(FinalString)):
            	LedString.append(FinalString[i])


#=====================================================================================
#Generate lines for UV curing routine (including motion to led position)
#=====================================================================================
    LC=["\n",
        ";Stringa per il cambio layer",
        "\n"]
    if LedActive==True:
        LC=[]

        LC1=["\n",
             ";LAYER CHANGE WITH UV CURING",
             "G60;",
             "G91;",
             "G1 {};".format(ExtraString),
             "G1 Z20 F300;",
             "G90;",
             "G1 X0 Y0 F3000;",
             "G91;",
             "G1 X{} Y{} F2400;",
             "G400;",
             "G1 Z-20 F300;",
             "G1 Z{};",
             "\n"]

        LC2=[   "\n",
       		    "G1 Z{};",
        		"G1 Z20;",
                "G1 X{} Y{} F2400;",
                "G400;",
                "G1 Z-1 F300;",
                "G90;",
                "G61 [X] [Y];",
                "\n",
                "\n"]

        for i in range(len(LC1)):
            	LC.append(LC1[i])
        for i in range(len(LedString)):
            	LC.append(LedString[i])
        for i in range(len(LC2)):
            	LC.append(LC2[i])


#=====================================================================================
#Generate a dictionary containing layer change blocks for each head
#=====================================================================================
    layerchange_dict = {}


#=====================================================================================
#Head 0
#=====================================================================================
    Head=0
    LC_final=[]
    Subst=[[0 for x in range(3)] for y in range(len(LC))]

    if LedActive==True:
        Subst[9][0]=LedPos[0]+pos[Head][0]
        Subst[9][1]=LedPos[1]+pos[Head][1]
        Subst[12][0]=LedPos[2]+pos[Head][2]
        Subst[len(LC1)-1+len(LedString)+2][0]=-LedPos[2]-pos[Head][2]
        Subst[len(LC1)-1+len(LedString)+4][0]=-LedPos[0]-pos[Head][0]
        Subst[len(LC1)-1+len(LedString)+4][1]=-LedPos[1]-pos[Head][1]

        for i in range(len(Retraction_penumatic)):
        			LC_final.append(Retraction_penumatic[i])
        for i in range(len(LC)):
        			LC_final.append(LC[i].format(Subst[i][0], Subst[i][1], Subst[i][2]))

    else:
        LC_final=LC

    layerchange_dict[Head] = LC_final
    del(LC_final)



#=====================================================================================
#Head 1
#=====================================================================================
    Head=1
    LC_final=[]
    Subst=[[0 for x in range(3)] for y in range(len(LC))]

    if LedActive==True:
        Subst[9][0]=LedPos[0]+pos[Head][0]
        Subst[9][1]=LedPos[1]+pos[Head][1]
        Subst[12][0]=LedPos[2]+pos[Head][2]
        Subst[len(LC1)-1+len(LedString)+2][0]=-LedPos[2]-pos[Head][2]
        Subst[len(LC1)-1+len(LedString)+4][0]=-LedPos[0]-pos[Head][0]
        Subst[len(LC1)-1+len(LedString)+4][1]=-LedPos[1]-pos[Head][1]


        for i in range(len(Retraction_penumatic)):
        			LC_final.append(Retraction_penumatic[i])
        for i in range(len(LC)):
        			LC_final.append(LC[i].format(Subst[i][0], Subst[i][1], Subst[i][2]))

    else:
        LC_final=LC

    layerchange_dict[Head] = LC_final
    del(LC_final)


#=====================================================================================
#Head 2
#=====================================================================================
    Head=2
    LC_final=[]
    Subst=[[0 for x in range(3)] for y in range(len(LC))]

    if LedActive==True:
        Subst[9][0]=LedPos[0]+pos[Head][0]
        Subst[9][1]=LedPos[1]+pos[Head][1]
        Subst[12][0]=LedPos[2]+pos[Head][2]
        Subst[len(LC1)-1+len(LedString)+2][0]=-LedPos[2]-pos[Head][2]
        Subst[len(LC1)-1+len(LedString)+4][0]=-LedPos[0]-pos[Head][0]
        Subst[len(LC1)-1+len(LedString)+4][1]=-LedPos[1]-pos[Head][1]


        for i in range(len(Retraction_penumatic)):
        			LC_final.append(Retraction_penumatic[i])
        for i in range(len(LC)):
        			LC_final.append(LC[i].format(Subst[i][0], Subst[i][1], Subst[i][2]))

    else:
        LC_final=LC

    layerchange_dict[Head] = LC_final
    del(LC_final)


#=====================================================================================
#Head 3
#=====================================================================================
    Head=3
    LC_final=[]
    Subst=[[0 for x in range(3)] for y in range(len(LC))]

    if LedActive==True:
        Subst[9][0]=LedPos[0]+pos[Head][0]
        Subst[9][1]=LedPos[1]+pos[Head][1]
        Subst[12][0]=LedPos[2]+pos[Head][2]
        Subst[len(LC1)-1+len(LedString)+2][0]=-LedPos[2]-pos[Head][2]
        Subst[len(LC1)-1+len(LedString)+4][0]=-LedPos[0]-pos[Head][0]
        Subst[len(LC1)-1+len(LedString)+4][1]=-LedPos[1]-pos[Head][1]


        for i in range(len(LC)):
    			     LC_final.append(LC[i].format(Subst[i][0], Subst[i][1], Subst[i][2]))
    else:
        LC_final=LC
    layerchange_dict[Head] = LC_final
    del(LC_final)


    return(layerchange_dict)
