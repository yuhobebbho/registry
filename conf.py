
import cPickle

try:
    p=[]
    p.append('192.168.100.89')
    p.append('9596')
    db=open(str("conf.dat"),'w')
    cPickle.dump(p, db)
    db.close() 
except:
    pass

infile=open('conf.dat','r')
data = cPickle.load(infile)
infile.close()
print data[0]