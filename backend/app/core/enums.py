import enum

class Gender(str, enum.Enum):
    """角色的性别枚举"""
    MALE = "Male"
    FEMALE = "Female"
    NON_BINARY = "Non-binary"
    OTHER = "Other"


class BuildType(str, enum.Enum):
    """角色的体型枚举"""
    SLIM = "Slim"
    ATHLETIC = "Athletic"
    AVERAGE = "Average"
    MUSCULAR = "Muscular"
    HEAVYSET = "Heavyset"


class RelationshipType(str, enum.Enum):
    """角色之间的关系类型枚举"""
    FAMILY = "Family"
    FRIEND = "Friend"
    RIVAL = "Rival"
    LOVER = "Lover"
    ENEMY = "Enemy"
    MENTOR = "Mentor"
    SUBORDINATE = "Subordinate"

# --- 新增的枚举 ---

class Race(str, enum.Enum):
    """角色的种族枚举"""
    HUMAN = "Human"
    ELF = "Elf"
    DWARF = "Dwarf"
    ORC = "Orc"
    GOBLIN = "Goblin"
    DRAGON = "Dragon"
    ANDROID = "Android"
    OTHER = "Other"


class Alignment(str, enum.Enum):
    """角色的阵营枚举 (基于D&D阵营)"""
    LAWFUL_GOOD = "Lawful Good"
    NEUTRAL_GOOD = "Neutral Good"
    CHAOTIC_GOOD = "Chaotic Good"
    LAWFUL_NEUTRAL = "Lawful Neutral"
    TRUE_NEUTRAL = "True Neutral"
    CHAOTIC_NEUTRAL = "Chaotic Neutral"
    LAWFUL_EVIL = "Lawful Evil"
    NEUTRAL_EVIL = "Neutral Evil"
    CHAOTIC_EVIL = "Chaotic Evil"


class Status(str, enum.Enum):
    """角色的当前状态枚举"""
    ALIVE = "Alive"
    DECEASED = "Deceased"
    MISSING_IN_ACTION = "Missing in Action"
    UNKNOWN = "Unknown"