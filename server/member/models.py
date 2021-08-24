# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import os

from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib import admin 

def get_image_path(instance, filename):
  return os.path.join('photos', str(instance.id), filename)

# Create your models here.
# 使用者帳號
class member(models.Model):
  SEX_TYPE = (
      ('', ''),
      ('1', '男'),
      ('2', '女'),
      ('3', '其他')
  )
  STATUS_TYPE = ( 
      ('1', '在線'),
      ('2', '忙線'),
      ('3', '離線')
  )
  uid = models.AutoField(_("UID"),primary_key=True)

  account = models.CharField(_("會員帳號"), max_length=20)
  real_name = models.CharField(_("會員姓名"), max_length=30, null=True, blank=True, default='')
  nick_name = models.CharField(_("會員暱稱"), max_length=30, null=True, blank=True, default='')
  idNo = models.CharField(_("身分證號碼"), max_length=20, null=True, blank=True, default='')
  email = models.EmailField(_("Email"), max_length=200, null=True, blank=True, default='')
  address = models.CharField(_("住址"), max_length=200, null=True, blank=True, default='')
  sex = models.CharField(_("性別"), max_length=1, choices=SEX_TYPE, null=True, blank=True, default='')
  myself = models.CharField(_("自我介紹"), max_length=200, null=True, blank=True, default='')
  photo = models.CharField(_("照片"), max_length=254, null=True, blank=True, default='')
  user_password = models.CharField(_("密碼"), max_length=20)
  fb_account = models.CharField(_("fb綁定的信箱"),  max_length=100, null=True, blank=True, default='')
  google_account = models.CharField(_("google綁定的信箱"),  max_length=100, null=True, blank=True, default='')
  qr_code = models.CharField(_("QR code"), max_length=200, null=True, blank=True, default='')
  status = models.CharField(_("狀態"), max_length=1, choices=STATUS_TYPE, null=True, blank=True, default='3')
  is_doctor = models.BooleanField(_("醫師身份"), default=False)
  is_clinic = models.BooleanField(_("診所身份"), default=False)
  is_store = models.BooleanField(_("店家身份"), default=False)

  created_date = models.DateTimeField(auto_now_add=True)
  last_login_date = models.DateTimeField(_("最後登入時間"),null=True,blank=True)
  last_modify_date = models.DateTimeField(_("最後異動時間"),null=True, blank=True)

  def __str__(self):
      return str(self.uid) + '：' + self.real_name

# 前端登入登出資料
class LoginInfo(models.Model):
  LOGIN_TYPE = (
      (0, '一般登入'),
      (1, 'google 登入'),
      (2, 'facebook 登入')
  )  
  id = models.AutoField(_("id"),primary_key=True)
  member_id = models.IntegerField(_("會員ID"), default=0)
  login_type = models.PositiveIntegerField(_("登入方式"), choices=LOGIN_TYPE, default=0)
  login_success = models.BooleanField(_("登入成功/失敗"),default=False)
  message = models.CharField(_("訊息"), max_length=200)
  login_date = models.DateTimeField(auto_now=True, verbose_name=_("登入時間"))
 
# 寵物資料
class pet(models.Model):
  CATEGORY_TYPE = ( 
      (1, '貓'),
      (2, '狗')
  )
  SEX_TYPE = (
      (1, '雄'),
      (2, '雌')
  )

  id = models.AutoField(_("寵物ID"),primary_key=True)
  member = models.ForeignKey(member, on_delete=models.CASCADE, verbose_name=_("會員ID"))
  pet_name = models.CharField(_("寵物名稱"), max_length=30, null=True, blank=True, default='')
  chip = models.CharField(_("晶片號碼"), max_length=150, null=True, blank=True, default='')
  category = models.PositiveIntegerField(_("動物別"), choices=CATEGORY_TYPE, null=True)
  breed = models.CharField(_("品種"), max_length=200, null=True, blank=True, default='')
  sex = models.PositiveIntegerField(_("性別"), choices=SEX_TYPE, null=True)
  age = models.CharField(_("年齡"), max_length=8, null=True, blank=True, default='')
  weight = models.CharField(_("體重"), max_length=8, null=True, blank=True, default='')
  description = models.CharField(_("介紹"), max_length=200, null=True, blank=True, default='')
  photo = models.CharField(_("照片"), max_length=254, null=True, blank=True, default='')
  created_date = models.DateTimeField(_("建立時間"), auto_now_add=True)
  last_modify_date = models.DateTimeField(_("最後異動時間"),null=True, blank=True)

  def __str__(self):
      return str(self.id) + '：' + self.pet_name

