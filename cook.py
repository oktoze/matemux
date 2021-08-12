import os

from recipe import Session, Window


def cook_session(session: Session):
    os.system(
        f"tmux new-session -d -s {session.name} -n {session.windows[0].name} -c {session.root}"
    )

    for i, window in enumerate(session.windows):
        needs_creation = i > 0
        cook_window(window, session, needs_creation)

    os.system(f"tmux select-window -t {session.name}:{session.focus}")

    os.system(f"tmux attach-session -t {session.name}")


def cook_window(window: Window, session: Session, needs_creation: bool = True):
    root = window.root or session.root

    if needs_creation:
        os.system(f"tmux new-window -t {session.name} -n {window.name} -c {root} -d ")

    for i, pane in enumerate(window.panes):
        root = pane.root or root
        split_vertical = None if i == 0 else window.panes[i - 1].next_split_vertical
        split_flag = "v" if split_vertical else "h"

        if i > 0:
            os.system(
                f"tmux split-window -{split_flag} -t {session.name}:{window.name} -c {root}"
            )

        commands = [*session.commands, *window.commands, *pane.commands]

        for command in commands:
            os.system(
                f"tmux send-keys -t {session.name}:{window.name}.{i} '{command}' ENTER"
            )

    os.system(f"tmux select-pane -t {session.name}:{window.name}.{window.focus}")
