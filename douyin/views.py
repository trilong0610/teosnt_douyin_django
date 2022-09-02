import datetime
import random
from itertools import count
import ssl
from sys import flags

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
import requests
import re
import urllib.request
from django.utils import timezone
from django.conf import settings
import os
from video.models import CodeModel
from douyin.settings import MEDIA_ROOT
from video.views import *
import shutil

header = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Upgrade-Insecure-Requests': '1',
}


class home(View):
    def get(self, request):
        return render(request, 'douyin/home.html', {})


class downVideoNoEdit(View):

    def post(self, request):
        # Lấy link tiktok
        req_url = request.POST['url']
        req_code = request.POST['code']
        if not req_url:
            return HttpResponse("Vui lòng nhập URL")
        if not CodeModel.objects.filter(code = req_code).exists():
            return HttpResponse("Code hết hạn, vui lòng lấy code mới")

        url = find_url(req_url)
        id_video = get_id_video(url)
        data = download_video(id_video)

        video_name = data["name_video"]

        with open(os.path.join(MEDIA_ROOT, video_name), 'rb') as fh:
            # plug_cleaning_into_stream(fh, os.path.join(MEDIA_ROOT, video_name))
            response = HttpResponse(
                fh.read(), content_type='video/mp4')
            response['Content-Disposition'] = "attachment; filename=%s" % video_name
        os.remove(os.path.join(MEDIA_ROOT, video_name))
        return response

def get_link1s(url):
    response = requests.get(
        'https://link1s.com/api?api=1aaf8a3adce3bd6cb47f9ad1069cca97a0b6d733&url=' + str(url))
    return response.json()


# class downVideoAuthor(View):
#     def post(self, request):
#
#         # Lay sec_id tu nguoi dung de lay toan bo video
#         save_info = {}
#         url_author = request.POST['url_author']
#         count_vid = request.POST['count_vid']
#         checkbox_video = request.POST['checkbox_video']
#
#         print('count_vid------ ' + str(count_vid))
#
#         sec_uid = get_sec_uid(url_author)
#
#         # Lay danh sach video
#         json_data = get_all_posts(sec_uid=sec_uid, count_vid=count_vid)
#
#         print('aweme_list: ' + str(len(json_data['aweme_list'])))
#
#         # Kiem tra video co ton tai chua
#         # Neu checkbox = true va chua ton tai thi tai
#         nick_name = json_data['aweme_list'][0]['author']['nickname']
#         short_id = json_data['aweme_list'][0]['author']['short_id']
#
#         folder_name = "%s_%s_%d" % (
#             nick_name, short_id, time.time_ns())
#
#         folder_path = "assets/videos/%s" % (folder_name)
#         # Tai video da co tren db
#
#         for json in json_data['aweme_list']:
#
#             url_video = json['video']["play_addr"]['url_list'][2]
#             id_video = json['aweme_id']
#
#             # Neu video chua co tren db thi luu len db
#             if not Video.objects.filter(id_video=id_video).exists():
#                 video = Video.objects.create(id_video=id_video, sec_uid=sec_uid)
#                 video.save()
#
#             video_name = "%s_%d.mp4" % (short_id, int(time.time_ns()))
#
#             video_path = "assets/videos/%s/%s" % (folder_name, video_name)
#             # Tai video - luu ve may
#             save_video_author(video_path=video_path, folder_path=folder_path, url_video=url_video)
#             time.sleep(0.2)
#
#         print("Đã lưu toàn bô video")
#         try:  # Neu co tai ve video tu author
#             save_path = shutil.make_archive(folder_name, 'zip', folder_path)
#             response = HttpResponse(open(save_path, 'rb'))
#             response['Content-Disposition'] = 'attachment; filename=%s' % (folder_name)
#             response['Content-Type'] = 'application/zip'
#             return response
#         except:
#             return HttpResponse('Không tồn tại video để tải về, vui lòng thử lại')
#         print(save_path)
#
#         # with open(save_path, 'rb') as fd:
#         #     response = HttpResponse(fd.read(), content_type='application/x-zip-compressed')
#         #     response['Content-Disposition'] = "attachment; filename=%s.zip" % folder_name



