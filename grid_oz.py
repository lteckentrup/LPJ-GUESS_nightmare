import numpy as np

we=open('gridlist_cf_oz.txt','w')
lon = np.arange(112.25,154.25,0.5)
lat = np.arange(10.25,44.25,0.5)*(-1)

with open('gridlist_global_test.txt') as f:
    for line in f:

         line = line.replace("\n", "")
         a,b=line.split('\t')

         if float(a) in lon and float(b) in lat:

             c=(float(a)-112.25)/0.5
             d=(float(b)-(-43.75))/0.5

             e = ''.join(("(",str(a),",",str(b),")"))
             we.write(str(int(c))+' '+str(int(d))+' '+e+"\n")
         else:
             pass
