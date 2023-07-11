import shutil
from os import getcwd
from pathlib import Path
from .utils import Singleton, Utils


class NcsUml(metaclass=Singleton):
    name = 'ncs-yang'
    ncs_uml = "/tmp/.ncs_uml"

    command = []
    ncs_path = None

    def __init__(self, opt, *args, **kwargs):
        self.path = getcwd()
        self.util = Utils(**kwargs)

        self.log = self.util.log
        self.opt = opt

    def create_workdir(self):
        if self.util.file.is_folder(self.ncs_uml):
            shutil.rmtree(self.ncs_uml)

        self.util.cmd.call(f'mkdir {self.ncs_uml}')

    def copy(self, paths):
        for each in paths:
            self.util.cmd.call(f'cp -r {each}/* {self.ncs_uml}')

    def get_dependencies(self, file):
        dep_files = set()
        # read makefile to identify the dependency yang files
        makefile = f"{file.parent.parent}/Makefile"
        if not self.util.file.is_file(makefile):
            # msg = f"could not find Makefile in the following path: {makefile}"
            # raise FileNotFoundError(msg)
            return '.'

        mkf = self.util.make.read(makefile)
        yang_paths = mkf.get('YANGPATH', '').split()
        for each in yang_paths:
            if each == '--yangpath':
                continue
            dep_files.add(f'{file.parent.parent}/{each}')
        return dep_files

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

    def generate(self, yf):
        self.create_workdir()
        self.copy([self.get_ncs_path()] + self.opt.dependent_yang_paths)
        cmd = self.get_pyang()

        if not self.util.file.is_file(yf):
            msg = f"could not find yang file {yf} in {self.path}"
            raise FileNotFoundError(msg)

        self.log.debug("file {file} exists, fetching dependencies")
        file = Path(yf).expanduser().absolute()
        self.copy(self.get_dependencies(file))
        self.generate_umlfile(cmd, file)

    def generate_umlfile(self, cmd, file):
        path = Path(__file__).absolute().parent.as_posix()
        uml_file = f"{file.stem}.uml"
        cmd += f" --plugindir={path}/plugins/ -f uml {file} --path={self.ncs_uml}"
        cmd += f" --uml-no=module,import,annotation"
        if not self.opt.no_inline_groupings:
            cmd += f" --uml-inline-groupings "
        if getattr(self.opt, 'no_inline_groupings_from', False):
            cmd += f"--uml-no-inline-groupings-from={','.join(self.opt.no_inline_groupings_from)} "
        if getattr(self.opt, 'add_legend', False):
            cmd += f"--uml-add-legend "
        cmd += f" --uml-output-directory=. 1> {uml_file} 2> /dev/null"
        self.log.debug(f"command: {cmd}")
        self.util.cmd.call(cmd)
        self.log.info(f"uml file: {uml_file}")

        self.clean_uml(uml_file)
        self.log.info(f"uml clean up done.")

    def clean_uml(self, uml_file):
        lines = open(f"{uml_file}", "r").readlines()
        start_index, end_index = 0, -1
        notes = -1
        for i, line in enumerate(lines):
            if 'startuml' in line:
                start_index = i
            if 'center footer' in line:
                end_index = i
            if 'note top of' in line:
                notes = i
        if notes != -1:
            lines = [f'@startuml {Path(uml_file).stem}\n'] + lines[start_index+1:notes] + lines[notes+1:end_index]+ ['@enduml', '\n']
        else:
            lines = [f'@startuml {Path(uml_file).stem}\n'] + lines[start_index+1:end_index] + ['@enduml', '\n']
        open(f"{uml_file}", "w").writelines(lines)

