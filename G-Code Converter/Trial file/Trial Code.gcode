==========================================================
In this file some relevant strings are present. They are
triggers and will be substituted/transformed by the code.

In order to have actions on all lines, it is important to 
select "UV at layer change" on the GUI before clicking on
"Convert!".
==========================================================


==========================================================
Here a tool activation sequence will be inserted
==========================================================

T0 ; change extruder



==========================================================
Here a tool change sequence will be inserted
==========================================================

T1 ; change extruder



==========================================================
Here a layer change sequence will be inserted
==========================================================

;LAYER_CHANGE
;LAYER_CHANGE



==========================================================
Here a retraction sequence will be inserted
==========================================================

G1 X1 Y1 Z1 F36000 ;



==========================================================
Here a de-retraction sequence will be inserted
==========================================================

G1 X1 Y1 Z1 F72000 ;



==========================================================
Here a "E" commands will be deleted
==========================================================

G1 X1 Y1 Z1 E123 ;



==========================================================
Here head will be changed from 1 to 4
Doing so, "E" commands will be kept
==========================================================

T4 ; change extruder
	    
	    
G1 X1 Y1 Z1 E123 ; <==
	   ^^^^^



==========================================================
Here command relative to skirt will be deleted
==========================================================

line to be kept

G1 X2 ; go to the first skirt point ;
line to be deleted
line to be deleted

G1 X1 ; go to the first perimeter point ;
line to be kept





