# matemux
---
matemux is a simple tmux session generator: it generates a session with customized window and pane layouts from a yaml file, called a recipe.

## usage 

`$ matemux [RECIPE-FILE-NAME] [--args] [ARGS]...`

create the session based on .matemux/RECIPE-FILE-NAME.yml with ARGS following --args flag. `$MATEMUX_DIR` is ~/.matemux by default. You could change it by setting `$MATEMU_DIR` in your environment.

### examples
`$ matemux example --args --command runserver --port 8000`
create a session based on ~/.matemux/example.yml and pass command=runserver and port=8000 to example.yml commands.

## recipes
each session is generated from a .yml file called a recipe. a sample recipe is shown below:

`~/.matemux/example.yml`

```
---
session: example
root: ~/projects/example
defaults:
  command: runserver
  port: 8000
commands:
  - source activate venv/bin/activate
  - C-l
focus: sql
windows:
  - window: main
    focus: 2
    panes:
        - pane: 0
          commands:
            - htop
        - pane: 1
          commands:
            - neofetch
          next-split-vertical: true
        - pane: 2
          root: ~/projects/example/server
          commands:
            - "{{command}} {{port}}"
  - window: home
    root: ~/
```

At the top level of a .yml file, the following keys could be defined:
  - `session` is the name of the session to be created. It accepts strings and integer values.
  - `root` defines the default directory for all virtual terminals in the session. It must be a valid path. By default, it's set to '~/'.
  - `defaults` is the default arguments to be passed to commands, we'll cover them later on. they should be an object of key-value pairs. It could be omitted.
  - `commands` are a list of commands that are executed in all virtual terminals in the session. it could be omitted.
  - `focus` defines the window to focus on at the initial state of the session. By default, it's the first window. It accepts strings (name of the window) or integers (window number (0, 1, ...))
  - `windows` is a list of window configuration, with the following keys:
    - `window` is the name of the window. It could be omitted, in that case,
	  it's set by default to its index.
    - `root` defines the default directory for all panes in the window. It must be
       a valid path. By default, it's set to the session's root.
    - `focus` defines the pane to focus on at the initial state of the window.
	  By default, it's the first pane (index 0)
     - `panes` is a list of pane configuration, with the following keys:
       - `pane` it's completely optional and has no effect. It could be set to the pane index to make the .yml file more readable, especially in regards to window focus.
       - `root` defines the default directory for the pane. It must be a valid path. By default, it's set to the parent window's root.
	   - `commands` are a list of commands to be executed in the pane.
       - `next-split-vertical` is a boolean that defines whether or not the split for the next pane should be vertical. By default, it's set to `false`. Imagine the current layout is like this:
        ```
		 ----------------
		 |              |
		 |      0       |
		 |              |
		 |              |
		 ----------------
		 ```
		 if it's false, when if we define another pane, the new layout would be:
		 ```
		 ----------------
		 |       |      |
		 |   0   |   1  |
		 |       |      |
		 |       |      |
		 ----------------
		 ```
		 but if it's true, the new layout would be:
		 ```
		 ----------------
		 |      0       |
		 |______________|
		 |      1       |
		 |              |
		 ----------------
		 ```
		 
running `$ matemux example` creates a session with two windows:
first window is called `main` and has the following layout:
```
---------------
|      |   1  |
|  0   |______|
|      |   2  |
|      |      |
---------------
```
`htop` is running in pane 0, `neofetch` is running in pane 1, and `runserver 8000` is running in in pane 2.
second window is called `home` and has a single pane.

### Notes about commands and defaults:
  - commands are propagated: If you set some commands for a session, some commands for a window, and some commands for a pane, they're all executed in the pane's virtual terminal, in that order.

  - You could use custom arguments in commands, in the form `{{arg}}` and pass the arguments through commandline.  For example, if you have a command
   `mysql -u {{user}}`
   you could pass user like this:
    `$ matemux example --args --user myuser`
  if you want a default value for user, you should set it in session's defaults like:
```
    defaults:
      user: myuser
```
  - It's important to note argument names should only contain characters from the English alphabet and they're case-sensitive.

## Author
[Kamyab Taghizadeh](https://github.com/kamyab.zad)
