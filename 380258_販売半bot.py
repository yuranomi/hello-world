# -*- coding: utf-8 -*-
from linepy import *
from datetime import datetime
import time,random,sys,json,codecs,threading,glob,sys
import re,string,datetime,os
import os.path,sys,urllib,shutil,subprocess


cl = LINE()
cl.log("Auth Token : " + str(cl.authToken))

print (u"login success")
oepoll = OEPoll(cl)

admins = [cl.getProfile().mid]

helpMessage ="""コマンド一覧
(βがついているコマンドはテスト中又は修正中のため使えない可能性があります。)
[gid]対象のIDを表示します。
[mid]自分のmidを送ります。
[おみくじ]おみくじを引きます
[参加グループid]参加しているグループidを全て表示します。
[参加グル数]参加しているグループ数を確認します。
[全招待拒否]グループ招待を拒否します。
[連絡先:オン]連絡先を送ったあと、情報を送るようにします。
[連絡先:オフ]連絡先を送ったあと、情報を送らないようにします。
[自動参加:オン]グループに自動で参加するようにします。(β)
[自動参加:オフ]自動でグループに参加しないようにします。
[招待拒否：人数]「人数」以下のグループ招待は自動で拒否します。
[招待拒否：オフ]招待を全て許可します。
[強制自動退出:オン]強制を自動で抜けます。
[強制自動退出:オフ]強制を自動で抜けないようにします。
[自動追加:オン]友達を自動で追加します。
[自動追加:オフ]自動追加をオフにします。
[自動追加メッセージ変更:テキスト]自動追加する際のメッセージを変更します。
[自動追加メッセージ確認]自動追加する際のメッセージを確認します。
[コメント:オン]自動コメントをオンにします。(β)
[コメント:オフ]自動コメントをオフにします。
[コメント確認]自動コメントを確認します。
[コメント変更:テキスト]自動コメントのメッセージを変更します。
[コメントブラックリスト追加]自動コメントをしない人を設定します。
[コメントブラックリスト削除]コメントブラックリストから削除します。
[コメントブラックリスト確認]コメントブラックリストを確認します。
[ブラックリスト登録]登録されたユーザーは招待できなくなります。グループ内にすでにいる場合は、追い出しコマンドで退会させることができます。
[ブラックリスト削除]ブラックリストから削除します。
[ブラックリスト確認]ブラックリストを確認します。
[追い出し]グループからブラックリストユーザーを追い出します。
[speed]処理速度をはかります。
[設定確認]：botの設定を確認します。

-以下のコマンドはグループでのみ使用できます。-
[gurl:on]招待URL許可
[gurl:off]招待URL拒否
[gurl:get]グループURLを発行します。(グループURLがブロックされている場合、許可して発行します)
[既読ポイントセット]既読ポイントをセットします。
[既読確認]既読した人を確認します。(β)
[既読ポイント破棄]設定した既読ポイントをリセットします。
[midk：mid]指定したmidのユーザーをグループから蹴ります。
[kick:mid]　　〃
[bladd:メンション]メンションでブラックリストに追加します。
[bldel:メンション]メンションでブラックリストから削除します。
[メンバーチェック]グループ内にいるブラックリストユーザーのmidを出します。
[ginfo]グループ情報表示
[全キャンセル]グループで招待中のユーザーを全てキャンセルします。
[単蹴り]蹴ります（適当）
[gname:テキスト]グループ名を変更します。
[gurl取得:gid]自分の参加しているグループIDから招待URLを発行します。
[MK:メンション]グループからメンションしたユーザーを蹴ります。複数可
[NK：名前]グループから指定した名前のユーザーを蹴ります。複数当てはまる場合は、当てはまったユーザー全員蹴ります。
[STK:ステメ]指定したステータスメッセージを含むユーザーを蹴ります。
"""

me = cl.getProfile().mid

omikuzi = ["大吉","中吉","小吉","末吉","大凶","凶"]


wait = {
    'contact':True,
    'autoJoin':False,
    'autoCancel':{"on":True,"members":1},
    'leaveRoom':True,
    'timeline':True,
    'autoAdd':True,
    'message':"",
    "comment":"コメント",
    "commentOn":False,
    "commentBlack":{},
    "wblack":False,
    "dblack":False,
    "cName":"",
    "blacklist":{},
    "wblacklist":False,
    "dblacklist":False,
    'readMember':{},
    'readPoint':{}
}
st2=open("st2.json","w")
st2.write("{}")
st2.close()
f=codecs.open('st2.json','r','utf-8')
wait["commentBlack"] = json.load(f)

