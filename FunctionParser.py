import re
def limit(size,index):
    if index>=size:
        return size-1
    return index

def getFun(lines):
    #f_name = open(filename)
    #print f_name.read()
    fList=[]
    lineNo=0
    tlno = 0
    size = len(lines)
    i=0
    while i <size:
        fstr = ''
        brac = 0
        lineNo = i+1
        line = lines[i]
        rLine = re.sub('\s+','',line)
        if rLine.startswith("if(") or rLine.startswith("while(") or rLine.startswith("elseif(") or rLine.startswith("switch(") or rLine.startswith("return(") or rLine.startswith("for("):
            i+=1
            continue
        elif rLine.count('(')>0 :
            fstr+=str(line)
            #print line
            brac +=(rLine.count('(') - rLine.count(')'))
            ti=i
            while brac !=0:
                ti+=1
                line = lines[ti]
                rLine = re.sub('\s+','',line)
                brac += (rLine.count('(') - rLine.count(')'))
                fstr+=str(line)
            if (not rLine.endswith(";") and not re.sub('\s+','',lines[limit(size,ti+1)]).startswith(";")) and (line.count('{') > 0 or  re.sub('\s+','',lines[limit(size,ti+1)]).startswith("{")):
                tstr = fstr[0:fstr.rfind(')')+1]
                fList.append(FunData(tstr,lineNo))
        #print i

        i+=1
    #for x in fList:
    #    x.show()
    return fList

class FunData(object):
    def __init__(self,name,line):
        self.name=name
        self.line=line
        self.rawName=re.sub('\s+','',name)
    def show(self):
        print self.name
        print self.line
        print  self.rawName
        return
    pass
