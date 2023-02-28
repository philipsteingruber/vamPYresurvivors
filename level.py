import random

import pygame

from attack import Attack
from debug import debug
from entity import Entity
from monster import Monster
from player import Player
from timer import Timer
from utils import vector_between_sprites, AttackType
from experience_gem import ExperienceGem


class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = CameraGroup()
        self.monster_sprites: pygame.sprite.Group[Monster] = pygame.sprite.Group()
        self.attack_sprites: pygame.sprite.Group[Attack] = pygame.sprite.Group()
        self.xp_gem_sprites: pygame.sprite.Group[ExperienceGem] = pygame.sprite.Group()

        self.player = Player(pos=(750, 500), groups=[self.all_sprites], create_attack=self.create_attack)

        self.spawn_monsters()

        self.spawn_timer = Timer(15000, self.spawn_monsters)
        self.spawn_timer.activate()

    def spawn_monsters(self) -> None:
        for _ in range(10):
            Monster(groups=[self.all_sprites, self.monster_sprites], pos=(random.randint(-500, 1500), random.randint(-500, 1500)), monster_type='slime')

    def create_monster_quadrants(self) -> list[pygame.sprite.Group]:
        nw_monsters = []
        ne_monsters = []
        se_monsters = []
        sw_monsters = []

        player_pos = self.player.rect.center
        for monster in self.monster_sprites:
            if not (monster.get_player_distance(player_pos) > (self.display_surface.get_width() / 2) + 100):
                player_dir: pygame.math.Vector2 = monster.get_player_direction_normalized(player_pos)
                if player_dir.x >= 0 and player_dir.y >= 0:
                    se_monsters.append(monster)
                elif player_dir.x >= 0 and player_dir.y <= 0:
                    ne_monsters.append(monster)
                elif player_dir.x <= 0 and player_dir.y >= 0:
                    sw_monsters.append(monster)
                elif player_dir.x <= 0 and player_dir.y <= 0:
                    nw_monsters.append(monster)

        return [pygame.sprite.Group(nw_monsters), pygame.sprite.Group(ne_monsters), pygame.sprite.Group(se_monsters), pygame.sprite.Group(sw_monsters)]

    def check_attack_collisions(self) -> None:
        colliding_attacks: dict[Monster: Attack] = pygame.sprite.groupcollide(self.attack_sprites, self.monster_sprites, dokilla=False, dokillb=False)
        if colliding_attacks:
            for attack, monsterlist in colliding_attacks.items():
                monster = monsterlist[0]  # Each attack can only hit one monster
                if attack.attack_type == AttackType.MAGIC_WAND:
                    if monster.damageable:
                        monster.invulnerable.activate()
                        monster.health -= attack.damage
                    if attack.pierce_count < 1:
                        attack.kill()
                    else:
                        attack.pierce_count -= 1
                if monster.check_death():
                    if random.randint(1, 5) == 1:
                        self.spawn_xp_gem(pos=monster.rect.center, value=monster.xp_value)

    def increase_player_xp(self, amount: int) -> None:
        self.player.xp += amount

    def check_xp_gem_collisions(self):
        colliding_gems = pygame.sprite.spritecollide(self.player, self.xp_gem_sprites, False)
        if colliding_gems:
            for gem in colliding_gems:
                self.increase_player_xp(gem.value)
                gem.kill()

    @staticmethod
    def check_monster_collisions(monster_quadrants: list[pygame.sprite.Group]) -> None:
        sprite_radius = 14
        for quadrant in monster_quadrants:
            for monster in quadrant:
                other_monster: Monster
                for other_monster in quadrant:
                    if monster is other_monster:
                        continue
                    collision_vector = pygame.math.Vector2(monster.pos - other_monster.pos) * 0.5
                    if collision_vector.magnitude() < sprite_radius:
                        collision_vector = collision_vector.normalize() * (abs(sprite_radius - collision_vector.magnitude()))
                        monster.pos += collision_vector
                        monster.rect.center = monster.pos
                        other_monster.pos -= collision_vector
                        other_monster.rect.center = other_monster.pos

    def create_attack(self, attack_type: AttackType) -> None:
        monster_sprites_by_distance = self.monster_sprites_sorted_by_distance()
        if attack_type == AttackType.MAGIC_WAND:
            for i in range(self.player.projectile_counts[AttackType.MAGIC_WAND]):
                try:
                    nearest_monster: Monster = monster_sprites_by_distance[i]
                except IndexError:
                    if not monster_sprites_by_distance:
                        continue
                    nearest_monster: Monster = random.choice(monster_sprites_by_distance)
                Attack(pos=self.player.rect.center,
                       direction=vector_between_sprites(nearest_monster, self.player).normalize(),
                       attack_type=attack_type,
                       groups=[self.attack_sprites, self.all_sprites],
                       pierce_count=self.player.pierce_counts[attack_type],
                       damage_mod=self.player.flat_damage_mods[attack_type])

    def monster_distance_to_player(self, monster: Monster) -> float:
        return vector_between_sprites(self.player, monster).magnitude()

    def monster_sprites_sorted_by_distance(self) -> list[Monster]:
        return sorted(self.monster_sprites.sprites(), key=self.monster_distance_to_player)

    def spawn_xp_gem(self, pos: tuple[int, int], value: int):
        ExperienceGem([self.all_sprites, self.xp_gem_sprites], value, pos)

    def run(self, dt: float) -> None:
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.player)

        for monster in self.monster_sprites:
            monster.update_monster(player_pos=self.player.rect.center, dt=dt)

        # Start using quadrants if we get performance issues
        # self.check_monster_collisions(self.create_monster_quadrants())
        self.check_monster_collisions([self.monster_sprites])
        self.check_attack_collisions()
        self.check_xp_gem_collisions()

        self.spawn_timer.update()

        if dt > 0:
            debug(round(1 / dt))
            # debug((self.player.weapon_levels['magic_wand'], self.player.projectile_counts['magic_wand']))


class CameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()

        self.display_surface = pygame.display.get_surface()

        # Camera attributes
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2(0, 0)

        # Floor attributes
        self.floor_surface = pygame.image.load('assets/map/map.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def set_offset(self, player: Player) -> None:
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

    def draw_floor(self) -> None:
        offset_rect = self.floor_rect.copy()
        offset_rect.center -= self.offset
        self.display_surface.blit(self.floor_surface, offset_rect)

    def draw_sprites(self) -> None:
        sprite: Entity
        for sprite in self.sprites():
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

    def draw(self, player: Player) -> None:
        self.set_offset(player)
        self.draw_floor()
        self.draw_sprites()
