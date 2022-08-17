import os

globalSettings = {
'EN_CORE_COL_SYNC'       :     "0",
'EN_CORE_COL_LIN_1'      : "65535",
'EN_CORE_COL_LIN_2'      :     "1",
'EN_CORE_COL_DIFF_1'     :     "0",
'EN_CORE_COL_DIFF_2'     :     "0",
 
'EN_MACRO_COL_CAL_LIN_1' : "65535",
'EN_MACRO_COL_CAL_LIN_2' : "65535",
'EN_MACRO_COL_CAL_LIN_3' : "65535",
'EN_MACRO_COL_CAL_LIN_4' : "65535",
'EN_MACRO_COL_CAL_LIN_5' :    "15",

'EN_MACRO_COL_CAL_SYNC_1': "65535",
'EN_MACRO_COL_CAL_SYNC_2': "65535",
'EN_MACRO_COL_CAL_SYNC_3': "65535",
'EN_MACRO_COL_CAL_SYNC_4': "65535",

'EN_MACRO_COL_CAL_DIFF_1': "65535",
'EN_MACRO_COL_CAL_DIFF_2': "65535",
'EN_MACRO_COL_CAL_DIFF_3': "65535",
'EN_MACRO_COL_CAL_DIFF_4': "65535",
'EN_MACRO_COL_CAL_DIFF_5':    "15",

'HITOR_0_MASK_LIN_0'     :     "0",
'HITOR_0_MASK_LIN_1'     :     "0",
'HITOR_1_MASK_LIN_0'     :     "0",
'HITOR_1_MASK_LIN_1'     :     "0",
'HITOR_2_MASK_LIN_0'     :     "0",
'HITOR_2_MASK_LIN_1'     :     "0",
'HITOR_3_MASK_LIN_0'     :     "0",
'HITOR_3_MASK_LIN_1'     :     "0",

'HITOR_0_MASK_SYNC'      : "65535",
'HITOR_1_MASK_SYNC'      : "65535",
'HITOR_2_MASK_SYNC'      : "65535",
'HITOR_3_MASK_SYNC'      : "65535",

'HITOR_0_MASK_DIFF_0'    : "65535",
'HITOR_0_MASK_DIFF_1'    :     "1",
'HITOR_1_MASK_DIFF_0'    : "65535",
'HITOR_1_MASK_DIFF_1'    :     "1",
'HITOR_2_MASK_DIFF_0'    : "65535",
'HITOR_2_MASK_DIFF_1'    :     "1",
'HITOR_3_MASK_DIFF_0'    : "65535",
'HITOR_3_MASK_DIFF_1'    :     "1",

'LOCKLOSS_CNT'           :     "0",
'BITFLIP_WNG_CNT'        :     "0",
'BITFLIP_ERR_CNT'        :     "0",
'CMDERR_CNT'             :     "0",
'SKIPPED_TRIGGER_CNT'    :     "1",
'HITOR_0_CNT'            :     "0",
'HITOR_1_CNT'            :     "0",
'HITOR_2_CNT'            :     "0",
'HITOR_3_CNT'            :     "0",

}

globalSettings_CROC = {
'DAC_PREAMP_L_LIN'       :   "300",
'DAC_PREAMP_R_LIN'       :   "300",
'DAC_PREAMP_TL_LIN'      :   "300",
'DAC_PREAMP_TR_LIN'      :   "300",
'DAC_PREAMP_T_LIN'       :   "300",
'DAC_PREAMP_M_LIN'       :   "300",
'DAC_FC_LIN'             :    "20",
'DAC_KRUM_CURR_LIN'      :    "70",
'DAC_REF_KRUM_LIN'       :   "360",
'DAC_COMP_LIN'           :   "110",
'DAC_COMP_TA_LIN'        :   "110",
'DAC_GDAC_L_LIN'         :   "500",
'DAC_GDAC_R_LIN'         :   "500",
'DAC_GDAC_M_LIN'         :   "500",
'DAC_LDAC_LIN'           :   "110",
'LEACKAGE_FEEDBACK'      :     "0",
'AnalogInjectionMode'    :     "0",
'VCAL_HIGH'              :  "1800",
'VCAL_MED'               :   "300",
}

