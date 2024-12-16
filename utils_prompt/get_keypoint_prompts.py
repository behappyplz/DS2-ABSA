import json

from brainstorm_output.objects import *
from brainstorm_output.categories import *
from brainstorm_output.aspects import *
from brainstorm_output.opinions import *
from brainstorm_output.sentiments import *
from prompts.keypoint_driven import *
from prompts.templates import *

def get_keypoint_prompts(domain, dataset, seed, num_shots, num_samples, num_examples):

    with open(f'data/{domain}/sample{num_shots}_{dataset}.json', 'r', encoding='utf-8-sig') as file:
        train = json.load(file)

    train_exp = []
    for t in train:
        if len(t['aspects']) > 0:
            train_exp.append(t)
    print(f"Number of examples with aspects: {len(train_exp)}")
    
    sent_type = sentiments

    if "res" in domain:
        obj = res_objects
        ac = res_ac
        at = [at for v in res_at.values() for at in v] # all aspects
        ot = res_opinions
    elif domain == "lap":
        obj = lap_objects
        ac = lap_ac
        at = [at for v in lap_at.values() for at in v] # all aspects
        ot = lap_opinions

    import random
    random.seed(seed)

    output = []
    for i in range(num_samples):
        prompt = {}
        prompt['ID'] = i
        prompt['object'] = random.choice(obj)
        prompt['aspect'] = random.choice(at)
        prompt['category'] = random.choice(ac)
        ot_for_cat = ot[prompt['category']]
        prompt['opinion'] = random.choice(ot_for_cat)
        prompt['sentiment'] = random.choice(sent_type)
        prompt['examples'] = []
        for _ in range(num_examples):
            prompt['examples'].append(random.choice(train_exp))
        opinion = prompt['opinion'][0]
        if prompt['sentiment'] == "a consistent sentiment":
            sentiment = prompt['sentiment'] + f" ({prompt['opinion'][1]})"
        else:
            sentiment = prompt['sentiment']
        keypoint_prompt = generate_prompt.replace("{domain}", "restaurant" if "res" in domain else "laptop")\
            .replace("{object}", prompt['object'])\
            .replace("{aspect}", prompt['aspect']).replace("{category}", prompt['category'])\
            .replace("{opinion}", opinion).replace("{sentiment}", sentiment)
        for example in prompt['examples']:
            keypoint_prompt += get_input_template(example)
            label = [[asp["target"], asp["polarity"]] for asp in example['aspects']]
            keypoint_prompt += f"{label}\n\n"
        #print(keypoint_prompt)
        prompt['prompt_gen'] = keypoint_prompt + "Sentence: "
        output.append(prompt)
        
    with open(f'prompts/keypoint_prompts/{domain}_{dataset}{num_shots}.json', 'w', encoding='utf-8-sig') as file:
        json.dump(output, file, indent=4, ensure_ascii=False)


