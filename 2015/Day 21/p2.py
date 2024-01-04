import sys
from math import ceil

sys.path.append('../../')

from Core import SolverCore

shop = {
    'weapons': [
        (8, 4, 0),
        (10, 5, 0),
        (25, 6, 0),
        (40, 7, 0),
        (74, 8, 0)
    ],
    'armor_pieces': [
        (0, 0, 0),
        (13, 0, 1),
        (31, 0, 2),
        (53, 0, 3),
        (75, 0, 4),
        (102, 0, 5)
    ],
    'rings': [
        (0, 0, 0),
        (0, 0, 0),
        (25, 1, 0),
        (50, 2, 0),
        (100, 3, 0),
        (20, 0, 1),
        (40, 0, 2),
        (80, 0, 3)
    ]
}

class Solver(SolverCore):
    def _solve(self, problem_input):
        boss_hp, boss_d, boss_a = tuple([int(line.strip().split(': ')[1]) for line in problem_input])
        player = (100, 0, 0)
        
        weapons, armor_pieces, rings = shop['weapons'], shop['armor_pieces'], shop['rings']
        
        result = 0
        
        for weapon in weapons:
            w_c, w_d, w_a = weapon
            for armor in armor_pieces:
                a_c, a_d, a_a = armor
                for r1_i, ring1 in enumerate(rings):
                    r1_c, r1_d, r1_a = ring1
                    for r2_i, ring2 in enumerate(rings):
                        if r1_i == r2_i:
                            continue
                        r2_c, r2_d, r2_a = ring2
                        
                        player_hp, player_d, player_a = player
                        equipped_player_hp, equipped_player_d, equipped_player_a = player_hp, player_d + w_d + a_d + r1_d + r2_d, player_a + w_a + a_a + r1_a + r2_a
                        
                        # (p_damage- - b_armor) * p_t >= b_hp <=> p_t = ceil(b_hp / (p_damage- - b_armor))
                        # (b_damage - p_armor) * b_t >= p_hp <=> b_t = ceil(p_hp / (b_damage - p_armor))
                        
                        p_t = ceil(boss_hp / max(1, equipped_player_d - boss_a))
                        b_t = ceil(equipped_player_hp / max(1, boss_d - equipped_player_a))
                        
                        if p_t > b_t:
                            result = max(result, w_c + a_c + r1_c + r2_c)
                        
        return result


solver = Solver(28)
solver.solve()