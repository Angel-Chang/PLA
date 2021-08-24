# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime, timedelta
from django.db.models import Count, aggregates, Sum, Q, Max, Avg

from rest_framework import generics, status, mixins, viewsets
from rest_framework.response import Response

from member.models import *
from member.serializers import *

import uuid , calendar, requests
import decimal
import logging
import sys
import traceback

from django.http import HttpResponse, Http404, JsonResponse

logger1 = logging.getLogger('member.cron')

# {
# "current_page": 1,
# "data": [
# {
# "post_id": "672",
# "post_published": null,
# "post_created_at": "2021-06-24 08:37:17",
# "post_update_at": "2021-06-24 08:37:17",
# "post_content": "最近狗狗的尿味重、顏色特別深，該注意嗎？\n",
# "post_decription": "<h1><span style=\"color:#2ecc71\"><strong>容易產生泌尿道疾病的高危險群</strong></span></h1>\n\n<p>
# 	產生泌尿道疾病的原因有很多，與生活習慣更是息息相關，如果家中狗狗本身不愛喝水或是容易憋尿，都會成為高危險群的一份子。</p>\n\n<h3><strong>品種</strong></h3>\n\n<p>
# 	雪納瑞、米格魯、巴哥、大麥町等犬種較常好發</p>\n\n<p>
# 	<img alt=\"\" height=\"376\" src=\"/ckfinder/ckfinder/userfiles/files/image(8).png\" width=\"675\" /></p>\n\n<p>
# 		&bull;&nbsp;尿液氣味重，顏色也變得很深或不正常（如：血尿）</p>\n\n<p><iframe allowfullscreen=\"true\" frameborder=\"0\"
# 			height=\"1000px\"
# 			src=\"https://www.facebook.com/v2.8/plugins/quote.php?app_id=469437609887759&amp;channel=https%3A%2F%2Fstaticxx.facebook.com%2Fx%2Fconnect%2Fxd_arbiter%2F%3Fversion%3D46%23cb%3Df23aa0972fa512c%26domain%3Dwww.pettalk.tw%26origin%3Dhttps%253A%252F%252Fwww.pettalk.tw%252Ff276156dbb8db68%26relation%3Dparent.parent&amp;container_width=1170&amp;href=https%3A%2F%2Fwww.pettalk.tw%2Fblog%2F%25E6%259C%2580%25E8%25BF%2591%25E7%258B%2597%25E7%258B%2597%25E7%259A%2584%25E5%25B0%25BF%25E5%2591%25B3%25E9%2587%258D%25E3%2580%2581%25E9%25A1%258F%25E8%2589%25B2%25E7%2589%25B9%25E5%2588%25A5%25E6%25B7%25B1%25EF%25BC%258C%25E8%25A9%25B2%25E6%25B3%25A8%25E6%2584%258F%25E5%2597%258E%25EF%25BC%259F%25EF%25BD%259C%25E5%25B0%2588%25E6%25A5%25AD%25E7%258D%25B8%25E9%2586%25AB%25E2%2580%2594%25E5%25AE%258B%25E5%25AD%2590%25E6%258F%259A&amp;locale=zh_TW&amp;sdk=joey\"
# 			width=\"1000px\"></iframe></p>\n\n<p>&bull;&nbsp;頻尿</p>\n\n<p>&bull;&nbsp;尿得很多或很少</p>\n\n<p>
# 		&bull;&nbsp;需要用力排尿，或排尿困難</p>\n\n<p>&bull;&nbsp;排尿習慣改變，或是走到哪尿到哪</p>\n\n<p>&bull;&nbsp;尿尿時會哀鳴</p>\n\n<p>
# 		&bull;&nbsp;容易口渴</p>\n\n<p>&bull;&nbsp;一直想舔尿道口的位置</p>\n\n<p>&bull;&nbsp;急性腎衰竭</p>\n\n<p>
# 		<img alt=\"\" height=\"420\" src=\"/ckfinder/ckfinder/userfiles/files/image(9).png\" width=\"578\" /></p>\n",
# 		"post_picture": null,
# 		"post_url": "http://104.46.236.7/page/B2VTOPF8/show/672",
# 		"post_like": "0",
# 		"post_views": "1",
# 		"page_provider": "lovemetw",
# 		"page_name": "LovemeStory",
# 		"page_icon": "https://www.lovemestory.com.tw/assets/uploads/155_kol_avatar_1_thumb.png"
# 		},
# 		{
# 		"post_id": "671",
# 		"post_published": null,
# 		"post_created_at": "2021-03-04 15:56:28",
# 		"post_update_at": "2021-03-05 11:44:26",
# 		"post_content": "寵物_api_文章標題\n",
# 		"post_decription": "<p>
# 			{<br />\n&nbsp;&nbsp;&nbsp;&nbsp;&quot;type&quot;: &quot;test_type&quot;,<br />\n&nbsp;&nbsp;&nbsp;&nbsp;&quot;goto&quot;: &quot;<a
# 				href=\"https://supr.link/XbkVo\">https://supr.link/XbkVo </a>&quot;,
# 				<br />\n&nbsp;&nbsp;&nbsp;&nbsp;&quot;desc&quot;:
# 			&quot;test_desc&quot;,<br />\n&nbsp;&nbsp;&nbsp;&nbsp;&quot;price&quot;: &quot;test_price&quot;<br />\n}</p>
# 			\n",
# 			"post_picture": "http://104.46.236.7/assets/uploads/PhotoGrid_Plus_16112917680921_thumb.jpg",
# 			"post_url": "http://104.46.236.7/page/B2VTOPF8/show/671",
# 			"post_like": "0",
# 			"post_views": "25",
# 			"page_provider": "lovemetw",
# 			"page_name": "LovemeStory",
# 			"page_icon": "https://www.lovemestory.com.tw/assets/uploads/155_kol_avatar_1_thumb.png"
# 			}
# 			],
# 			"first_page_url": "/?page=1",
# 			"from": 1,
# 			"last_page": 0,
# 			"last_page_url": "/?page=0",
# 			"next_page_url": null,
# 			"path": "/",
# 			"per_page": "20",
# 			"prev_page_url": null,
# 			"to": 1,
# 			"total": "2"
# 			}

