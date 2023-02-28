from utils import AttackType, LevelUpType

DIMENSIONS = {'WIDTH': 1280, 'HEIGHT': 720}
TILE_SIZE = 32
MONSTER_SIZE = 64

LEVEL_UP_DATA = {
    AttackType.MAGIC_WAND: {
        2: (LevelUpType.PROJECTILE_COUNT, 1),
        3: (LevelUpType.COOLDOWN_MOD, 200),
        4: (LevelUpType.PROJECTILE_COUNT, 1),
        5: (LevelUpType.FLAT_DAMAGE_MOD, 10),
        6: (LevelUpType.PROJECTILE_COUNT, 1),
        7: (LevelUpType.PIERCE_COUNT, 1),
        8: (LevelUpType.FLAT_DAMAGE_MOD, 10)
    }
}