tuneablevalues = []
tuneablevalues.append('DAC_GDAC_R_LIN')
tuneablevalues.append('DAC_GDAC_L_LIN')
tuneablevalues.append('DAC_GDAC_M_LIN')
tuneablevalues.append('DAC_LDAC_LIN')
tuneablevalues.append('DAC_KRUM_CURR_LIN')


###-------This block of code opens the RD53B.toml file that's in the test directory and grabs any tuneable-----###
###-------values that would result from tests such as ThresholdTuning and GainTuning.  Those tests save the ---###
###-------optimal values in $Ph2_ACF_AREA/test/RD53B.toml.  This file gets overwritten with each test----------###
tomlFile = open("{0}/test/RD53B.toml".format(os.environ.get("Ph2_ACF_AREA")),"r")
for line in tomlFile:
	for tuneablevalue in tuneablevalues:	
		if tuneablevalue in line:
			reg = line.split('=')[0]
			reg = reg.strip()
			newvalue = line.split('=')[1]
			newvalue = newvalue.strip('\n').strip()
			globalSettings_CROC[reg] = newvalue

globalSettings_Dict = {
    'Latency'                    :    globalSettings,
    'PixelAlive'                 :    globalSettings,
    'NoiseScan'                  :    globalSettings,
    'GainScan'                   :    globalSettings,
    'SCurveScan'                 :    globalSettings,
    'ThresholdEqualization'      :    globalSettings,
    'GainOptimization'           :    globalSettings,
    'ThresholdMinimization'      :    globalSettings,
    'ThresholdAdjustment'        :    globalSettings,
    'InjectionDelay'             :    globalSettings,
    'ClockDelay'                 :    globalSettings,
    'BitErrorRate'               :    globalSettings,
    'DataRBOptimization'         :    globalSettings,
    'ChipIntVoltageTuning'       :    globalSettings,
    'GenericDAC-DAC'             :    globalSettings,
    'Physics'                    :    globalSettings,
	'CROCThresholdOptimize'      :    globalSettings_CROC,
    'CROCRegReader'              :    globalSettings_CROC,
	'CROCRegTest'                :    globalSettings_CROC,
	'CROCDigitalScan'            :    globalSettings_CROC,
	'CROCAnalogScan'             :    globalSettings_CROC,
	'CROCAnalogScanFast'         :    globalSettings_CROC,
	'CROCAnalogScanSparse'       :    globalSettings_CROC,
	'CROCThresholdScan'          :    globalSettings_CROC,
	'CROCThresholdScanFast'      :    globalSettings_CROC,
	'CROCThresholdScanSparse'    :    globalSettings_CROC,
	'CROCThresholdEquilization'  :    globalSettings_CROC,
	'CROCGlobalThresholdTuning'  :    globalSettings_CROC,
	'CROCThresholdTuning'        :    globalSettings_CROC,
    'CROCNoiseScan'              :    globalSettings_CROC,
	'CROCStuckPixelScan'         :    globalSettings_CROC,
	'CROCTimeWalkInjectionScan'  :    globalSettings_CROC,
	'CROCTimeWalk'               :    globalSettings_CROC,
	'CROCRingOsc'                :    globalSettings_CROC,
	'CROCShortRingOsc'           :    globalSettings_CROC,
	'CROCMuxScan'                :    globalSettings_CROC,
	'CROCIVScan'                 :    globalSettings_CROC,
	'CROCADCScan'                :    globalSettings_CROC,
	'CROCDACScan'                :    globalSettings_CROC,
	'CROCTempSensor'             :    globalSettings_CROC,
	'CROCShortTempSensor'        :    globalSettings_CROC,
	'CROCVrefTrimming'           :    globalSettings_CROC,
	'CROCCapMeasureScan'         :    globalSettings_CROC,
	'CROCCapMeasure'             :    globalSettings_CROC,
	'CROCBERscanTest'            :    globalSettings_CROC,
}
