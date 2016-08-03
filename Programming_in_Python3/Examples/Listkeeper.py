#!/usr/bin/env python3

import os, sys

def get_string(message, name="string", default=None,
               minimum_length=0, maximum_length=80):
    message += ": " if default is None else " [{0}]: ".format(default)
    while True:
        try:
            line = input(message)
            if not line:
                if default is not None:
                    return default
                if minimum_length == 0:
                    return ""
                else:
                    raise ValueError("{0} may not be empty".format(
                                     name))
            if not (minimum_length <= len(line) <= maximum_length):
                raise ValueError("{name} must have at least "
                        "{minimum_length} and at most "
                        "{maximum_length} characters".format(
                        **locals()))
            return line
        except ValueError as err:
            print("ERROR", err)


def get_integer(message, name="integer", default=None, minimum=0,
                maximum=100, allow_zero=True):

    class RangeError(Exception): pass

    message += ": " if default is None else " [{0}]: ".format(default)
    while True:
        try:
            line = input(message)
            if not line and default is not None:
                return default
            i = int(line)
            if i == 0:
                if allow_zero:
                    return i
                else:
                    raise RangeError("{0} may not be 0".format(name))
            if not (minimum <= i <= maximum):
                raise RangeError("{name} must be between {minimum} "
                        "and {maximum} inclusive{0}".format(
                        " (or 0)" if allow_zero else "", **locals()))
            return i
        except RangeError as err:
            print("ERROR", err)
        except ValueError as err:
            print("ERROR {0} must be an integer".format(name))

def main():
    dir_list = os.listdir(".")
    dir_list_lst = list()
    for i in dir_list:
        if i.endswith(".lst"):
            dir_list_lst.append(i)
    if dir_list_lst:
        for i in dir_list_lst:
            print ("{0}.{1}".format(dir_list_lst.index(i)+1, i))
        filename = get_integer("Choose file from 0[new file] to {0}".format(len(dir_list_lst)), default=1)
        if not filename:
        	get_name()
        	get_option(("[A]dd [Q]uit [a]: "), add='a', quit='q', default='a')
        else:
            fh = None
            filename = dir_list_lst[filename-1]
            if filename in dir_list_lst:
                fh = open(filename)
                if os.stat(filename).st_size == 0:
                    print("-- no items are in the list --")
                    if get_option(("[A]dd [Q]uit [a]: "), add='a', quit='q', default='a') == "a":
                    	add_string(filename, get_string("Add item"))
                    elif get_option(("[A]dd [Q]uit [a]: "), add='a', quit='q', default='a') == "q":
                    	print("Exiting...")
                else:
                    list_file(filename)
                    option = get_option(("[A]dd [D]elete [S]ave [Q]uit [a]: "), add='a', quit='q', delete='d', save='s', default='a')
                    if  option == 'a':
                        add_string(filename, get_string("Add item"))
                    elif option == "q":
                        print("Exiting...")
                fh.close()
    else:
        get_name()
        get_option(("[A]dd [Q]uit [a]: "), add='a', quit='q', default='a')
    


def get_name():
    message = "Choose filename: "
    #fh = None
    while True:
        try:
            line = input(message)
            if line.endswith(".lst"):
                return line
            else:
                line += ".lst"
                return line
        except ValueError:
            pass

def get_option(args, add="", delete="", quit="", save="", default="a"):
	class InvalidKey(Exception): pass
	while True:
		try:
			option = input("{0}".format(args))
			if option.lower() == '':
				return default.lower
			if option.lower() not in add and option.lower() not in delete and option.lower() not in quit and option.lower() not in save:
				raise InvalidKey("ERROR: invalid choice--enter one of: {0}{1}{2}{3}{4}{5}{6}{7}".format(add.upper(), add, delete.upper(), delete, quit.upper(), quit, save.upper(), save))
			else:
				return option.lower()
		except InvalidKey as err:
			print(err)


def add_string(filename, string):
    fh = None
    try:
        fh = open(filename, "a")
        fh.write(string+"\n")
    except EnvironmentError as err:
        print("ERROR", err)
    else:
        print("Added", string)
    finally:
        if fh is not None:
            fh.close()


def list_file(filename):
    fh = None
    try:
        fh = open(filename, "r")
        for i, line in enumerate(fh, 1):
            print("{0}.{1}".format(i, line))
    except EnvironmentError as err:
        print("ERROR", err)
    finally:
        if fh is not None:
            fh.close()

def load_list(filename):
    fh = None
    l = list()
    try:
        fh = open(filename, "r")
        for i in fh:
        	l.append(i)
        return l
    except EnvironmentError as err:
        print("ERROR", err)
    finally:
        if fh is not None:
            fh.close()

def del_item(lst, number_to_delete):
	del lst[number_to_delete-1]
	return lst


main()
#gg = get_option(("[A]dd [Q]uit [a]: "), add='a', quit='q',save='s', default='a')
#add_string(get_name(), get_string("Add item"))
#list_file(get_name())
#print(load_list("m.lst"))