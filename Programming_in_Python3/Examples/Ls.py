#!/usr/bin/env python3

import optparse
import os
import time
import locale
locale.setlocale(locale.LC_ALL, "")

def main():
	parser = optparse.OptionParser("Usage: ls.py [options] [path1 [path2 [... pathN]]]")
	parser.add_option("-H", "--hidden", action="store_true", dest="hidden",
						help='show hidden files')
	parser.add_option("-m", "--modified", action="store_true", dest="modified",
						help='show last modified date/time')
	parser.add_option("-o", "--order", type='choice', choices=['name', 'n', 'modified', 'm', 'size', 's'], dest="order", default="name",
						help="order by ('name', 'n', 'modified', 'm', 'size', 's')[default: name]")
	parser.add_option("-r", "--recursive", action="store_true", dest="recursive",
						help='recurse into subdirectories [default: off]')
	parser.add_option("-s", "--size", action="store_true", dest="size",
						help='show sizes [default: off]')
	opts, args = parser.parse_args()
	if not args:
		args = ['./']
	else:
		for i in args:
			if not i.endswith('/'):
				args[args.index(i)] += "/"

	if opts.order in ['m', 'modified']:
		mod = 'date'
	elif opts.order in ['s', 'size']:
		mod = 'size'
	else:
		mod = 'name'
	line_keys = []
	if not opts.recursive:
		for n in args:
			for i in os.listdir(n):
				if opts.hidden:
					info = {
						'name': i,
						'size': (os.path.getsize(n+i)),
						'date': (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.path.getmtime(n+i))))
					}
					line_keys.append(info)
				else:
					if i.startswith('.'):
						continue
					else:
						info = {
						'name': i,
						'size': (os.path.getsize(n+i)),
						'date': (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.path.getmtime(n+i))))
						}
						line_keys.append(info)
	else:	
		for i in args:
			for root, dirs, files in os.walk(i):
				gen1 =  (x for x in dirs)
				if opts.hidden:
					for n in gen1:
						info = {
						'name': root + (n if root.endswith('/') else '/'+n),
						'size': (os.path.getsize(root + (n if root.endswith('/') else '/'+n))),
						'date': (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.path.getmtime(root + (n if root.endswith('/') else '/'+n)))))
						}
						line_keys.append(info)
					#gen =  (x for x in files if os.path.isfile(x) or os.path.isdir(x))
					for n in files:
						info = {
						'name': root + (n if root.endswith('/') else '/'+n),
						'size': (os.path.getsize(root + (n if root.endswith('/') else '/'+n))),
						'date': (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.path.getmtime(root + (n if root.endswith('/') else '/'+n)))))
						}
						line_keys.append(info)
				else:
					for n in gen1:
						if n.startswith('.'):
							continue
						else:
							info = {
							'name': root + (n if root.endswith('/') else '/'+n),
							'size': (os.path.getsize(root + (n if root.endswith('/') else '/'+n))),
							'date': (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.path.getmtime(root + (n if root.endswith('/') else '/'+n)))))
							}
							line_keys.append(info)
					for n in files:
						if n.startswith('.'):
							continue
						else:
							info = {
							'name': root + (n if root.endswith('/') else '/'+n),
							'size': (os.path.getsize(root + (n if root.endswith('/') else '/'+n))),
							'date': (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.path.getmtime(root + (n if root.endswith('/') else '/'+n)))))
							}
							line_keys.append(info)

	# print(line_keys)

	if line_keys:
		max_size = len(str(max(line_keys, key=lambda x: x['size']).get('size')))
	else:
		max_size = 0
	if opts.size and opts.modified:
		print_format = '{date} {size:>{ln}n} {name}'
	elif opts.size:
		print_format = '{size:>{ln}n} {name}'
	elif opts.modified:
		print_format = '{date} {name}'
	else:
		print_format = '{name}'
	for i in sorted(line_keys, key=lambda x: x[mod]):
		print(print_format.format(**i,ln=max_size+1))
main()