# 醫生資料
class doctor(models.Model):

  id = models.AutoField(_("醫生ID"),primary_key=True)
  member = models.ForeignKey(member, on_delete=models.CASCADE, verbose_name=_("會員ID"))
  doc_name = models.CharField(_("醫生姓名"), max_length=30, null=True, blank=True, default='')
  clinic = models.CharField(_("診所"), max_length=100, null=True, blank=True, default='')
  title = models.CharField(_("職稱"), max_length=100, null=True, blank=True, default='')
  skill = models.CharField(_("專長"), max_length=1000, null=True, blank=True, default='')
  experience = models.CharField(_("學經歷"), max_length=1000, null=True, blank=True, default='')
  created_date = models.DateTimeField(_("建立時間"), auto_now_add=True)
  last_modify_date = models.DateTimeField(_("最後異動時間"),null=True, blank=True)
  is_approved = models.BooleanField(_("是否已確認"), default=False)
  area = models.CharField(_("地區"), max_length=10, null=True, blank=True, default='')
  clinic_addr = models.CharField(_("診所地址"), max_length=200, null=True, blank=True, default='')
  doc_photo = models.CharField(_("醫生圖案"), max_length=254, null=True, blank=True, default='')
  room_url = models.CharField(_("醫生會議室連結"), max_length=200, null=True, blank=True, default='')
  approve_account = models.CharField(_("確認者帳號"), max_length=20, null=True, blank=True, default='')
  approve_date = models.DateTimeField(_("確認時間"),null=True, blank=True)

  def __str__(self):
      return str(self.id) + '：' + self.doc_name

  # 取得狀態
  def get_status(self):
    try:
      matched = member.objects.get(pk = self.member_id)
      return matched.status
  
    except:
      return ""

# 醫生看診資料
class docAppoint(models.Model):
  APPOINT_SECTION = (
    (1, '0-20分'),
    (2, '20-40分'),
    (3, '40-60分')
  )
  APPOINT_STATUS = (
    (1, '可預約'),
    (2, '不可預約'),
    (3, '已預約'),
    (4, '待確認')
  )

  appoint_id = models.AutoField(_("看診表ID"),primary_key=True)
  doc = models.ForeignKey(doctor, on_delete=models.CASCADE, verbose_name=_("醫生ID"))
  set_date = models.DateField(_("設定日期"))
  set_hour = models.PositiveIntegerField(_("預約時間"))
  set_section = models.PositiveIntegerField(_("預約時段"), choices=APPOINT_SECTION, default=1)
  status = models.PositiveIntegerField(_("預約狀態"), choices=APPOINT_STATUS, default=1)
  created_date = models.DateTimeField(_("建立時間"), auto_now_add=True)
  last_modify_date = models.DateTimeField(_("最後異動時間"),null=True, blank=True)

  def __str__(self):
      return str(self.appoint_id)

# 會員預約看診資料
class userAppoint(models.Model): 
  APPOINT_MARK = (
    (0, '非即時'),
    (1, '即時')
  )

  user_appoint_id = models.AutoField(_("會員預約看診ID"),primary_key=True)
  appoint = models.ForeignKey(docAppoint, on_delete=models.CASCADE, verbose_name=_("看診表ID"))
  member = models.ForeignKey(member, on_delete=models.CASCADE, verbose_name=_("會員ID"))
  pet = models.ForeignKey(pet, on_delete=models.CASCADE, verbose_name=_("寵物ID"))
  mark = models.PositiveIntegerField(_("預約註記"), choices=APPOINT_MARK, default=0)
  paid_no = models.PositiveIntegerField(_("繳費單號"), default=0)
  created_date = models.DateTimeField(_("建立時間"), auto_now_add=True)
  last_modify_date = models.DateTimeField(_("最後異動時間"),null=True, blank=True)

  def __str__(self):
      return str(self.user_appoint_id)

