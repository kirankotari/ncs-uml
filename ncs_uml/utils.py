import re
import sys
import logging
import subprocess

from os import path, remove, chdir
from itertools import chain, takewhile


class Singleton(type):
    name = __name__
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=Singleton):
    name = __name__
    format = '%(levelname)5s | %(module)6s | %(message)s'

    def __init__(self, level=None):
        self.level = level or logging.INFO

    def setup(self):
        logging.basicConfig(
            stream=sys.stdout, 
            level=self.level, 
            format=self.format,
            datefmt=None
        )
        log = logging.getLogger(self.name)
        log.setLevel(self.level)
        return log


class Files(metaclass=Singleton):
    name = __name__

    def __init__(self):
        self.log = Logger().setup()

    def is_file(self, fname):
        self.log.debug("checking {} is a file".format(fname))
        return path.isfile(fname)

    def is_folder(self, fname):
        self.log.debug("checking {} is a folder".format(fname))
        return path.isdir(fname)

    def delete(self, fname): # _delete_file
        self.log.debug("deleting {}".format(fname))
        if path.exists(fname):
            remove(fname)
        self.log.debug("deleted {}".format(fname))

    def get_ext(self, fname):
        self.log.debug("get extention of {}".format(fname))
        return path.splitext(fname)[-1]


class Command(metaclass=Singleton):
    name = __name__
    stdout = subprocess.PIPE
    stderr = subprocess.PIPE

    def __init__(self, allow_log=True):
        self.allow_log = allow_log
        if self.allow_log:
            self.log = Logger().setup()

    def decode(self, args):
        return (i.decode('utf-8') for i in args)

    def call(self, cmd): # _run_bash_commands
        if self.allow_log: self.log.debug("executing $ {}".format(cmd))
        try:
            subprocess.call(cmd, shell=True)
            if self.allow_log: self.log.debug("done")
        except EnvironmentError as e:
            if self.allow_log: self.log.error("failed to run: {}".format(cmd))
            if self.allow_log: self.log.error(e)

    def run(self, cmd, raiseError=True): # _run_command
        if self.allow_log: self.log.debug("executing $ {}".format(cmd))
        try:
            p = subprocess.Popen(
                    cmd, 
                    stdout=self.stdout,
                    stderr=self.stderr
                )
            out, err = self.decode(p.communicate())
            if err == '' or 'env.sh' in err:
                if self.allow_log: self.log.debug('done')
                return out
            if raiseError:
                if '% Total' in err:
                    return err
                if self.allow_log: self.log.debug('validating the error')
                if 'command not found' in err or 'Unknown command' in err:
                    msg = "command `{}` not found".format(cmd)
                    raise SyntaxError(msg)
                raise SyntaxError(err)
        except SyntaxError as e:
            if self.allow_log: self.log.error("failed to run: {}".format(cmd))
            if self.allow_log: self.log.error(e)


class MakeFile(metaclass=Singleton):
    name = __name__

    def __init__(self) -> None:
        self.log = Logger().setup()

    def read(self, fpath):
        data = self.read_data(fpath)
        self.vars = self.get_variables(data)
        return self.vars

    def read_data(self, fpath):
        fp = open(fpath) 
        data = fp.readlines()
        fp.close()
        return data

    def remove_comment(self, data, comment='#'):
        i = data.find(comment)
        if i >= 0:
            data = data[:i]
        return data.strip()

    def get_variables(self, data, add_oper=' '):
        makevar = re.compile(r'^([a-zA-Z0-9_]+)[\s\t]*([\+=]*)(.*?)([\\#]+.*)?$')
        addvar = re.compile(r'^([^=]+)$')
        addvar_flag = False
        vars = {}
        for each in data:
            if addvar_flag is False:
                result = re.search(makevar, each)
                if result is None:
                    continue
                name, oper, value, end = result.groups()
                if oper == '':
                    continue

                if name in vars:
                    vars[name] += add_oper + value.rstrip()   
                else:
                    vars[name] = value.rstrip()
                
                if end is None:
                    continue
                end = self.remove_comment(end)
                if '\\' in end:
                    addvar_flag = True
                continue

            if name is None:
                continue
            value = None
            result = re.search(addvar, each)
            if result:
                value, = result.groups()
                value = self.remove_comment(value)
            if value is None:
                continue
            if '\\' not in value:
                addvar_flag = False
            value = self.remove_comment(value, '\\')
            vars[name] += add_oper + value
        return vars


class Utils(metaclass=Singleton):
    name = __name__

    def __init__(self, **kwargs):
        self.path = path.abspath('.')
        self.level=kwargs.get('level', None)
        self.log = Logger(self.level).setup()
        self.file = Files()
        self.cmd = Command()
        self.make = MakeFile()

    @property
    def exit(self):
        sys.exit()

    def rstrip(self, s:str): # _rstrip_digits
        return s.rstrip('1234567890')

    def iloc(self, lst, e): # get_index
        try:
            return lst.index(e)
        except ValueError:
            return None

    def change_dir(self, path):
        chdir(path)

    def flatset(slef, s):
        return set(chain(*s))

    def append_log(self, out:str, method='info'):
        if not out:
            return
        for line in out.split('\n'):
            if line: getattr(self.log, method)(line)
        if self.log.level == logging.DEBUG:
            print('')

