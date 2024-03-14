class Heuristic:
    def get_evaluation(self, state):
        pass


class ExampleHeuristic(Heuristic):
    def get_evaluation(self, state):
        return 0

class Hamming(Heuristic):
    def get_evaluation(self, state):
        # broj plocica koje nisu na odgovoarajucim pozicijama
        initial_state, goal_state = s.get_init_and_goal_states()
        hamming = 0
        for i in range(config.N ** 2):
            if state[i] != goal_state[i] and state[i] != 0:
                hamming = hamming + 1
        print(hamming)
        return hamming

class Manhattan(Heuristic):
    def get_evaluation(self, state):
        # suma distanci  do ciljne
        manhattan = 0
        for i in range(config.N ** 2):
            if state[i] != 0:
                curr_pos = s.get_pos_2d(i, config.N)
                goal_pos = s.get_pos_2d(state[i], config.N)
                manhattan += abs(curr_pos[0] - goal_pos[0]) + abs(curr_pos[1] - goal_pos[1])
        return manhattan

        