def Cmd(string, commands):
    tex = [""]
    for texX in tex:
        for command in commands:
            if string ==texX + command:
                return True
    return False

def NOTIFIED_ADD_CONTACT(op):
    try:
        if wait["autoAdd"] == True:
            cl.findAndAddContactsByMid(op.param1)
            if (wait["message"] in [""," ","\n",None]):
                pass
            else:
                cl.sendMessage(op.param1,str(wait["message"]))
    except Exception as e:
        print(e)
        
def NOTIFIED_INVITE_INTO_GROUP(op):
    try:
        if me in op.param3:
            G = cl.getGroup(op.param1)
            if wait["autoJoin"] == True:
                if wait["autoCancel"]["on"] == True:
                    if len(G.members) <= wait["autoCancel"]["members"]:
                        cl.rejectGroupInvitation(op.param1)
                    else:
                        cl.acceptGroupInvitation(op.param1)
                else:
                    cl.acceptGroupInvitation(op.param1)
            elif wait["autoCancel"]["on"] == True:
                if len(G.members) <= wait["autoCancel"]["members"]:
                    cl.rejectGroupInvitation(op.param1)
        else:
            Inviter = op.param3.replace("",',')
            InviterX = Inviter.split(",")
            matched_list = []
            for tag in wait["blacklist"]:
                matched_list+=filter(lambda str: str == tag, InviterX)
            if matched_list == []:
                pass
            else:
                cl.cancelGroupInvitation(op.param1, matched_list)
    except Exception as e:
        print(e)
       
def NOTIFIED_KICKOUT_FROM_GROUP(op):
    try:
        if mid in op.param3:
            wait["blacklist"][op.param2] = True
    except Exception as e:
        print(e)

def NOTIFIED_INVITE_INTO_ROOM(op):
    try:
        if wait["leaveRoom"] == True:
                cl.leaveRoom(op.param1)
    except Exception as e:
        print(e)
def NOTIFIED_LEAVE_ROOM(op):
    try:
        if wait["leaveRoom"] == True:
                cl.leaveRoom(op.param1)
    except Exception as e:
        print(e)
def RECEIVE_MESSAGE(op):
    try:
        msg = op.message
        if msg.toType == 0:
            msg.to = msg._from
            if msg._from == "u356f45dcbdd5261625061f9f26d2004a":
                if "join:" in msg.text:
                    list_ = msg.text.split(":")
                    try:
                        cl.acceptGroupInvitationByTicket(list_[1],list_[2])
                        G = cl.getGroup(list_[1])
                        G.preventedJoinByTicket = True
                        cl.updateGroup(G)
                    except:
                        cl.sendMessage(msg.to,"error")
        if msg.toType == 1:
            if wait["leaveRoom"] == True:
                cl.leaveRoom(msg.to)
        if msg.contentType == 16:
            url = msg.contentMetadata["postEndUrl"]
            cl.like(url[25:58], url[66:], likeType=1001)
    except Exception as e:
        print(e)
