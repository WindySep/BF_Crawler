'''
    ① 先提供如下网址：
        https://api.bilibili.com/x/relation/followers?vmid=UID&pn=页数
        https://api.bilibili.com/x/relation/stat?vmid=UID&jsonp=jsonp
    第一个网站查粉丝信息，第二个网址查粉丝数量（有几个）。

    ② 对于某位指定用户，我们需要知道ta的UID，查询UID的方式是进入ta的主页，在主页网址中的“space.bilibili.com”后面那一串数字就是我们需要的UID。

    ③ 页数的可行范围为1，2，3，4，5，每页提供50个粉丝的数据。超过这个范围，网页弹出：{"code":22007,"message":"限制只访问前5页","ttl":1}，
    这不在本文讨论范围，本文只提供前250个粉丝数据。

    ④ 对于粉丝数≤250的用户，利用以下代码可以查到所有粉丝的信息，否则只能查看前250位粉丝的信息，
    粉丝信息包括昵称、头像、个性签名等（抓取的关键字不同），本文提供的代码仅爬取了粉丝昵称作为示例。

    ⑤ 运行环境为 jupyter notebook(Anaconda3), windows11, Edge 浏览器。

    ⑥ 爬取B站的数据，有有些数据可以直接爬，有些数据需要登录才能看到，这些数据爬的时候就要在请求头里面加入cookie。
    若代码请求头里只有一个User-Agent，可以在审查元素里面看一看这个get请求的请求头有哪些，最好全部复制过来。

    ⑦ 如何获取请求头：
        1.F12进入审查元素，Network->Fetch/XHR->右键选择需要爬取的界面->Copy->Copy as cURL(bash)
        2.进入Convert curl commands to code网站，将复制的内容粘贴到这个网站上，即可自动生成完整的请求头
        3.复制回代码即可

    ⑧ 关闭后再次使用本程序，可能需要重复⑦步骤，复制界面选带fans的
'''


# 导入request库来下载网页元素，其本质是向服务器发送请求并得到响应。
import requests

# 输入目标的UID，作为一个字符串
# uid = str(input("输入查询用户的UID："))
# uid = '44286718'
uid = '2070667222'
# 三个字符串加在一起，形成查粉丝数量的网址，来确定后续页数的范围
url01 = "https://api.bilibili.com/x/relation/stat?vmid="+uid+"&jsonp=jsonp"


# 请求头参数，不解释了，照抄就行
cookies = {
    'buvid3': 'ABE892DE-9C66-4E32-8A67-6AF90166EDB434780infoc',
    'LIVE_BUVID': 'AUTO7216276505543377',
    'i-wanna-go-back': '-1',
    'buvid_fp_plain': 'undefined',
    'buvid4': 'E636343F-0FBF-E1DB-AB4C-1334D9BE31AF21423-022012416-eFZHYp%2FCJ3hELeUgt8J3Kg%3D%3D',
    'rpdid': '0zbfVH22y8|14DN5xNBN|2z|3w1OVasS',
    'header_theme_version': 'CLOSE',
    'nostalgia_conf': '-1',
    'hit-new-style-dyn': '1',
    'CURRENT_PID': 'b2494590-d497-11ed-8b55-efaa196276eb',
    'FEED_LIVE_VERSION': 'V8',
    'hit-dyn-v2': '1',
    '_uuid': '1C8E2314-5A106-EFCA-BA53-B8285555510A829140infoc',
    'DedeUserID': '2070667222',
    'DedeUserID__ckMd5': 'fe503b49c951d0c9',
    'CURRENT_FNVAL': '4048',
    'fingerprint': 'fa89269df4585942347f02ef84fe99d0',
    'is-2022-channel': '1',
    'b_nut': '100',
    'CURRENT_QUALITY': '80',
    'home_feed_column': '5',
    'browser_resolution': '1536-715',
    'buvid_fp': 'fa89269df4585942347f02ef84fe99d0',
    'innersign': '0',
    'b_lsid': 'DC77102E6_18B0527744A',
    'SESSDATA': 'ececea1a%2C1712153021%2Cff296%2Aa1CjAMRLTcfDnaO1p20kqw07NUK_IAMDHKKqppvMoIzVB7-jGWDppllSrDRCI-QaJMZTcSVllsQ2M4MUdqXzN1Ni1uRzkyS3dpWHRwbUx3SndpS2tGRDU0cFpmTUlkN050eFRXSnl1dmNqQmJJd29FYnNaYUMyUzNDTy16VXdzaDYzSEtqZFJQNzZnIIEC',
    'bili_jct': '84f2c68263c6b602d05f267bf14823d5',
    'bp_video_offset_2070667222': '849191772621897729',
    'PVID': '1',
    'sid': '667nuthi',
    'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTY4NjI2MTgsImlhdCI6MTY5NjYwMzM1OCwicGx0IjotMX0.wFQpxtcSBSdGdw9FIDgZ18ucLxFYo2EHaFZ9gbDD4Nw',
    'bili_ticket_expires': '1696862558',
}

