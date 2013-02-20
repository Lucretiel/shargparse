pyparse
=======

pyparse brings the power of argparse to your shell scripts. It is designed to be
an extremely simple program you can embed into your scripts.

Example
=======

Let's get started with a simple example:

    #/bin/sh

    #myscript.sh
    cat << EOF | pyparse "$@"
        :parser:
            prog: $(basename $0)
            desctiption: This is a description of my shell script
        :argument:
            --arg1 -a

        :argument:
            --arg2 -b

        :argument:
            --flag1 -e
            action: 'store_true'

        :argument:
            --flag2 -f
            action: 'store_true'

        :argument:
            --flag3 -g
            action: 'store_true'

        :argument:
            config-file

        :end:
    EOF
    #end of myscript.sh

Running the script:

    shell> myscript.sh -b "here's an argument!" -eg /etc/config.cfg
    arg1="";
    arg2="here's an argument";
    config-file="/etc/config.cfg";
    flag1="True";
    flag2="False";
    flag3="True";
    shell> myscript.sh -h
    usage: myscript.sh [-h] [--arg1 ARG1] [--arg2 ARG2] [--flag1] [--flag2]
                       config-file

    This is a description of my shell script

    positional arguments:
      config-file

    optional arguments:
      -h, --help            show this help message and exit
      --arg1 ARG1, -a ARG1
      --arg2 ARG2, -b ARG2
      --flag1, -f
      --flag2, -g
    shell> myscript.sh --bad-argument
    usage: myscript.sh [-h] [--arg1 ARG1] [--arg2 ARG2] [--flag1] [--flag2]
                       config-file
    myscript.sh: error: too few arguments
    shell> myscript.sh --bad /etc/conf
    usage: myscript.sh [-h] [--arg1 ARG1] [--arg2 ARG2] [--flag1] [--flag2]
                       config-file
    myscript.sh: error: unrecognized arguments: --bad
    shell>

Usage
=====

The basic usage of pyparse is very simple. Call the script with your scripts
arguments exactly as you received them, and pipe into it the argparse
configuration you want to use. The script will exit with a 0 return code if it
successfully parses the arguments and is ready to return them, and a 10 if an
expected error state happens. If this happens, you should print the output
exactly as given, as it is a formatted usage or parse error message.

If it exits with 0, then it successfully parsed the arguments. The arguments are
printed in a sourcable `var="data";` format, and the script will automatically
make sure the argument names are valid by converting all `-` characters to `_`
and removing all other nonalphanumeric characters. Every argument is guarenteed
to be present, even ones that weren't provided on the original argument set.
Numbers and strings are printed as they are. Boolean values (including cases
where the argument is a flag with no argument) are reperesented as True or
False. None isn't printed at all. Lists are printed as just their contents,
separated by spaces (no [] or '' or commas). Note that, while all the arguments
are guarenteed to be sent, the order in which they are sent is arbitrary.

argparse configuration
======================

The argparse configuration is a custom syntax designed specifically for pyparse.
It is designed to be easy to construct on the fly, and send into the script
with just an echo or cat command.

The configuration is divided into sections, of which there are two kinds-
parser and argument. Sections start with a section header flag and end when the
next section begins with its header. Headers look like `:<header-name>:`

Each section is made of lines that control the contents of that section. Some
lines can be literal lines, which have no special formatting, while others can
be parameter lines, which look like `<parameter-name>: <parameter-value>`. Blank
lines are ignored. There is no support for commenting or other ignored text.

In addition to the parser and argument headers, you can also add the optional
header `:end:`, which immediatly ends reading the configuration.

parser section
--------------

The parser section configures global parser options and starts with `:parser:`.
You can have as many parser sections as you want, but once the configuration is
read, they will all be merged together, with parameters in later parser sections
overriding those in earlier ones. The parser section supports these parameters:

-   `description:`
-   `epilog:`
-   `prog:`

These corrospond directly with their equivelents in the ArgumentParser init. The
`description` and `epilog` parameters are used in usage output, and are printed
before and after the argument descriptions, respectively. `prog` controls the
name of the program that appears in the usage message, and should almost always
be argv\[0\] ($0 or $(basename $0) for you script writers).

argument section
----------------

Each argument section corrosponds to a different argument for the parser. Each
argument has one or more names, and various parameters. These names and
parameters corrospond directly to the arguments used in `argparse`'s
`add_argument` method, and will be breifly summarized here. See
http://docs.python.org/2/library/argparse.html for more details.

(Still working on these docs. Go read the python thing for now.)
