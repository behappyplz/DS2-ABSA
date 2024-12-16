
'''
Brainstorming Prompts in Key-Point-Driven Synthesis
'''

def prompt_subject(domain):
    # brainstorm subject
    prompt = (
        f"Brainstorm a list of {domain} subjects (at least 200).\n"
        "\n"
        "Please adhere to the following guidelines:\n"
        "  - Names are not required.\n"
        "  - Summarize the core features and specialties in a short, neutral sentence.\n"
        "\n"
        "Your output should be a Python list of strings, with each element being a description."
    )

    return prompt

def prompt_AspectCategory(domain):
    # brainstorm aspect categories
    pre_prompt =  (
        f"Brainstorm a list of commonly used aspect categories in **{domain}** reviews.\n"
        "\n"
        "Please adhere to the following guidelines:\n" 
        f"  - Aspect categories should cover various potential aspects that opinions can be expressed about within the corresponding domain.\n"
        "  - Aspect categories are coarse-grained overviews, not including specific things.\n"
        "\n"
        "Your output should be a Python list of strings, with each element being a brief word denoting an aspect category."
    )
    
    filter_prompt = (
        f"Please filter the list to retain only distinct and representative aspect categories within the {domain} domain\n" 
        "Output the main reasons for selection along with the filtered Python list."
    )
    
    return pre_prompt, filter_prompt

def prompt_AspectTerm(domain, category):
    # brainstorm aspect terms
    prompt = (
        f"Brainstorm a list of commonly used aspect terms for the aspect category **{category}** within the **{domain}** domain.\n"
        "\n"
        f"Please adhere to the following guidelines:\n"
        f"  - Aspect terms should cover various potential things that opinions can be expressed about within the corresponding category.\n"
        "  - Aspect terms are fine-grained and concrete things.\n"
        "  - Aspect terms are single or multiword terms naming particular aspects of the target entity.\n"
        "\n"
        f"Your output should be a Python list of strings, with each element being an aspect term."
    )
    return prompt

def prompt_OpinionTerm(domain, category):
    # brainstorm opinion terms
    prompt = (
        f"Brainstorm a list of commonly used opinion terms for the aspect category **{category}** within the **{domain}** domain.\n"
        "\n"
        f"Please adhere to the following guidelines:\n"
        "  - Opinion terms refer to the expression carrying subjective emotions.\n"
        "  - Provide diverse words and phrases covering positive, negative, and neutral sentiments.\n"
        "\n"
        "Your output should be a Python list of lists, with each element being an [opinion, sentiment] pair."
    )

    return prompt

# *********************************************************************************************************************

'''
Attributed Prompts in Key-Point-Driven Synthesis 
'''

generate_prompt = (
'''Write a review sentence for the {domain}: {object}
Label the sentence by extracting the aspect term(s) and identifying their corresponding sentiment polarity (positive, negative, or neutral).

Requirements:
  - Keep a consistent style and annotation standard with the examples.
  - Mention the aspect term '{aspect}'.
  - Describe {category} by the opinion term '{opinion}'.
  - Express {sentiment} across aspects. 

Here are some examples:

'''
)