# 諮詢表
class advisory(models.Model): 
  advisory_id = models.AutoField(_("諮詢表ID"),primary_key=True)
  user_appoint = models.ForeignKey(userAppoint, on_delete=models.CASCADE, verbose_name=_("預約看診ID"))
  member = models.ForeignKey(member, on_delete=models.CASCADE, verbose_name=_("會員ID"))
  pet = models.ForeignKey(pet, on_delete=models.CASCADE, verbose_name=_("寵物ID"))
  doc = models.ForeignKey(doctor, on_delete=models.CASCADE, verbose_name=_("醫生ID"))
  advisory_date = models.DateField(_("諮詢日期"))
  advisory_time = models.CharField(_("時間"), max_length=20, null=True, blank=True, default='')
  fee = models.PositiveIntegerField(_("費用"), default=0)
  description = models.CharField(_("飼主描述"), max_length=1000, null=True, blank=True, default='')
  case_history = models.CharField(_("病例史"), max_length=1000, null=True, blank=True, default='')
  sympton = models.CharField(_("徵狀描述"), max_length=1000, null=True, blank=True, default='')
  suggest = models.CharField(_("諮詢建議"), max_length=1000, null=True, blank=True, default='')
  medcine = models.CharField(_("用藥"), max_length=1000, null=True, blank=True, default='')
  created_date = models.DateTimeField(_("建立時間"), auto_now_add=True)
  last_modify_date = models.DateTimeField(_("最後異動時間"),null=True, blank=True)

  def __str__(self):
      return str(self.advisory_id)

# 醫生評價資料
class docComment(models.Model):
  STAR_TYPE = (
    (1, '一顆星'),
    (2, '二顆星'),
    (3, '三顆星'),
    (4, '四顆星'),
    (5, '五顆星'),
  )
  comment_id = models.AutoField(_("評價表ID"),primary_key=True)
  member = models.ForeignKey(member, on_delete=models.CASCADE, verbose_name=_("會員ID"))
  doc = models.ForeignKey(doctor, on_delete=models.CASCADE, verbose_name=_("醫生ID"))
  advisory_id = models.PositiveIntegerField(_("諮詢表ID"), null=True,default=0)
  stars = models.PositiveIntegerField(_("評價星數"), choices=STAR_TYPE, default=5)
  memo = models.CharField(_("留言"), max_length=2000, null=True, blank=True, default='')
  user_photo = models.CharField(_("照片"), max_length=254, null=True, blank=True, default='')
  created_date = models.DateTimeField(_("建立時間"), auto_now_add=True)
  last_modify_date = models.DateTimeField(_("最後異動時間"),null=True, blank=True)

  def __str__(self):
      return str(self.comment_id)

# 醫生營業時段
class docBH(models.Model):

  bh_id = models.AutoField(_("醫生營業時段ID"),primary_key=True)
  doc = models.ForeignKey(doctor, on_delete=models.CASCADE, verbose_name=_("醫生ID"))
  bh1_name = models.CharField(_("看診時段一(起、迄)"), max_length=20, null=True, blank=True, default='')
  bh2_name = models.CharField(_("看診時段二(起、迄)"), max_length=20, null=True, blank=True, default='')
  bh3_name = models.CharField(_("看診時段三(起、迄)"), max_length=20, null=True, blank=True, default='')
  bh1_setting = models.CharField(_("看診時段一星期設定"), max_length=20, null=True, blank=True, default='')
  bh2_setting = models.CharField(_("看診時段二星期設定"), max_length=20, null=True, blank=True, default='')
  bh3_setting = models.CharField(_("看診時段三星期設定"), max_length=20, null=True, blank=True, default='')
  created_date = models.DateTimeField(_("建立時間"), auto_now_add=True)
  last_modify_date = models.DateTimeField(_("最後異動時間"),null=True, blank=True)

  def __str__(self):
      return str(self.bh_id)

# 診所資料
class clinic(models.Model):

  clinic_id = models.AutoField(_("診所ID"),primary_key=True)
  member = models.ForeignKey(member, on_delete=models.CASCADE, verbose_name=_("會員ID"))
  clinic_name = models.CharField(_("診所名稱"), max_length=100, null=True, blank=True, default='')
  area = models.CharField(_("地區"), max_length=10, null=True, blank=True, default='')
  address = models.CharField(_("診所地址"), max_length=200, null=True, blank=True, default='')
  tel = models.CharField(_("電話"), max_length=20, null=True, blank=True, default='')
  serv_content = models.CharField(_("服務內容"), max_length=200, null=True, blank=True, default='')
  desc = models.CharField(_("簡介"), max_length=200, null=True, blank=True, default='')
  email = models.CharField(_("信箱"), max_length=100, null=True, blank=True, default='')
  photo = models.CharField(_("照片"), max_length=254, null=True, blank=True, default='')
  created_date = models.DateTimeField(_("建立時間"), auto_now_add=True)
  last_modify_date = models.DateTimeField(_("最後異動時間"),null=True, blank=True)
  is_approved = models.BooleanField(_("是否已確認"), default=False)
  approve_account = models.CharField(_("確認者帳號"), max_length=20, null=True, blank=True, default='')
  approve_date = models.DateTimeField(_("確認時間"),null=True, blank=True)

  def __str__(self):
      return str(self.clinic_id) + '：' + self.clinic_name

