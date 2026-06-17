from copy import deepcopy
from heapq import nlargest
from itertools import product




from .State import State
from .ndiyamloonde_bigramme import SUBSTITUTIONS, normalize_text, get_prob
from ndiyamloonde_v2.n_gram import get_score_ngram as get_score
import numpy as np
from .MCTS_node import MCTSNode

class Computer:
    def __init__(self, model, N):
        self._model = model
        self._nodes:set[MCTSNode] = set()
        self._maxiterations = 1000
        self._rollout_limit = 50
        self._DOMINENCE=0.5
        self.N =N

    def best_move_from_root(self, root:"MCTSNode") -> "MCTSNode":
        """On s'est un peu inspire de Alpha Go,
           On prend le meilleur selon le nombre de visites."""

        if not root.children:
            return None

        best_node = max(
            root.children,
            key=lambda n : n.visits
        )

        return best_node

    def uct(self,node:"MCTSNode"):
        if node.visits == 0:
            return float('inf')

        if node.parent is None:
            return -100

        ni:int = node.visits
        N:float = max(1.0, node.parent.visits)
        xi:float = node.winrate
        c:float = 1.41

        return xi + c * (np.sqrt(np.log(N) / ni))

    def heuristic(self, state: State):
        """
        Génère un état de fallback si aucune route complète n'est trouvée.
        """
        text = state.text

        EXPECTATIONS = self._model 

        # copie l'état actuel
        new_state = deepcopy(state)

            # score heuristique : somme log probabilité bigramme
        score = 0.0
        for i in range(len(text) - 1):
            a, b = text[i], text[i + 1]
            prob = EXPECTATIONS.get((a, b), 1e-8)
            score += np.log(prob)

        # fallback pour lettres restantes : on estime prob max pour chaque lettre
        max_prob = max(EXPECTATIONS.values())
        score += (len(text) - 1) * np.log(max_prob)

        new_state.score = score
        return new_state

    # def pickOne(self, words:dict[str,list[str]]):
    #     r = np.random.rand()
    #     choices = {}
    #     if r < 0.5:
    #         for word,subs in words.items():
    #             choices[word] = subs[0]
    #     else:
    #         for word, subs in words.items():
    #             choices[word] = np.random.choice(subs)

    #     return choices
    def pickOne(self, words):

        choices = {}

        for word, subs in words.items():

            if len(subs) == 1:
                choices[word] = subs[0]
                continue

            scores = np.array([get_score(s, self._model, n=self.N) for s in subs])

            # softmax
            probs = np.exp(scores - np.max(scores))
            probs /= probs.sum()

            choices[word] = np.random.choice(subs, p=probs)

        return choices

    def select_node(self, nodes:set["MCTSNode"]):
        maximum = float('-inf')
        best_node:"MCTSNode" = None
        for node in nodes:
            uct_value = self.uct(node)
            if uct_value > maximum:
                maximum = uct_value
                best_node = node
        return best_node

    def generate_possible_substitutions_by_word(self,text: str, model, n=3):

        text = normalize_text(text)

        options = []

        for char in text:

            if char in SUBSTITUTIONS:

                if char == "n":
                    options.append([char] + list(SUBSTITUTIONS[char]))
                else:
                    options.append([char, SUBSTITUTIONS[char]])

            else:
                options.append([char])

        results = []

        for combo in product(*options):
            candidate = "".join(combo)
            score = get_score(candidate, model, n)
            results.append((candidate, score))

        best = nlargest(n, results, key=lambda x: x[1])

        return [x[0] for x in best]

    def generate_subs(self,text:str):
        dictionnary = {}

        words = text.split(" ")

        for word in words:
            subs = self.generate_possible_substitutions_by_word(word, self._model, 3)
            dictionnary[word]=subs
            print(f"WORD : {word} -> {subs}")
        return dictionnary

    def mcts_analyse(self, state:State):

        root:"MCTSNode" = MCTSNode(state)
        root.increase_visits()
        self._nodes.add(root)
        final_path = []

        for k in range(self._maxiterations):
            selected_path:list["MCTSNode"] = []
            current_node:"MCTSNode" = root
            selected_path.append(current_node)
            reward:float = 0.0

            while len(current_node.children) > 0:
                current_node = self.select_node(current_node.children)
                if current_node.state.is_final():
                    selected_path.append(current_node)
                    self._nodes.add(current_node)
                    break
                selected_path.append(current_node)
                self._nodes.add(current_node)

            """Expansion"""

            if current_node.state.is_final():
                reward = 1.0
                for node in selected_path:
                    node.increase_visits()
                    node.update_winrate(reward)
                break

            possible_subs:dict[str,list[str]] = self.generate_subs(current_node.state.text)

            child:"MCTSNode" = MCTSNode(self.apply_mock_substitution(current_node.state,self.pickOne(possible_subs)))
            child.set_parent(current_node)
            current_node.add_child(child)
            self._nodes.add(child)
            selected_path.append(child)

            switchable_state:State = child.state
            already_visited:set[State] = set()
            steps:int = 0

            while(not switchable_state.is_final() and steps < self._rollout_limit):
                steps += 1
                possible_subs:dict[str,list[str]] = self.generate_subs(switchable_state.text)

                switchable_state = self.apply_mock_substitution(switchable_state,self.pickOne(possible_subs))

                if switchable_state in already_visited:
                    reward = -1.0
                    break
                if switchable_state.is_final():
                    reward = 1.0
                    already_visited.add(switchable_state)

                already_visited.add(switchable_state)

            if reward==0.0:
                reward = self.compute_reward(switchable_state, current_node.state)

            """Backprop"""
            for node in selected_path:
                node.increase_visits()
                node.update_winrate(reward)

            final_path = selected_path

            
        the_node:"MCTSNode" = self.best_move_from_root(root)

        if the_node is None:
            print("DEBUG: No solution found, fallback to heuristic.")
            the_node = MCTSNode(self.heuristic(state))
            the_node.update_winrate(-2)

        else:
            print("DEBUG: the node is found.")

        final_text:str  = the_node.state.text
        score = the_node.totalwin
        return final_text,final_path,score

    def apply_mock_substitution(self, current_state: State, choices):

        clone_state = deepcopy(current_state)
        words = clone_state.text.split()

        new_words = []

        for w in words:
            new_words.append(choices.get(w, w))

        clone_state.text = " ".join(new_words)
        clone_state.score = get_score(clone_state.text, self._model, n=self.N)

        return clone_state

    def compute_reward(self, state, parent_state):

        delta = get_score(state.text, self._model, n=self.N) - get_score(parent_state.text, self._model, n=self.N)

        return np.tanh(5 * delta)