import requests
import os
import requests.auth
import praw
from moviepy.editor import *
import sys
from time import sleep


CLIENT_ID = 'client_id.txt'
SECRET_KEY = 'secret_key.txt'
USERNAME = 'username.txt'
PASSWORD = 'password.txt'

sys.path.append("C:\\FFmpeg\\bin")


# reddit.com/prefs/apps
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=SECRET_KEY,
    username=USERNAME,
    password=PASSWORD,
    user_agent="test",

)

# Subreddit escolhido para baixar videos
subreddit = reddit.subreddit("FunnyAnimals")

count = 1

# Pega o link dos últimos posts com vídeo (últimos 50 posts)
for submission in subreddit.new(limit=50):

    if 'https://v.redd.it/' in submission.url:

        # Pegando url do vídeo e do audio
        video_url = submission.url + '/DASH_480.mp4'
        audio_url = submission.url + '/DASH_audio.mp4'

       # Nomeando vídeos/audios
        video_name = 'video'+str(count)+'.mp4'
        audio_name = 'audio'+str(count)+'.mp3'
        output_name = 'output'+str(count)+'.mp4'

        # Baixando video
        with open(video_name, 'wb') as f:
            g = requests.get(video_url, stream=True)
            f.write(g.content)

        # Baixando audio do video
        with open(audio_name, 'wb') as f:
            g = requests.get(audio_url, stream=True)
            f.write(g.content)

        # Juntando vídeo e audio
        os.system('ffmpeg -i '+video_name+' -i ' +
                  audio_name+' -c copy '+output_name)

        sleep(1)

        # renomeando arquivos
        os.system('rename "'+output_name+'" "'+submission.title+'.mp4"')

        sleep(2)

        # tirando as duas barras (\\) do texto para poder executar o comando no cmd
        comando_mover = 'C:\\Users\\Eliezer\\Desktop\\RedditVideoDownloader\\videos'
        comando_mover.replace('\\', 'x')
        comando_mover.replace("x", "")

        # movendo os outputs renomeados para a pasta videos
        os.system('move "'+submission.title + '.mp4" ' + comando_mover)

        print('move "'+submission.title +
              '.mp4" C:\\Users\Eliezer\\Desktop\\RedditVideoDownloader\\videos')
        print('move "'+submission.title + '.mp4" ' + comando_mover)

        print(count)
        count = count + 1
    else:
        print('Post Sem Vídeo')
