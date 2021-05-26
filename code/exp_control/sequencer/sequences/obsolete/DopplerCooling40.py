function_name="incl.DopplerCooling40"
description="Doppler cooling with Ca40"
arguments="length=1000"

class DopplerCooling40(PulseCommand):  #for Ca40
    def __init__(self,length=1000):
        configuration=self.get_config()
        trigger_length=configuration.PMT_trigger_length #new
        detection_count=self.get_variable("detection_count") 
        self.set_variable("detection_count",detection_count+2)
        self.add_to_return_list("PM Count","detection_count")

        ttl_pulse(trigger_length,"PMT trigger",is_last=False) #new
        #ttl_pulse(0,length,"dopp/det",is_last=False) #JB 7.8.06
#        ttl_pulse(length,"397sig sw",is_last=False)   #warum?
        ttl_set("dopp/det",1)  #CR bugfix
        ttl_pulse(length,"397 sw",is_last=False)
        ttl_pulse(length+20,"866 sw",is_last=False)
        ttl_pulse(trigger_length,"PMT trigger",start_time=max(length-trigger_length,trigger_length+1)) #new
        
incl.DopplerCooling40=DopplerCooling40