# 診所營業時段
class clinicBH(models.Model):

  bh_id = models.AutoField(_("診所營業時段ID"),primary_key=True)
  clinic = models.ForeignKey(clinic, on_delete=models.CASCADE, verbose_name=_("診所ID"))
  bh1_name = models.CharField(_("看診時段一(起、迄)"), max_length=20, null=True, blank=True, default='')
  bh2_name = models.CharField(_("看診時段二(起、迄)"), max_length=20, null=True, blank=True, default='')
  bh3_name = models.CharField(_("看診時段三(起、迄)"), max_length=20, null=True, blank=True, default='')
  bh1_setting = models.CharField(_("看診時段一星期設定"), max_length=20, null=True, blank=True, default='')
  bh2_setting = models.CharField(_("看診時段二星期設定"), max_length=20, null=True, blank=True, default='')
  bh3_setting = models.CharField(_("看診時段三星期設定"), max_length=20, null=True, blank=True, default='')
  created_date = models.DateTimeField(_("建立時間"), auto_now_add=True)
  last_modify_date = models.DateTimeField(_("最後異動時間"),null=True, blank=True)

  def __str__(self):
      return str(self.bh_id)

# 店家資料
class store(models.Model):

  store_id = models.AutoField(_("店家ID"),primary_key=True)
  member = models.ForeignKey(member, on_delete=models.CASCADE, verbose_name=_("會員ID"))
  store_name = models.CharField(_("店家名稱"), max_length=100, null=True, blank=True, default='')
  area = models.CharField(_("地區"), max_length=10, null=True, blank=True, default='')
  address = models.CharField(_("店家地址"), max_length=200, null=True, blank=True, default='')
  tel = models.CharField(_("電話"), max_length=20, null=True, blank=True, default='')
  serv_content = models.CharField(_("服務內容"), max_length=200, null=True, blank=True, default='')
  desc = models.CharField(_("簡介"), max_length=200, null=True, blank=True, default='')
  email = models.CharField(_("信箱"), max_length=100, null=True, blank=True, default='')
  photo = models.CharField(_("照片"), max_length=254, null=True, blank=True, default='')
  created_date = models.DateTimeField(_("建立時間"), auto_now_add=True)
  last_modify_date = models.DateTimeField(_("最後異動時間"),null=True, blank=True)
  is_approved = models.BooleanField(_("是否已確認"), default=False)
  approve_account = models.CharField(_("確認者帳號"), max_length=20, null=True, blank=True, default='')
  approve_date = models.DateTimeField(_("確認時間"),null=True, blank=True)

  def __str__(self):
      return str(self.store_id) + '：' + self.store_name

# 店家營業時段
class storeBH(models.Model):

  bh_id = models.AutoField(_("店家營業時段ID"),primary_key=True)
  store = models.ForeignKey(store, on_delete=models.CASCADE, verbose_name=_("店家ID"))
  bh1_name = models.CharField(_("看診時段一(起、迄)"), max_length=20, null=True, blank=True, default='')
  bh2_name = models.CharField(_("看診時段二(起、迄)"), max_length=20, null=True, blank=True, default='')
  bh3_name = models.CharField(_("看診時段三(起、迄)"), max_length=20, null=True, blank=True, default='')
  bh1_setting = models.CharField(_("看診時段一星期設定"), max_length=20, null=True, blank=True, default='')
  bh2_setting = models.CharField(_("看診時段二星期設定"), max_length=20, null=True, blank=True, default='')
  bh3_setting = models.CharField(_("看診時段三星期設定"), max_length=20, null=True, blank=True, default='')
  created_date = models.DateTimeField(_("建立時間"), auto_now_add=True)
  last_modify_date = models.DateTimeField(_("最後異動時間"),null=True, blank=True)

  def __str__(self):
      return str(self.bh_id)

