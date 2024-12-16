import json

import spacy
spacy.require_cpu()

import random
from prompts.instance_driven import *
from prompts.templates import *

nlp = spacy.load("en_core_web_sm")

def mask_aspect_terms(sentence, aspects, window_size=2):
    doc = nlp(sentence)
    masks = [False] * len(doc)
    for aspect in aspects:
        start_token_idx = None
        end_token_idx = None
        for token in doc:
            if token.idx >= int(aspect['from']):
                start_token_idx = token.i
                break
        for token in doc:
            if token.idx + len(token.text) >= int(aspect['to']):
                end_token_idx = token.i
                break
        # print(sentence)
        assert start_token_idx is not None and end_token_idx is not None
        start_idx = max(start_token_idx - window_size, 0)
        end_idx = min(end_token_idx + window_size, len(doc) - 1)

        for i in range(start_idx, end_idx + 1):
            masks[i] = True

    masked_sentence = []
    for i, token in enumerate(doc):
        if masks[i]:
            masked_sentence.append("<mask>")
        else:
            masked_sentence.append(token.text)

    final_sentence = []
    previous_mask = False
    for word in masked_sentence:
        if word == "<mask>" and previous_mask:
            continue
        final_sentence.append(word)
        previous_mask = (word == "<mask>")

    return ' '.join(final_sentence)


def mask_context(sentence, aspects, sample_times=2):
    doc = nlp(sentence)
    masks = [False] * len(doc)
    
    for aspect in aspects:
        start = int(aspect['from'])
        end = int(aspect['to'])
        for token in doc:
            if not (token.idx >= end or token.idx + len(token.text) <= start):
                masks[token.i] = True
    outputs = []
    for i in range(sample_times):
        max_start = int(len(doc) * 0.4)
        start_point = random.randint(0, max_start)
        end_point = start_point + int(len(doc) * 0.6)
        end_point = min(end_point, len(doc))

        masked_sentence = []
        for i, token in enumerate(doc):
            if start_point <= i < end_point and not masks[i]:
                masked_sentence.append("<mask>")
            else:
                masked_sentence.append(token.text)
                
        final_sentence = []
        previous_mask = False
        for word in masked_sentence:
            if word == "<mask>" and previous_mask:
                continue
            final_sentence.append(word)
            previous_mask = (word == "<mask>")
        outputs.append(' '.join(final_sentence))
    return outputs


def get_instance_prompts(domain, dataset, seed, num_shots):
    with open(f'data/{domain}/sample{num_shots}_{dataset}.json', 'r', encoding='utf-8-sig') as file:
        train = json.load(file)
        
    train_exp = []
    for t in train:
        if len(t['aspects']) > 0:
            train_exp.append(t)
    print(f"Number of examples with aspects: {len(train_exp)}")
    
    import random
    random.seed(seed)

    # 采样20k个样本
    output = []
    type = "paraphrase_one"
    for i in range(len(train_exp)):
        prompt = {}
        prompt['ID'] = train_exp[i]['ID'] + f"_{type}"
        example = train_exp[i]
        example_prompt = get_input_template(example)
        label = [[asp["target"], asp["polarity"]] for asp in example['aspects']]
        example_prompt += f"{label}\n\n"
        prompt_aug = paraphrase_prompt.replace("{domain}", "restaurant" if "res" in domain else "laptop")
        prompt_aug += example_prompt
        prompt['prompt_aug'] = prompt_aug + "4 Diverse Paraphrased Sentences with Labels:\n\n1. Sentence: "
        output.append(prompt)
    
    type = "paraphrase_comb"
    # Initialize a set to track unique combinations
    combined_set = set()

    # Maximum number of combinations allowed
    MAX_COMBINE = 1000 # Adjust this number as necessary

    # Main loop to generate combinations
    while len(combined_set) < MAX_COMBINE:
        i, j = random.randint(0, len(train_exp)-1), random.randint(0, len(train_exp)-1)
        if i != j:  # Ensure different samples
            combo_id = f"{train_exp[i]['ID']}_{train_exp[j]['ID']}_{type}"
            
            # Check if this combination has already been used
            if combo_id not in combined_set:
                combined_set.add(combo_id)  # Mark this combination as used
                prompt = {}
                prompt['ID'] = combo_id
                example1 = train_exp[i]
                example2 = train_exp[j]

                example1_prompt = get_input_template(example1)
                label1 = [[asp["target"], asp["polarity"]] for asp in example1['aspects']]
                example1_prompt += f"{label1}\n\n"
                example2_prompt = get_input_template(example2)
                label2 = [[asp["target"], asp["polarity"]] for asp in example2['aspects']]
                example2_prompt += f"{label2}\n\n"
                
                prompt_aug = combination_prompt.replace("{domain}", "restaurant" if "res" in domain else "laptop")
                prompt_aug += "1. " + example1_prompt + "2. " + example2_prompt
                prompt['prompt_aug'] = prompt_aug + "4 Diverse Combined Sentences with Labels:\n\n1. Sentence: "
                
                
                output.append(prompt)
                
        # Break if all possible combinations have been tried
        if len(combined_set) == len(train_exp) * (len(train_exp) - 1):
            break
        
    type = "aspect_mask"
    for i in range(len(train_exp)):
        for window in [0, 2]:
            prompt = {}
            prompt['ID'] = train_exp[i]['ID'] + f"_{type}_{window}"
            # mask aspect terms
            masked_sentence = mask_aspect_terms(train_exp[i]['sentence'], train_exp[i]['aspects'], window_size=window)
            example = train_exp[i]
            example_prompt = get_input_template(example)
            label = [[asp["target"], asp["polarity"]] for asp in example['aspects']]
            example_prompt += f"{label}\n\n"
            prompt_aug = mask_generate_prompt.replace("{domain}", "restaurant" if "res" in domain else "laptop")\
                .replace("{mask}", masked_sentence)
            prompt_aug += example_prompt
            prompt['prompt_aug'] = prompt_aug + "4 Diverse Reconstructed Sentences with Labels:\n\n1. Sentence: "
            output.append(prompt)
    
    type = "context_mask"
    for i in range(len(train_exp)):
        # mask context words
        masked_sentences = mask_context(train_exp[i]['sentence'], train_exp[i]['aspects'], sample_times=2)
        for idx, masked_sentence in enumerate(masked_sentences):
            prompt = {}
            prompt['ID'] = train_exp[i]['ID'] + f"_{type}_{idx}"
            example = train_exp[i]
            example_prompt = get_input_template(example)
            label = [[asp["target"], asp["polarity"]] for asp in example['aspects']]
            example_prompt += f"{label}\n\n"
            prompt_aug = mask_generate_prompt.replace("{domain}", "restaurant" if "res" in domain else "laptop")\
                .replace("{mask}", masked_sentence)
            prompt_aug += example_prompt
            prompt['prompt_aug'] = prompt_aug + "4 Diverse Reconstructed Sentences with Labels:\n\n1. Sentence: "
            output.append(prompt)

    with open(f'prompts/instance_prompts/{domain}_{dataset}{num_shots}.json', 'w', encoding='utf-8-sig') as file:
        json.dump(output, file, indent=4, ensure_ascii=False)

    return output
    