def SEND_MESSAGE(op):
    try:
        msg = op.message
        if msg.contentType == 16:
            url = msg.contentMetadata["postEndUrl"]
            cl.likePost(url[25:58], url[66:], likeType=1001)
            print(url[25:58])
            print(url[66:])
        
        if msg.contentType == 13:
            if wait["wblack"] == True:
                if msg.contentMetadata["mid"] in wait["commentBlack"]:
                    cl.sendMessage(msg.to,"すでにブラックリストに入っています。")
                    wait["wblack"] = False
                else:
                    wait["commentBlack"][msg.contentMetadata["mid"]] = True
                    wait["wblack"] = False
                    cl.sendMessage(msg.to,"コメントしないようにしました。")
                    f=codecs.open('st2.json','w','utf-8')
                    json.dump(wait["commentBlack"], f, sort_keys=True, indent=4,ensure_ascii=False)
            elif wait["dblack"] == True:
                if msg.contentMetadata["mid"] in wait["commentBlack"]:
                    del wait["commentBlack"][msg.contentMetadata["mid"]]
                    cl.sendMessage(msg.to,"ブラックリストから削除しました。")
                    wait["dblack"] = False
                    f=codecs.open('st2.json','w','utf-8')
                    json.dump(wait["commentBlack"], f, sort_keys=True, indent=4,ensure_ascii=False)
                else:
                    wait["dblack"] = False
                    cl.sendMessage(msg.to,"ブラックリストに入っていません。")
            elif wait["wblacklist"] == True:
                if msg.contentMetadata["mid"] in wait["blacklist"]:
                    cl.sendMessage(msg.to,"すでにブラックリストに入っています。")
                    wait["wblacklist"] = False
                else:
                    wait["blacklist"][msg.contentMetadata["mid"]] = True
                    wait["wblacklist"] = False
                    cl.sendMessage(msg.to,"ブラックリストに追加しました。")
                    f=codecs.open('st2__b.json','w','utf-8')
                    json.dump(wait["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)
            elif wait["dblacklist"] == True:
                if msg.contentMetadata["mid"] in wait["blacklist"]:
                    del wait["blacklist"][msg.contentMetadata["mid"]]
                    cl.sendMessage(msg.to,"ブラックリストから削除しました。")
                    wait["dblacklist"] = False
                    f=codecs.open('st2__b.json','w','utf-8')
                    json.dump(wait["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)
                else:
                    wait["dblacklist"] = False
                    cl.sendMessage(msg.to,"ブラックリストに入っていません。")
            elif wait["contact"] == True:
                msg.contentType = 0
                cl.sendMessage(msg.to,msg.contentMetadata["mid"])
                if 'displayName' in msg.contentMetadata:
                    contact = cl.getContact(msg.contentMetadata["mid"])
                    try:
                        cu = cl.channel.getCover(msg.contentMetadata["mid"])
                    except:
                        cu = ""
                    cl.sendMessage(msg.to,"[displayName]:\n" + msg.contentMetadata["displayName"] + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[statusMessage]:\n" + contact.statusMessage + "\n[pictureStatus]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[coverURL]:\n" + str(cu))
                else:
                    contact = cl.getContact(msg.contentMetadata["mid"])
                    try:
                        cu = cl.channel.getCover(msg.contentMetadata["mid"])
                    except:
                        cu = ""
                    cl.sendMessage(msg.to,"[displayName]:\n" + contact.displayName + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[statusMessage]:\n" + contact.statusMessage + "\n[pictureStatus]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[coverURL]:\n" + str(cu))
        
        elif msg.text is None:
            return
        elif msg.text in ["help","ヘルプ","へるぷ"]:
             cl.sendMessage(msg.to,helpMessage)
        elif Cmd(msg.text,["now","NOW"]):
            cl.sendMessage(msg.to,datetime.datetime.today().strftime('%Y年%m月%d日%H:%M %S秒'))
        elif "おみくじ" == msg.text:
            c = random.choice(omikuzi)
            cl.sendMessage(msg.to,c)
        elif ("gname:" in msg.text):
            if msg.toType == 2:
                group = cl.getGroup(msg.to)
                group.name = msg.text.replace("gname:","")
                cl.updateGroup(group)
            else:
                cl.sendMessage(msg.to,"グループ以外では使用できません。")
        elif "kick:" in msg.text:
            midd = msg.text.replace("kick:","")
            cl.kickoutFromGroup(msg.to,[midd])
        elif "召喚:" in msg.text:
            midd = msg.text.replace("召喚:","")
            cl.findAndAddContactsByMid(midd)
            cl.inviteIntoGroup(msg.to,[midd])
        elif Cmd(msg.text,["me"]):
            MID = cl.getContact(msg._from).mid
            M = Message()
            M.to = msg.to
            M._from = MID
            M.contentType =13
            M.contentMetadata = {"mid":MID}
            cl.sendMessage(M)
        elif msg.text in ["愛のプレゼント"]:
            msg.contentType = 9
            msg.contentMetadata={'PRDID': '3b92ccf5-54d3-4765-848f-c9ffdc1da020',
                                'PRDTYPE': 'THEME',
                                'MSGTPL': '5'}
            msg.text = None
            cl.sendMessage(msg)
        elif msg.text in ["全キャンセル","エクスプロージョン！","エクスプロージョン!"]:
            if msg.toType == 2:
                group = cl.getGroup(msg.to)
                if group.invitee is not None:
                    gInviMids = [contact.mid for contact in group.invitee]
                    cl.cancelGroupInvitation(msg.to, gInviMids)
                else:
                    cl.sendMessage(msg.to,"招待中の人はいません。")
            else:
                cl.sendMessage(msg.to,"グループ以外では使用できません。")
        #elif "gurl" == msg.text:
            #print cl.getGroup(msg.to)
            ##cl.sendMessage(msg)
        elif msg.text in ["gurl:on"]:
            if msg.toType == 2:
                group = cl.getGroup(msg.to)
                group.preventedJoinByTicket = False
                cl.updateGroup(group)
                cl.sendMessage(msg.to,"URLを許可しました。")
            else:
                cl.sendMessage(msg.to,"グループ以外では使用できません。")
        elif msg.text in ["gurl:off"]:
            if msg.toType == 2:
                group = cl.getGroup(msg.to)
                group.preventedJoinByTicket = True
                cl.updateGroup(group)
                cl.sendMessage(msg.to,"URLを拒否しました。")
            else:
                cl.sendMessage(msg.to,"グループ以外では使用できません。")
        elif msg.text == "ginfo":
            if msg.toType == 2:
                ginfo = cl.getGroup(msg.to)
                try:
                    gCreator = ginfo.creator.displayName
                except:
                    gCreator = "Error"
                    if ginfo.invitee is None:
                        sinvitee = "0"
                    else:
                        sinvitee = str(len(ginfo.invitee))
                    if ginfo.preventedJoinByTicket == True:
                        u = "拒否"
                    else:
                        u = "許可"
                    cl.sendMessage(msg.to,"[名前]\n" + str(ginfo.name) + "\n[gid]\n" + msg.to + "\n[グループの作成者]\n" + gCreator + "\n[グループアイコン]\nhttp://dl.profile.line.naver.jp/" + ginfo.pictureStatus + "\nメンバー:" + str(len(ginfo.members)) + "人\n招待中:" + sinvitee + "人\n招待URL:" + u + "中です。")
                else:
                    cl.sendMessage(msg.to,"グループ以外では使用できません")
        elif "gid" == msg.text:
            cl.sendMessage(msg.to,msg.to)
        elif "mid" == msg.text:
            cl.sendMessage(msg.to,msg._from)
        elif "り" == msg.text:
            msg.contentType = 7
            msg.text = None
            msg.contentMetadata = {
                                 "STKID": "12623182_",
                                 "STKPKGID": "2",
                                  }
            cl.sendMessage(msg)
        elif "ダメ" == msg.text:
            msg.contentType = 7
            msg.text = None
            msg.contentMetadata = {
                                 "STKID": "12623183_",
                                 "STKPKGID": "2",
                                  }
            cl.sendMessage(msg)
        elif "少女祈祷中" == msg.text:
            msg.contentType = 7
            msg.text = None
            msg.contentMetadata = {
                                 "STKID": "12623191_",
                                 "STKPKGID": "2",
                                  }
            cl.sendMessage(msg)
        elif "TL:" in msg.text:
            tl_text = msg.text.replace("TL:","")
            cl.sendMessage(msg.to,"line://home/post?userMid="+me+"&postId="+cl.new_post(tl_text)["result"]["post"]["postInfo"]["postId"])
        elif "我が名は" in msg.text:
            string = msg.text.replace("我が名は","")
            if len(string.decode('utf-8')) <= 20:
                profile = cl.getProfile()
                profile.displayName = string
                cl.updateProfile(profile)
                cl.sendMessage(msg.to,"名前を" + string + "に変更しました。")
        elif "mtoc:" in msg.text:
            mmid = msg.text.replace("mtoc:","")
            msg.contentType = 13
            msg.contentMetadata = {"mid":mmid}
            cl.sendMessage(msg)
        elif msg.text in ["連絡先:オン","連絡先:on","連絡先：オン","顯示：開"]:
            if wait["contact"] == True:
                cl.sendMessage(msg.to,"既にオンです。")
            else:
                wait["contact"] = True
                cl.sendMessage(msg.to,"オンにしました。")
        elif msg.text in ["連絡先:オフ","連絡先:off","連絡先：オフ","顯示：關"]:
            if wait["contact"] == False:
                cl.sendMessage(msg.to,"既にオフです。")
            else:
                wait["contact"] = False
                cl.sendMessage(msg.to,"オフにしました。")
        elif msg.text in ["自動参加:オン","自動参加：オン","自動参加:on","自動參加：開"]:
            if wait["autoJoin"] == True:
                cl.sendMessage(msg.to,"既にオンです。")
            else:
                wait["autoJoin"] = True
                cl.sendMessage(msg.to,"オンにしました。")
        elif msg.text in ["自動参加:オフ","自動参加：オフ","自動参加:on","自動參加：關"]:
            if wait["autoJoin"] == False:
                cl.sendMessage(msg.to,"既にオフです。")
            else:
                wait["autoJoin"] = False
                cl.sendMessage(msg.to,"オフにしました。")

        elif "招待拒否:" in msg.text:
            strnum = msg.text.replace("招待拒否:","")
            if strnum == "オフ":
                wait["autoCancel"]["on"] = False
                cl.sendMessage(msg.to,"招待拒否をオフしました。\nオンにするときは人数を指定して送信してください。")
            else:
                num =  int(strnum)
                wait["autoCancel"]["on"] = True
                cl.sendMessage(msg.to,strnum + "人以下のグループは自動で招待拒否するようにしました。")
        elif msg.text in ["強制自動退出:オン","強制自動退出：オン","強制自動退出:on"]:
            if wait["leaveRoom"] == True:
                cl.sendMessage(msg.to,"既にオンです。")
            else:
                wait["leaveRoom"] = True
                cl.sendMessage(msg.to,"オンにしました。")
        elif msg.text in ["強制自動退出:オフ","強制自動退出：オフ","強制自動退出:off"]:
            if wait["leaveRoom"] == False:
                cl.sendMessage(msg.to,"既にオフです。")
            else:
                wait["leaveRoom"] = False
                cl.sendMessage(msg.to,"オフにしました。")
        elif msg.text in ["共有:オン","共有：オン","共有:on"]:
            if wait["timeline"] == True:
                cl.sendMessage(msg.to,"既にオンです。")
            else:
                wait["timeline"] = True
                cl.sendMessage(msg.to,"オンにしました。")
        elif msg.text in ["共有:オフ","共有：オフ","共有:off"]:
            if wait["timeline"] == False:
                cl.sendMessage(msg.to,"既にオフです。")
            else:
                wait["timeline"] = False
                cl.sendMessage(msg.to,"オフにしました。")
        elif "設定確認" == msg.text:
            md = ""
            if wait["contact"] == True: md+="連絡先:オン\n"
            else: md+="連絡先→オフ\n"
            if wait["autoJoin"] == True: md+="自動参加:オン\n"
            else: md +="自動参加→オフ\n"
            if wait["autoCancel"]["on"] == True:md+="招待拒否:" + str(wait["autoCancel"]["members"]) + "\n"
            else: md+= "招待拒否:オフ\n"
            if wait["leaveRoom"] == True: md+="強制自動退出:オン\n"
            else: md+="強制自動退出:オフ\n"
            if wait["timeline"] == True: md+="共有:オン\n"
            else:md+="共有:オフ\n"
            if wait["autoAdd"] == True: md+="自動追加:オン\n"
            else:md+="自動追加:オフ\n"
            if wait["commentOn"] == True: md+="自動コメント:オン"
            else:md+="自動コメント:オフ"
            cl.sendMessage(msg.to,md)
        elif "アルバム取得:" in msg.text:
            gid = msg.text.replace("アルバム取得:","")
            album = cl.getAlbum(gid)
            if album["result"]["items"] == []:
                cl.sendMessage(msg.to,"アルバムはありません。")
            else:
                mg = "以下が対象のアルバムです。"
                for y in album["result"]["items"]:
                    if "photoCount" in y:
                        mg += str(y["title"]) + ":" + str(y["photoCount"]) + "枚\n"
                    else:
                        mg += str(y["title"]) + ":0枚\n"
                cl.sendMessage(msg.to,mg)
        elif msg.text in ["参加グループid"]:
            gid = cl.getGroupIdsJoined()
            g = ""
            for i in gid:
                g += "[%s]:%s\n" % (cl.getGroup(i).name,i)
            cl.sendMessage(msg.to,g)
        elif "参加グル数" == msg.text:
            cl.sendMessage(msg.to,str(len(cl.getGroupIdsJoined())))
        elif msg.text in ["全招待拒否"]:
            gid = cl.getGroupIdsInvited()
            for i in gid:
                cl.rejectGroupInvitation(i)
            cl.sendMessage(msg.to,"すべての招待を拒否しました。")
        elif "アルバム削除:" in msg.text:
            gid = msg.text.replace("アルバム削除:","")
            albums = cl.getAlbum(gid)["result"]["items"]
            i = 0
            if albums != []:
                for album in albums:
                    cl.deleteAlbum(gid,album["id"])
                    i += 1
            cl.sendMessage(msg.to,str(i) + "件のアルバムを削除しました。")
        elif msg.text in ["自動追加:オン","自動追加：オン","自動追加:on"]:
            if wait["autoAdd"] == True:
                cl.sendMessage(msg.to,"既にオンです。")
            else:
                wait["autoAdd"] = True
                cl.sendMessage(msg.to,"オンにしました。")
        elif msg.text in ["自動追加:オフ","自動追加：オフ","自動追加:off"]:
            if wait["autoAdd"] == False:
                cl.sendMessage(msg.to,"既にオフです。")
            else:
                wait["autoAdd"] = False
                cl.sendMessage(msg.to,"オフにしました。")
        elif "自動追加メッセージ変更:" in msg.text:
            wait["message"] = msg.text.replace("自動追加メッセージ変更:","")
            cl.sendMessage(msg.to,"メッセージを変更しました。")
        elif msg.text in ["自動追加メッセージ確認"]:
            cl.sendMessage(msg.to,"自動追加メッセージは以下のように設定されています。\n\n" + wait["message"])
        elif "コメント変更:" in msg.text:
            c = msg.text.replace("コメント変更:","")
            if c in [""," ","\n",None]:
                cl.sendMessage(msg.to,"変更できない文字列です。")
            else:
                wait["comment"] = c
                cl.sendMessage(msg.to,"変更しました。\n\n" + c)
        elif msg.text in ["コメント:オン","コメント：オン","コメント:on"]:
            if wait["commentOn"] == True:
                cl.sendMessage(msg.to,"既にオンです。")
            else:
                wait["commentOn"] = True
                cl.sendMessage(msg.to,"オンにしました。")
        elif msg.text in ["コメント:オフ","コメント：オフ","コメント:off"]:
            if wait["commentOn"] == False:
                cl.sendMessage(msg.to,"既にオフです。")
            else:
                wait["commentOn"] = False
                cl.sendMessage(msg.to,"オフにしました。")

        elif msg.text in ["コメント確認"]:
            cl.sendMessage(msg.to,"現在自動コメントは以下のように設定されています。\n\n" + str(wait["comment"]))
        elif msg.text in ["gurl:get"]:
            if msg.toType == 2:
                g = cl.getGroup(msg.to)
                if g.preventedJoinByTicket == True:
                    g.preventedJoinByTicket = False
                    cl.updateGroup(g)
                gurl = cl.reissueGroupTicket(msg.to)
                cl.sendMessage(msg.to,"line://ti/g/" + gurl)
            else:
                cl.sendMessage(msg.to,"グループ以外では使用できません。")
        elif "gurl取得:" in msg.text:
            if msg.toType == 2:
                gid = msg.text.replace("gurl取得:","")
                gurl = cl.reissueGroupTicket(gid)
                cl.sendMessage(msg.to,"line://ti/g/" + gurl)
            else:
                cl.sendMessage(msg.to,"グループ以外では使用できません。")
        elif msg.text in ["コメントブラックリスト追加"]:
            wait["wblack"] = True
            cl.sendMessage(msg.to,"ブラックリストに追加する人の連絡先を送信してください。")
        elif msg.text in ["コメントブラックリスト削除"]:
            wait["dblack"] = True
            cl.sendMessage(msg.to,"ブラックリストから追加する人の連絡先を送信してください。")
        elif msg.text in ["コメントブラックリスト確認"]:
            if wait["commentBlack"] == {}:
                cl.sendMessage(msg.to,"ブラックリストにしている人はいません。")
            else:
                cl.sendMessage(msg.to,"以下がブラックリストです。")
                mc = ""
                for mi_d in wait["commentBlack"]:
                    mc += "・" +cl.getContact(mi_d).displayName + "\n"
                cl.sendMessage(msg.to,mc)
        elif "NK:" in msg.text:
            if msg.toType == 2:
                print ("ok")
                _name = msg.text.replace("NK:","")
                gs = cl.getGroup(msg.to)
                targets = []
                for g in gs.members:
                    if _name in g.displayName:
                        targets.append(g.mid)
                if targets == []:
                    cl.sendMessage(msg.to,"Not found.")
                else:
                    for target in targets:
                        try:
                            cl.kickoutFromGroup(msg.to,[target])
                        except:
                            cl.sendMessage(msg.to,"Error")
        elif "MK:" in msg.text:
              targets = []
              key = eval(msg.contentMetadata["MENTION"])
              key["MENTIONEES"][0]["M"]
              for x in key["MENTIONEES"]:
                  targets.append(x["M"])
              for target in targets:
                  try:
                      cl.kickoutFromGroup(msg.to,[target])
                  except:
                      cl.sendMessage(msg.to,"Error")
        if "mid:" in msg.text:
            key = eval(msg.contentMetadata["MENTION"])
            key1 = key["MENTIONEES"][0]["M"]
            cl.sendMessage(msg.to,key1)
        elif "midk:" in msg.text:
              key = msg.text[5:]
              cl.kickoutFromGroup(msg.to, [key])
              contact = cl.getContact(key)
              cl.sendMessage(msg.to,"ok!")
        elif "STK:" in msg.text:
              _name = msg.text.replace("STK:","")
              gs = cl.getGroup(msg.to)
              targets = []
              for g in gs.members:
                  if _name in g.statusMessage:
                     targets.append(g.mid)
              if targets == []:
                 cl.sendMessage(msg.to,"Not found.")
              else:
                  for target in targets:
                      try:
                         cl.kickoutFromGroup(msg.to,[target])
                      except:
                         cl.sendMessage(msg.to,"Error")
        elif msg.text == "speed":
            start = time.time()
            cl.sendMessage(msg.to,"loading...")
            elapsed_time = time.time() - start
            cl.sendMessage(msg.to,"result\n>>%ssec" % (elapsed_time))
        elif "test" == msg.text:
            cl.sendMessage(msg.to,"正常に動作しています")
        elif msg.text in ["ブラックリスト登録"]:
            wait["wblacklist"] = True
            cl.sendMessage(msg.to,"ブラックリストに登録するアカウントを送信してください。")
        elif "bladd:" in msg.text:
            key = eval(msg.contentMetadata["MENTION"])
            key1 = key["MENTIONEES"][0]["M"]
            mid = cl.getContact(key1)
            if mid.mid in wait["blacklist"]:
                cl.sendMessage(msg.to,"Already added")
            else:
                wait["blacklist"][mid.mid] = True
                wait["wblacklist"] = False
                cl.sendMessage(msg.to,"ブラックリストに追加しました。")
                f=codecs.open('st2__b.json','w','utf-8')
                json.dump(wait["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)
        elif "bldel:" in msg.text:
            key = eval(msg.contentMetadata["MENTION"])
            key1 = key["MENTIONEES"][0]["M"]
            mid = cl.getContact(key1)
            if mid.mid in wait["blacklist"]:
                del wait["blacklist"][mid.mid]
                cl.sendMessage(msg.to,"ブラックリストから削除しました。")
                wait["dblacklist"] = False
                f=codecs.open('st2__b.json','w','utf-8')
                json.dump(wait["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)
            else:
                wait["dblacklist"] = False
                cl.sendMessage(msg.to,"ブラックリストに入っていません。")
        elif msg.text in ["ブラックリスト削除"]:
            wait["dblacklist"] = True
            cl.sendMessage(msg.to,"ブラックリストから削除するアカウントを送信してください。")
        elif msg.text in ["ブラックリスト確認"]:
            if wait["blacklist"] == {}:
                cl.sendMessage(msg.to,"ブラックリストにしている人はいません。")
            else:
                cl.sendMessage(msg.to,"以下がブラックリストです。")
                mc = ""
                for mi_d in wait["blacklist"]:
                    mc += "・" +cl.getContact(mi_d).displayName + "\n"
                cl.sendMessage(msg.to,mc)
        elif msg.text in ["メンバーチェック"]:
            try:
                if msg.toType == 2:
                    group = cl.getGroup(msg.to)
                    gMembMids = [contact.mid for contact in group.members]
                    matched_list = []
                    for tag in wait["blacklist"]:
                        matched_list+=filter(lambda str: str == tag, gMembMids)
                    cocoa = ""
                    for mm in matched_list:
                        cocoa += mm + "\n"
                    cl.sendMessage(msg.to,cocoa + "がブラックリストです。")
            except:
                cl.sendMessage(msg.to,"ブラックリストユーザーはいません。")
        elif msg.text in ["追い出し"]:
            if msg.toType == 2:
                group = cl.getGroup(msg.to)
                gMembMids = [contact.mid for contact in group.members]
                matched_list = []
                for tag in wait["blacklist"]:
                    matched_list+=filter(lambda str: str == tag, gMembMids)
                if matched_list == []:
                    cl.sendMessage(msg.to,"ブラックリストユーザーはいませんでした。")
                    return
                for jj in matched_list:
                    cl.kickoutFromGroup(msg.to,[jj])
                cl.sendMessage(msg.to,"ブラックリストユーザーの追い出しが完了しました。")
        elif msg.text in ["単蹴り"]:
            if msg.toType == 2:
                group = cl.getGroup(msg.to)
                gMembMids = [contact.mid for contact in group.invitee]
                for _mid in gMembMids:
                    cl.cancelGroupInvitation(msg.to,[_mid])
                cl.sendMessage(msg.to,"と見せかけてキャンセルしました。")
        elif Cmd(msg.text,["既読ポイントセット"]):
            cl.sendMessage(msg.to,"既読ポイントを設定しました\n\n確認は(既読確認)")
            try:
                del wait['readPoint'][msg.to]
                del wait['readMember'][msg.to]
            except:
                pass
            wait['readPoint'][msg.to] = msg.id
            wait['readMember'][msg.to] = ""
        elif Cmd(msg.text,["既読確認"]):
            if msg.to in wait['readPoint']:
                cl.sendMessage(msg.to,"既読を付けた人は\n" + "\n" + wait['readMember'][msg.to] + "\n" + "以上です(^^♪")
            else:
                cl.sendMessage(msg.to,"既読ポイントがセットされていません\n設定は〔既読ポイントセット〕")
        elif Cmd(msg.text,["既読ポイント破棄"]):
            cl.sendMessage(msg.to,"既読ポイントを破棄しました\n再設定は〔既読ポイントセット〕")
            try:
                del wait['readPoint'][msg.to]
                del wait['readMember'][msg.to]
            except:
                pass
        elif "random:" in msg.text:
            if msg.toType == 2:
                strnum = msg.text.replace("random:","")
                source_str = 'abcdefghijklmnopqrstuvwxyz1234567890@:;./_][!&%$#)(=~^|'
                try:
                    num = int(strnum)
                    group = cl.getGroup(msg.to)
                    for var in range(0,num):
                        name = "".join([random.choice(source_str) for x in xrange(10)])
                        time.sleep(0.01)
                        group.name = name
                        cl.updateGroup(group)
                except:
                    cl.sendMessage(msg.to,"Error")
        elif "アルバム作成:" in msg.text:
            try:
                albumtags = msg.text.replace("アルバム作成:","")
                gid = albumtags[:33]
                name = albumtags.replace(albumtags[:34],"")
                cl.createAlbum(gid,name)
                cl.sendMessage(msg.to,name + "アルバムを作成しました。")
            except:
                cl.sendMessage(msg.to,"Error")
        elif "fakec→" in msg.text:
            try:
                source_str = 'abcdefghijklmnopqrstuvwxyz1234567890@:;./_][!&%$#)(=~^|'
                name = "".join([random.choice(source_str) for x in xrange(10)])
                amid = msg.text.replace("fakec→","")
                cl.sendMessage(msg.to,str(cl.channel.createAlbumF(msg.to,name,amid)))
            except Exception as e:
                try:
                    cl.sendMessage(msg.to,str(e))
                except:
                    pass
    except ZeroDivisionError as e:
        print("例外args:", e.args)
def NOTIFIED_READ_MESSAGE(op):
    try:
        if op.param1 in wait['readPoint']:
            Name = cl.getContact(op.param2).displayName
            if Name in wait['readMember'][op.param1]:
                pass
            else:
                wait['readMember'][op.param1] += "" + Name + " さん\n"
    except:
        pass

    
oepoll.addOpInterruptWithDict({
    OpType.NOTIFIED_ADD_CONTACT: NOTIFIED_ADD_CONTACT,
    OpType.NOTIFIED_INVITE_INTO_GROUP: NOTIFIED_INVITE_INTO_GROUP,
    OpType.NOTIFIED_KICKOUT_FROM_GROUP: NOTIFIED_KICKOUT_FROM_GROUP,
    OpType.NOTIFIED_INVITE_INTO_ROOM: NOTIFIED_INVITE_INTO_ROOM,
    OpType.NOTIFIED_LEAVE_ROOM: NOTIFIED_LEAVE_ROOM,
    OpType.SEND_MESSAGE: SEND_MESSAGE,
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE,
    OpType.NOTIFIED_READ_MESSAGE: NOTIFIED_READ_MESSAGE
    
})
while True:
    oepoll.trace()
