import sys

sys.path.append('../../')

from Core import SolverCore

required_triplets = ['{}{}{}'.format(chr(i), chr(i + 1), chr(i + 2)) for i in range(ord('a'), ord('y'))]
disallowed_letters = ['i', 'o', 'l']
potential_pairs = ['{}{}'.format(chr(i), chr(i)) for i in range(ord('a'), ord('z') + 1)]

class Solver(SolverCore):
    def increment_password(self, password):
        # We want to make sure that we handle the case of having offending letters first. If we
        # think about it, we can very easily conclude that rules 1 and 3 are going to be fulfilled
        # at the very end of the string every time (for example aabcc is a valid ending) and it will
        # take at most 5 characters to do so (so 26 ^ 5 combinations, which isn't particularly a lot).
        # So, if an offending character exists, we handle its first iteration and let the bruteforce handle
        # the rest of the cases. If no offending characters exist, there will always be at most 26^5 (probably
        # much, much less than this) different passwords that we need to go through.
        # As a further optimization, the next password can probably be found in near-constant time (the length
        # of the input password rather, but that one's short so we can say constant) if we programmatically analyze
        # what the password looks like, i.e up until the last 5 letters how many rules are fulfilled (or partially
        # fulfilled). Then, we can easily deduce how we want to fulfill the next rule (for example, if rule 1 is fulfilled
        # then we can just construct a 4 letter ending that takes care of rule 3, which would probably be something like XXaa,
        # where X is the 4th letter of the password from the right etc). There are a lot of edge cases for this
        # though and I couldn't bother.
        if any([letter in password for letter in disallowed_letters]):
            i_idx = password.find('i')
            o_idx = password.find('o')
            l_idx = password.find('l')
            
            if i_idx == -1:
                i_idx = sys.maxsize
            if o_idx == -1:
                o_idx = sys.maxsize
            if l_idx == -1:
                l_idx = sys.maxsize
                
            offending_index = min(i_idx, o_idx, l_idx)
            if offending_index < sys.maxsize:
                result = password[:offending_index]
                result += chr(ord(password[offending_index]) + 1)
                result += 'a' * (len(password) - 1 - offending_index)
                
                return result
            
        result = ''
        increment = 1
        
        for idx, char in enumerate(password[::-1]):
            next_char = char
            if increment:
                next_char = chr(ord(char) + 1)
                increment = 0
                if char == 'z':
                    next_char = 'a'
                    increment = 1
            result += next_char
        
        return result[::-1]
    
    def is_valid_password(self, password):
        triplets_check = any([triplet in password for triplet in required_triplets])
        pairs_check = sum([password.count(pair) for pair in potential_pairs]) >= 2
        
        return triplets_check and pairs_check
        
    def _solve(self, problem_input):
        password = problem_input[0].strip()
        
        while True:
            password = self.increment_password(password)
            if self.is_valid_password(password):
                break
            
        return password


solver = Solver('ghjaabcc')
solver.solve()