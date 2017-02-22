new varElement TestVar_0 150 90 15 refName="TestVar_0"
new varElement Variable_id4 150 140 15 refName="Variable_id4_1" 
new varElement Variable_id4 400.0 100.0 15 refName="Variable_id4_2"
new basicOperator + 300.0 100.0 name=u"Operator_1"
new connector TestVar_0 Operator_1 idxInPin=-1
new connector Variable_id4_1 Operator_1 idxInPin=-2
# This is a test commentary
###########################

new connector Operator_1 Variable_id4_2 idxInPin=-1
new varElement Variable_id8 140.0 190.0 15
select Variable_id8_id7
@selection set xy (10.0,0.0) -p
new basicOperator * 300.0 200.0
new varElement Variable_id10 150.0 250.0 15
new varElement Variable_id11 410.0 200.0 15
select
@latent new connector 7 idxOutPinConnectorPloting=0
@latent set 11_id11.connectInfo ("Operator_mult_id9",-1)
@latent new connector 9 idxOutPinConnectorPloting=0
@latent set 13_id13.connectInfo ("Operator_mult_id9",-2)
@latent new connector 8 idxOutPinConnectorPloting=0
@latent set 15_id15.connectInfo ("Variable_id11_id10",-1)
new basicOperator - 530.0 100.0
select Operator_minus_id18
@selection set xy (10.0,0.0) -p
@selection set xy (0.0,10.0) -p
select
@latent new connector 2 idxOutPinConnectorPloting=0
@latent set 18_id18.connectInfo ("Operator_minus_id18",-1)
@latent new connector 10 idxOutPinConnectorPloting=0
@latent set 20_id20.connectInfo ("Operator_minus_id18",-2)
select 20_id20
set 20_id20.listPoints [80.0,-80.0]
new varElement Variable_id23 650.0 110.0 15
select
@latent new connector 17 idxOutPinConnectorPloting=0
@latent set 23_id23.connectInfo ("Variable_id23_id22",-1)
@mainController set bSimulationMode True
@signals new signalFile D:/Projekte/PyLinX/Aptana-Projekte/PyLinX2/Recources/Testdata/Testdata1.mf4
#@objects set ./variables/TestVar_0.signalMapped var5|Signal_id36
#@objects set ./variables/Variable_id4.signalMapped Variable_id4|Signal_id36

#@mainController set bSimulationMode True
#select TestVar_0
#set /ObjectHandler/variables/TestVar_0.stim_sine {u'stim_sine_amplitude':1.0,u'stim_sine_frequency':1.0,u'stim_sine_phase':0.0,u'stim_sine_offset':2.0}
@mainController set bSimulationMode False
select Variable_id10_id9
@selection set xy (0.0,10.0) -p
@selection set xy (0.0,10.0) -p
@selection set xy (0.0,10.0) -p
new varElement Variable_id38 230.0 410.0 15
select
select Variable_id38_id37
select Variable_id38_id37 
del Variable_id38_id37
@mainController set bSimulationMode True
select TestVar_0
@objects set ./variables/TestVar_0.signalMapped Variable_id4|Signal_id36
select Variable_id4_1
select
select Variable_id4_1
set /ObjectHandler/variables/Variable_id4.stim_sine {u'stim_sine_amplitude':1.0,u'StimulationFunction':'Sine',u'stim_sine_frequency':1.0,u'stim_sine_phase':0.0,u'stim_sine_offset':1.0}
select TestVar_0
new dataViewer 50 50
set /ObjectHandler/variables/TestVar_0.listSelectedDispObj [1]
select
select Variable_id4_1
set /ObjectHandler/variables/Variable_id4.listSelectedDispObj [1]
@mainController set bSimulationMode False
@mainController set bSimulationMode True
select VarDispElement_id49
@objects set recorder_RecordState 0
@objects set recorder_VariablesToRecord []
@objects set recorder_fileFormat mdf
@objects set recorder_RecordState 0
@objects set recorder_VariablesToRecord []
@objects set recorder_fileFormat mdf
@objects set recorder_RecordState 0
@objects set recorder_VariablesToRecord []
@objects set recorder_fileFormat mdf
select 11_id11
select