import hashlib 
from os import walk, makedirs
import os.path
import shutil

def GetDataPathFromUser(): 
    print("Please enter folder path:")
    userDataPath=input()
    return userDataPath
    #add error checking here

def MakeFileList(path):
    print("Scanning Directory...")
    filelist=[]
    for dir, subdirs, fnames in walk(path):
        for fname in fnames:
            fullpath=str('{}\{}'.format(dir,fname))
            filelist.append(fullpath)
    print(str('{} files found!'.format(len(filelist))))
    return filelist
        
def GetExensions(filelist):
    print("Collecting Extensions...")
    extensions=set()
    for f in filelist:
        fname, extension = os.path.splitext(f)
        extension.lower()
        extensions.add(extension)
    print (extensions)
    return extensions

def CreateToFolders(extensions,topath):
    print("Creating Folders...")
    for ext in extensions:
        destpath = os.path.join(topath,ext)
        if os.path.exists(destpath)==False:
            os.mkdir(destpath)

def GetHash(file):
    f = open(file,'rb')
    c = f.read()
    f.close()
    hashmd5 = check = hashlib.md5(c).hexdigest()
    return hashmd5

def PrintDirectory(filelist,topath):
    print("Printing Directory Listing...")
    directorylist = os.path.join(topath,"directory.txt")
    dl=open(directorylist,'w')
    for f in filelist:
        dl.write(f)
        dl.write('\n')
    dl.close()

def CopyFiles(filelist,topath):
    print("Copying Files...")
    for f in filelist:
        fname, extension = os.path.splitext(f)
        del fname
        
        extension.lower()
        targetpath = os.path.join(topath,extension)
        targetbase = os.path.basename(f)
        targetfile = os.path.join(targetpath,targetbase)
        
        if os.path.isfile(targetfile):
            srchash = GetHash(f)
            targethash = GetHash(targetfile)
            
            if targethash != srchash:
                found=0
                dupfolder=1
                while found==0:
                    targetpathd = os.path.join(targetpath,str("duplicates"+str(dupfolder)))
                    if os.path.isdir(targetpathd)==False:
                        os.mkdir(targetpathd)
                        shutil.copy2(f,targetpathd)
                        found=1
                    elif os.path.isdir(targetpathd)==True:
                        if os.path.exists(os.path.join(targetpathd,targetbase))==True:
                            targetfile = os.path.join(targetpathd,targetbase)
                            targethash = GetHash(targetfile)
                            if targethash != srchash:
                                dupfolder=dupfolder+1
                            elif targethash == srchash:
                                found=1
                        elif os.path.exists(os.path.join(targetpathd,targetbase))==False:
                            shutil.copy2(f,targetpathd)
                            found=1

        elif os.path.isfile(targetfile)==False:
            shutil.copy2(f,targetpath)

def Main():
    topath="sorted"
    frompath=GetDataPathFromUser() 
    filelist=MakeFileList(frompath)
    extensions=GetExensions(filelist)
    CreateToFolders(extensions,topath)
    PrintDirectory(filelist,topath)
    CopyFiles(filelist,topath)

Main()

