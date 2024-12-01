import kpm.package_def
import kpm.requirements
import kpm.xreader

class ProjectContext:
    FILENAME_REQUIREMENTS = 'kpm_requirements.txt'
    FILENAME_PROJECT = 'kpm_project.toml'
    REPOSITORY_LIST = '~/.config/kpm/repos'
    def __init__(self, Package_def, Requirements):
        self.package_def = Package_def
        self.requirements = Requirements
        try:
            with open(ProjectContext.REPOSITORY_LIST, 'r') as f:
                self.repositories = f.read().split('\n')
        except FileNotFoundError:
            self.repositories = []
    
    def __repr__(self):
        return f'ProjectContext({self.package_def}, {self.requirements})'
    
    def writeback(self, path):
        with open(f'{path}/{ProjectContext.FILENAME_PROJECT}', 'w') as f:
            f.write(self.package_def.to_toml())
        with open(f'{path}/{ProjectContext.FILENAME_REQUIREMENTS}', 'w') as f:
            f.write(self.requirements.serialize())
    
    @classmethod
    def from_path(cls, path):
        try:
            with kpm.xreader.xFile(f'{path}/{ProjectContext.FILENAME_PROJECT}') as f:
                package_def = kpm.package_def.PkgInfo.from_toml(f.read())
        except FileNotFoundError:
            return None
        try:
            with kpm.xreader.xFile(f'{path}/{ProjectContext.FILENAME_REQUIREMENTS}') as f:
                requirements = kpm.requirements.Requirements(f.read())
        except FileNotFoundError:
            requirements = kpm.requirements.Requirements('')
        return cls(package_def, requirements)
    