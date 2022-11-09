import sys
exec(open("./shell.py").read())

app_name = sys.argv[1]
if 0 == len(Site.objects.filter(domain=app_name)):
    Site.objects.create(domain=app_name)
