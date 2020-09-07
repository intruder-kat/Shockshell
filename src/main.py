#!/usr/bin/env python3
import sys
import os
import select
import asyncio

import _plug

PLUGDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'plug')

INFO = (

)

def main():
    try:
        mod_name  = sys.argv[1]
        plug_args = sys.argv[2:]

    except IndexError:
        print("usage:\nshockshell [OPTIONS]... PLUGIN [ARGS]...\nfor help, see beautty -h/--help", file=sys.stderr)

        return 1

    plugin_name = mod_name[:-3] if mod_name.endswith('.py') else mod_name

    try:
        plugin = _plug.plug(mod_name, [PLUGDIR])

    except ModuleNotFoundError as e:
        print("[!] failed to find module:\n{}".format(e), file=sys.stderr)
        return 1

    print("initializing session")

    err = plugin.init_session(*plug_args)
    if None is not err:
        print("Failed to init plugin {}: {}".format(plugin_name, err), file=sys.stderr)
        return 1

    # begin main loop, reading a line of stdin and sending it to the remote,
    # then waiting for a response.
    while True:
        command = input("[{}]$ ".format(plugin_name))

        if command == 'exit':
            err = plugin.exit_session()
            if None is not err:
                print("[!] unable to perform a clean exit:\n{}".format(err), file=sys.stderr)
                return 1

            break

        _status, output = plugin.command(command.encode())
        sys.stdout.buffer.write(output)

    return 0

if __name__ == "__main__":
    sys.exit(main())

