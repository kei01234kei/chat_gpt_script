from datetime import datetime
import json
import sys
import openai

CHARACTER_FILE_PATH = ''
CHARACTER = open(CHARACTER_FILE_PATH).read()


def add_conversation_to_prompt(role: str, utterance: str, prompt: list) -> list:
    prompt.append(
        {'role': role, 'content': utterance},
    )
    return prompt


def create_prompt(role_to_specify_character: str, character: str, user_prompt: str) -> list:
    prompt = [
        {'role': role_to_specify_character, 'content': character},
        # {'role': role_to_specify_character, 'content': ''},
        {'role': 'user', 'content': user_prompt},
    ]
    return prompt


def request_to_chat_gpt(prompt: list) -> str:
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=prompt,
    )
    return completion['choices'][0]['message']['content']


def interact_with_chat_gpt(chat_gpt_role: str) -> list:
    user_prompt = 'オーナー: ' + input('オーナー: ')
    prompt = create_prompt(chat_gpt_role, CHARACTER, user_prompt)
    while True:
        romi_prompt = request_to_chat_gpt(prompt)
        print(romi_prompt)
        prompt = add_conversation_to_prompt('assistant', romi_prompt, prompt)
        user_prompt = 'オーナー: ' + input('オーナー: ')
        while user_prompt == 'オーナー: prompt':
            print(prompt)
            user_prompt = 'オーナー: ' + input('オーナー: ')
        if user_prompt == 'オーナー: exit':
            break
        prompt = add_conversation_to_prompt('user', user_prompt, prompt)
    return prompt


def save_json_file(file_name: str, text: str):
    with open(file=f'{file_name}.json', mode='w') as f:
        f.write(text)


def read_prompt(path: str):
    ...


def main():
    if sys.argv[1] == 'system' or sys.argv[1] == 'user':
        text = json.dumps(interact_with_chat_gpt(sys.argv[1]), indent=2, ensure_ascii=False)
        file_name = str(datetime.now())
        save_json_file(file_name, text)
        print(text)
        exit(0)
    elif sys.argv[1] == 'prompt':
        with open(sys.argv[2]):
            ...
        ...
    exit(1)


if __name__ == '__main__':
    main()
