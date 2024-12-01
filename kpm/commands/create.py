import kpm.package_def
import kpm.requirements
import kpm.project_context

class Create:
    NAMES = ['c', 'create']
    PKG_TYPES = ['module', 'project']

    def exec(self, cmd_line, ctx):
        # print(f'Command Create: {" - ".join(cmd_line)}')
        if len(cmd_line) < 5:
            print('Usage: kpm create <type> <package_name> <version> <author> <license>')
            return
        if ctx != None:
            print('Already a KPM project ! Aborting.')
            return
        pkg_type = cmd_line[0]
        if pkg_type not in self.PKG_TYPES:
            print(f'Invalid package type: {pkg_type}')
            print(f'Valid package types: {", ".join(self.PKG_TYPES)}')
            return
        package_name = cmd_line[1]
        version = cmd_line[2]
        author = cmd_line[3]
        license = cmd_line[4]
        requirements = kpm.requirements.Requirements('')
        package = kpm.package_def.PkgInfo(package_name, pkg_type, version, '', author, license)
        ctx = kpm.project_context.ProjectContext(package, requirements)
        ctx.writeback('.')
