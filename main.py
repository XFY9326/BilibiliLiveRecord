import time

import requests

bilibiliUserId = '67141'


def get_user_info(user_id: str) -> dict:
    url = f'https://api.bilibili.com/x/space/acc/info?mid={user_id}'
    with requests.get(url) as r:
        return r.json()['data']


def get_record_list(room_id: int) -> dict:
    page_size = 20
    while True:
        url = f'https://api.live.bilibili.com/xlive/web-room/v1/record/getList?room_id={room_id}&page=1&page_size={page_size}'
        with requests.get(url) as r:
            data = r.json()
            total_record_amount = data['data']['count']
            if total_record_amount > page_size:
                page_size = total_record_amount
            else:
                return data['data']


def main():
    user_info = get_user_info(bilibiliUserId)
    print(f'主播名称：{user_info["name"]}')
    print(f'直播间ID：{user_info["live_room"]["roomid"]}')
    record_list = get_record_list(user_info["live_room"]["roomid"])
    print(f'回放总量：{record_list["count"]}')
    print('所有回放：')
    for record in record_list['list']:
        print(f'\t标题：{record["title"]}')
        print(f'\t分区名称：{record["parent_area_name"]}-{record["area_name"]}')
        print(f'\t开播时间：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record["start_timestamp"]))}')
        second_length = record["length"] / 1000
        print(f'\t时长：{int(second_length / (60 * 60))}:{int((second_length / 60) % 60)}:{int(second_length % 60)}')
        print('\t热度：%.1f万' % (record["online"] / 10000))
        print(f'\t弹幕量：{record["danmu_num"]}')
        print(f'\t回放地址：https://live.bilibili.com/record/{record["rid"]}', end='\n\n')


if __name__ == '__main__':
    main()
