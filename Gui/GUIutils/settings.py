DBServerIP = {
	'Central-remote'		 :  '0.0.0.0',
	'local'					 :  '127.0.0.1',
	'OSU-remote'			 :  '128.146.38.1',
}


# Note: First element of list will be shown as default value
DBNames = {
	'All'					 :  ['phase2pixel_test', 'DBName2', 'DBName3'],
	'Central-remote'		 :  ['phase2pixel_test', 'DBName2', 'DBName3'],
	'local'					 :  ['phase2pixel_test'],
	'OSU-remote'			 :  ['SampleDB','phase2pixel_test'],
}

FirmwareList =  {
	'fc7.board.1' 			 :  '192.168.1.80',
	'fc7.board.2'			 :  '127.0.0.1' #'192.168.1.81',
}

# Set the IT_uTDC_firmware for test
FPGAConfigList =  {
	'fc7.board.1' 			 :  'IT-uDTC_L12-KSU-3xQUAD_L8-KSU2xQUAD_x1G28',
	'fc7.board.2'			 :  'IT-uDTC_L12-KSU-3xQUAD_L8-KSU2xQUAD_x1G28'
}

ModuleType = {
	1	:	"SingleSCC",
	2	:	"DualSCC",
	3	:	"QuadSCC",
}

BoxSize = {
	"SingleSCC" : 1,
	"DualSCC"	: 2,
	"QuadSCC"	: 4
}


ConfigFiles = {
	'Latency'                :  '/Configuration/Defaults/CMSIT.xml',
	'PixelAlive'             :  '/Configuration/Defaults/CMSIT.xml',
	'NoiseScan'              :  '/Configuration/Defaults/CMSIT.xml',
	'SCurveScan'             :  '/Configuration/Defaults/CMSIT.xml',
	'GainScan'               :  '/Configuration/Defaults/CMSIT.xml',
	'ThresholdEqualization'  :  '/Configuration/Defaults/CMSIT.xml',
	'GainOptimization'       :  '/Configuration/Defaults/CMSIT.xml',
	'ThresholdMinimization'  :  '/Configuration/Defaults/CMSIT.xml',
	'ThresholdAdjustment'    :  '/Configuration/Defaults/CMSIT.xml',
	'InjectionDelay'         :  '/Configuration/Defaults/CMSIT.xml',
	'ClockDelay'             :  '/Configuration/Defaults/CMSIT.xml',
	'Physics'                :  '/Configuration/Defaults/CMSIT.xml',
	'AllScan'                :  '/Configuration/Defaults/CMSIT.xml',
}

Test = {
	'AllScan'                :  'pixelalive',
	'StandardStep1'          :  'pixelalive',
	'StandardStep2'          :  'pixelalive',
	'StandardStep3'          :  'pixelalive',
	'StandardStep4'          :  'pixelalive',
	'Latency'                :  'latency',
	'PixelAlive'             :  'pixelalive',
	'NoiseScan'              :  'noise',
	'SCurveScan'             :  'scurve',
	'GainScan'               :  'gain',
	'ThresholdEqualization'  :  'threqu',
	'GainOptimization'       :  'gainopt',
	'ThresholdMinimization'  :  'thrmin',
	'ThresholdAdjustment'    :  'thradj',
	'InjectionDelay'         :  'injdelay',
	'ClockDelay'             :  'clockdelay',
	'Physics'                :  'physics',
}

SingleTest = ['Latency','PixelAlive','NoiseScan','SCurveScan','GainScan',
					 'ThresholdEqualization','GainOptimization','ThresholdMinimization',
					 'ThresholdAdjustment','InjectionDelay','ClockDelay','Physics']

CompositeTest = ['AllScan','StandardStep1','StandardStep2','StandardStep3','StandardStep4']
CompositeList = {
	'AllScan': ['Latency','PixelAlive', 'GainScan','SCurveScan','ThresholdEqualization','GainOptimization','ThresholdMinimization',
				'ThresholdAdjustment','InjectionDelay','ClockDelay','Physics'],
	'StandardStep1': ['Latency','PixelAlive'],
	'StandardStep2': ['Latency','PixelAlive', 'SCurveScan'],
	'StandardStep3': ['Latency','PixelAlive'],
	'StandardStep4': ['Latency','PixelAlive']
}
firstTimeList = ['AllScan', 'StandardStep1', 'PixelAlive']

header = ['Source', 'Module_ID', 'User', 'Test', 'Time', 'Grade', 'DQMFile'] #Stop using