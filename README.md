# issue-explorer
Z-Inspection® Issue Explorer for easier mapping from free text to the key
requirements for trustworthy AI. 

Built with Vue.js and cytoscape.js on node:16.4.2

## Project setup

Frontend (web) was configured with yarn 1.22.5.
```
cd web
yarn install
```
Backend is built with python (django and neomodel), uses neo4j as database backend. 
Initial content of the database can be created with the `bootstrap_db.cql` script.
Install python dependencies with:
```
cd django-api
pip install -r requirements.txt
```

The following environment variables are required:
- `DJANGO_SETTINGS_MODULE`: here `config.settings`
- `DJANGO_SECRET_KEY`: required for session management (JWT signing),
set so some non-empty value 

### Compiles and hot-reloads for development
Start frontend
```
cd web
yarn serve
```
Start backend
```
cd django-api
python manage.py runserver
```

### Compiles and minifies for production
```
yarn build
```

### Lints and fixes files
```
yarn lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

### Common problems
1. Hot reload is not working when using WSL  
If yarn is called from WSL, the code directory must not be on Windows, as 
WSL can't watch non-WSL files for changes. Moving to a WSL directory solves
this. See https://github.com/microsoft/WSL/issues/6255#issuecomment-730701001
2. IntelliJ / PyCharm hangs on indexing task when using WSL    
This was frequently observed during development, cause is often that the PyCharm process 
can not connect to WSL. Verify with running \<PyCharmInstallDir\>\pycharm.bat in 
PowerShell, if errors like `java.net.ConnectException: Connection refused: no further information`
appear, stop PyCharm process, type `wsl --shutdown` in PowerShell and restart PyCharm