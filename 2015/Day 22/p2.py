import sys

sys.path.append('../../')

from Core import SolverCore

# Let me preface this with the fact that I am aware of how ugly the code is. There are a lot of cases
# to cover, so I couldn't figure out how to do it better. I'm sure there's a fancy way to organize all
# of this but I feel it would've taken longer to make it pretty than writing this galactic mess.
# Essentially, what we want to do in this problem is implement a BFS going through all of the possible
# moves we can do, but with a twist. We do it in a smart way, implementing somewhat of a "glass cannon mage".
# What this means is we greedily try to deal as much damage as possible in a single branch of the algorithm
# and kill the boss if possible. If this is a viable scenario, the first solution we find is going to be the
# most optimal one (this is sort of hinted as well since the 2 direct damaging spells in our arsenal just so
# happen to be the least cost ones). We only ever resort to other strategies if we absolutely cannot get the
# boss down fast. Since the spell costs are conveniently made to suit this, we can reliably run it on any input
# and it's going to give us the optimal answer.
# The reason why I went with BFS is a) because it doesn't particularly matter and b) I had a feeling that if
# the solution is somewhere in the middle branches of the traversal tree BFS would be much better.
# I kind of have a feeling that an edge case might exist where this is not the case, but if we think about it
# it does not really matter the order in which we execute the moves but rather the subset of moves that we want
# to do. With that in mind, greedily going for the cheapest first should grant us a solution that is always the
# minimum cost.
class Solver(SolverCore):
    def _solve(self, problem_input):
        boss_hp, boss_d = tuple([int(line.strip().split(': ')[1]) for line in problem_input])
        
        # player_hp, player_mp, shield_timer, poison_timer, recharge_timer, boss_hp, mana_spent
        start_state = (50, 500, 0, 0, 0, boss_hp, 0)
        queue = [start_state]
        
        while queue:
            state = queue.pop(0)
            p_h, p_m, s_t, p_t, r_t, boss_hp, mana_spent = state
            
            if boss_hp <= 0:
                # the boss is dead, our greedy found the quickest way to do it
                return mana_spent
            
            if p_h <= 0:
                # we lost, try a different approach
                continue
            
            current_player_d = 0
            shield_timer = 0
            recharge_timer = 0
            poison_timer = 0
            player_mp = 0
            player_hp = 0
            
            def reset():
                nonlocal shield_timer
                nonlocal recharge_timer
                nonlocal poison_timer
                nonlocal current_player_d
                nonlocal player_mp
                nonlocal player_hp
                nonlocal s_t
                nonlocal r_t
                nonlocal p_t
                nonlocal p_m
                nonlocal p_h
                
                shield_timer = s_t
                recharge_timer = r_t
                poison_timer = p_t
                current_player_d = 0
                player_mp = p_m
                player_hp = p_h - 1
            
            def do_overtime_effects():
                nonlocal shield_timer
                nonlocal recharge_timer
                nonlocal poison_timer
                nonlocal current_player_d
                nonlocal player_mp
                
                if shield_timer:
                    shield_timer -= 1
                
                if recharge_timer:
                    recharge_timer -= 1
                    player_mp += 101
                    
                if poison_timer:
                    poison_timer -= 1
                    current_player_d += 3
            
            def calculate_damage_taken():
                nonlocal shield_timer
                nonlocal boss_d
                
                return boss_d - 7 if shield_timer else boss_d
            
            reset()
            
            if player_hp <= 0:
                # died before making a turn, try again
                continue
            
            # cast magic missiles
            if player_mp >= 53:
                reset()
                mana_lost = 53
                do_overtime_effects()
                if boss_hp - current_player_d <= 0:
                    mana_lost = 0
                current_player_d += 4
                do_overtime_effects()
                
                queue += [(player_hp - calculate_damage_taken(), player_mp - mana_lost, shield_timer, poison_timer, recharge_timer, boss_hp - current_player_d, mana_spent + mana_lost)]
                reset()
            
            if player_mp >= 73:
                reset()
                mana_lost = 73
                do_overtime_effects()
                if boss_hp - current_player_d <= 0:
                    mana_lost = 0
                current_player_d += 2
                player_hp += 2
                do_overtime_effects()
                
                queue += [(player_hp - calculate_damage_taken(), player_mp - mana_lost, shield_timer, poison_timer, recharge_timer, boss_hp - current_player_d, mana_spent + mana_lost)]
                reset()
            
            if player_mp >= 113:
                reset()
                mana_lost = 0
                do_overtime_effects()
                cast = False
                if shield_timer == 0 and boss_hp - current_player_d > 0:
                    shield_timer = 6
                    mana_lost = 113
                    cast = True
                do_overtime_effects()
                
                if cast:
                    queue += [(player_hp - calculate_damage_taken(), player_mp - mana_lost, shield_timer, poison_timer, recharge_timer, boss_hp - current_player_d, mana_spent + mana_lost)]
                reset()
            
            if player_mp >= 173:
                reset()
                mana_lost = 0
                do_overtime_effects()
                cast = False
                if poison_timer == 0 and boss_hp - current_player_d > 0:
                    poison_timer = 6
                    mana_lost = 173
                    cast = True
                do_overtime_effects()
                
                if cast:
                    queue += [(player_hp - calculate_damage_taken(), player_mp - mana_lost, shield_timer, poison_timer, recharge_timer, boss_hp - current_player_d, mana_spent + mana_lost)]
                reset()
            
            if player_mp >= 229:
                reset()
                mana_lost = 0
                do_overtime_effects()
                cast = False
                if recharge_timer == 0 and boss_hp - current_player_d > 0:
                    recharge_timer = 5
                    mana_lost = 229
                    cast = True
                do_overtime_effects()
                
                if cast:
                    queue += [(player_hp - calculate_damage_taken(), player_mp - mana_lost, shield_timer, poison_timer, recharge_timer, boss_hp - current_player_d, mana_spent + mana_lost)]
                reset()
        
        # there is no possible scenario in which we can kill the boss, should not happen
        return -1


solver = Solver(279)
solver.solve()