headers = {
    'authority': 'api.bilibili.com',
    'accept': '*/*',
    'accept-language': 'zh,en;q=0.9,zh-CN;q=0.8',
    'cookie': 'buvid3=ABE892DE-9C66-4E32-8A67-6AF90166EDB434780infoc; LIVE_BUVID=AUTO7216276505543377; i-wanna-go-back=-1; buvid_fp_plain=undefined; buvid4=E636343F-0FBF-E1DB-AB4C-1334D9BE31AF21423-022012416-eFZHYp%2FCJ3hELeUgt8J3Kg%3D%3D; rpdid=0zbfVH22y8|14DN5xNBN|2z|3w1OVasS; header_theme_version=CLOSE; nostalgia_conf=-1; hit-new-style-dyn=1; CURRENT_PID=b2494590-d497-11ed-8b55-efaa196276eb; FEED_LIVE_VERSION=V8; hit-dyn-v2=1; _uuid=1C8E2314-5A106-EFCA-BA53-B8285555510A829140infoc; DedeUserID=2070667222; DedeUserID__ckMd5=fe503b49c951d0c9; CURRENT_FNVAL=4048; fingerprint=fa89269df4585942347f02ef84fe99d0; is-2022-channel=1; b_nut=100; CURRENT_QUALITY=80; home_feed_column=5; browser_resolution=1536-715; buvid_fp=fa89269df4585942347f02ef84fe99d0; innersign=0; b_lsid=DC77102E6_18B0527744A; SESSDATA=ececea1a%2C1712153021%2Cff296%2Aa1CjAMRLTcfDnaO1p20kqw07NUK_IAMDHKKqppvMoIzVB7-jGWDppllSrDRCI-QaJMZTcSVllsQ2M4MUdqXzN1Ni1uRzkyS3dpWHRwbUx3SndpS2tGRDU0cFpmTUlkN050eFRXSnl1dmNqQmJJd29FYnNaYUMyUzNDTy16VXdzaDYzSEtqZFJQNzZnIIEC; bili_jct=84f2c68263c6b602d05f267bf14823d5; bp_video_offset_2070667222=849191772621897729; PVID=1; sid=667nuthi; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTY4NjI2MTgsImlhdCI6MTY5NjYwMzM1OCwicGx0IjotMX0.wFQpxtcSBSdGdw9FIDgZ18ucLxFYo2EHaFZ9gbDD4Nw; bili_ticket_expires=1696862558',
    'origin': 'https://space.bilibili.com',
    'referer': 'https://space.bilibili.com/2070667222/fans/fans?spm_id_from=333.1007.0.0',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
}

params = {
    'vmid': '2070667222',
    'pn': '1',
    # 'ps': '20',
    'ps': '50',
    'order': 'desc',
    'order_type': 'attention',
    'gaia_source': 'main_web',
    'web_location': '333.999',
    'w_rid': '8186e6c91c1647b449b7c494a0b84ff3',
    'wts': '1696603480',
}


# 用request.get()函数，参数为url和headers，也就是网址和请求头，我们于是得到了服务器的响应
res01 = requests.get(url=url01, params=params, cookies=cookies, headers=headers)
# print(res01.text)
p = res01.text.find("follower")
# 这两步找到了目标的粉丝数量，定义为变量fans_number
fans_number = int(res01.text[p+10:len(res01.text)-2])
# 建立空列表来搜集信息
fans_listName = []
fans_listUid = []
fans_list = {}

