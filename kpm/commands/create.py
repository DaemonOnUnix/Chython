import kpm.package_def
import kpm.requirements
import kpm.project_context

class Create:
    NAMES = ['c', 'create']

    def exec(self, cmd_line, ctx):
        print(f'Command Create: {" - ".join(cmd_line)}')
        if len(cmd_line) < 4:
            print('Usage: kpm create <package_name> <version> <author> <license> [requirements]')
            return
        if ctx != None:
            print('Already a KPM project ! Aborting.')
            return
        package_name = cmd_line[0]
        version = cmd_line[1]
        author = cmd_line[2]
        license = cmd_line[3]
        requirements = kpm.requirements.Requirements('')
        package = kpm.package_def.PkgInfo(package_name, version, '', author, license)
        ctx = kpm.project_context.ProjectContext(package, requirements)
        ctx.writeback('.')
