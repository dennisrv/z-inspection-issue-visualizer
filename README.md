# issue-explorer
Z-Inspection® Issue Explorer for easier mapping from free text to the key
requirements for trustworthy AI. 

Frontend built with Vue.js and cytoscape.js on node:16.4.2,
backend built with django and neo4j

## Project setup (docker-compose)
For an easy start to developing use the provided docker compose file.  
1. Make a copy of `example-enviromnemt.compose.conf` called `<something>.compose.conf`, 
with the `.compose.conf` file suffix it will be ignored by git 
(please don't version your copy) 
2. The following variables need to be set in that copy
   1. NEO4J_DATA_DIR: storage location for neo4j data (i.e. `./data`)
   2. NEO4J_USER: username for the neo4j instance (should be neo4j)
   3. NEO4J_PASS: password for the neo4j instance 
   4. DJANGO_SECRET_KEY: some long alphanumeric string, will be used by django
3. With the file saved as `<env-file>`, run 
    ```
    docker-compose --env-file=<env-file> up
    ```
   to start the complete stack.
4. Initialize the database by running 
   ```
   docker exec -it issue-explorer_backend_1 python manage.py setup_database 
   ```
5. The application can now be accessed at `localhost:8080`, and all changes in the code
will lead to updates in the displayed application.

## Project setup (manual)

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
3. When running django_api / tests make sure to use the correct settings (i.e. `test.util.test_settings.py` 
instead of `src.config.settings.py`).
The settings file can be set via `--settings` option of the `manage.py` script or via
the environment variable `DJANGO_SETTINGS_MODULE`.