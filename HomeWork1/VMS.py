import os
import E1
PATH = 'C:\\Users\\wangl\\Documents\\dou\\'
PPath = 'C:\\Users\\wangl\\Documents\\'

def getdiffwords():
    f = open(PPath+'data.txt', 'r', errors='ignore')
    diffwords = f.readlines()
    f.close()
    return diffwords
def getmatrix():
    wlist = []
    filelist = []
    for dirname in [PATH]:
        for root,dirs,files in os.walk(dirname):
            for subfile in files:
                filelist.append(os.path.join(root, subfile))
    diffwords = getdiffwords()
    d = 1
    for filename in filelist:
        f = open(filename,'r',errors='ignore')
        words = f.readlines()
        for diffword in diffwords:
            if diffword in words:
            	wlist.append('1')
            else :
            	wlist.append('0')
        f.close()
        f=open(PPath+'result.txt','a')
        for i in wlist:
            f.write(i)
        f.write('\n')
        f.close()
        print(d)
        print(filename)
        d=d+1
        wlist.clear()

def main():
    getmatrix()
    

if __name__ == '__main__':
    main()
