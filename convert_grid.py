we=open('gridlist_global_cf.txt','w')
with open('gridlist_global_test.txt') as f:
    for line in f:
        
         # read a line
         line = line.replace("\n", "")
         a,b=line.split('\t')
        
         # get two values as string
         c=(float(a)-(-179.75))/0.5
         d=(float(b)-(-89.75))/0.5
         print(a)
            
         # calculate the other two values
         e = ''.join(("(",str(a),",",str(b),")"))
         print(e)
         we.write(str(int(c))+' '+str(int(d))+' '+e+"\n")
