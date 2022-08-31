import os
import sys
import zipfile
import requests
import shutil
import zlib

className = 'ECE121'

toDir='C:\\'
sourceURL='http://soe.ucsc.edu/~mdunne/ClassZips/'+className+'.zip'
print(sourceURL)
rawZip=requests.get(sourceURL,stream=True)
zipPath=os.path.join(os.environ['TMP'],className+'.zip')
#we currently write this to a file and read it back in, we should be able to do it directly in memory instead
with open(zipPath,'wb') as f:
	rawZip.raw.decode_content = True
	shutil.copyfileobj(rawZip.raw,f)


zip=zipfile.ZipFile(zipPath)

#iterate all the files to completely mirror the structure

filesInZip=[]
for fileInfo in zip.infolist():
	localFilePath='\\'.join(os.path.join(toDir,fileInfo.filename).split('/')) # some fiddly bits because of file formats between windows and unix
	filesInZip.append(localFilePath)
	#print(localFilePath)
	[localDir,localFileName]=os.path.split(localFilePath)
	#print(localDir)
	if not os.path.exists(localDir):
		try:
			os.makedirs(localDir)
		except:
			print('Can not build directory structure, exiting')
			input()
			sys.exit(1)
		print('creating '+localDir)
	try:
		curCRC=zlib.crc32(open(localFilePath,'rb').read())
		if curCRC != fileInfo.CRC:
			print('replacing '+localFilePath)
			zip.extract(fileInfo, toDir)
	except FileNotFoundError: # if we don't have a file we can move the file
		zip.extract(fileInfo,toDir)
zip.close()
for root,dir,files in os.walk(toDir+className):
	for file in files:
		curFilePath=os.path.join(root,file)
		if not curFilePath in filesInZip: # compare against zip
			if toDir+'CMPE118' in curFilePath: # confirm that still in base directory for massive error prevention
				print('file not found: '+curFilePath)
				try:
					os.remove(curFilePath)
					print('trying to remove'+curFilePath)
				except:
					print('Unable to remove: '+curFilePath)
					sys.exit(1)
for root,dir,files in os.walk(toDir+className,topdown=False):
	for name in dir:
		try:
			os.rmdir(os.path.join(root, name))
		except OSError :
			pass
		except Exception as e:
			print("Unknown error in folder deletion")
			print(e)
			sys.exit(1)
sys.exit(0)
