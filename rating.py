import pandas as pd
import requests
df_user = pd.read_csv('user_info_with_loved_tracks.csv')


df_apple_music = pd.read_csv('RecSetters_music.csv')

values=[]

for i in range(len(df_apple_music['tags'])):
    id = i % 5000 + 1  #
    values.append(id)

df_apple_music['id'] = values
values.clear()
for i in range(len(df_user['name'])):
    id = i + 1
    values.append(id)
df_user['id'] = values
id_to_trackname = {}

for idx, row in df_apple_music.iterrows():
    id_to_trackname[row['id']] = row['trackName']

rating=[]
id_lst=[]

index_count = {}

df_lst=[]
cnt = 0
for i in range(len(df_user)):
    start_marker = "'track_name': '"
    end_marker = "',"
    loved_tracks_str = df_user.loc[i, 'loved_tracks']
    
    track_names = []    
    size = len([pos for pos in range(len(loved_tracks_str)) if loved_tracks_str.startswith('track_name', pos)])
    start_pos = 0
    while True:
        start_pos = loved_tracks_str.find(start_marker, start_pos)
        if start_pos == -1:
            break
        start_pos += len(start_marker)
        end_pos = loved_tracks_str.find(end_marker, start_pos)
        if end_pos == -1:
            break
        track_name = loved_tracks_str[start_pos:end_pos]
        track_names.append(track_name)
        start_pos = end_pos + len(end_marker)

    for j, name in enumerate(track_names):       
        if name in df_apple_music['trackName'].values:
            index = df_apple_music.index[df_apple_music['trackName'] == name].tolist()[0]
            id_lst.append(i)
            id_lst.append(index)

            if index in index_count:
                index_count[index] += 1
            else:
                index_count[index] = 1

            df_lst.append(list(id_lst))
            id_lst.clear()
            cnt +=1
    if cnt < 5:
        df_lst = df_lst[:-cnt] if cnt != 0 else df_lst
    else: 
        df_lst
    print(index_count)
    cnt = 0


df_result = pd.DataFrame(df_lst, columns=['user_id', 'track_id'])




df_result.to_csv('interactions.csv', index=False)





# go through each user and check each track in their collection add one to both the track_cnt and user_cnt if it was used
# go through users and if the users has less than 5 interactions with tracks (do it by summing using the track id) remove the user
# then after each person has a min of 5 tracks they interact with
# go through tracks and if the track has less than 5 interactions with users (do it by summing using the track id) remove the track
# if either tracks or users had things deleted
# reload the dataset
