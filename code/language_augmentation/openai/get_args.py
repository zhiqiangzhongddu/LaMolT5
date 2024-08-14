import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--provider', help='The provider of LLM, could be openai (by default) or aoai', default='openai')
    parser.add_argument('-m', '--model', help='Which LLM to use', default='gpt-3.5-turbo-0125')
    args = parser.parse_args()

    return args