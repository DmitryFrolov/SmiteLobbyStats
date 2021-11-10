from enum import Enum

class Queue(Enum):
    Conquest = "426"
    Arena = "435"
    Joust = "448"
    Assault = "445"
    Clash = "466"
    MOTD = "434"
    Siege = "459"
    ArenaVsAIVeryEasy = "457"
    ArenaVsAIEasy = "10163"
    ArenaVsAIMedium = "468"

    def __str__(self):
        return self.value