we=open('gridlist_global_cf.txt','w')
with open('gridlist_global_test.txt') as f:
    for line in f:
        
         # read a line
         line = line.replace("\n", "")
         a,b=line.split('\t')
        
         # get two values as string
         c=360+(2*(float(a)-0.25))
         d=180+(2*(float(b)-0.25))
         print(a)
            
         # calculate the other two values
         e = ''.join(("(",str(a),",",str(b),")"))
         print(e)
         we.write(str(int(c))+' '+str(int(d))+' '+e+"\n")
