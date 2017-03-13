from FunctionParser import getFun
from ProcessDiff import processDiff
from RecCheck import checkRecon
import re

with open('sample.cxx') as f:
    olines = f.readlines()
with open('sample3') as f:
    nlines = f.readlines()

fl_list = getFun(olines)
fn_list = getFun(nlines)
diffList=processDiff("sample.cxx","samplw2.cxx",fl_list,olines,1,1)
outList = checkRecon(nlines,diffList,fn_list,1,1)
msg = "-------------------------------------------------------------\n"
true = 1
for x in outList:
    x.makeDec()
    msg+=x.logger()
    if x.res<0.60:
        true = 0
if true == 0:
    msg = "Reconciliation needed!!\n" + msg
else:
    msg = "Reconciliation NOT needed!!\n" + msg
print msg