if fans_number > 250:
    print("该用户粉丝数共", fans_number, "个，目前只能查询到前250位粉丝信息如下：")
    for i in range(0, 5):
        # 三个字符串加在一起，形成查粉丝信息的网址，i从0-4，页码就从1-5遍历
        url = "http://api.bilibili.com/x/relation/followers?vmid="+uid+"&pn="+str(i+1)
        # 用了最上面的请求头
        header = headers
        params = params
        cookies = cookies
        res = requests.get(url=url, params=params, cookies=cookies, headers=headers)
        # res = requests.get(url=url, headers=headers)
        res.encoding = "utf-8"
        # 对于某页，返回了文本形式的信息，我们将其字符串化即str()，定义为fans_data
        fans_data = str(res.text)
        # 统计一下该页提供的粉丝数量，有可能是50不到，这一步在这里不需要，因为＞250粉丝肯定有5页了，仅仅保持和后文的统一
        num = fans_data.count("uname")

        # 粉丝昵称是 "uname" 后的信息，紧接着提供了 “face” 即头像的信息，格式是固定的。
        # 所以这里利用了for循环和切片，将字符串中出现的第一个粉丝的名字提取出来并放入fans_list中，
        # 注意是自动放在了列表末尾，所以最后打印出的列表里排在越前面的粉丝是越近关注的。
        # 然后，裁减字符串，使得原先的第二个粉丝变为新字符串里的第一个粉丝，继续循环提取。
        for i in range(0, num):
            a = fans_data.find("uname")
            b = fans_data.find("face")
            c = fans_data.find("track_id")
            d = fans_data.find("mid")
            f = fans_data.find("attribute")

            fans_listName.append(fans_data[a + 8:b - 3])
            fans_listUid.append(fans_data[d + 5:f - 2])
            fans_data = str(fans_data[c+10:])

# 同理，这部分是对粉丝数≤250的用户进行的爬取。
else:
    print("该用户粉丝数共", fans_number, "个，所有粉丝信息如下：")
    # 这里计算了页码信息。最大是 pagemax页，比如粉丝数为200，pagemax=5；粉丝数为199，pagemax=4，int()是整数化
    '''
        这里有个疑问：
        如果按照变量url的网址进行查看，他会显示一个每页有50个人的界面。但如果我在这个界面打开Network->Fetch/XHR找不到任何可以复制的请求头。
        所以我只能在b站的界面去寻找请求头，但是我发现这样一来，他每页就不是50个人的信息，而是和b站列表一样是20个人的，
        也就是正确的页数应该是pagemax = int(fans_number/20)+1，这是为什么？
        是和请求头有关吗？因为我用的是b站本身网站的请求头？
        但是，如果我用最开始的代码，不加cookies等，我又访问不到任何数据
    '''
    '''
        关于这个问题，有一个方案是将'ps': '20'改成'ps': '50'，另外headers中将已登录的cookie带上就可以返回50个粉丝数据了.
        尝试了一下是可以的。
    '''
    pagemax = int(fans_number/50)+1
    # pagemax = int(fans_number/20)+1
    print("该用户粉丝页数共", pagemax, "个")

    for i in range(0, pagemax + 1):
        url = "http://api.bilibili.com/x/relation/followers?vmid="+uid+"&pn="+str(i+1)
        header = headers
        params = params
        cookies = cookies
        res = requests.get(url=url, params=params, cookies=cookies, headers=headers)
        # res = requests.get(url=url, headers=headers)
        res.encoding = "utf-8"
        fans_data = str(res.text)
        # print("fans_data: ", fans_data)
        # 用于统计字符串或列表中某个元素出现的次数. 即统计粉丝数
        num = fans_data.count("uname")

        for i in range(0, num):
            a = fans_data.find("uname")
            b = fans_data.find("face")
            c = fans_data.find("track_id")
            d = fans_data.find("mid")
            f = fans_data.find("attribute")

            # fans_list.append(fans_data[a+8:b-3])
            fans_listName.append(fans_data[a+8:b-3])
            fans_listUid.append(fans_data[d+5:f-2])
            # print(fans_list)
            fans_data = str(fans_data[c+10:])
            # print(fans_data)


# 最终得到粉丝信息列表和这一列表的元素个数即粉丝数量。
fans_list=dict(zip(fans_listName,fans_listUid))
print(fans_list, len(fans_list))