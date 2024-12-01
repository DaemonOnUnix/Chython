import kpm.commands.create
import kpm.commands.install
import kpm.commands.remove

CMD_LIST = [
    kpm.commands.create.Create,
    kpm.commands.install.Install,
    kpm.commands.remove.Remove
]

def handle_command(args):
    cmd_name = args[0]
    cmd_args = args[1:]
    for cmd_class in CMD_LIST:
        if cmd_name in cmd_class.NAMES:
            cmd = cmd_class()
            cmd.exec(cmd_args)
            return
    print(f'Command not found: {cmd_name}')