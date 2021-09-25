import os

import requests

from removeBg import RemoveBg

# https://www.remove.bg/
api_keys = iter(['H1DqC78S4G3U9bMU6YB8gKaJ',
                 'UNJbipqkXZCqDopaByH3bJyy',
                 'z8Nhk7pzPDhyYwRda92w9DtE',
                 'Arrciej7xjjZiHScaAJc8JVq',
                 'ZJ3vidG9B4fy2sYZT1kSJsTm',
                 'sPmmWovBstgDwRdgAc9hyuBq',
                 'vofJ89AU3UGa8CkWhuUymq4e',
                 'eB4u46snqhvrkqYEkqWAMz7Q',
                 'Ys9u78JRyMt5Wt8uDhEmSxUV',
                 '5KpcscyqH1j97U1NsX4kk3KJ'])

# 失败列表 目前观察白色背景的会失败 需要列出另行处理
fail_list = []


def changeBg(rmbg, img_file_path, new_file_name, bg):
    try:
        rmbg.remove_background_from_img_file(img_file_path=img_file_path, bg_type='path', bg=bg,
                                             new_file_name=new_file_name)
    except requests.exceptions.HTTPError as e:
        # 402表示免费额度用完了
        if e.response.status_code == 402:
            print('api_key已失效:%s' % rmbg.api_key)
            try:
                # 换下一个api_key
                rmbg.api_key = next(api_keys)
            except StopIteration as e:
                raise Exception('没有可用的api_key了')
            # 重来
            changeBg(rmbg, img_file_path, new_file_name, bg)
        else:
            print('转换出错:%s' % img_file_path)
            fail_list.append(img_file_path)
            # raise e
    except Exception as e:
        print('未知的转换出错:%s' % img_file_path)
        raise e
    else:
        print('转换成功:%s=>%s' % (img_file_path, new_file_name))


def main():
    rmbg = RemoveBg(next(api_keys), "error.log")
    # 要转换的图片放到程序的同级文件夹 picture/old 里面, 转换后的图片将输出到 picture/new 里
    path = '%s\\picture\\old' % os.getcwd()
    # 新背景
    bg = '%s\\picture\\newBg.jpg' % os.getcwd()
    try:
        for root, dirs, files in os.walk(path):
            for pic in files:
                img_file_path = os.path.join(root, pic)
                new_file_name = img_file_path.replace('\\old\\', '\\new\\')
                if os.path.exists(new_file_name):
                    print('%s已转换, 将忽略' % pic)
                    continue
                elif not os.path.exists(os.path.dirname(new_file_name)):
                    os.makedirs(os.path.dirname(new_file_name))
                changeBg(rmbg, img_file_path, new_file_name, bg)
    finally:
        if len(fail_list) > 0:
            print('失败的转换:')
            print(fail_list)
        print('转换结束.')


if __name__ == '__main__':
    main()
