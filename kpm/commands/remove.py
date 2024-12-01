class Remove:
    NAMES = ['r', 'remove']

    def run(self, cmd_line):
        print(f"Removing package: {' - '.join(cmd_line)}")