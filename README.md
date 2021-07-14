# issue-explorer
Z-Inspection® Issue Explorer for easier mapping from free text to the key
requirements for trustworthy AI. 

Built with Vue.js and cytoscape.js on node:16.4.2

## Project setup
Project was configured with yarn 1.22.5.
```
yarn install
```

### Compiles and hot-reloads for development
```
yarn serve
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
