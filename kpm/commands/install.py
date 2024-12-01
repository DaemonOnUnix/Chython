import kpm.project_context

class Install:
    NAMES = ['i', 'install']

    def exec(self, cmd_line, ctx):
        print(f'Command Install: {" - ".join(cmd_line)}')