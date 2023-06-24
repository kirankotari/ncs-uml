import logging
import shutil
from os import getcwd
from pathlib import Path
from utils import Singleton, Utils


class NcsUml(metaclass=Singleton):
    name = 'ncs-yang'
    command = []
    ncs_path = None
    uml_tpath = None

    def __init__(self, *args, **kwargs):
        self.util = Utils(**kwargs)
        self.path = getcwd()
        self.log = self.util.log

    @property
    def help(self):
        return """
ncs-uml <YangFileName>
        -v  | --version
        -vv | --verbose
        -h  | --help
        """

    @property
    def options(self):
        self._help = ['-h', '--help']
        self._version = ['-v', '--version']
        self._verbose = ['-vv', '--verbose']
        return self.util.flatset([self._help, self._version, self._verbose])

    def get_ncs_path(self):
        ncs_path = None
        try:
            ncs_path = self.util.cmd.run(['which', 'ncsc'])
        except Exception as e:
            msg = f"source <NCS-DIR>/ncsrc\n\n{e.message}"
            raise SystemError(msg)
        if ncs_path is None or ncs_path == '':
            self.util.exit
        ncs_path = Path(ncs_path).absolute()
        # returning ncs yang file path
        return f"{ncs_path.parent.parent}/src/ncs/yang"

    def create_workdir(self, ncs_path):
        self.uml_tpath = f"/tmp/.ncs_uml"
        if self.util.file.is_folder(self.uml_tpath):
            shutil.rmtree(self.uml_tpath)

        self.util.cmd.call(f'mkdir {self.uml_tpath}')
        self.util.cmd.call(f'cp -r {ncs_path} {self.uml_tpath}')

    def get_pyang(self):
        # not formatted
        pyang_path = None
        pyang_lst = str(self.util.cmd.run(['type', '-a', 'pyang'])).lower().split("\n")
        ncs_pyang_bool = lambda x: 'nso' not in x and 'ncs' not in x and 'current' not in x
        
        for each in pyang_lst:
            if 'pyang' in each and ('python' in each or 'env' in each or ncs_pyang_bool(each)):
                pyang_path = each.split()[-1]
                break
            else:
                pyang_path = each.split()[-1]

        if pyang_path is None or 'pyang' not in pyang_path:
            self.log.error("pyang is not installed, please install pyang command: `pip install pyang`")
            self.util.exit

        if not ncs_pyang_bool(pyang_path):
            self.log.error("we are getting ncs pyang, but we required python pyang")
            self.log.error("add python path before ncs path, and source them.")
            self.util.exit

        paths =[
            "/usr/local/share/yang",
            "/usr/local/share/yang/modules",
            "/usr/local/share/yang/schema",
            "/usr/local/share/yang/xslt",
        ]
        for each in paths:
            if Path(each).exists() == False:
                msg = f"mandatory files are missing: {paths}"
                raise FileNotFoundError(msg)
        return pyang_path

    def generate(self, files):
        ncs_path = self.get_ncs_path()
        self.create_workdir(ncs_path)
        cmd = self.get_pyang()

        for each in files:
            if not self.util.file.is_file(each):
                msg = f"could not find yang file {file} in {self.path}"
                raise FileNotFoundError(msg)

            self.log.debug("file {file} exists, fetching dependencies")
            file = Path(each).absolute()
            self.generate_umlfile(cmd, file)

    def copy_yangs(self, file):
        # read makefile to identify the dependency yang files
        makefile = f"{file.parent.parent}/Makefile"
        if not self.util.file.is_file(makefile):
            msg = f"could not find Makefile in the following path: {makefile}"
            raise FileNotFoundError(msg)

        mkf = self.util.make.read(makefile)
        yang_paths = mkf.get('YANGPATH', '').split()
        for each in yang_paths:
            if each == '--yangpath':
                continue
            self.util.cmd.call(f"cp -r {file.parent.parent}/{each} {self.uml_tpath}")

    def generate_umlfile(self, cmd, file):
        uml_file = f"{file.stem}.uml"
        self.copy_yangs(file)
        cmd += f" -f uml {file} --path={self.uml_tpath}/yang"
        cmd += f" --uml-no=import,annotation --uml-output-directory=. 1> {uml_file} 2> /dev/null"
        self.log.debug(f"command: {cmd}")
        self.util.cmd.call(cmd)
        self.log.info(f"uml file: {uml_file}")

        self.clean_uml(uml_file)
        self.log.info(f"uml clean up done.")

    def clean_uml(self, uml_file):
        lines = open(f"{uml_file}", "r").readlines()
        start_index, end_index = 0, -1
        for i, line in enumerate(lines):
            if 'startuml' in line:
                start_index = i
            if 'center footer' in line:
                end_index = i
        lines = [f'@startuml {Path(uml_file).stem}\n'] + lines[start_index+1:end_index] + ['@enduml', '\n']
        open(f"{uml_file}", "w").writelines(lines)


if __name__ == "__main__":
    # uml = NcsUml()
    # print(uml.help)
    # print(uml.options)
    pass