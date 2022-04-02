# -*- coding: utf-8 -*-
import csv, re, os, sys
from operator import itemgetter


class HKConv:
    stats = {}
    total = 0
    src_dir = ''
    dest_dir = ''

    def __init__(self, src, dest=''):
        self.convdict = ()
        if src == '':
            exit()
        elif dest == '':
            dest = src + '-new'
        self.src_dir = src
        self.dest_dir = dest

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
        startdir = self.src_dir
        try:
            os.mkdir(self.dest_dir)
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
                # META-INF browser chrome localization manifest.json
                if not(re.search('META-INF', filename) or 
                   re.search('browser', filename) or
                   re.search('chrome', filename) or
                   re.search('localization', filename) or
                   re.search('manifest.json', filename)):
                       continue
                newfilename = re.sub("^%s"%startdir, "%s-new"%startdir, filename)
                filelist += [ filename ]
                newf = open(newfilename, 'w', errors='ignore')
                print(filename)
                with open(filename) as f:
                    try:
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
                    except:
                        break
                    newf.close()


    def showstats(self):
        count = 0
        for k, v in self.stats.items():
            print('%s = %s'%(k, v))
            count += v
        return count


if __name__ == "__main__":
    try:
        hkconv = HKConv(sys.argv[1], sys.argv[2])
    except:
        hkconv = HKConv(sys.argv[1])
    hkconv.readcsv()
    #hkconv.printdict()
    hkconv.convlangpack()
    count = hkconv.showstats()
    print("Changed: %s/%s (%s%%)"%(count, hkconv.total, (count / hkconv.total * 100)))
