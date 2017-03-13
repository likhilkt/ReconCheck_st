from os import popen
from FunctionParser import FunData
def safe(size,index):
    if(size<=index):
        return size-1
    return index
def findFun(flist,lineNo):
    size = len(flist)-1
    while size>=0:
        if flist[size].line<lineNo:
            return flist[size]
        size-=1
    return FunData('NONAMAE | Please check this manually',-1)
def processDiff(low , high, flist, l_file, A,B):
    ABOVE = 3
    BELOW = 3
    diffList =[]
    result = popen("diff -biw "+low+" "+high).readlines()
    i=0;
    size = len(result)
    f_size=len(l_file)
    while size>i:
        line = result[i]
        to_lines=''
        tn_lines=''
        msg=line
        if result[i][0].isdigit():
            mid = line.find('c') + line.find('a') + line.find('d')+2
            midchar = line[mid]
            #print mid
            #print midchar
            if midchar == 'c':
                if line[:mid].count(',')>0:
                    lineNo = int(line[:line.find(',')])
                    endLine = int(line[line.find(',')+1:mid])
                else:
                    lineNo = int(line[:mid])
                    endLine=lineNo
                #safe read next line
                i+=1
                line=result[i]
                while not line[0].isdigit():
                    msg += line
                    if line[0] == '<':
                        to_lines+=line[2:]
                    elif line[0]== '>':
                        tn_lines+=line[2:]
                    i+=1
                    if size>i:
                        line = result[i]
                    else:
                        break

            elif midchar == 'a':
                #print "adddddd"
                lineNo = int(line[:mid])
                endLine = lineNo
                i += 1
                line = result[i]
                while not line[0].isdigit():
                    msg += line
                    if line[0] =='>':
                        tn_lines+=line[2:]
                    i+=1
                    if size>i:
                        line = result[i]
                    else:
                        break
                pass
            elif midchar == 'd':
                if line[:mid].count(',')>0:
                    lineNo = int(line[:line.find(',')])
                    endLine = int(line[line.find(',')+1:mid])
                else:
                    lineNo = int(line[:mid])
                    endLine=lineNo
                i += 1
                line = result[i]

                while not line[0].isdigit():
                    msg += line
                    if line[0] == '<':
                        to_lines += line[2:]
                    i += 1
                    if size > i:
                        line = result[i]
                    else:
                        break
                pass
            #read line above
            aboveLine = lineNo - 2 #line index starts from 0
            t_above=''
            count = 0
            while aboveLine>=0 and ABOVE>count and A==1:
                t_above=l_file[aboveLine]+t_above
                aboveLine-=1
                count+=1
            belowLine = endLine  # line index starts from 0
            t_below = ''
            count = 0
            while belowLine < f_size and BELOW > count and B == 1:
                t_below+= l_file[belowLine]
                belowLine += 1
                count += 1
            tfdata = findFun(flist,lineNo)
            #print "-------------------"
            diffList.append(DiffData(tfdata,midchar,t_above,t_below,tn_lines,to_lines,msg))
            #print "--------------------"
        #i+=1
    #for x in diffList:
    #    x.show()
    return diffList

class DiffData(object):
    def __init__(self,tfdata,midchar,t_above,t_below,tn_line,to_line,msg):
        super(DiffData, self).__init__()
        self.tfdata = tfdata
        self.midchar = midchar
        self.t_above = t_above
        self.t_below = t_below
        self.tn_line = tn_line
        self.to_line = to_line
        self.diffMsg= msg
    def show(self):
        print self.t_above
        print self.t_below
        print self.tn_line
        print self.to_line
        print self.midchar
        self.tfdata.show()
    pass
