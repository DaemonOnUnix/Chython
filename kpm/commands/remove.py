import kpm.project_context

class Remove:
    NAMES = ['r', 'remove']

    def run(self, cmd_line, ctx):
        print(f"Removing package: {' - '.join(cmd_line)}")