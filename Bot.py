import tweepy,time,json,random
import perfil_foto as pfp

auth = tweepy.OAuthHandler('XXXX','XXX')
auth.set_access_token('XXXX','XXXX')
carinhas = ('(◕‿◕✿)','(◠‿◠✿)','(◠﹏◠✿)','（＊＾Ｕ＾）','人（≧Ｖ≦＊）/','ʕ·ᴥ·ʔ','＼（＾○＾）','✿◕ ‿ ◕✿','(◡‿◡✿)','(*^ -^*)','≖‿≖','(￣ｰ￣)','╰(◡‿◡✿╰)','＼(*^▽^*)/','(｡◕‿◕｡)','(*￣▽￣*)','◑﹏◐','(*^▽^*)','(✿◡‿◡)','~(￣▽￣)~','*┏ (゜ω゜)=☞','~(=^‥^)ノ','ヾ(≧▽≦*)o', '(/≧▽≦)/', '( *︾▽︾)', '( •̀ ω •́ )y', '( •̀ .̫ •́ )✧')
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

dict = {}

TWITTER_USER = "XXXX" #informe o @nome do perfil do twitter(sem o "@")


"""
A bot made to study the twitter api, it repeats the sentences sent by some user in their last post;
editing the sentence by pulling some words from the dictionary into words.json, thus sending the modified message along
to an image in the "imagens" folder numbered by numbers and in .jpg format and also some random caracteres from the variable
carinhas.

It has commands to change the bot profile set in the auth variable and also to change its name.
!profile
!name

PT/BR

"""




with open('palavras.json','r',encoding="utf-8") as f: #Abre o dicionario e coloca todas os valores e keys na variavel dict
   dict = json.load(f)


def ultima_postagem_por(post): #Salva a ID da ultima postagem que o bot respondeu para evitar que ele envie mensagens repetidas no mesmo post.
    print('Last post ID has saved')
    with open('ultimo_post.txt','w') as posz:
         posz.write(post) 
         posz.close()

def comandos(textostr,post,nome):#Função dos comandos, é chamada quando algum comando é encontrado na função iniciar
        print('Function Commands has triggered')
        rr = random.randrange(0,28)
        if "!profile" in textostr:
            print('!profile command triggered')
            entities = post._json['entities']
            if 'media' in entities:
                print('photo found')
                foto = "".join(post._json['entities']['media'][0]['media_url_https'])
                pfp.baixar_foto(url=foto)
                time.sleep(5)
                api.update_profile_image(filename="foto.jpg")
                api.update_status(status=f'@{nome} You change my photo! {carinhas[rr]}）',in_reply_to_status_id=post.id_str)
                ultima_postagem_por(post.id_str)
                return
            else:
                print('photo has not found')     
                ultima_postagem_por(post.id_str)
                api.update_with_media(status=f'@{nome} I didnt find any photo, you must upload it with the desired photo or gif and type "!profile" in the text field as in the screenshot below {carinhas[rr]}:',in_reply_to_status_id=post.id_str, filename="perfil_help.png")
                return
        elif "!name" in textostr:
            print('!name command triggered')
            novonick = [nick for nick in textostr]
            novonick.remove('!name')
                

            nomenovo = " ".join(novonick)
            if len(nomenovo) > 48: #Usando len() para ver se o tamanho do nome informado pelo o usuário é maior do que o limite de nome do twitter
                print('Unable to change name because it is too big')
                api.update_status(status=f'@{nome} Unable to change name because it is too big  ({len(nomenovo)})! {carinhas[rr]}',in_reply_to_status_id=post.id_str)
                ultima_postagem_por(post.id_str)

                return
            api.update_profile(name=nomenovo)
            print('New username:', " ".join(textostr))
            ultima_postagem_por(post.id_str)
            api.update_status(status=f'@{nome} the name has changed {carinhas[rr]}',in_reply_to_status_id=post.id_str)

        elif "!link" in textostr:
            try:
                status = api.get_status(post.in_reply_to_status_id)
            except Exception as e:
                ultima_postagem_por(post.id_str)
                print("Error log: " + str(e))
    
                return

            entities = status._json['extended_entities']
            if 'media' in entities:
                print('media found')
                ur = entities['media'][0]['video_info']['variants'][0]["content_type"]
                ur3 = entities['media'][0]['video_info']['variants'][0]["url"] 
                try:
                    ur1 = entities['media'][0]['video_info']['variants'][1]["content_type"]
                    ur4 = entities['media'][0]['video_info']['variants'][1]["url"]
                    print("link full found")
                    
                
                except:
                    print("link found[ur, ur3]")
                    api.update_status(status=f'@{nome} Download the video below in x-mpegURL or mp4:\n{ur}: {ur3}',in_reply_to_status_id=post.id_str)
                    ultima_postagem_por(post.id_str)
                    return
                
                
                api.update_status(status=f'@{nome} Download the video below in x-mpegURL or mp4:\n{ur}: {ur3}\n{ur1}: {ur4}',in_reply_to_status_id=post.id_str)
                ultima_postagem_por(post.id_str)
            else:
                api.update_status(status=f'@{nome} Not found',in_reply_to_status_id=post.id_str)
                print("link not found")
                ultima_postagem_por(post.id_str)



