player_name = None

def set_player_name(name: str):
    global player_name
    player_name = name

def get_player_name() -> str:
    return player_name or "Player"