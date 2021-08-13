from matemux.recipe import Session, Window
from matemux.tmux import Tmux


def cook_session(session: Session):
    Tmux.create_session(session.name, session.windows[0].name, session.root)

    for i, window in enumerate(session.windows):
        needs_creation = i > 0
        cook_window(window, session, needs_creation)

    Tmux.select_window(session.name, session.focus)

    Tmux.attach(session.name)


def cook_window(window: Window, session: Session, needs_creation: bool = True):
    root = window.root or session.root

    if needs_creation:
        Tmux.new_window(session.name, window.name, root)

    for i, pane in enumerate(window.panes):
        root = pane.root or root
        split_vertical = None if i == 0 else window.panes[i - 1].next_split_vertical
        split_type = "-v" if split_vertical else "-h"

        if i > 0:
            Tmux.split_window(session.name, window.name, split_type, root)

        commands = [*session.commands, *window.commands, *pane.commands]

        for command in commands:
            Tmux.send_keys(command, session.name, window.name, str(i))

    Tmux.select_pane(session.name, window.name, window.focus)
