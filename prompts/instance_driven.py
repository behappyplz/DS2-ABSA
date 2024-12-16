'''
Prompts for Sample Combination in Instance-Driven Synthesis
'''

combination_prompt = (
'''Given 2 {domain} example reviews with the labels, please combine them to generate 4 diverse sentences. Label each sentence by extracting the aspect term(s) and determine their corresponding sentiment polarity.

Requirements:
  - Keep a consistent style and annotation standard with the examples.
  - Maintain the same format as the examples.
  - Combine the aspects and meanings of both examples in every generated sentence.

Examples:

'''
)

paraphrase_prompt = (
'''Given a {domain} example review with the label, please paraphrase it to generate 4 diverse sentences. Label each sentence by extracting the aspect term(s) and determine their corresponding sentiment polarity.

Requirements:
  - Keep a consistent style and annotation standard with the example. 
  - Maintain the same format as the example.
  - The meaning of the example sentence should be unchanged. 

Example:

'''
)

# *********************************************************************************************************************

'''
Prompts for Selective Reconstruction in Instance-Driven Synthesis
'''

mask_generate_prompt = (
'''Given a partially masked {domain} review sentence, please reconstruct it to generate 4 diverse sentences. Label each sentence by extracting the aspect term(s) and determine their corresponding sentiment polarity.

Masked Sentence: {mask}

Requirements:
  - Keep a consistent style and annotation standard with the example.
  - Maintain the same format as the example.
  - The unmasked part of the should be unchanged.

Example: 

'''
)

