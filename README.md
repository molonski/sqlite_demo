# SQLite_Demo

This is a simple example package built by Chris Moloney to serve as demonstration code with unittests and documentation.
It's purpose is to interact with SQLite Databases.

More through documentation is available through the Sphinx and reStructedText docs. 
Clone the repo, change to the /docs directory, then run the following commands:
* run `pip install -r requirements.txt` to install python dependencies.
* change into the docs directory
* run `sphinx-apidoc -o ./ ../sqlite_demo ` - to include the sphinx autodoc documentation. 
* run `make html` - to render the html documentation.

The html docs will then be available at `docs/_build/_static/index.html`.