def getDynaMsg_job():
  d1=datetime.datetime.now()
  msg = "[getDynaMsg_job]1-start====================================="
  logger1.warning(msg)

  url = 'http://104.46.236.7/api/posts/寵物_api/20'
  # call api (get), timeout unit: seconds
  result = requests.get(url, timeout=30)
  jsondata = result.json()
  datalist = jsondata['data']
  # 跟貼文有關的欄位
  post_id = ""
  post_published = ""
  post_created_at = ""
  post_update_at = ""
  post_content = ""
  post_decription = ""
  post_picture = ""
  post_url = ""
  post_like = ""
  post_views = ""
  page_provider = ""
  page_name = ""
  page_icon = ""

  try:
    for data in datalist:
      post_id = data['post_id']
      date1 = data['post_published']
      if date1 is not None and len(date1) > 0:
        post_published = datetime.datetime.strptime(date1,"%Y-%m-%d %H:%M:%S")
      else:
        post_published = None

      date1 = data['post_created_at']
      if date1 is not None and len(date1) > 0:
        post_created_at = datetime.datetime.strptime(date1,"%Y-%m-%d %H:%M:%S")
      else:
        post_created_at = None

      date1 = data['post_update_at']
      if date1 is not None and len(date1) > 0:
        post_update_at = datetime.datetime.strptime(date1,"%Y-%m-%d %H:%M:%S")
      else:
        post_update_at = None

      post_content = data['post_content']
      desc_source = data['post_decription']
      post_decription = desc_source.replace("/ckfinder/","http://104.46.236.7/ckfinder/")
      post_picture = data['post_picture']
      post_url = data['post_url']
      post_like = data['post_like']
      post_views = data['post_views']
      page_provider = data['page_provider']
      page_name = data['page_name']
      page_icon = data['page_icon']
      # 用post_id去資料庫表中找尋是否有相同的post_id資料，
      # 沒有 => 新增資料
      # 有 => 再比對post_update_at是否相同，相同不更新，不同則將資料更新到資料表中
      isExist = dynaPost.objects.filter(post_id=post_id).exists()
      # 檢查post_id是否存在
      if not isExist:
        # 新增貼文資料
        createdObj = dynaPost.objects.create(
            post_id = post_id,
            post_published = post_published,
            post_created_at = post_created_at,
            post_update_at = post_update_at,
            post_content = post_content,
            post_decription = post_decription,
            post_picture = post_picture,
            post_url = post_url,
            post_like = post_like,
            post_views = post_views,
            page_provider = page_provider,
            page_name = page_name,
            page_icon = page_icon,
            last_modify_date = datetime.datetime.now()
        )
        msg = f"[getDynaMsg_job]post_id:{post_id} created !"
        logger1.warning(msg)        
      else:
        matched = dynaPost.objects.get(post_id=post_id)
        old_post_update_at = matched.post_update_at
        str = f"old_post_update_at:{old_post_update_at} post_update_at:{post_update_at}"

        if old_post_update_at != post_update_at:
          matched.post_published = post_published
          matched.post_created_at = post_created_at
          matched.post_update_at = post_update_at
          matched.post_content = post_content
          matched.post_decription = post_decription
          matched.post_picture = post_picture
          matched.post_url = post_url
          # matched.post_like = post_like
          matched.post_views = post_views
          matched.page_provider = page_provider
          matched.page_name = page_name
          matched.page_icon = page_icon
          matched.last_modify_date = datetime.datetime.now()
          matched.save()
          msg = f"[getDynaMsg_job]post_id:{post_id} updated !"
          logger1.warning(msg)

  except Exception as e:
    d1=datetime.datetime.now()
    msg = f"[getDynaMsg_job]error:{e}"
    logger1.warning(msg)
    return HttpResponse(msg,status=400)
    
  d2=datetime.datetime.now()
  diff = (d2 - d1).total_seconds()
  msg = f"[getDynaMsg_job]done, spent : {diff} seconds"
  logger1.debug(msg)

  return HttpResponse(msg,status=200)
