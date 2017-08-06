This app depends upon the third party library, trueskill.
In order to deploy to app engine, this library must be included as it is not
one of the available libraries provided by app engine. In order to include the
required code, execute the command:
    `pip install -t lib trueskill`

Alternatively, all of the required packages can be installed locally by running
    `pip install -t lib -r requirements.txt