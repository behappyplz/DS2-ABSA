'''
E2E-ABSA Prompt Templates
'''

label_space = {
    "res": ["negative", "neutral", "positive"],
    "lap": ["negative", "neutral", "positive"]
}

def get_input_template(example, task_name="absa", cot=False):
    if task_name in ["ate", "absa"]:
        if cot:
            return f'''Sentence: {example['sentence']}\nRationale: {example['rationale']}\nLabel: '''
        else:
            return f'''Sentence: {example['sentence']}\nLabel: '''
    if task_name in ["asc"]:
        return (f"Sentence: {example['sentence']}", f"Aspects: {example['terms']}")
    
# *********************************************************************************************************************

'''
Zero-shot Prompting & In-Context Learning
'''

zero_instruction_prompt = {
    "absa":
        "Given a review, extract the aspect term(s) and determine their corresponding sentiment polarity (positive, negative, or neutral). Format the label as follows: [['aspect1', 'sentiment1'], ['aspect2', 'sentiment2'], ...]. If there are no aspect terms, use an empty list [].\n\n"
}

icl_instruction_prompt = {
    "absa":  # End2End-ABSA
        "Given a review, extract the aspect term(s) and determine their corresponding sentiment polarity (positive, negative, or neutral). Format the label as follows: [['aspect1', 'sentiment1'], ['aspect2', 'sentiment2'], ...]. If there are no aspect terms, use an empty list []. Here are some examples:\n\n"
}

# *********************************************************************************************************************

'''
Baseline: AugGPT
'''

AugGPT_prompt = (
'''Please rephrase the following sample. Label the sentence by extracting the aspect term(s) and identifying their corresponding sentiment polarity (positive, negative, or neutral). Format the label as follows: [['aspect1', 'sentiment1'], ['aspect2', 'sentiment2'], ...]. If there are no aspect terms, use an empty list [].

Sample:

'''
)

# *********************************************************************************************************************

'''
Baseline: CoTAM
'''

CoTAM_prompt = (
## add the Sentence-Label pair here
'''Please think step by step:
1. What are some other attributes of the above sentence except “<attr>”?
2. How to write a similar sentence with these attributes and “<newattr>”?
3. Write such a sentence without any other explanation. Label the sentence by extracting the aspect term(s) and identifying their corresponding sentiment polarity (positive, negative, or neutral). 

'''
)

# *********************************************************************************************************************

'''
Baseline: ZeroGen
'''

ZeroGen_prompt = (
'''Write a {domain} review in {label} sentiment. Label the sentence by extracting the aspect term(s) and identifying their corresponding sentiment polarity (positive, negative, or neutral).

Example:

'''
)

# *********************************************************************************************************************

'''
Baseline: Self-Instruct
'''

SelfInstruct_prompt = (
'''Come up with new samples refer to the following examples. Try to generate 4 sentences. Label each sentence by extracting the aspect term(s) and determine their corresponding sentiment polarity (positive, negative, or neutral). Format the label as follows: [['aspect1', 'sentiment1'], ['aspect2', 'sentiment2'], ...]. If there are no aspect terms, use an empty list [].

Examples:

'''
)

# *********************************************************************************************************************

'''
Baseline: UniNER
'''

UniversalNER_prompt = (
'''Given a review, your task is to extract all aspects and identify their sentiments. The output should be a list of lists of the following format:  [["aspect 1", "sentiment of aspect 1"],...]. If there are no aspects, return an empty list [].

Review: {review}'''
)






