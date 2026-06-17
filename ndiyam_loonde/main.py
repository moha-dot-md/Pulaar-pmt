import os
from ndiyamloonde_v1.plausibility_score import get_score
from ngram_greedy_part.correction import correct_text
from ngram_greedy_part.n_gram import get_prob_ngram
from ndiyamloonde_v1.State import State
from ndiyamloonde_v1.ndiyamloonde_bigramme import load_text, get_prob, beam_search_substitution
from ndiyamloonde_v1.analyse_mcts import Computer



if __name__ == "__main__":

    script_dir = os.path.dirname(os.path.abspath(__file__))
    ref_path = os.path.join(script_dir, "pulaar.txt")
    test_path = os.path.join(script_dir, "test_text.txt")
    comp_path = os.path.join(script_dir, "complete.txt")

    print("DEBUG : Loading texts...")
    ref_text = load_text(ref_path)
    test_text = load_text(test_path)

    print("DEBUG : Building models...")
    
    
    
    def toAlpha(word):
        w = ""
        for c in word:
            w += c if c.isalpha() else ""
        return w
    
    s = 0
    for word in test_text.split():
        word = toAlpha(word)
        s+= len(word)
        
    N = int(s/len(test_text.split())) + 1
    print("Got the average word length : ", N)
    model_bigramme = get_prob(ref_text)
    model_ngramme = get_prob_ngram(ref_text, n=N)
    
    
  

    second_text = beam_search_substitution(test_text, model_bigramme, beam_width=30)[0]
    third_text = correct_text(test_text, model_ngramme, n=N)
    comupter  = Computer(model_ngramme, N)
    initial_state = State(test_text, get_score(test_text, model_ngramme, n=N))


    print("DEBUG : Calculating scores...")
    second_score = get_score(second_text, model_bigramme , n=2)
    third_score = get_score(third_text, model_ngramme, n=N)
    
    



    print(f"Original text: {test_text}")
    print(f"Beam search score: {second_score/len(second_text)}")
    print(f"N-gram correction score: {third_score/len(third_text)}")
  
   
    SCOR = max(second_score, third_score)
    if SCOR == second_score:
        CHOSEN_TEXT = second_text
    else:
        CHOSEN_TEXT = third_text
    

    print(f"Chosen text: {CHOSEN_TEXT}")
   



