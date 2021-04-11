import vk_api
import matplotlib
# 6121396
# from config import token

session = vk_api.VkApi(token="a9c722ecb97db0ffcef87ce045eea75941129264e99e797f09c3373d2bb29106e3a891a70ce82083197eb")
vk = session.get_api()


def get_user_status(user_id):
    friends = session.method("friends.get", {"user_id": user_id})
    # status = session.method("status.get", {"user_id": user_id})
    # print(friends["items"])
    for friend in friends["items"]:
        user = session.method("users.get", {"user_ids": friend})
        try:
            status = session.method("status.get", {"user_id": friend})
        except:
            status = {"text": ""}

        if status["text"] == "":
            continue
        else:
            print(f"{user[0]['first_name']} {user[0]['last_name']} | {status['text']}")


def set_user_status():
    vk.status.set(text="New text for my status")


def send_message(user_id):
    session.method("messages.send", {
        "user_id": user_id,
        "message": "Отправлено из консоли",
        "random_id": 0
    })


def get_wal(idWall):
    wal = session.method("wall.get", {"owner_id": -idWall, 'count': 100})
    ids = []
    # print(wal)
    for item in wal['items']:
        ids.append(item["id"])
    return ids


def down_comments(id_post, idWall, id_comment, result_comments, ids, counts, countsLikes):
    count_comments = session.method("wall.getComments", {"owner_id": -idWall, "post_id": id_post, "comment_id":id_comment , "count": 1})["count"]

    i = 0
    if count_comments < 100:
        k = count_comments
    else:
        k = 100
    count_hundred = count_comments - count_comments % 100
    while i < count_comments:
        comments = session.method("wall.getComments",
                                  {"owner_id": -idWall, "post_id": id_post, 'offset': i, "comment_id": id_comment, 'need_likes': True,
                                   "count": k})
        if i != count_hundred:
            i += count_comments % 100
            k = count_comments % 100
        else:
            i += 100
        com = {}
        for comment in comments['items']:
            if 'from_id' in comment:
                com[comment["from_id"]] = com.get(comment["from_id"],  0) + 0
            if 'reply_to_user' in comment:
                com[comment["reply_to_user"]] = com.get(comment["reply_to_user"],  0) + 1
        for comment in comments['items']:
            try:
                result_comments.append(f"-----([id{comment['id']}]. Лайков:{comment['likes']['count']} Лтветов:{com[comment['from_id']]}). \n Текст комментария: {comment['text']}")
                ids.append(str(comment['id']))
                counts.append(com[comment['from_id']])
                countsLikes.append(comment['likes']['count'])
            except:
                continue


        return result_comments

def get_post(id_post, idWall, plt):
    count_comments = session.method("wall.getComments", {"owner_id": -idWall, "post_id": id_post, "count": 1})["count"]

    result_comments = []
    i = 0
    k=0
    if count_comments < 100:
        k = count_comments
    else:
        k = 100
    count_hundred = count_comments - count_comments % 100
    ids  = []
    countsComents = []
    countsLikes = []
    while i < count_comments:
        comments = session.method("wall.getComments", {"owner_id": -idWall, "post_id": id_post, 'offset': i, 'need_likes': True, "count": k})
        if i != count_hundred:
            i += count_comments % 100
            k = count_comments % 100
        else:
            i += 100
        for comment in comments['items']:
            ids.append(str(comment['id'])) # id коммента
            countsComents.append(comment['thread']['count']) # комментарии
            countsLikes.append(comment['likes']['count']) # комментарии
            try:
                result_comments.append(f"([id{comment['id']}]. Лайков {comment['likes']['count']}. Комментариев {comment['thread']['count']}). Текст комментария:- {comment['text']} ")
                down_comments(id_post, idWall, comment['id'], result_comments, ids, countsComents, countsLikes)
            except:
                continue

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(121)
    plt.xticks(rotation=90)
    plt.title('likes')
    ax2 = fig.add_subplot(122)
    ax.bar(ids, countsLikes)
    ax2.bar(ids, countsComents)
    plt.xticks(rotation=90)
    plt.title('comments')
    return result_comments
