#Written by Tariq A.
#Special thanks to https://www.rototron.info for inspiring me to use the numpy FFT







import alsaaudio as alsa
import wave
from struct import unpack
import numpy as np
import os as OS
import sys as SYS


#VARs


WAVFILE = str(SYS.argv[1])

print("Input file:" + WAVFILE)
SPECTRUM  = [1,1,1,3,3,3,2,2]
FREQ_DOMAIN = [0,0,0,0,0,0,0,0]
weighting = [2,8,8,16,16,32,32,64] 
FREQ_60Hz_LVL=0
FREQ_LVL = ["' ________________'","' |_______________'","' ||______________'","' ||||____________'","' ||||||||________'","' ||||||||||||||||'"]
AMP= []



#End of #VARs


#WAVSAMPLE
# Audio setup
WAVSAMPLE = wave.open(WAVFILE,'r')
SAMPLING_RATE = WAVSAMPLE.getframerate()
NUM_CH = WAVSAMPLE.getnchannels()
BLOCKS = 4096    #2^x

print("Playing audio sample ")
print("File-name: "+ WAVFILE)
print ("Blocks at a time: " + str(BLOCKS))
print("The number of channels: "+ str(NUM_CH))
print("The sampling rate: " + str(SAMPLING_RATE) + " Hz")


#End of #WAVSAMPLE


#ALSA
ALSA_OUT = alsa.PCM(alsa.PCM_PLAYBACK, alsa.PCM_NORMAL)
ALSA_OUT.setchannels(NUM_CH)
ALSA_OUT.setrate(SAMPLING_RATE)
ALSA_OUT.setformat(alsa.PCM_FORMAT_S16_LE)
ALSA_OUT.setperiodsize(BLOCKS)
#End of #ALSA



# Return AMP array index corresponding to a particular frequency
def piff(val):
   return int(2*BLOCKS*val/SAMPLING_RATE) #val = 1 --> (2*2048*1)/22050
   
def GET_LVLs(data, BLOCKS,SAMPLING_RATE):
   global FREQ_DOMAIN

   # Convert raw data (ASCII string) to numpy array
   data = unpack("%dh"%(len(data)/2),data)
   data = np.array(data, dtype='h')

   # Apply FFT - real data
   FFT=np.fft.rfft(data)
   # Remove last element in array to make it the same size as BLOCKS
   FFT=np.delete(FFT,len(FFT)-1)
   
   
   
   # Find average 'amplitude' for specific frequency ranges in Hz
   AMP = np.abs(FFT)   #absolute
   
   FREQ_DOMAIN[0]= int(np.mean(    AMP[piff(0)    :piff(100):1])       )
   FREQ_DOMAIN[1]= int(np.mean(AMP[piff(100)  :piff(250):1]))
   FREQ_DOMAIN[2]= int(np.mean(AMP[piff(250)  :piff(500):1]))
   FREQ_DOMAIN[3]= int(np.mean(AMP[piff(500)  :piff(1000):1]))
   FREQ_DOMAIN[4]= int(np.mean(AMP[piff(1000) :piff(2300):1]))
   FREQ_DOMAIN[5]= int(np.mean(AMP[piff(2300) :piff(4500):1]))
   FREQ_DOMAIN[6]= int(np.mean(AMP[piff(4500) :piff(10000):1]))
   #FREQ_DOMAIN[7]= int(np.mean(AMP[piff(10000):piff(12000):1]))
  
   # Tidy up column values 
   FREQ_DOMAIN=np.divide(np.multiply(FREQ_DOMAIN,weighting),1000000)
   # Set floor at 0 and ceiling at 8 
   FREQ_DOMAIN=(FREQ_DOMAIN.clip(0,8))
   

   return FREQ_DOMAIN







#WAVESAMPLE read
data = WAVSAMPLE.readframes(BLOCKS)

try:
    while data!='':
       ALSA_OUT.write(data)
       FREQ_DOMAIN=GET_LVLs(data, BLOCKS,SAMPLING_RATE)
       #OS.system("echo -en "+str(FREQ_DOMAIN) + "\r")  
       FREQ_DOMAIN = FREQ_DOMAIN.astype(int)
       
       if FREQ_DOMAIN[0] == 0:
            FREQ_60Hz_LVL=FREQ_LVL[0]
       elif FREQ_DOMAIN[0] <=1 and FREQ_DOMAIN[0] > 0:
            FREQ_60Hz_LVL=FREQ_LVL[1]
       elif FREQ_DOMAIN[0] <=2 and FREQ_DOMAIN[0] > 1:
            FREQ_60Hz_LVL=FREQ_LVL[2]
       elif FREQ_DOMAIN[0] <=3 and FREQ_DOMAIN[0] > 2:
            FREQ_60Hz_LVL=FREQ_LVL[3]
       elif FREQ_DOMAIN[0] <=4 and FREQ_DOMAIN[0] > 3:
            FREQ_60Hz_LVL=FREQ_LVL[4]
       elif FREQ_DOMAIN[0] <=5 and FREQ_DOMAIN[0] > 4:
            FREQ_60Hz_LVL=FREQ_LVL[5]

       OS.system("echo -en " + str(FREQ_DOMAIN) + str(FREQ_60Hz_LVL) + "\r")
    
       
     
    

       data = WAVSAMPLE.readframes(BLOCKS)


    WAVESAMPLE.close()
except KeyboardInterrupt:
    
    WAVSAMPLE.close()