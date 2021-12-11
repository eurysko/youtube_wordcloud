# youtube_wordcloud

## 概要
YouTubeのコメントやチャットの特徴的なフレーズからフレーズクラウドを作成

## 使い方

### 1. YouTubeのコメントデータ・チャットデータの取得
- `get_comment.py`  
入力：YouTubeの動画のURL  
出力：動画のJSON形式のコメントデータ  
API_keyの書き換えが必要  

- `get_comment_pl.py`  
入力：YouTubeのプレイリストのURL、出力ファイルの最初のprefix  
出力：各動画のJSON形式のコメントデータ  
API keyの書き換えが必要  

- `get_chat.py`  
入力：YouTubeライブのアーカイブのURLを入力  
出力：動画のJSON形式のチャットデータ  

- `get_chat_pl.py`  
入力：YouTubeライブのアーカイブのプレイリストのURL、出力ファイルの最初のprefix  
出力：各動画のJSON形式のチャットデータ  

### 2.特徴フレーズの抽出
- `comment_tf.py`  
入力：JSON形式のコメントデータ  
出力："フレーズ tf値"の標準出力、リダイレクトでファイルへ出力  

- `chat_tf.py`  
入力：JSON形式のチャットデータ  
出力："フレーズ tf値"の標準出力、リダイレクトでファイルへ出力  

- `chat_idf.py`  
入力："フレーズ tf値"のファイルを含むディレクトリ  
出力："フレーズ idf値"の標準出力、リダイレクトでファイルへ出力  

### 3.フレーズクラウドの作成

Jupyter_Notebook形式
- `comment_wordcloud.ipynb`  
入力：tf値のファイル、マスクの画像ファイル  
出力：フレーズクラウド  
フォントのパスの書き換えが必要  

- `chat_wordcloud.ipynb`  
入力：tf値のファイル、idf値のファイル  
出力：フレーズクラウド  
フォントのパスの書き換えが必要  
