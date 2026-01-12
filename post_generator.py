from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


# def generate_post(length, language, tag):
#     prompt = f"""
# Write a LinkedIn post.

# Length: {length}
# Language: {language}
# Topic/Tag: {tag}

# Make it professional, engaging, and human-like.
# """

#     response = llm.invoke(prompt)   # prompt is now PURE STRING
#     return response.content


# def generate_post(length, language, tag):
#     prompt = get_prompt(length, language, tag)
#     response = llm.invoke(prompt)
#     return response.content


def generate_post(length, language, tag):
    prompt = f"""
You are a professional LinkedIn content writer.

Write a LinkedIn post with:
- Length: {length}
- Language: {language}
- Topic: {tag}

Keep it engaging, human-like and professional.
"""

    try:
        response = llm.invoke(prompt)

        # LangChain returns AIMessage
        if hasattr(response, "content"):
            return response.content

        return str(response)

    except Exception as e:
        return f"❌ LLM Error: {e}"

def get_prompt(length, language, tag):
    length_str = get_length_str(length)

    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    If Language is Hinglish then it means it is a mix of Hindi and English. 
    The script for the generated post should always be English.
    '''
    # prompt = prompt.format(post_topic=tag, post_length=length_str, post_language=language)

    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "4) Use the writing style as per the following examples."

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f'\n\n Example {i+1}: \n\n {post_text}'

        if i == 1: # Use max two samples
            break

    return prompt


if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health"))