def find_url(string):
    # Parse the link in the Douyin share password and return to the list
    url = re.findall(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return url[0]


def get_id_video(url):
    data = requests.get(headers=header, url=url, timeout=15)
    vid = re.findall(r'\d+', data.url)
    return vid[0]


def download_video(id_video):
    response = requests.get(
        headers=header, url='https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' + str(id_video))
    # item = response.json"().get("item_list")[0]

    item = response.json()

    #  Lay link tai video tu response
    url_mp4 = item["item_list"][0]["video"]["play_addr"]["url_list"][0].replace(
        "playwm", "play").replace(
        "720p", "1080p")

    #  Lay id tac gia video tu response

    name_video = "%s_%s.mp4" % (str(id_video), str(int(time.time())))

    path_video = "%s/%s" % (MEDIA_ROOT, name_video)

    opener = urllib.request.URLopener()

    opener.addheader(header)

    # urllib.request.urlretrieve(url=url_mp4, filename=path_video)
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url=url_mp4, filename=path_video)

    return {
        "path_video": path_video,
        "name_video": name_video
    }


def get_notification(error, tittle, message):

    return {'tag': error, 'title': tittle, 'data': message}


class create_code(View):
    def get(self, request):
        while True:
            # rand_code = random.randint(1000000, 9999999)
            rand_code = str(random.randint(1000000, 9999999))
            # rand_code = "123"
            #  neu code chua ton tai thi insert vao db
            if not CodeModel.objects.filter(code=rand_code).exists():
                print("Khong trung: " + rand_code)
                code = CodeModel(code=rand_code, time_out=timezone.now() + datetime.timedelta(hours=1))
                code.save()
                print("ccode: " + str(code.id))
                print(request.META['HTTP_HOST'])
                # Tao link rut gon bang code vua tao
                link1s = get_link1s('https://teont.tech/get_code/' + rand_code)
                print(link1s)
                if str(link1s["status"]) == "success":
                    # Tra ve ket qua
                    return JsonResponse(
                        {'link1s': link1s["shortenedUrl"], 'tag': 'success', 'title': 'Thành công', 'data': "Đã xong, lấy code ở dưới"})
                else:
                    return JsonResponse(
                        {'tag': 'error', 'title': 'Thất bại',
                         'data': "Lấy link rút gọn thất bại \n Vui lòng thử lại sau"})
            else:
                # Neu code da ton tai thi capnhat thoi gian
                code = CodeModel.objects.get(code=rand_code)
                # Neu key da het han thi xoa khoi db
                # sau do quay lai vong lap tim so khac
                if code.time_out < timezone.now():
                    print("Delete time out key: " + rand_code)
                    code.delete()
                    continue
        return JsonResponse({'tag': 'error', 'title': 'Lỗi', 'data': "Tạo link rút gọn thất bại\nVui lòng thử lại."})
        # return code


class get_code(View):
    def get(self, request, code):
        if CodeModel.objects.filter(code=code).exists():
            code = CodeModel.objects.get(code=code)
            time_out = str(code.time_out - timezone.now()).split('.')[0] + "s"
            return HttpResponse("<h3>Code: %s</h4><h5>Hết hạn: %s</h5>" % (code.code, time_out))
        return HttpResponse("Không tìm thấy code, vui lòng lấy code mới")


class check_code(View):
    def get(self, request, code):
        if CodeModel.objects.filter(code=code).exists():
            code_model = CodeModel.objects.get(code=code)
            print(code_model)
            if code_model.time_out > timezone.now():
                print("success")
                return JsonResponse({"success": "true"})
        print("failed")
        return JsonResponse(get_notification("error", "Lỗi", "Code hết hạn\nVui lòng lấy code mới"))

