# -*- coding: utf-8 -*-
import csv, re, os
from operator import itemgetter


class HKConv:
    stats = {}
    total = 0

    def __init__(self):
        self.convdict = ()


    def readcsv(self):
        filename = 'tw2hk.csv'
        with open(filename, newline='') as csvfile:
            userreader = csv.reader(csvfile, delimiter=',')
            for i in userreader:
                self.convdict += ((i[0], i[1]),)


    def printdict(self):
        for i, j in self.convdict:
            print("> %s %s"%(i,j))


    def convlangpack(self):
        filelist = []
        startdir = 'langpack-zh-TW@firefox.mozilla.org'
        try:
            os.mkdir("%s-new"%startdir)
        except FileExistsError:
            pass
        for root, dirs, files in os.walk(startdir):
            for i in dirs:
                pathdir = "%s/%s"%(root, i)
                newdir = re.sub("^%s"%startdir, "%s-new"%startdir, pathdir)
                try:
                    os.mkdir(newdir)
                except FileExistsError:
                    pass
            for i in files:
                filename = "%s/%s"%(root, i)
                newfilename = re.sub("^%s"%startdir, "%s-new"%startdir, filename)
                filelist += [ filename ]
                newf = open(newfilename, 'w')
                with open(filename) as f:
                    lines = f.readlines()
                    for j in lines:
                        self.total += 1
                        changed = False
                        for sk, sv in self.convdict:
                            try:
                                if re.search(sk, j):
                                    newstr = re.sub(sk, sv, j)
                                    newf.write(newstr)
                                    changed = True
                                    if sk in self.stats.keys():
                                        self.stats[sk] += 1
                                    else:
                                        self.stats[sk] = 1
                            except re.error:
                                pass
                        if not changed:
                            newf.write(j)
                newf.close()


    def showstats(self):
        count = 0
        for k, v in self.stats.items():
            print('%s = %s'%(k, v))
            count += v
        return count


if __name__ == "__main__":
    hkconv = HKConv()
    hkconv.readcsv()
    #hkconv.printdict()
    hkconv.convlangpack()
    count = hkconv.showstats()
    print("Changed: %s/%s (%s%%)"%(count, hkconv.total, (count / hkconv.total * 100)))
