import re

def ArduinoParser(text):
    print(text)
    try:
        StopSingal, ProbeReadsText = ArduinoParserCustomOSU(text)
        return StopSingal, ProbeReadsText
    except Exception as err:
        return False,""


#################Arduino formatting for OSU###############
ProbeMapOSU = {
    'DHT22_temperature': "Temperature",
    'DHT22_humidity'   : "Humidity",
}
ThresholdMapOSU = {
    'DHT22_temperature': [-20,50],
    'DHT22_humidity'   : [0,60],
}

##-----This section needs some work---------------------
def ArduinoParserCustomOSU(text):
    StopSignal = False
    values = re.split(",",text)[1:]
#    values = re.split(" |\t",text)[1:]
    readValue = {}
    ProbeReads = []

    for index,value in enumerate(values):
        value = value.rstrip(":")
        if value in ProbeMapOSU.keys():
            readValue[value] = float(values[index+1])

    for probeName,probeValue in readValue.items():
        if probeName in ThresholdMapOSU.keys():
            if type(ThresholdMapOSU[probeName])!= list or len(ThresholdMapOSU[probeName]) !=2:
                continue
            else:
                if probeValue < ThresholdMapOSU[probeName][0] or  probeValue > ThresholdMapOSU[probeName][1]:
                    colorCode = "#FF0000"
                    if probeName in ['MAX31850','MAX31865']:
                        StopSignal = True
                        
                else:
                    colorCode = "#008000"
                ProbeReads.append('{0}:<span style="color:{1}";>{2}</span>'.format(ProbeMapOSU[probeName],colorCode,probeValue))
                
        else:
            ProbeReads.append('{0}:{1}'.format(ProbeMapOSU[probeName],probeValue))
    ProbeReadsText = '\t'.join(ProbeReads)
    return StopSignal,ProbeReadsText
##--------------------------------------------------------
    
