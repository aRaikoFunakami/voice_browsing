import os
import sys
import logging
import json
import openai

# load config
def load_config():
    args = sys.argv
    config_file = os.path.dirname(__file__) + "/config.json" if len(args) <=1 else args[1]
    logging.info(config_file)
    with open(config_file, 'r') as file:
        config = json.load(file)
    return {
            "openai_api_key": config['openai_api_key'],
            "persist_dir": os.path.dirname(__file__) + '/'+ config['persist_directory']
        }
    
def init_openai_key():
    if openai.api_key is None:
        config = load_config()
        openai.api_key = config["openai_api_key"]

def remove_leading_whitespace(text):
    lines = text.split('\n')  # 文字列を改行で分割してリストに変換
    cleaned_lines = [line.lstrip() for line in lines]  # 各行の先頭の空白やタブを取り除く
    cleaned_text = '\n'.join(cleaned_lines)  # リストを改行で結合して文字列に変換
    return cleaned_text

def selenum_command_by_gpt(txt):
    # 入力を説明したプロンプト
    prompt = '''
    あなたはSeleniumを利用してChromeを操作するプログラムを開発しているプログラマ
    以下の制約条件と模範回答リストと入力文をもとにSeleniumの関数を呼び出す単純なPythonコードを作成せよ。
    # 制約条件:
    Selenumのバージョンは4.3.0以上
    模範回答リストを優先する
    模範回答リストの回答内容は変更して回答してはならない open_youtube_tv() は "driver.open_youtube_tv()" ではなく "open_youtube_tv()" で回答する
    すでにSeleniumはChromeを起動しており、driver変数でブラウザを操作できる
    入力文から適切なSelenumの関数の作成が難しければ "#対応する処理がない" というコメント行のみ作成せよ。
    名詞のみの入力文の場合は"Xのリンクをクリック"と読み替える
    # 模範回答リスト:
    PC用のブラウジングモードに戻る:'open_pc_site()'
    テレビ用のYouTubeサイトを開く:'open_youtube_tv()'
    YouTubeサイトを開く:'driver.get("https://www.youtube.com/")'
    Xを開く:'driver.get(X)'
    Xのリンクをクリック:'link_click(X)'
    Xのリンク:'link_click(X)'
    名詞Xのみの場合:'link_click(X)'
    '''
    prompt = prompt + f'''
    # 入力文:
    {txt}
    '''
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.2,
        max_tokens=150
    )
    command = response.choices[0].text.strip()
    return remove_leading_whitespace(command)

def description_by_gpt(cmd):
    # 入力を説明したプロンプト
    prompt = f'''
    以下の制約条件と入力文をもと python プログラムの動作をエンドユーザにわかりやすく簡潔に20文字程度で説明せよ
    # 制約条件:
    例外処理など制御の説明は行わない
    プログラムを実行した場合のアウトプットを説明する
    制約条件の内容は説明に含めない
    Selenumは説明に含めない
    # 入力文:
    {cmd}
    '''
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.4,
        max_tokens=150
    )
    description = response.choices[0].text.strip()
    return description

def generate_selenum_command_by_gpt(input):
    init_openai_key()
    selenium_command = selenum_command_by_gpt(input)
    description = description_by_gpt(selenium_command)
    return {"command": selenium_command, "description": description}
    
def main():
    # Question
    query = "テレビ用のYouTubeサイトを開く"
    response = generate_selenum_command_by_gpt(query)
    print(response)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s:%(name)s - %(message)s")    
    main()