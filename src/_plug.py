import importlib
import sys


"""
To load a plugin, the specified module name is imported, and the object assigned
to its `plugin` attribute is loaded as a new plugin. This object must implement some
mandatory attributes and may implement additional optional attributes as specified:

MANDATORY:
.init_session(*args):
    called upon initialization and given any user-supplied arguments required to
    start the interactive TTY. This should catch any expected errors and return None on success,
    or a string describing the error on failure, and should only generate an Exception if
    unexpected conditions occur.

.command(bstr):
    bstr: a bytes-like object containing command data to be executed on the remote.

    return a tuple of (code, output), where code is a zero integer on successful execution
    and a nonzero integer otherwise, and output is a bytes-like object containing the output

    DON'T perform exit by expecting a command. exit input will be processed by beatty
    and the plugin will receive an exit_session() call.

.exit_session():
    called when the user wishes to close down their session and should perform
    any and all required cleanup. if session is unable to close cleanly due to an
    expected reason, should return a string describing the error, otherwise None.
    (same as init_session, only generate an Exception if unexpected conditions arise)

OPTIONAL:
.usage:
    string describing usage for module
"""

# load and return a plugin with the specified name from the specified list of
# plugin directory paths. returns the plugin object from the module
#
# this is approximately a 4 IQ way of doing drag-and-droppable plugins
# a better way would be to check a plugin directory for files and generate a
# staging file which resolves plugin imports, then import the staging file
def plug(mod_name, paths):
    saved_path = sys.path

    sys.path = paths

    try:
        mod = importlib.import_module(mod_name)

    finally:
        sys.path = saved_path

    if not hasattr(mod, 'plugin'):
        raise AttributeError("Module {} does not export a plugin".format(mod_name))

    return mod.plugin

