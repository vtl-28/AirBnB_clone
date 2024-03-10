#!/usr/bin/python3
""" HBNBCommand class for command interpreter """
import cmd
import sys
from models.base_model import BaseModel
import models
from models.user import User
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ entry point of the HBNBCommand class """
    prompt = "(hbnb) "

    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """

        _cmd = _cls = _id = _args = ''

        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:
            pline = line[:]

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                       and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')

            line = ' '.join([_cmd, _cls, _id, _args])
        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, line):
        """ Quit command to exit the program """
        return True

    def do_EOF(self, line):
        """ Quit command to exit the program """
        return True

    def emptyline(self):
        """ override default emptyline function to ensure last command is not
            run when a line has been skipped
        """
        pass

    def do_create(self, line):
        """ Creates a new instance of BaseModel,
            saves it (to the JSON file) and prints the id
        """

        if line:
            args = line.split()
            if len(args) == 1:
                if str(args[0]) in HBNBCommand.__classes:
                    print(eval(args[0])().id)
                    models.storage.save()
                else:
                    print("** class doesn't exist **")
            else:
                pass
        else:
            print("** class name missing **")

    def do_show(self, line):
        """ Prints the string representation of an
            instance based on the class name and id
        """

        if line:
            args = line.split()

            if len(args) == 1:
                print("** instance id missing **")

            if len(args) == 2:
                if str(args[0]) in HBNBCommand.__classes:
                    models.storage.reload()
                    objects = models.storage.all()
                    key = args[0] + "." + args[1]

                    try:
                        value = objects[key]
                        print(value)
                    except KeyError:
                        print("** no instance found **")

                else:
                    print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_destroy(self, line):
        """ Deletes an instance based on the class name and id
            (save the change into the JSON file)
        """

        if line:
            args = line.split()

            if len(args) == 1:
                print("** instance id missing **")

            if len(args) == 2:
                if str(args[0]) in HBNBCommand.__classes:
                    models.storage.reload()
                    objects = models.storage.all()

                    key = args[0] + "." + args[1]
                    try:
                        del objects[key]
                    except KeyError:
                        print("** no instance found **")

                    models.storage.save()
                else:
                    print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_all(self, line):
        """ Prints all string representation of all instances
            based or not on the class name
        """

        if line:
            obj_list = []
            models.storage.reload()
            objects = models.storage.all()

            if line in HBNBCommand.__classes:
                for key, val in objects.items():
                    if type(val) is eval(line):
                        obj_list.append(str(val))
                print(obj_list)
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_update(self, line):
        """ Updates an instance based on the class name and id by
            adding or updating attribute (save the change into the JSON file)
        """

        models.storage.reload()
        objects = models.storage.all()
        args = line.split()

        if len(args) == 0:
            print("** class name missing **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        elif len(args) == 2:
            print("** attribute name missing **")
            return
        elif len(args) == 3:
            print("** value missing **")
            return

        try:
            eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return

        key = args[0] + "." + args[1]

        try:
            obj_value = objects[key]
        except KeyError:
            print("** no instance found **")
            return

        try:
            attr_type = type(getattr(obj_value, args[2]))
            args[3] = attr_type(args[3])
        except AttributeError:
            pass

        setattr(obj_value, args[2], args[3])
        obj_value.save()

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in models.storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
