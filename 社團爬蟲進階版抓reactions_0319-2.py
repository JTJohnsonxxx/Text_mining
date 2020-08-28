
import requests
import pandas as pd 
from dateutil.parser import parse


#在Facebook Graph API Exploer取得token以及粉絲專頁的ID

token = 'EAACEdEose0cBALkvu0fqQuLXBwD1F07xdzdZAvA2EY7qTC2jZBAwH4zwiAstlVpa079gLQUfEtMfZCviRk4TqqGraZC6PSLegEVjq5M26a1PeYl7mRTARsNhQUMNn5oXf5j4kQazlNoW30c3mixASZAjzDaSqg5cokIVfarcEwBekTZAvyDEoYLOO0belQ4qZCzlDQpYlbgcQZDZD'
fanpage_id = '247472339038741'

#建立一個空的list


information_list = []
#likes_list=[]
reaction_list=[]
id_list=[]

#目標頁面


res = requests.get('https://graph.facebook.com/v2.9/{}/feed?&access_token={}'.format(fanpage_id, token))
page = 1  
    

#API最多一次呼叫100筆資料，因此使用while迴圈去翻頁取得所有的文章


while 'paging' in res.json(): 
    for index, information in enumerate(res.json()['data']):
        print('正在爬取第{}頁，第{}篇文章'.format(page, index + 1))    
        #判斷是否為發文，是則開始蒐集PO文ID
        id_list.append(information['id'])
        if 'message' in information:
            res_reply= requests.get('https://graph.facebook.com/v2.9/{}/comments?order=reverse_chronological&filter=stream&limit=400&access_token={}'.format(information['id'], token))
            #print(res_reply.text)
            for i in res_reply.json()['data']:
                #res_likes=requests.get('https://graph.facebook.com/v2.9/{}/likes?&limit=1000&access_token={}'.format(i['id'], token))
                #if 'data' in res_likes.json():
                    #if res_likes.json()['data']:
                        #for likes in res_likes.json()['data']:
                            #likes_list.append([likes['id'],likes['name']])
                    #else:
                        #likes_list.append(['NA','NA'])
                information_list.append([id_list[-1],i['id'], i['from']['name'],i['from']['id'],i['message'], i['created_time']])
    

    if 'next' in res.json()['paging']:                
        res = requests.get(res.json()['paging']['next'])
        page += 1
    else:
        break



##for o in range(len(information_list)):
##    #print(o)
##    res3=requests.get('https://graph.facebook.com/v2.9/'+information_list[o][0] +'/comments?filter=stream&order=reverse_chronological&fields=reactions,message&access_token='+token)
##    #print(res3.json())
##    if o==0:
##        for re in res3.json()['data']:
##            if 'reactions' in re:
##                for re2 in re['reactions']['data']:
##                    idd=re2['id']
##                    name=re2['name']
##                    types = re2['type']
##                    reaction_list.append([information_list[o][0],re['id'],idd,name,types])
##    else:
##        if information_list[o][0]!=information_list[o-1][0]:
##            #print(information_list[o])
##            for re in res3.json()['data']:
##                if 'reactions' in re:
##                    for re2 in re['reactions']['data']:
##                        idd=re2['id']
##                        name=re2['name']
##                        types = re2['type']
##                        reaction_list.append([information_list[o][0],re['id'],idd,name,types])

print('爬取結束!')



import pandas as pd

df = pd.DataFrame(information_list, columns=['post_id','reply_ID','from_name', 'from_id', 'response_內容', 'response_時間'])
df.to_csv('105_adv_statistics_comments.csv', index=False, encoding='utf-8-sig')

#df2=pd.DataFrame(likes_list, columns=['likes_id', 'likes_name'])
#df2.to_csv('reply_likes.csv', index=False, encoding='utf-8-sig')


##df3=pd.DataFrame(reaction_list, columns=['post_id', 'comments_id', 'reaction_id','reaction_name','reaction_type'])
##df3.to_csv('reaction_list.csv', index=False, encoding='utf-8-sig')

