import os


class Tmux:
    base_command = "tmux "

    @staticmethod
    def create_session(
        session: str = None, window: str = None, root: str = None, detached: bool = True
    ):
        command = Tmux.base_command + "new-session "

        if detached:
            command += "-d "

        if session:
            command += f"-s {session} "

        if window:
            command += f"-n {window} "

        if root:
            command += f"-c {root}"

        os.system(command)

    @staticmethod
    def attach(session: str):
        command = Tmux.base_command

        if os.environ.get("TMUX"):
            command += "switch-client "
        else:
            command += "attach-session "

        command += f"-t {session}"

        os.system(command)

    @staticmethod
    def new_window(
        session: str, window: str = None, root: str = None, detached: bool = True
    ):
        command = Tmux.base_command + f"new-window -t {session} "

        if detached:
            command += f"-d "

        if window:
            command += f"-n {window} "

        if root:
            command += f"-c {root} "

        os.system(command)

    @staticmethod
    def select_window(session: str, window: str = "0"):
        command = Tmux.base_command + f"select-window -t {session}:{window}"

        os.system(command)

    @staticmethod
    def select_pane(session: str, window: str = "0", pane: str = "0"):
        command = Tmux.base_command + f"select-pane -t {session}:{window}.{pane}"

        os.system(command)

    @staticmethod
    def send_keys(
        keys, session: str, window: str = "0", pane: str = "0", press_enter: bool = True
    ):
        command = (
            Tmux.base_command + f"send-keys -t {session}:{window}.{pane} '{keys}' "
        )

        if press_enter:
            command += "ENTER"

        os.system(command)

    @staticmethod
    def split_window(
        session: str, window: str = "0", split_type: str = "-h", root: str = None
    ):
        command = (
            Tmux.base_command + f"split-window {split_type} -t {session}:{window} "
        )

        if root:
            command += f"-c {root}"

        os.system(command)