def iniciar(nome):#Verifica o ultimo post do usuario
    usuario = api.get_user(nome).id
    post = api.user_timeline(user_id=usuario,page=1,count=1,tweet_mode="extended")[0]
    #print(post._json)
    with open('ultimo_post.txt','r') as ultimopost1:#Verifica se o post já foi respondido pelo o bot
        ultimopost = ultimopost1.read()
        ultimopost1.close()
    if "retweeted_status" in post._json:#Verifica se é RT
        return
    elif post.id_str in ultimopost:
        return 
    
    textostr = str(post.full_text).lower()
    cacador = textostr.find("@")#a procura de @ para evitar que a mensagem seja enviada mencionando alguém
    if cacador == 0:# Se cacador == 0 == mentions found
      print("Mentions found")
      if "!profile" in textostr:
          comandos(textostr,post,api.get_user(nome).screen_name)
          return

      texto = textostr.split()
      for arroba in texto:
          if "@" in arroba[0]:
              texto.remove(f"{arroba}") 

      if "@" in texto[0]:
          texto.remove(f"{texto[0]}")

      if "!name" in textostr:
          print('!name')
          comandos(texto,post,api.get_user(nome).screen_name)
          return

      if "!link" in textostr:
          comandos(texto,post,api.get_user(nome).screen_name)
          return

      tradutor(frase=" ".join(texto),post_id=post.id_str,usuario=api.get_user(nome).screen_name) 
    
    else:
        print("@ not found")
        if "!profile" in textostr:
          print('!profile trigger')
          comandos(textostr,post,api.get_user(nome).screen_name)
          return
        
        elif "!name" in textostr:
          print('!name trigger')
          comandos(str(textostr),post,api.get_user(nome).screen_name)
          return
        
        elif "!link" in textostr:
          comandos(textostr,post,api.get_user(nome).screen_name)
          return
        
        else:
          print(textostr)
          tradutor(frase=textostr,post_id=post.id_str,usuario=api.get_user(nome).screen_name)


def tradutor(frase,post_id,usuario):#Essa é a função que envia a mensagem, ela recebe a frase e usa o metodo split() para deixar a frase separada em palavras e assim alterando para algo do dicionario
    frase = frase.split()
    frase_sep = []
    for palavra in frase:
        frase_sep.append(dict.get(palavra, palavra))
    correç = " ".join(frase_sep)
    part = correç.replace('mete','meti').replace('que',"qui").replace('😈','😇').replace('n','ny').replace('lha','lhya').replace('mos','myos')

    choice = random.randrange(0, 28)#Escolhe aleatoriamente uma das 27 carinhas
    imgs = random.randrange(0,1)

    api.update_with_media(status=f"@{usuario} {part[0:270]} {carinhas[choice]}", in_reply_to_status_id=post_id, filename=f"imagens\{imgs}.jpg")
    print("Message: ", part[0:270])
    ultima_postagem_por(post_id)
    api.create_favorite(post_id)
    return



while True:#Loop checa novas mensagens de um X usuario a cada 10 segundos
    iniciar(TWITTER_USER)
    time.sleep(10)