import android
import os
import codecs
import CreateHtml

droid = android.Android()

droid.addOptionsMenuItem('Index', 'index', None, 'ic_menu_agenda')
droid.addOptionsMenuItem('Edit', 'edit', None, 'ic_menu_edit')
droid.addOptionsMenuItem('Quit', 'kill', None, 'ic_menu_close_clear_cancel')

if os.path.isfile(fullpath+'currentpath.dat'):
	f = open(fullpath+'currentpath.dat','r')
	currentpath = f.readlines()[0]
	f.close()
else:
	currentpath = fullpath+"welcome.txt"

if os.path.isfile(fullpath+'currentzim.htm'):
    droid.webViewShow(fullpath+'currentzim.htm')
else:
    f = open(fullpath+"currentzim.htm","w")
    html = CreateHtml.create(fullpath+"welcome.txt",fullpath,currentpath)
    f.write(html)
    f.close()
    droid.webViewShow(fullpath+"currentzim.htm")
        
while True:
	res = droid.eventWait().result
	if res == None:
		continue
	elif res['name'] == 'kill':
		break
	elif res['name'] == 'index':
		title = 'Choose page'
		droid.dialogCreateAlert(title)
		filelist = []
		pathlist = []
		for dirname, dirnames, filenames in os.walk(fullpath+notebook):
			for filename in sorted(filenames):
				if filename[-3:] == "txt":
					pathlist.append(os.path.join(dirname, filename))
					filelist.append(str(os.path.join(dirname, filename))[len(fullpath+notebook)+1:-4])
			if '.zim' in dirnames:
				dirnames.remove('.zim')
		droid.dialogSetItems(filelist)
		droid.dialogShow()
		response = droid.dialogGetResponse()
		droid.dialogDismiss()
		index = int(response.result["item"])
		# Create and save HTML
		currentpath = pathlist[index]
		f = open(fullpath+'currentpath.dat','w')
		f.write(currentpath)
		f.close()
		f = open(fullpath+"currentzim.htm","w")
		html = CreateHtml.create(pathlist[index],fullpath,currentpath)
		f.write(html)
		f.close()
		content = CreateHtml.createcontentonly(pathlist[index],fullpath, currentpath)
		droid.eventPost('loadnewpage', content)
		continue
	elif res['name'] == 'edit':
		content = CreateHtml.createedit(currentpath,fullpath)
		droid.eventPost('loadnewpage', content)
		continue
	elif res['name'] == 'save':
		changedtext = res['data']
		f = codecs.open(currentpath,'w',encoding='utf8')
		f.write(unicode(changedtext))
		f.close()
		f = open(fullpath+"currentzim.htm","w")
		html = CreateHtml.create(currentpath,fullpath,currentpath)
		f.write(html)
		f.close()
		content = CreateHtml.createcontentonly(currentpath,fullpath,currentpath)
		droid.eventPost('loadnewpage', content)
		continue
	elif res['name'] == 'cancel':
		f = open(fullpath+"currentzim.htm","w")
		html = CreateHtml.create(currentpath,fullpath,currentpath)
		f.write(html)
		f.close()
		content = CreateHtml.createcontentonly(currentpath,fullpath,currentpath)
		droid.eventPost('loadnewpage', content)
		continue
	elif res['name'] == 'link':
		linkpath = res['data']
		if os.path.isfile(linkpath):
			f = open(linkpath,"w")
			html = CreateHtml.create(linkpath,fullpath,currentpath)
			f.write(html)
			f.close()
			content = CreateHtml.createcontentonly(linkpath,fullpath,currentpath)
			droid.eventPost('loadnewpage', content)
			continue
		else:
			f = open(fullpath+"currentzim.htm","w")
			html = CreateHtml.create(currentpath,fullpath,currentpath)
			f.write(html)
			f.close()
			content = CreateHtml.createcontentonly(currentpath,fullpath,currentpath)
			droid.eventPost('loadnewpage', content)
			continue
