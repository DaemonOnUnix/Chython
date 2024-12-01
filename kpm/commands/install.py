class Install:
    NAMES = ['i', 'install']

    def exec(self, cmd_line):
        print(f'Command Install: {" - ".join(cmd_line)}')