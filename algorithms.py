import random
import time

import config


class Algorithm:
    def __init__(self, heuristic=None):
        self.heuristic = heuristic
        self.nodes_evaluated = 0
        self.nodes_generated = 0

    def get_legal_actions(self, state):
        self.nodes_evaluated += 1
        max_index = len(state)
        zero_tile_ind = state.index(0)
        legal_actions = []
        if 0 <= (up_ind := (zero_tile_ind - config.N)) < max_index:
            legal_actions.append(up_ind)
        if 0 <= (right_ind := (zero_tile_ind + 1)) < max_index and right_ind % config.N:
            legal_actions.append(right_ind)
        if 0 <= (down_ind := (zero_tile_ind + config.N)) < max_index:
            legal_actions.append(down_ind)
        if 0 <= (left_ind := (zero_tile_ind - 1)) < max_index and (left_ind + 1) % config.N:
            legal_actions.append(left_ind)
        return legal_actions

    def apply_action(self, state, action):
        self.nodes_generated += 1
        copy_state = list(state)
        zero_tile_ind = state.index(0)
        copy_state[action], copy_state[zero_tile_ind] = copy_state[zero_tile_ind], copy_state[action]
        return tuple(copy_state)

    def get_steps(self, initial_state, goal_state):
        pass

    def get_solution_steps(self, initial_state, goal_state):
        begin_time = time.time()
        solution_actions = self.get_steps(initial_state, goal_state)
        print(f'Execution time in seconds: {(time.time() - begin_time):.2f} | '
              f'Nodes generated: {self.nodes_generated} | '
              f'Nodes evaluated: {self.nodes_evaluated}')
        return solution_actions


class ExampleAlgorithm(Algorithm):
    def get_steps(self, initial_state, goal_state):
        state = initial_state
        solution_actions = []
        while state != goal_state:
            legal_actions = self.get_legal_actions(state)
            action = legal_actions[random.randint(0, len(legal_actions) - 1)]
            solution_actions.append(action)
            state = self.apply_action(state, action)
        return solution_actions
        
from collections import deque

class BreathFirstAlgorithm(Algorithm):
    def get_steps(self, initial_state, goal_state):
        state = initial_state
        queue = deque([(initial_state, [])])
        solution_actions = []
        visited = set()

        while state != goal_state and queue:
            state, solution_actions = queue.popleft()

            if state == goal_state:
                return solution_actions 

            if state in visited:
                continue
            visited.add(state)
            legal_actions = self.get_legal_actions(state)

            for action in legal_actions:
                new_state = self.apply_action(state, action)
                new_actions = solution_actions + [action]
                queue.append((new_state, new_actions))

        return solution_actions



class BestFirstAlgorithm(Algorithm):
    def get_steps(self, initial_state, goal_state):
        state = initial_state
        heap = [(0, initial_state, [])]
        heapq.heapify(heap)
        solution_actions = []
        visited = set()
        h = self.heuristic

        while state != goal_state and heap:
            heuristic, state, solution_actions = heapq.heappop(heap)
            if state == goal_state:
                return solution_actions

            if state in visited:
                continue
            visited.add(state)
            legal_actions = self.get_legal_actions(state)

            for action in legal_actions:
                add_state = self.apply_action(state, action)
                add_solution_actions = solution_actions + [action]
                add_heuristic = h.get_evaluation(add_state)
                heapq.heappush(heap, (add_heuristic, add_state, add_solution_actions))

        return solution_actions
        
        
class AStarAlgorithm(Algorithm):
    def get_steps(self, initial_state, goal_state):
        state = initial_state
        h = self.heuristic
        partial_path = [(self.heuristic.get_evaluation(initial_state), initial_state, [])]
        heapq.heapify(partial_path)
        solution_actions = []
        visited = set()

        while partial_path:

            heuristic, state, solution_actions = heapq.heappop(partial_path)

            if state == goal_state:
                return solution_actions

            if state in visited:
                continue
            visited.add(state)
            legal_actions = self.get_legal_actions(state)

            for action in legal_actions:
                add_state = self.apply_action(state, action)
                add_cost = len(solution_actions) + 1
                add_heuristic = h.get_evaluation(add_state)
                add_value = add_cost + add_heuristic
                add_solution_actions = solution_actions + [action]
                #partial_path.append((add_value, add_state, add_solution_actions))
                heapq.heappush(partial_path, (add_value, add_state, add_solution_actions))

        return solution_actions