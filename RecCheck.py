from FunctionParser import FunData
from ProcessDiff import DiffData
import re
def findFun(flist,fname):
    ret=[]
    size = len(flist)
    i=0
    while size>i:
        if flist[i].name == fname or flist[i].rawName == (re.sub('\s+','',fname)):
            ret.append(flist[i].line)
            if i+1<size:
                ret.append(flist[i+1].line)
            else:
                ret.append(-404)
            #print ret
            return ret
        i+=1
    ret.append(-1)
    ret.append(-1)
    #print ret
    return ret

def strMatch(n_file,s_line,e_line,diffData,A,B):
    isAboveMatch = 0
    isBelowMatch = 0
    isOldLineMatch = 0
    isNewLineMatch = 0
    midchar ='x'
    if e_line == -404:
        f_substr = re.sub('\s+','',''.join(n_file[s_line-1:]))
    else:
        f_substr = re.sub('\s+','',''.join(n_file[s_line - 1:e_line]))

    max = len(f_substr) -1
    #find above line if A=1
    tabove_nospac = re.sub('\s+','',diffData.t_above)
    above_index = f_substr.find(tabove_nospac)
    if above_index == -1:
        above_index = 0
        isAboveMatch = 0
    else:
        isAboveMatch = 1

    #find changed line alaways!
    if diffData.midchar == 'a':
        tn_lines_nospace = re.sub('\s+','',diffData.tn_line)
        tn_index = f_substr.find(tn_lines_nospace,above_index)
        if tn_index >= 0:
            isNewLineMatch = 1
        else:
            isNewLineMatch = 0
    elif diffData.midchar == 'd':
        to_lines_nospace = re.sub('\s+', '', diffData.to_line)
        to_index = f_substr.find(to_lines_nospace, above_index)
        #print to_lines_nospace
        if to_index >= 0:
            isOldLineMatch = 0
        else:
            isOldLineMatch = 1
        #print isOldLineMatch
    elif diffData.midchar == 'c':
        tn_lines_nospace = re.sub('\s+', '', diffData.tn_line)
        tn_index = f_substr.find(tn_lines_nospace, above_index)
        if tn_index >= 0:
            isNewLineMatch = 1
        else:
            isNewLineMatch = 0
    #find below
    tbelow_nospac = re.sub('\s+', '', diffData.t_below)
    below_index = f_substr.find(tbelow_nospac,above_index)
    if below_index == -1:
        below_index = max
        isBelowMatch = 0
    else:
        isBelowMatch = 1

    out = OutData(diffData,isAboveMatch,isBelowMatch,isOldLineMatch,isNewLineMatch,A,B)
    #out.makeDec()
    #print re.sub('\s+','',f_substr)
    return out
    pass


def checkRecon(n_file,diffList,fList,A,B):
    size = len(diffList)
    i=0
    outList=[]
    while size>i:
        data = diffList[i]
        lineNos = findFun(fList,data.tfdata.name)
        outList.append(strMatch(n_file,lineNos[0],lineNos[1],data,A,B))
        i+=1
    return outList
    #for x in outList:

    pass

class OutData(object):
    def __init__(self,diffData,isAboveMatch,isBelowMatch,isOldLineMatch,isNewLineMatch,A,B):
        self.diffData = diffData
        self.isAboveMatch = isAboveMatch
        self.isBelowMatch = isBelowMatch
        self.isOldLineMatch = isOldLineMatch
        self.isNewLineMatch = isNewLineMatch
        self.accuracy = 0.0
        self.A=A
        self.B=B
        self.out = ''
        self.res = 0.0
        self.msg = ''
        pass
    def makeDec(self):
        total = 0.0
        rem = 1.0+self.A+self.B
        if self.diffData.midchar == 'a':
            if self.A==1:
                total+=(self.isAboveMatch/2.0)
            if self.B==1:
                total+=(self.isBelowMatch/2.0)
            total+=(self.isNewLineMatch*2)
            #print self.isBelowMatch

        elif self.diffData.midchar == 'd':
            if self.A == 1:
                total += (self.isAboveMatch/2.0)
            if self.B == 1:
                total += (self.isBelowMatch/2.0)
            total += (self.isOldLineMatch*2)
            pass
        else:
            if self.A == 1:
                total += (self.isAboveMatch/2.0)
            if self.B == 1:
                total += (self.isBelowMatch/2.0)
            total += (self.isNewLineMatch*2.0)
            pass
        self.res = total/rem
        self.msg = self.diffData.diffMsg
        if(self.res>0.80):
            self.msg+="\nSame changes present in new File in Function "+self.diffData.tfdata.name+"\nAccuracy : "+str(self.res*100)
        elif self.res>0.61:
            self.msg += "\nSame changes May be present in new File in Function "+self.diffData.tfdata.name+"\n Accuracy : " + str(self.res*100)
        else:
            self.msg += "\nSame changes are NOT present in new File in Function "+self.diffData.tfdata.name
        self.msg += "\n-------------------------------------------------------------\n"
        pass
    def logger(self):
        return self.msg
    pass