# 後台使用者帳號
class Account(models.Model):
  LEVEL_TYPE = (
      ("1", "一般客服"),
      ("2", "客服主管"),
      ("8", "系統主管"),
      ("9", "工程師")
  )
  user_id = models.AutoField(_("ID"),primary_key=True)

  user_account = models.CharField(_("帳號"), max_length=20)
  user_password = models.CharField(_("密碼"), max_length=20)
  user_name = models.CharField(_("名稱"), max_length=50)
  level = models.CharField(_("系統身份"), max_length=1, choices=LEVEL_TYPE, default='8')

  create_user = models.CharField(_("創建者帳號"), max_length=20)
  created_date = models.DateTimeField(auto_now_add=True)
  last_login_date = models.DateTimeField(_("最後登入時間"),blank=True,null=True)
  modify_user = models.CharField(_("異動者帳號"),max_length=20)
  last_modify_date = models.DateTimeField(_("最後異動時間"),null=True, blank=True)

  is_delete = models.BooleanField(_("是否被刪除"), default=False)
  deleted_user = models.CharField(_("刪除者帳號"),max_length=20, null=True, blank=True)
  deleted_date = models.DateTimeField(_("帳號刪除時間"),blank=True,null=True)

  def __str__(self):
      return str(self.user_id) + '：' + self.user_account

# 後台系統登入登出資料
class BKLoginInfo(models.Model): 
  id = models.AutoField(_("id"),primary_key=True)
  account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=_("登入帳號ID"))
  login_success = models.BooleanField(_("登入成功/失敗"),default=False)
  message = models.CharField(_("訊息"), max_length=200)
  login_date = models.DateTimeField(auto_now=True, verbose_name=_("登入時間"))

# 動態資料：資料來源外call api 取得
class dynaPost(models.Model):

  post_id = models.CharField(_("貼文ID"),max_length=20, primary_key=True)
  post_published = models.DateTimeField(_("發佈時間"),null=True, blank=True)
  post_created_at = models.DateTimeField(_("貼文建立時間"),null=True, blank=True)
  post_update_at = models.DateTimeField(_("貼文最後異動時間"),null=True, blank=True)
  post_content = models.CharField(_("標題"), max_length=150, null=True, blank=True, default='')
  post_decription = models.TextField(_("貼文"), null=True, blank=True, default='')
  post_picture = models.CharField(_("照片"), max_length=254, null=True, blank=True, default='')
  post_url = models.CharField(_("貼文url"), max_length=254, null=True, blank=True, default='')
  post_like = models.IntegerField(_("按讚次數"), default=0)
  post_views = models.IntegerField(_("已讀次數"), default=0)
  page_provider = models.CharField(_("資料來源"), max_length=150, null=True, blank=True, default='')
  page_name = models.CharField(_("page_name"), max_length=150, null=True, blank=True, default='')
  page_icon = models.CharField(_("page_icon"), max_length=254, null=True, blank=True, default='')
	
  created_date = models.DateTimeField(_("DB建立時間"), auto_now_add=True)
  last_modify_date = models.DateTimeField(_("最後異動時間"),null=True, blank=True)

  def __str__(self):
      return self.post_id + '：' + self.post_content

# 用戶動態資料按讚紀錄
class MemberLikePost(models.Model):
  LIKE_TYPE = (
    (0, 'None'),
    (1, 'like'),
    (2, 'dislike')
  )  
  id = models.AutoField(_("likeId"),primary_key=True)
  member = models.ForeignKey(member, on_delete=models.CASCADE, verbose_name=_("會員ID"))
  post_id = models.ForeignKey(dynaPost, on_delete=models.CASCADE, verbose_name=_("貼文ID"))
  isLike = models.PositiveIntegerField(_("是否喜歡"), choices=LIKE_TYPE, default=0)
	
  created_date = models.DateTimeField(_("建立時間"), auto_now_add=True)
  last_modify_date = models.DateTimeField(_("最後異動時間"),null=True, blank=True)

  def __str__(self):
      return str(self.id) + '：(member_id:' + str(self.member_id) + ',post_id:' + self.post_id_id + ')'

class SocialAccount(models.Model):
    provider = models.CharField(max_length=200, default='google') # 若未來新增其他的登入方式,如Facebook,GitHub...
    unique_id = models.CharField(max_length=200)
    user = models.ForeignKey(
        User, related_name='social', on_delete=models.CASCADE)
    member_id = models.IntegerField(_("會員ID"), default=0)

class test(models.Model):
    provider = models.CharField(max_length=200, default='google') # 若未來新增其他的登入方式,如Facebook,GitHub...
    unique_id = models.CharField(max_length=200)
    member_id = models.IntegerField(_("會員ID"), default=0)

class mytest(models.Model):
    provider = models.CharField(max_length=200, default='google') # 若未來新增其他的登入方式,如Facebook,GitHub...
    unique_id = models.CharField(max_length=200)
    member_id = models.IntegerField(_("會員ID"), default=0)