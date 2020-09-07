Crappy thing I made for interfacing with RCE (ex: mostly webshells) conveniently

Drag and drop plugin support so it's easy to extend this with a less bad webshell, bindshell, etc

More features to come once I figure out what I actually want to add. Maybe exploitation modules to do the setup for you? dunno

The basic POST webshell embeds command output as a b64 string within an easily identifiable div. The webshell plugin extracts the embedded command output and displays it so you don't have to look at a webpage or type commands in burpsuite intercept / the URL bar to interact with your shell

