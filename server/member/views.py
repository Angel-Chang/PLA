# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime, timedelta
from django.db.models import Count, aggregates, Sum, Q, Max, Avg
#
from django.forms import ModelForm
from django.views import View

from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from django.views.decorators.clickjacking import xframe_options_exempt

from rest_framework import generics, status, mixins, viewsets
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView

from member.models import *
from member.serializers import *

import uuid , calendar, requests
import decimal
import logging
import sys
import traceback

from django import forms
from member.forms import LoginForm
from django.shortcuts import render, redirect

from django.http import HttpResponse, Http404, JsonResponse

logger1 = logging.getLogger('member.views')

# Create your views here.
class Helpers():
    # 新增 Django user record
    def NewUser(self, username, password):
        user = User.objects.create_user(username=username , password =password)
        return user

    # 新增 Django user record
    def UpdateUserPassword(self, username, password):
        msg = ""
        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            msg = "success"

        except user.DoesNotExist:
            msg = f"User:{username} doesn't exist!"

        return msg

    # 新增前端登入記錄
    def addLoginData(self, member_id, login_type, login_success, message):
       # Insert data 
        createdObj = LoginInfo.objects.create(
            member_id = member_id,
            login_type = login_type,
            login_success = login_success,
            message = message
        )
        return createdObj
    # 計算醫生評價
    def calDocStar(self, doc_id):
       
        avg_star = docComment.objects.filter(doc_id=doc_id).aggregate(Avg('stars'))['stars__avg']
        if avg_star is None:
            return 0

        return int(avg_star)

    # 取得診所當日營業時段
    def getClinicTodayBH(self, clinic_id):
        bh = ""
        
        msg = ""
        try:
            matched = clinicBH.objects.get(clinic_id = clinic_id)
            bh1_name = matched.bh1_name
            bh2_name = matched.bh2_name
            bh3_name = matched.bh3_name
            bh1 = matched.bh1_setting.split(',')
            bh2 = matched.bh2_setting.split(',')
            bh3 = matched.bh3_setting.split(',')
            msg = f"[getClinicTodayBH]bh1:({bh1}) ,bh2:({bh2}) ,bh3:({bh3}) "
            logger1.warning(msg)
            # 當日是星期幾，星期一是0，星期天是6
            # business hour是星期天為0，星期六是6
            week = datetime.datetime.today().weekday()
            msg = f"[getClinicTodayBH]weekday:{week} "
            logger1.warning(msg)
            if week == 6:
                week = 0
            else:
                week = week + 1
            msg = f"[getClinicTodayBH]adjust weekday:{week} "
            logger1.warning(msg)                
            # 取出對應的星期設定
            now_bh1 = bh1[week]
            now_bh2 = bh2[week]
            now_bh3 = bh3[week]
            msg = f"[getClinicTodayBH]now_bh1:({now_bh1}) ,now_bh2:({now_bh2}) ,now_bh3:({now_bh3}) "
            logger1.warning(msg)

            bh = f"{bh1_name},{now_bh1},{bh2_name},{now_bh2},{bh3_name},{now_bh3}"
            msg = f"[getClinicTodayBH]bh:({bh})"
            logger1.warning(msg)

        except clinicBH.DoesNotExist:
            msg = f"[getClinicTodayBH]The clinic_id({clinic_id}) 尚未設定看診時間!!"
            logger1.warning(msg)

        return bh

    # 取得診所當日營業時段
    def getStoreTodayBH(self, store_id):
        bh = ""
        
        msg = ""
        try:
            matched = storeBH.objects.get(store_id = store_id)
            bh1_name = matched.bh1_name
            bh2_name = matched.bh2_name
            bh3_name = matched.bh3_name
            bh1 = matched.bh1_setting.split(',')
            bh2 = matched.bh2_setting.split(',')
            bh3 = matched.bh3_setting.split(',')
            msg = f"[getStoreTodayBH]bh1:({bh1}) ,bh2:({bh2}) ,bh3:({bh3}) "
            logger1.warning(msg)
            # 當日是星期幾，星期一是0，星期天是6
            # business hour是星期天為0，星期六是6
            week = datetime.datetime.today().weekday()
            msg = f"[getStoreTodayBH]weekday:{week} "
            logger1.warning(msg)
            if week == 6:
                week = 0
            else:
                week = week + 1
            msg = f"[getStoreTodayBH]adjust weekday:{week} "
            logger1.warning(msg)                
            # 取出對應的星期設定
            now_bh1 = bh1[week]
            now_bh2 = bh2[week]
            now_bh3 = bh3[week]
            msg = f"[getStoreTodayBH]now_bh1:({now_bh1}) ,now_bh2:({now_bh2}) ,now_bh3:({now_bh3}) "
            logger1.warning(msg)

            bh = f"{bh1_name},{now_bh1},{bh2_name},{now_bh2},{bh3_name},{now_bh3}"
            msg = f"[getStoreTodayBH]bh:({bh})"
            logger1.warning(msg)

        except storeBH.DoesNotExist:
            msg = f"[getStoreTodayBH]The store_id({store_id}) 尚未設定看診時間!!"
            logger1.warning(msg)

        return bh

    def getDocStars(self, advisory_id):
        stars = 0

        try:
            matched = docComment.objects.get(advisory_id=advisory_id)
            stars = matched.stars

        except docComment.DoesNotExist:
            pass
        return stars

    # 新增後台系統登入記錄
    def addBKLoginData(self, user_id, isSuccess, msg):
       # Insert data 
        createdObj = BKLoginInfo.objects.create(
            account_id = user_id,
            login_success = isSuccess,
            message = msg
        )
        return createdObj

# register new member
class AddMemberView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    #permission_classes = (IsAuthenticated,)
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        result = {}
        code = -1
        msg = ""
        uid = -1
        if serializer.is_valid():
            account = serializer.validated_data.get('account')
            user_password = serializer.validated_data.get('user_password')

            # Check account exists or not
            if member.objects.filter(account=account).count() != 0:
                code = -1
                msg = f"會員帳號[{account}] 已經存在."
              #return Response("會員帳號[%s] 已經存在." % account, status=status.HTTP_400_BAD_REQUEST)
            else:
                # save data into DB
                post_instance = serializer.save()
                # 將資料寫入到Django user object
                Helpers().NewUser(account,user_password)

                uid = post_instance.uid
                code = 0
                msg = "success"
            #serializer1 = RegisterSerializer(post_instance, context={'request': request})
            #return Response(serializer1.data)
        else:
            #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            code = -1
            msg = serializer.errors
        
        if code == 0:
            result = {
                "code": code,
                "msg" : msg,
                "uid" : uid
            }
            return JsonResponse(result, safe=False)
        else:
            result = {
                "code": code,
                "msg": msg
            }
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# reset member password
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UpdatePasswordSerializer
    #permission_classes = (IsAuthenticated,)
    
    def put(self, request, format=None):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        result = {}
        code = -1
        msg = ""
        if serializer.is_valid():
            uid = serializer.validated_data.get('uid')
            new_password = serializer.validated_data.get('new_password')

            try:
                matched = member.objects.get(uid=uid)
                account = matched.account
                matched.user_password = new_password
                matched.last_modify_date = datetime.datetime.now()
                matched.save()
                # 需要連同 User資料表的密碼一同更新(因為關係到取 token 時需要用到)
                msg = Helpers().UpdateUserPassword(account,new_password)
                if msg == "success":
                    code = 0
                else:
                    code = -1

            except member.DoesNotExist:
                code = -1
                msg = f"The uid:{uid} 不存在."
        else:
            code = -1
            msg = serializer.errors

        result = {
            "code": code,
            "msg" : msg
        }
        if code == 0:
            return JsonResponse(result, safe=False)
        else:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# get uid by account
def get_member_uid(request):
    if request.method == 'GET':
        account = request.GET.get("username",None)
        result = {}
        code = -1
        msg = ""
        uid = -1
        if account is not None and len(account) > 0:
            try:
                matched = member.objects.get(account=account)
                uid = matched.uid
                code = 0
                msg = "success"

            except member.DoesNotExist:
                code =-1
                msg = f"會員帳號:{account} 不存在."            
        else:
            msg = "Need account data!"

        if code == 0:
            result = {
                "code": code,
                "msg" : msg,
                "uid" : uid
            }
            return JsonResponse(result, safe=False)
        else:
            result = {
                "code": code,
                "msg": msg
            }
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# login
class LoginView(APIView):
    #permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    permission_classes = (IsAuthenticated,)

    # login_method : 
    #   0 : 一般登入
    #   1 : google 登入，2021/07/17 canceled
    #   2 : facebook 登入，2021/07/17 canceled
    def get(self, request, format=None):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        result = {}
        code = -1
        msg = ""
        uid = -1
        if serializer.is_valid():
            account = serializer.validated_data.get('account')
            login_type = serializer.validated_data.get('login_type')
            in_password = serializer.validated_data.get('user_password')

            try:
                # 一般登入比對帳號、密碼
                if login_type == 0:
                    matched1 = member.objects.get(account=account)
                    user_pwd = matched1.password
                    if user_pwd != in_password:
                        msg = f"帳號 {account} 密碼錯誤！"
                    else:
                        uid = matched1.uid
                # google 登入:比對 google綁定的信箱
                # elif login_type == 1:
                #     matched2 = member.objects.get(google_account=account)
                #     uid = matched2.uid
                # # facebook 登入:比對 facebook綁定的信箱
                # elif login_type == 2:
                #     matched3 = member.objects.get(fb_account=account)
                #     uid = matched3.uid
                else:
                    msg = "非支援的登入方式！"

                if len(msg) == 0:
                    code = 0
                    msg = "success"

            except member.DoesNotExist:
                code = -1
                msg = f"會員帳號:{account} 不存在."
        else:
            code = -1
            msg = serializer.errors

        if code == 0:
            result = {
                "code": code,
                "msg" : msg,
                "uid" : uid
            }
            # 新增登入記錄
            Helpers().addLoginData(uid,login_type,True,msg)

            return JsonResponse(result, safe=False)
        else:
            result = {
                "code": code,
                "msg": msg
            }
            # 新增登入記錄
            Helpers().addLoginData(uid,login_type,False,msg)

            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 取得會員資料
class GetMemberInfoView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        uid = request.GET.get("uid",None)

        success = False
        error = ""
        result = {}
        if uid is not None:
            try:
                matched = member.objects.get(uid=uid)
                if matched.photo is not None and len(matched.photo) > 0:
                    image_path = f"{settings.IMAGE_URL}member/{uid}/"
                    logger1.warning(image_path)
                    imagefile = os.path.join(image_path,matched.photo)
                    matched.photo = imagefile

                serializer = MemberSerializer(matched, context={'request': request})

                success = True
                result["data"] = serializer.data
            except member.DoesNotExist:
                error = f"The uid:{uid} 不存在."

            result["success"] = success
            if len(error) > 0:
                result["error"] = error
        else:
            success = False
            result["error"] = "Need uid data!"

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 更新會員資料
class UpdateMemberView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MemberSerializer
    
    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        serializer = self.serializer_class(data=request.data)
        msg = ""
        if serializer.is_valid():
            uid = serializer.validated_data.get('uid')
            account = serializer.validated_data.get('account')
            real_name = serializer.validated_data.get('real_name')
            nick_name = serializer.validated_data.get('nick_name')
            idNo = serializer.validated_data.get('idNo')
            email = serializer.validated_data.get('email')
            address = serializer.validated_data.get('address')
            sex = serializer.validated_data.get('sex')
            myself = serializer.validated_data.get('myself')
            mystatus = serializer.validated_data.get('status')
            is_doctor = serializer.validated_data.get('is_doctor')
            is_clinic = serializer.validated_data.get('is_clinic')
            is_store = serializer.validated_data.get('is_store')

            try:
                matched = member.objects.get(uid=uid)
                # matched.account = account
                matched.real_name = real_name
                matched.nick_name = nick_name
                matched.idNo = idNo
                matched.email = email
                matched.address = address
                matched.sex = sex
                matched.myself = myself
                matched.status = mystatus
                matched.is_doctor = is_doctor
                matched.is_clinic = is_clinic
                matched.is_store = is_store

                matched.last_modify_date = datetime.datetime.now()
                matched.save()

                # 檢查姓名是否有修改，同步更新醫生的姓名
                isDoc = doctor.objects.filter(member_id=uid).exists()
                if isDoc:
                    matchedDoc = doctor.objects.get(member_id=uid)
                    if matchedDoc.doc_name != real_name:
                        matchedDoc.doc_name = real_name
                        matchedDoc.last_modify_date = datetime.datetime.now()
                        matchedDoc.save()

                image = request.FILES.get("image", None)

                if not image:
                    msg = f"No image upload~"
                    logger1.warning(msg)
                else:
                    image_path = f"{settings.IMAGE_ROOT}/member/{uid}/"
                    logger1.warning(image_path)
                    if not os.path.exists(image_path):
                        os.makedirs(image_path)
                    destination = open(os.path.join(image_path,image.name),'wb+')
                    for chunk in image.chunks():
                        destination.write(chunk)
                    destination.close()
                    matched.photo = image.name
                    matched.save()

                success = True
            except member.DoesNotExist:
                success = False
                error = f"The uid:{uid} 不存在."

        else:
            success = False
            error = serializer.errors

        result["success"] = success
        if len(error) > 0:
            result["error"] = error

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 新增寵物資料
class AddPetInfoView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NewPetSerializer
    
    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        serializer = self.serializer_class(data=request.data)
        id = -1
        msg = ""
        if serializer.is_valid():
            member_id = serializer.validated_data.get('member_id')
            # 檢查會員ID是否存在
            if member.objects.filter(uid=member_id).count() == 0:
                success = False
                error = f"會員ID {member_id} 不存在!!"
            else:
                pet_name = serializer.validated_data.get('pet_name')
                chip = serializer.validated_data.get('chip')
                category = serializer.validated_data.get('category')
                breed = serializer.validated_data.get('breed')
                sex = serializer.validated_data.get('sex')
                age = serializer.validated_data.get('age')
                weight = serializer.validated_data.get('weight')
                description = serializer.validated_data.get('description')

                # save data into DB
                post_instance = serializer.save()
                id = post_instance.id

                # save photo
                image = request.FILES.get("image", None)
                if not image:
                    msg = f"No image upload~"
                    logger1.warning(msg)
                else:
                    image_path = f"{settings.IMAGE_ROOT}/member/{member_id}/pet/"
                    logger1.warning(image_path)
                    if not os.path.exists(image_path):
                        os.makedirs(image_path)
                    destination = open(os.path.join(image_path,image.name),'wb+')
                    for chunk in image.chunks():
                        destination.write(chunk)
                    destination.close()
                    post_instance.photo = image.name
                    post_instance.save()
                
                success = True
            
        else:
            success = False
            error = serializer.errors
        
        result["success"] = success
        if len(error) > 0:
            result["error"] = error
        else:
            result["id"] = id

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 取得寵物資料
class GetPetInfoView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        pet_id = request.GET.get("id",None)
        msg = f"[GetPetInfoView(getPetInfo)]1.start,pet_id:{pet_id}"
        logger1.warning(msg)
        success = False
        error = ""
        result = {}
        if pet_id is not None:
            try:
                matched = pet.objects.get(id=pet_id)
                member_id = matched.member_id
                if matched.photo is not None and len(matched.photo) > 0:
                    image_path = f"{settings.IMAGE_URL}member/{member_id}/pet/"
                    logger1.warning(image_path)
                    imagefile = os.path.join(image_path,matched.photo)
                    matched.photo = imagefile

                serializer = PetSerializer(matched, context={'request': request})

                success = True
                result["data"] = serializer.data
            except pet.DoesNotExist:
                error = f"The id:{pet_id} 不存在."

            result["success"] = success
            if len(error) > 0:
                result["error"] = error
        else:
            success = False
            result["error"] = "Need id data!"

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 更新寵物資料
class UpdatePetInfoView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PetSerializer
    
    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        serializer = self.serializer_class(data=request.data)
        msg = ""
        if serializer.is_valid():
            id = serializer.validated_data.get('id')
            member_id = serializer.validated_data.get('member_id')
            pet_name = serializer.validated_data.get('pet_name')
            chip = serializer.validated_data.get('chip')
            category = serializer.validated_data.get('category')
            breed = serializer.validated_data.get('breed')
            sex = serializer.validated_data.get('sex')
            age = serializer.validated_data.get('age')
            weight = serializer.validated_data.get('weight')
            description = serializer.validated_data.get('description')

            try:
                matched = pet.objects.get(id=id)
                matched.member_id = member_id
                matched.pet_name = pet_name
                matched.chip = chip
                matched.category = category
                matched.breed = breed
                matched.sex = sex
                matched.age = age
                matched.weight = weight
                matched.description = description
                matched.last_modify_date = datetime.datetime.now()
                matched.save()

                image = request.FILES.get("image", None)

                if not image:
                    msg = f"No image upload~"
                    logger1.warning(msg)
                else:
                    image_path = f"{settings.IMAGE_ROOT}/member/{member_id}/pet/"
                    logger1.warning(image_path)
                    if not os.path.exists(image_path):
                        os.makedirs(image_path)
                    destination = open(os.path.join(image_path,image.name),'wb+')
                    for chunk in image.chunks():
                        destination.write(chunk)
                    destination.close()
                    matched.photo = image.name
                    matched.save()

                success = True
            except pet.DoesNotExist:
                success = False
                error = f"The id:{id} 不存在."

        else:
            success = False
            error = serializer.errors

        result["success"] = success
        if len(error) > 0:
            result["error"] = error

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 獲得寵物清單資料
class GetPetListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        member_id = request.GET.get("member_id",None)
        msg = f"[GetPetListView(getPetList)]1.start,member_id:{member_id}"
        logger1.warning(msg)
        success = False
        error = ""
        result = {}
        if member_id is not None:
            filters = Q()
            filters.children.append(("member_id",member_id))
            try:
                ret1 = pet.objects.filter(filters).order_by('pet_name')
                data = []
                
                for d1 in ret1:
                    rs1 = {}
                    photo = ""
                    rs1['pet_id'] = d1.id
                    rs1['pet_name'] = d1.pet_name
                    if d1.photo is not None and len(d1.photo) > 0:
                        image_path = f"{settings.IMAGE_URL}member/{member_id}/pet/"
                        logger1.warning(image_path)
                        imagefile = os.path.join(image_path,d1.photo)
                        photo = imagefile

                    rs1['photo'] = photo

                    data.append(rs1)

                success = True
                result["data"] = data

                if ret1.count() == 0:
                    error = f"查無資料!"

            except Exception as e:
                success = False
                error_class = e.__class__.__name__ #取得錯誤類型
                detail = e.args[0] #取得詳細內容
                cl, exc, tb = sys.exc_info() #取得Call Stack
                lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
                fileName = lastCallStack[0] #取得發生的檔案名稱
                lineNum = lastCallStack[1] #取得發生的行號
                funcName = lastCallStack[2] #取得發生的函數名稱
                error = f"[GetPetListView(getPetList)]File :{fileName}, line {lineNum}, in {funcName}: [{error_class}] {detail}"
                logger1.warning(error)

            result["success"] = success
            if len(error) > 0:
                result["error"] = error
        else:
            success = False
            result["error"] = "需要用戶ID!"

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 新增醫生資料
class AddDoctorInfoView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NewDoctorSerializer
    
    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        serializer = self.serializer_class(data=request.data)
        id = -1
        msg = ""
        if serializer.is_valid():
            member_id = serializer.validated_data.get('member_id')
            isExist1 = member.objects.filter(uid=member_id).exists()
            isExist2 = doctor.objects.filter(member_id=member_id).exists()
            # 檢查會員ID是否存在
            if not isExist1:
                success = False
                error = f"會員ID {member_id} 不存在!!"
            elif isExist2:
                success = False
                error = f"此會員(ID:{member_id})醫師資料已存在!!"                
            else:
                matched = member.objects.get(uid=member_id)
                doc_name = matched.real_name
                clinic = serializer.validated_data.get('clinic')
                title = serializer.validated_data.get('title')
                skill = serializer.validated_data.get('skill')
                experience = serializer.validated_data.get('experience')
                area = serializer.validated_data.get('area')
                clinic_addr = serializer.validated_data.get('clinic_addr')

                # save data into DB
                post_instance = serializer.save()
                id = post_instance.id
                post_instance.doc_name = doc_name
                post_instance.save()

                # save photo
                image = request.FILES.get("image", None)
                if not image:
                    msg = f"No image upload~"
                    logger1.warning(msg)
                else:
                    image_path = f"{settings.IMAGE_ROOT}/member/{member_id}/"
                    logger1.warning(image_path)
                    if not os.path.exists(image_path):
                        os.makedirs(image_path)
                    destination = open(os.path.join(image_path,image.name),'wb+')
                    for chunk in image.chunks():
                        destination.write(chunk)
                    destination.close()
                    post_instance.doc_photo = image.name
                    post_instance.save()

                success = True
        else:
            success = False
            error = serializer.errors
        
        result["success"] = success
        if len(error) > 0:
            result["error"] = error
        else:
            result["id"] = id

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 取得醫生資料
class GetDoctorInfoView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        member_id = request.GET.get("member_id",None)
        success = False
        error = ""
        result = {}
        if member_id is not None:
            try:
                matched = doctor.objects.get(member_id=member_id)
                if matched.doc_photo is not None and len(matched.doc_photo) > 0:
                    image_path = f"{settings.IMAGE_URL}member/{member_id}/"
                    logger1.warning(image_path)
                    imagefile = os.path.join(image_path,matched.doc_photo)
                    matched.doc_photo = imagefile

                # 檢查若是取到的doc_name 若為空白，則到member再取一次並更新到doctor資料表
                if matched.doc_name == '':
                    memberData = member.objects.get(uid=member_id)
                    real_name = memberData.real_name
                    if real_name != '':
                        matched.doc_name = real_name
                        matched.last_modify_date = datetime.datetime.now()
                        matched.save()

                serializer = DoctorSerializer(matched, context={'request': request})

                success = True
                result["data"] = serializer.data
            except doctor.DoesNotExist:
                error = f"The member id:{member_id} doesn't have doctor data!!"

            result["success"] = success
            if len(error) > 0:
                result["error"] = error
        else:
            success = False
            result["error"] = "Need member_id data!"

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 更新醫生資料
class UpdateDoctorInfoView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DoctorSerializer
    
    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        serializer = self.serializer_class(data=request.data)
        msg = ""
        if serializer.is_valid():
            id = serializer.validated_data.get('id')
            clinic = serializer.validated_data.get('clinic')
            title = serializer.validated_data.get('title')
            skill = serializer.validated_data.get('skill')
            experience = serializer.validated_data.get('experience')
            area = serializer.validated_data.get('area')
            clinic_addr = serializer.validated_data.get('clinic_addr')

            try:
                matched = doctor.objects.get(id=id)
                matched.clinic = clinic
                matched.title = title
                matched.skill = skill
                matched.experience = experience
                matched.area = area
                matched.clinic_addr = clinic_addr
                member_id = matched.member_id
                matched.last_modify_date = datetime.datetime.now()
                matched.save()

                image = request.FILES.get("image", None)

                if not image:
                    msg = f"No image upload~"
                    logger1.warning(msg)
                else:
                    image_path = f"{settings.IMAGE_ROOT}/member/{member_id}/"
                    logger1.warning(image_path)
                    if not os.path.exists(image_path):
                        os.makedirs(image_path)
                    destination = open(os.path.join(image_path,image.name),'wb+')
                    for chunk in image.chunks():
                        destination.write(chunk)
                    destination.close()
                    matched.doc_photo = image.name
                    matched.save()

                success = True
            except doctor.DoesNotExist:
                success = False
                error = f"The id:{id} 不存在."

        else:
            success = False
            error = serializer.errors

        result["success"] = success
        if len(error) > 0:
            result["error"] = error

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 取得所有醫生清單資料
class getDocListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        msg = f"[getDocListView(getDocList)]1.start"
        logger1.warning(msg)
        success = False
        error = ""
        result = {}
        ret1 = doctor.objects.filter(is_approved=True)
        data = []

        for d1 in ret1:
            rs1 = {}
            doc_photo = ""
            rs1['doc_id'] = d1.id
            rs1['member_id'] = d1.member_id
            rs1['doc_name'] = d1.doc_name
            rs1['clinic'] = d1.clinic
            rs1['area'] = d1.area
            rs1['title'] = d1.title
            rs1['skill'] = d1.skill
            rs1['star'] = Helpers().calDocStar(d1.id)
            rs1['status'] = d1.get_status()
            rs1['room_url'] = d1.room_url

            member_id = d1.member_id
            if d1.doc_photo is not None and len(d1.doc_photo) > 0:
                image_path = f"{settings.IMAGE_URL}member/{member_id}/"
                logger1.warning(image_path)
                imagefile = os.path.join(image_path,d1.doc_photo)
                doc_photo = imagefile

            rs1['doc_photo'] = doc_photo

            data.append(rs1)

        success = True
        result["data"] = data

        if ret1.count() == 0:
            error = f"查無資料!"
        
        result["success"] = success
        if len(error) > 0:
            result["error"] = error

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 建立醫生看診時間表
class AddDocAppointView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NewDocAppointSerializer
    
    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        serializer = self.serializer_class(data=request.data)
        appoint_id = 0
        msg = ""

        if serializer.is_valid():
            doc_id = serializer.validated_data.get('doc_id')
            set_date = serializer.validated_data.get('set_date')
            set_hour = serializer.validated_data.get('set_hour')
            set_section = serializer.validated_data.get('set_section')
            status1 = serializer.validated_data.get('status')
            # 檢查醫生看診資料是否已存在
            filters = Q()
            filters.children.append(("doc_id",doc_id))
            filters.children.append(("set_date",set_date))
            filters.children.append(("set_hour",set_hour))
            filters.children.append(("set_section",set_section))
            isExist = docAppoint.objects.filter(filters).exists()
            if isExist:
                success = False
                error = f"此筆醫生看診資料已存在!!"
            elif set_hour > 23:
                success = False
                error = f"時間格式錯誤!!"
            else:
                # save data into DB
                post_instance = serializer.save()
                appoint_id = post_instance.appoint_id
                post_instance.last_modify_date = datetime.datetime.now()
                post_instance = serializer.save()
                success = True
            
        else:
            success = False
            error = serializer.errors
        
        result["success"] = success
        if len(error) > 0:
            result["error"] = error
        else:
            result["appoint_id"] = appoint_id

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 更新醫生看診時間表
class UpdateDocAppointView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdDocAppointSerializer

    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        msg = ""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            appoint_id = serializer.validated_data.get('appoint_id')
            status1 = serializer.validated_data.get('status')

            if status1 is not None and status1 not in range(1,4):
                success = False
                error = f"狀態代碼錯誤，僅能為 1~3"
            else:
                # 檢查醫生看診資料是否已存在
                try:
                    matched = docAppoint.objects.get(appoint_id=appoint_id)
                    matched.status = status1
                    matched.last_modify_date = datetime.datetime.now()
                    matched.save()
                    success = True
                except docAppoint.DoesNotExist:
                    success = False
                    error = f"看診表ID:{appoint_id} 不存在!"

        else:
            success = False
            error = serializer.errors

        result["success"] = success
        if len(error) > 0:
            result["error"] = error

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 用戶獲得看診時間表
class GetDocAppointView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        doc_id = request.GET.get("doc_id",None)
        msg = f"[GetDocAppointView(getDocAppoint)]1.start,doc_id:{doc_id}"
        logger1.warning(msg)
        success = False
        error = ""
        result = {}
        if doc_id is not None:
            try:
                # 檢查醫生看診資料是否已存在
                filters = Q()
                filters.children.append(("doc_id",doc_id))
                # 只抓今日之後的醫生看診資料
                today = datetime.date.today()
                filters.children.append(("set_date__gte",today))
                queryset = docAppoint.objects.filter(filters).order_by('set_date')
                serializer = DocAppointSerializer(queryset, many=True, context={'request': request})

                if queryset.count() == 0:
                    success = True
                    error = f"查無資料!"
                else:
                    success = True
                    result["data"] = serializer.data

            except Exception as e:
                success = False
                error_class = e.__class__.__name__ #取得錯誤類型
                detail = e.args[0] #取得詳細內容
                cl, exc, tb = sys.exc_info() #取得Call Stack
                lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
                fileName = lastCallStack[0] #取得發生的檔案名稱
                lineNum = lastCallStack[1] #取得發生的行號
                funcName = lastCallStack[2] #取得發生的函數名稱
                error = f"[GetDocAppointView(getDocAppoint)]File :{fileName}, line {lineNum}, in {funcName}: [{error_class}] {detail}"
                logger1.warning(error)
                
            result["success"] = success
            if len(error) > 0:
                result["error"] = error
        else:
            success = False
            result["error"] = "需要醫生ID!"

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 建立用戶看診時間表
class AddUserAppointView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NewUserAppointSerializer
    
    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        serializer = self.serializer_class(data=request.data)
        msg = ""
        status = 4
        user_appoint_id = 0
        if serializer.is_valid():
            appoint_id = serializer.validated_data.get('appoint_id')
            member_id = serializer.validated_data.get('member_id')
            pet_id = serializer.validated_data.get('pet_id')
            mark = serializer.validated_data.get('mark')

            # save data into DB
            post_instance = serializer.save()
            user_appoint_id = post_instance.user_appoint_id
            matched = docAppoint.objects.get(appoint_id=appoint_id)
            now_status = matched.status
            if now_status == 1:  # 可預約
                if mark == 0:   # 非即時單
                    matched.status = 4 # 待確認
                    matched.last_modify_date = datetime.datetime.now()
                    matched.save()
                    status = matched.status
                elif mark == 1:   # 即時單
                    matched.status = 3 # 已預約
                    matched.last_modify_date = datetime.datetime.now()
                    matched.save()
                    status = matched.status
                success = True
            elif now_status == 2: # 不可預約
                success = False    
                error = "此時間時段不可預約!"
            elif now_status == 3: # 已預約
                success = False    
                error = "此時間時段已被預約!"
            elif now_status == 4: # 待確認
                success = False    
                error = "此時間時段已被預約待確認中!"
        else:
            success = False
            error = serializer.errors
        
        result["success"] = success
        if len(error) > 0:
            result["error"] = error
        else:
            result["user_appoint_id"] = user_appoint_id
            result["status"] = status

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 建立諮詢表
class AddAdvisoryView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NewAdvisorySerializer
    
    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        serializer = self.serializer_class(data=request.data)
        advisory_id = 0
        msg = ""

        if serializer.is_valid():
            user_appoint_id = serializer.validated_data.get('user_appoint_id')
            # 檢查醫生看診資料是否已存在
            filters = Q()
            filters.children.append(("user_appoint_id",user_appoint_id))
            isExist = advisory.objects.filter(filters).exists()
            if isExist:
                success = False
                error = f"此筆諮詢表資料已存在!!"
            else:
                # save data into DB
                post_instance = serializer.save()
                advisory_id = post_instance.advisory_id
                post_instance.last_modify_date = datetime.datetime.now()
                post_instance = serializer.save()
                success = True
            
        else:
            success = False
            error = serializer.errors
        
        result["success"] = success
        if len(error) > 0:
            result["error"] = error
        else:
            result["advisory_id"] = advisory_id

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 更新諮詢表
class UpdateAdvisoryView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AdvisorySerializer

    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        msg = ""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            advisory_id = serializer.validated_data.get('advisory_id')
            description = serializer.validated_data.get('description')
            case_history = serializer.validated_data.get('case_history')
            sympton = serializer.validated_data.get('sympton')
            suggest = serializer.validated_data.get('suggest')
            medcine = serializer.validated_data.get('medcine')
             
            try:
                matched = advisory.objects.get(advisory_id=advisory_id)
                matched.description = description
                matched.case_history = case_history
                matched.sympton = sympton
                matched.suggest = suggest
                matched.medcine = medcine
                matched.last_modify_date = datetime.datetime.now()
                matched.save()
                success = True
            except advisory.DoesNotExist:
                success = False
                error = f"諮詢表ID:{advisory_id} 不存在!"

        else:
            success = False
            error = serializer.errors

        result["success"] = success
        if len(error) > 0:
            result["error"] = error

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 獲得諮詢表明細
class GetAdvisoryDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        advisory_id = request.GET.get("advisory_id",None)
        msg = f"[GetAdvisoryDetailView(getAdvisoryDetail)]1.start,advisory_id:{advisory_id}"
        logger1.warning(msg)
        success = False
        error = ""
        result = {}
        if advisory_id is not None:
            try:
                matched = advisory.objects.get(advisory_id=advisory_id)
                serializer = AdvisoryDetailSerializer(matched, context={'request': request})
                success = True
                result["data"] = serializer.data
            except advisory.DoesNotExist:
                error = f"諮詢表ID:{advisory_id} 不存在."

            result["success"] = success
            if len(error) > 0:
                result["error"] = error
        else:
            success = False
            result["error"] = "Need advisory_id !"

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 獲得諮詢表清單(for用戶)
class GetUserAdvisoryListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        member_id = request.GET.get("member_id",None)
        start_date = request.GET.get("start_date",None)
        end_date = request.GET.get("end_date",None)
        pet_id = request.GET.get("pet_id",None)
        msg = f"[GetUserAdvisoryListView(getUserAdvisoryList)]1.start,member_id:{member_id}/start_date:{start_date}/end_date:{end_date}/pet_id:{pet_id}"
        logger1.warning(msg)
        success = False
        error = ""
        result = {}
        if member_id is not None:
            try:
                filters = Q()
                filters.children.append(("member_id",member_id))
                if start_date is not None:
                    filters.children.append(("advisory_date__gte",start_date))
                if end_date is not None:
                    filters.children.append(("advisory_date__lte",end_date))
                if pet_id is not None:
                    filters.children.append(("pet_id",pet_id))

                ret1 = advisory.objects.filter(filters).order_by('-advisory_date')
                data = []
                
                for d1 in ret1:
                    rs1 = {}
                    rs1['advisory_id'] = d1.advisory_id
                    rs1['advisory_date'] = datetime.datetime.strftime(d1.advisory_date, "%Y/%m/%d")
                    data.append(rs1)      

                success = True
                result["data"] = data

                if ret1.count() == 0:
                    error = f"查無資料!"

            except Exception as e:
                success = False
                error_class = e.__class__.__name__ #取得錯誤類型
                detail = e.args[0] #取得詳細內容
                cl, exc, tb = sys.exc_info() #取得Call Stack
                lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
                fileName = lastCallStack[0] #取得發生的檔案名稱
                lineNum = lastCallStack[1] #取得發生的行號
                funcName = lastCallStack[2] #取得發生的函數名稱
                error = f"[GetUserAdvisoryListView(getUserAdvisoryList)]File :{fileName}, line {lineNum}, in {funcName}: [{error_class}] {detail}"
                logger1.warning(error)

            result["success"] = success
            if len(error) > 0:
                result["error"] = error
        else:
            success = False
            result["error"] = "需要用戶ID!"

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 獲得諮詢表清單(for醫生)
class GetDocAdvisoryListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        doc_id = request.GET.get("doc_id",None)
        start_date = request.GET.get("start_date",None)
        end_date = request.GET.get("end_date",None)
        msg = f"[GetDocAdvisoryListView(getDocAdvisoryList)]1.start,doc_id:{doc_id}/start_date:{start_date}/end_date:{end_date}"
        logger1.warning(msg)
        success = False
        error = ""
        result = {}
        if doc_id is not None:
            try:
                filters = Q()
                filters.children.append(("doc_id",doc_id))
                if start_date is not None:
                    filters.children.append(("advisory_date__gte",start_date))
                if end_date is not None:
                    filters.children.append(("advisory_date__lte",end_date))

                ret1 = advisory.objects.filter(filters).order_by('-advisory_date')
                data = []
                
                for d1 in ret1:
                    rs1 = {}
                    rs1['advisory_id'] = d1.advisory_id
                    rs1['advisory_date'] = datetime.datetime.strftime(d1.advisory_date, "%Y/%m/%d")
                    data.append(rs1)      

                success = True
                result["data"] = data

                if ret1.count() == 0:
                    error = f"查無資料!"

            except Exception as e:
                success = False
                error_class = e.__class__.__name__ #取得錯誤類型
                detail = e.args[0] #取得詳細內容
                cl, exc, tb = sys.exc_info() #取得Call Stack
                lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
                fileName = lastCallStack[0] #取得發生的檔案名稱
                lineNum = lastCallStack[1] #取得發生的行號
                funcName = lastCallStack[2] #取得發生的函數名稱
                error = f"[GetDocAdvisoryListView(getDocAdvisoryList)]File :{fileName}, line {lineNum}, in {funcName}: [{error_class}] {detail}"
                logger1.warning(error)

            result["success"] = success
            if len(error) > 0:
                result["error"] = error
        else:
            success = False
            result["error"] = "需要醫生ID!"

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 建立醫生評價資料
class AddDocCommentView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NewDocCommentSerializer
    
    def post(self, request, format=None):
        msg = f"[AddDocCommentView(addDocComment)]1.start"
        logger1.warning(msg)
        success = False
        error = ""
        result = {}
        serializer = self.serializer_class(data=request.data)
        comment_id = -1
        msg = ""
        if serializer.is_valid():
                # 檢查諮詢表ID是否存在
                advisory_id = serializer.validated_data.get('advisory_id',None)
                if advisory_id is None:
                    error = f"諮詢表ID(advisory_id)不得為空值!!"
                else:
                    isExist = advisory.objects.filter(advisory_id=advisory_id).exists()
                    if not isExist:
                        error = f"諮詢表ID(advisory_id：{advisory_id})不存在!!"
                    else:
                        # save data into DB

                        post_instance = serializer.save()
                        comment_id = post_instance.comment_id

                        # save photo
                        image = request.FILES.get("image", None)
                        if not image:
                            msg = f"[AddDocCommentView(addDocComment)]2.No image upload~"
                            logger1.warning(msg)
                        else:
                            image_path = f"{settings.IMAGE_ROOT}/comment/"
                            logger1.warning(image_path)
                            if not os.path.exists(image_path):
                                os.makedirs(image_path)
                            destination = open(os.path.join(image_path,image.name),'wb+')
                            for chunk in image.chunks():
                                destination.write(chunk)
                            destination.close()
                            post_instance.user_photo = image.name
                            post_instance.save()
                        
                        success = True
            
        else:
            success = False
            error = serializer.errors
        
        result["success"] = success
        if len(error) > 0:
            result["error"] = error
        else:
            result["comment_id"] = comment_id

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST) 

# 取得醫生評價資料清單
class GetDocCommentListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        doc_id = request.GET.get("doc_id",None)
        msg = f"[GetDocCommentListView(getDocCommentList)]1.start,doc_id:{doc_id}"
        logger1.warning(msg)
        success = False
        error = ""
        result = {}
        if doc_id is not None:
            try:
                filters = Q()
                filters.children.append(("doc_id",doc_id))
                ret1 = docComment.objects.filter(filters).order_by('-created_date')
                data = []
                
                for d1 in ret1:
                    rs1 = {}
                    user_photo = ""
                    rs1['member_id'] = d1.member_id
                    rs1['stars'] = d1.stars
                    rs1['comment_date'] = datetime.datetime.strftime(d1.created_date, "%Y/%m/%d")
                    rs1['memo'] = d1.memo
                    if d1.user_photo is not None and len(d1.user_photo) > 0:
                        image_path = f"{settings.IMAGE_URL}comment/"
                        logger1.warning(image_path)
                        imagefile = os.path.join(image_path,d1.user_photo)
                        user_photo = imagefile

                    rs1['user_photo'] = user_photo

                    data.append(rs1)

                success = True
                result["data"] = data

                if ret1.count() == 0:
                    error = f"查無資料!"

            except Exception as e:
                success = False
                error_class = e.__class__.__name__ #取得錯誤類型
                detail = e.args[0] #取得詳細內容
                cl, exc, tb = sys.exc_info() #取得Call Stack
                lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
                fileName = lastCallStack[0] #取得發生的檔案名稱
                lineNum = lastCallStack[1] #取得發生的行號
                funcName = lastCallStack[2] #取得發生的函數名稱
                error = f"[GetDocCommentListView(getDocCommentList)]File :{fileName}, line {lineNum}, in {funcName}: [{error_class}] {detail}"
                logger1.warning(error)

            result["success"] = success
            if len(error) > 0:
                result["error"] = error
        else:
            success = False
            result["error"] = "需要醫生ID!"

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)  

# 建立醫生營業時段
class AddDocBussinssHourView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NewDocBHSerializer
    
    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        serializer = self.serializer_class(data=request.data)
        bh_id = 0
        msg = ""

        if serializer.is_valid():
            doc_id = serializer.validated_data.get('doc_id')
            # 檢查醫生營業時段資料是否已存在
            filters = Q()
            filters.children.append(("doc_id",doc_id))
            isExist = docBH.objects.filter(filters).exists()
            if isExist:
                success = False
                error = f"此筆醫生營業時段資料已存在!!"
            else:
                # save data into DB
                post_instance = serializer.save()
                bh_id = post_instance.bh_id
                post_instance.last_modify_date = datetime.datetime.now()
                post_instance = serializer.save()
                success = True
            
        else:
            success = False
            error = serializer.errors
        
        result["success"] = success
        if len(error) > 0:
            result["error"] = error
        else:
            result["bh_id"] = bh_id

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 更新醫生營業時段
class UpdateDocBussinssHourView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DocBHSerializer

    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        msg = ""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            bh_id = serializer.validated_data.get('bh_id')
            bh1_name = serializer.validated_data.get('bh1_name')
            bh2_name = serializer.validated_data.get('bh2_name')
            bh3_name = serializer.validated_data.get('bh3_name')
            bh1_setting = serializer.validated_data.get('bh1_setting')
            bh2_setting = serializer.validated_data.get('bh2_setting')
            bh3_setting = serializer.validated_data.get('bh3_setting')
             
            try:
                matched = docBH.objects.get(bh_id=bh_id)
                need_to_update = False
                if bh1_name is not None:
                    matched.bh1_name = bh1_name
                    need_to_update = True
                if bh2_name is not None:
                    matched.bh2_name = bh2_name
                    need_to_update = True
                if bh3_name is not None:
                    matched.bh3_name = bh3_name
                    need_to_update = True
                if bh1_setting is not None:
                    matched.bh1_setting = bh1_setting
                    need_to_update = True
                if bh2_setting is not None:
                    matched.bh2_setting = bh2_setting
                    need_to_update = True
                if bh3_setting is not None:
                    matched.bh3_setting = bh3_setting
                    need_to_update = True

                if need_to_update:
                    matched.last_modify_date = datetime.datetime.now()
                    matched.save()
                
                success = True
            except docBH.DoesNotExist:
                success = False
                error = f"醫生營業時段ID:{bh_id} 不存在!"

        else:
            success = False
            error = serializer.errors

        result["success"] = success
        if len(error) > 0:
            result["error"] = error

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 取得醫生營業時段
class GetDocBussinssHourView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        doc_id = request.GET.get("doc_id",None)
        msg = f"[GetDocBussinssHourView(getDocBH)]1.start,doc_id:{doc_id}"
        logger1.warning(msg)
        success = False
        error = ""
        result = {}
        if doc_id is not None:
            try:
                matched = docBH.objects.get(doc_id=doc_id)
                serializer = DocBHSerializer(matched, context={'request': request})
                success = True
                result["data"] = serializer.data
            except docBH.DoesNotExist:
                error = f"此醫生ID：{doc_id} 尚未建立營業時間資料。"

            result["success"] = success
            if len(error) > 0:
                result["error"] = error
        else:
            success = False
            result["error"] = "Need doc_id !"

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 新增診所資料
class AddClinicInfoView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NewClinicSerializer
    
    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        serializer = self.serializer_class(data=request.data)
        id = -1
        msg = ""
        if serializer.is_valid():
            member_id = serializer.validated_data.get('member_id')
            isExist1 = member.objects.filter(uid=member_id).exists()
            isExist2 = clinic.objects.filter(member_id=member_id).exists()
            # 檢查會員ID是否存在
            if not isExist1:
                success = False
                error = f"會員ID {member_id} 不存在!!"
            elif isExist2:
                success = False
                error = f"此會員(ID:{member_id})診所資料已存在!!"                
            else:
                clinic_name = serializer.validated_data.get('clinic_name')
                area = serializer.validated_data.get('area')
                address = serializer.validated_data.get('address')
                tel = serializer.validated_data.get('tel')
                serv_content = serializer.validated_data.get('serv_content')
                desc = serializer.validated_data.get('desc')
                email = serializer.validated_data.get('email')

                # save data into DB
                post_instance = serializer.save()
                clinic_id = post_instance.clinic_id

                # save photo
                image = request.FILES.get("image", None)
                if not image:
                    msg = f"No image upload~"
                    logger1.warning(msg)
                else:
                    image_path = f"{settings.IMAGE_ROOT}/member/{member_id}/"
                    logger1.warning(image_path)                    
                    if not os.path.exists(image_path):
                        os.makedirs(image_path)
                    destination = open(os.path.join(image_path,image.name),'wb+')
                    for chunk in image.chunks():
                        destination.write(chunk)
                    destination.close()
                    post_instance.photo = image.name
                    post_instance.save()

                success = True
        else:
            success = False
            error = serializer.errors
        
        result["success"] = success
        if len(error) > 0:
            result["error"] = error
        else:
            result["clinic_id"] = clinic_id

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 取得診所資料
class GetClinicInfoView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        member_id = request.GET.get("member_id",None)
        success = False
        error = ""
        result = {}
        if member_id is not None:
            try:
                matched = clinic.objects.get(member_id=member_id)
                if matched.photo is not None and len(matched.photo) > 0:
                    image_path = f"{settings.IMAGE_URL}member/{member_id}/"
                    imagefile = os.path.join(image_path,matched.photo)
                    matched.photo = imagefile

                serializer = ClinicSerializer(matched, context={'request': request})

                success = True
                result["data"] = serializer.data
            except clinic.DoesNotExist:
                error = f"The member id:{member_id} doesn't have clinic data!!"

            result["success"] = success
            if len(error) > 0:
                result["error"] = error
        else:
            success = False
            result["error"] = "Need member_id data!"

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 更新診所資料
class UpdateClinicInfoView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ClinicSerializer
    
    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        serializer = self.serializer_class(data=request.data)
        msg = ""
        if serializer.is_valid():
            clinic_id = serializer.validated_data.get('clinic_id')
            clinic_name = serializer.validated_data.get('clinic_name')
            area = serializer.validated_data.get('area')
            address = serializer.validated_data.get('address')
            tel = serializer.validated_data.get('tel')
            serv_content = serializer.validated_data.get('serv_content')
            desc = serializer.validated_data.get('desc')
            email = serializer.validated_data.get('email')

            try:
                matched = clinic.objects.get(clinic_id=clinic_id)
                member_id = matched.member_id
                matched.clinic_name = clinic_name
                matched.address = address
                matched.tel = tel
                matched.serv_content = serv_content
                matched.area = area
                matched.desc = desc
                matched.email = email
                matched.last_modify_date = datetime.datetime.now()
                matched.save()

                image = request.FILES.get("image", None)

                if not image:
                    msg = f"No image upload~"
                    logger1.warning(msg)
                else:
                    image_path = f"{settings.IMAGE_ROOT}/member/{member_id}/"
                    logger1.warning(image_path)
                    if not os.path.exists(image_path):
                        os.makedirs(image_path)
                    destination = open(os.path.join(image_path,image.name),'wb+')
                    for chunk in image.chunks():
                        destination.write(chunk)
                    destination.close()
                    matched.photo = image.name
                    matched.save()

                success = True
            except clinic.DoesNotExist:
                success = False
                error = f"The clinic_id:{clinic_id} 不存在."

        else:
            success = False
            error = serializer.errors

        result["success"] = success
        if len(error) > 0:
            result["error"] = error

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 取得所有診所清單資料
class getClinicListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        msg = f"[getClinicListView(getClinicList)]1.start"
        logger1.warning(msg)
        success = False
        error = ""
        result = {}
        ret1 = clinic.objects.filter(is_approved=True)
        data = []

        for d1 in ret1:
            rs1 = {}
            photo = ""
            rs1['clinic_id'] = d1.clinic_id
            rs1['clinic_name'] = d1.clinic_name
            rs1['area'] = d1.area
            rs1['address'] = d1.address
            rs1['serv_content'] = d1.serv_content
            rs1['bh'] = Helpers().getClinicTodayBH(d1.clinic_id)
            rs1['tel'] = d1.tel
            member_id = d1.member_id
            if d1.photo is not None and len(d1.photo) > 0:
                image_path = f"{settings.IMAGE_URL}member/{member_id}/"
                logger1.warning(image_path)
                imagefile = os.path.join(image_path,d1.photo)
                photo = imagefile

            rs1['photo'] = photo

            data.append(rs1)

        success = True
        result["data"] = data

        if ret1.count() == 0:
            error = f"查無資料!"
        
        result["success"] = success
        if len(error) > 0:
            result["error"] = error

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 建立診所營業時段
class AddClinicBussinssHourView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NewClinicBHSerializer
    
    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        serializer = self.serializer_class(data=request.data)
        bh_id = 0
        msg = ""

        if serializer.is_valid():
            clinic_id = serializer.validated_data.get('clinic_id')
            # 檢查診所營業時段資料是否已存在
            isExist = clinicBH.objects.filter(clinic_id=clinic_id).exists()
            if isExist:
                success = False
                error = f"此筆診所營業時段資料已存在!!"
            else:
                # save data into DB
                post_instance = serializer.save()
                bh_id = post_instance.bh_id
                post_instance.last_modify_date = datetime.datetime.now()
                post_instance = serializer.save()
                success = True
            
        else:
            success = False
            error = serializer.errors
        
        result["success"] = success
        if len(error) > 0:
            result["error"] = error
        else:
            result["bh_id"] = bh_id

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 更新診所營業時段
class UpdateClinicBussinssHourView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ClinicBHSerializer

    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        msg = ""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            bh_id = serializer.validated_data.get('bh_id')
            bh1_name = serializer.validated_data.get('bh1_name')
            bh2_name = serializer.validated_data.get('bh2_name')
            bh3_name = serializer.validated_data.get('bh3_name')
            bh1_setting = serializer.validated_data.get('bh1_setting')
            bh2_setting = serializer.validated_data.get('bh2_setting')
            bh3_setting = serializer.validated_data.get('bh3_setting')
             
            try:
                matched = clinicBH.objects.get(bh_id=bh_id)
                need_to_update = False
                if bh1_name is not None:
                    matched.bh1_name = bh1_name
                    need_to_update = True
                if bh2_name is not None:
                    matched.bh2_name = bh2_name
                    need_to_update = True
                if bh3_name is not None:
                    matched.bh3_name = bh3_name
                    need_to_update = True
                if bh1_setting is not None:
                    matched.bh1_setting = bh1_setting
                    need_to_update = True
                if bh2_setting is not None:
                    matched.bh2_setting = bh2_setting
                    need_to_update = True
                if bh3_setting is not None:
                    matched.bh3_setting = bh3_setting
                    need_to_update = True

                if need_to_update:
                    matched.last_modify_date = datetime.datetime.now()
                    matched.save()
                
                success = True
            except clinicBH.DoesNotExist:
                success = False
                error = f"診所營業時段ID:{bh_id} 不存在!"

        else:
            success = False
            error = serializer.errors

        result["success"] = success
        if len(error) > 0:
            result["error"] = error

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 取得診所營業時段
class GetClinicBussinssHourView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        clinic_id = request.GET.get("clinic_id",None)
        msg = f"[GetClinicBussinssHourView(getClinicBH)]1.start,clinic_id:{clinic_id}"
        logger1.warning(msg)
        success = False
        error = ""
        result = {}
        if clinic_id is not None:
            try:
                matched = clinicBH.objects.get(clinic_id=clinic_id)
                serializer = ClinicBHSerializer(matched, context={'request': request})
                success = True
                result["data"] = serializer.data
            except clinicBH.DoesNotExist:
                error = f"此診所ID：{clinic_id} 尚未建立營業時間資料。"

            result["success"] = success
            if len(error) > 0:
                result["error"] = error
        else:
            success = False
            result["error"] = "Need clinic_id !"

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 新增店家資料
class AddStoreInfoView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NewStoreSerializer
    
    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        serializer = self.serializer_class(data=request.data)
        id = -1
        msg = ""
        if serializer.is_valid():
            member_id = serializer.validated_data.get('member_id')
            isExist1 = member.objects.filter(uid=member_id).exists()
            isExist2 = store.objects.filter(member_id=member_id).exists()
            # 檢查會員ID是否存在
            if not isExist1:
                success = False
                error = f"會員ID {member_id} 不存在!!"
            elif isExist2:
                success = False
                error = f"此會員(ID:{member_id})店家資料已存在!!"                
            else:
                store_name = serializer.validated_data.get('store_name')
                area = serializer.validated_data.get('area')
                address = serializer.validated_data.get('address')
                tel = serializer.validated_data.get('tel')
                serv_content = serializer.validated_data.get('serv_content')
                desc = serializer.validated_data.get('desc')
                email = serializer.validated_data.get('email')

                # save data into DB
                post_instance = serializer.save()
                store_id = post_instance.store_id

                # save photo
                image = request.FILES.get("image", None)
                if not image:
                    msg = f"No image upload~"
                    logger1.warning(msg)
                else:
                    image_path = f"{settings.IMAGE_ROOT}/member/{member_id}/"
                    logger1.warning(image_path)                    
                    if not os.path.exists(image_path):
                        os.makedirs(image_path)
                    destination = open(os.path.join(image_path,image.name),'wb+')
                    for chunk in image.chunks():
                        destination.write(chunk)
                    destination.close()
                    post_instance.photo = image.name
                    post_instance.save()

                success = True
        else:
            success = False
            error = serializer.errors
        
        result["success"] = success
        if len(error) > 0:
            result["error"] = error
        else:
            result["store_id"] = store_id

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 取得店家資料
class GetStoreInfoView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        member_id = request.GET.get("member_id",None)
        success = False
        error = ""
        result = {}
        if member_id is not None:
            try:
                matched = store.objects.get(member_id=member_id)
                if matched.photo is not None and len(matched.photo) > 0:
                    image_path = f"{settings.IMAGE_URL}member/{member_id}/"
                    imagefile = os.path.join(image_path,matched.photo)
                    matched.photo = imagefile

                serializer = StoreSerializer(matched, context={'request': request})

                success = True
                result["data"] = serializer.data
            except store.DoesNotExist:
                error = f"The member id:{member_id} doesn't have store data!!"

            result["success"] = success
            if len(error) > 0:
                result["error"] = error
        else:
            success = False
            result["error"] = "Need member_id data!"

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 更新店家資料
class UpdateStoreInfoView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StoreSerializer
    
    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        serializer = self.serializer_class(data=request.data)
        msg = ""
        if serializer.is_valid():
            store_id = serializer.validated_data.get('store_id')
            store_name = serializer.validated_data.get('store_name')
            area = serializer.validated_data.get('area')
            address = serializer.validated_data.get('address')
            tel = serializer.validated_data.get('tel')
            serv_content = serializer.validated_data.get('serv_content')
            desc = serializer.validated_data.get('desc')
            email = serializer.validated_data.get('email')

            try:
                matched = store.objects.get(store_id=store_id)
                member_id = matched.member_id
                matched.store_name = store_name
                matched.area = area
                matched.address = address
                matched.tel = tel
                matched.serv_content = serv_content
                matched.desc = desc
                matched.email = email
                matched.last_modify_date = datetime.datetime.now()
                matched.save()

                image = request.FILES.get("image", None)

                if not image:
                    msg = f"No image upload~"
                    logger1.warning(msg)
                else:
                    image_path = f"{settings.IMAGE_ROOT}/member/{member_id}/"
                    logger1.warning(image_path)
                    if not os.path.exists(image_path):
                        os.makedirs(image_path)
                    destination = open(os.path.join(image_path,image.name),'wb+')
                    for chunk in image.chunks():
                        destination.write(chunk)
                    destination.close()
                    matched.photo = image.name
                    matched.save()

                success = True
            except store.DoesNotExist:
                success = False
                error = f"The store_id:{store_id} 不存在."

        else:
            success = False
            error = serializer.errors

        result["success"] = success
        if len(error) > 0:
            result["error"] = error

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 取得所有店家清單資料
class getStoreListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        msg = f"[getStoreListView(getStoreList)]1.start"
        logger1.warning(msg)
        success = False
        error = ""
        result = {}
        ret1 = store.objects.filter(is_approved=True)
        data = []

        for d1 in ret1:
            rs1 = {}
            photo = ""
            rs1['store_id'] = d1.store_id
            rs1['store_name'] = d1.store_name
            rs1['area'] = d1.area
            rs1['address'] = d1.address
            rs1['serv_content'] = d1.serv_content
            rs1['bh'] = Helpers().getStoreTodayBH(d1.store_id)
            rs1['tel'] = d1.tel
            member_id = d1.member_id
            if d1.photo is not None and len(d1.photo) > 0:
                image_path = f"{settings.IMAGE_URL}member/{member_id}/"
                logger1.warning(image_path)
                imagefile = os.path.join(image_path,d1.photo)
                photo = imagefile

            rs1['photo'] = photo

            data.append(rs1)

        success = True
        result["data"] = data

        if ret1.count() == 0:
            error = f"查無資料!"
        
        result["success"] = success
        if len(error) > 0:
            result["error"] = error

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 建立店家營業時段
class AddStoreBussinssHourView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NewStoreBHSerializer
    
    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        serializer = self.serializer_class(data=request.data)
        bh_id = 0
        msg = ""

        if serializer.is_valid():
            store_id = serializer.validated_data.get('store_id')
            # 檢查店家營業時段資料是否已存在
            isExist = storeBH.objects.filter(store_id=store_id).exists()
            if isExist:
                success = False
                error = f"此筆店家營業時段資料已存在!!"
            else:
                # save data into DB
                post_instance = serializer.save()
                bh_id = post_instance.bh_id
                post_instance.last_modify_date = datetime.datetime.now()
                post_instance = serializer.save()
                success = True
            
        else:
            success = False
            error = serializer.errors
        
        result["success"] = success
        if len(error) > 0:
            result["error"] = error
        else:
            result["bh_id"] = bh_id

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 更新店家營業時段
class UpdateStoreBussinssHourView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StoreBHSerializer

    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        msg = ""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            bh_id = serializer.validated_data.get('bh_id')
            bh1_name = serializer.validated_data.get('bh1_name')
            bh2_name = serializer.validated_data.get('bh2_name')
            bh3_name = serializer.validated_data.get('bh3_name')
            bh1_setting = serializer.validated_data.get('bh1_setting')
            bh2_setting = serializer.validated_data.get('bh2_setting')
            bh3_setting = serializer.validated_data.get('bh3_setting')
             
            try:
                matched = clinicBH.objects.get(bh_id=bh_id)
                need_to_update = False
                if bh1_name is not None:
                    matched.bh1_name = bh1_name
                    need_to_update = True
                if bh2_name is not None:
                    matched.bh2_name = bh2_name
                    need_to_update = True
                if bh3_name is not None:
                    matched.bh3_name = bh3_name
                    need_to_update = True
                if bh1_setting is not None:
                    matched.bh1_setting = bh1_setting
                    need_to_update = True
                if bh2_setting is not None:
                    matched.bh2_setting = bh2_setting
                    need_to_update = True
                if bh3_setting is not None:
                    matched.bh3_setting = bh3_setting
                    need_to_update = True

                if need_to_update:
                    matched.last_modify_date = datetime.datetime.now()
                    matched.save()
                
                success = True
            except clinicBH.DoesNotExist:
                success = False
                error = f"店家營業時段ID:{bh_id} 不存在!"

        else:
            success = False
            error = serializer.errors

        result["success"] = success
        if len(error) > 0:
            result["error"] = error

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 取得店家營業時段
class GetStoreBussinssHourView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        store_id = request.GET.get("store_id",None)
        msg = f"[GetStoreBussinssHourView(getStoreBH)]1.start,store_id:{store_id}"
        logger1.warning(msg)
        success = False
        error = ""
        result = {}
        if store_id is not None:
            try:
                matched = storeBH.objects.get(store_id=store_id)
                serializer = StoreBHSerializer(matched, context={'request': request})
                success = True
                result["data"] = serializer.data
            except storeBH.DoesNotExist:
                error = f"此店家ID：{store_id} 尚未建立營業時間資料。"

            result["success"] = success
            if len(error) > 0:
                result["error"] = error
        else:
            success = False
            result["error"] = "Need store_id !"

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 獲得用戶諮詢清單
class GetUserAdviseListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        member_id = request.GET.get("member_id",None)
        msg = f"[GetUserAdviseListView(getUserAdviseList)]1.start,member_id:{member_id}"
        logger1.warning(msg)
        success = False
        error = ""
        result = {}
        if member_id is not None:
            try:
                ret1 = advisory.objects.filter(member_id=member_id
                                              ).values('advisory_id',
                                                       'advisory_date',
                                                       'pet_id',
                                                       'pet__pet_name',
                                                       'doc__clinic',
                                                       'doc__doc_name',
                                                       'fee').order_by('-advisory_date')
                data = []        

                for d1 in ret1:
                    rs1 = {}
                    rs1['advisory_id'] = d1['advisory_id']
                    rs1['advisory_date'] = datetime.datetime.strftime(d1['advisory_date'], "%Y/%m/%d")
                    rs1['pet_id'] = d1['pet_id']
                    rs1['pet_name'] = d1['pet__pet_name']
                    rs1['clinic'] = d1['doc__clinic']
                    rs1['doc_name'] = d1['doc__doc_name']
                    rs1['fee'] = d1['fee']
                    rs1['stars'] = Helpers().getDocStars(d1['advisory_id'])
                    data.append(rs1)

                success = True
                result["data"] = data

                if ret1.count() == 0:
                    error = f"查無資料!"

            except Exception as e:
                success = False
                error_class = e.__class__.__name__ #取得錯誤類型
                detail = e.args[0] #取得詳細內容
                cl, exc, tb = sys.exc_info() #取得Call Stack
                lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
                fileName = lastCallStack[0] #取得發生的檔案名稱
                lineNum = lastCallStack[1] #取得發生的行號
                funcName = lastCallStack[2] #取得發生的函數名稱
                error = f"[GetUserAdviseListView(getUserAdviseList)]File :{fileName}, line {lineNum}, in {funcName}: [{error_class}] {detail}"
                logger1.warning(error)

            result["success"] = success
            if len(error) > 0:
                result["error"] = error
        else:
            success = False
            result["success"] = False
            result["error"] = "需要用戶ID!"

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 獲得用戶預約清單
class GetUserAppointListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        member_id = request.GET.get("member_id",None)
        msg = f"[GetUserAppointListView(getUserAppointList)]1.start,member_id:{member_id}"
        logger1.warning(msg)
        success = False
        error = ""
        result = {}
        if member_id is not None:
            try:
                filters = Q()
                filters.children.append(("member_id",member_id))
                # 只抓今日之後的預約資料
                today = datetime.date.today()
                filters.children.append(("appoint__set_date__gte",today))
                ret1 = userAppoint.objects.filter(filters
                                                 ).values('appoint_id',
                                                          'appoint__set_date',
                                                          'appoint__set_hour',
                                                          'appoint__set_section',
                                                          'appoint__status').order_by('appoint__set_date')

                data = []        

                for d1 in ret1:
                    rs1 = {}
                    rs1['appoint_id'] = d1['appoint_id']
                    date1 = datetime.datetime.strftime(d1['appoint__set_date'], "%Y/%m/%d")
                    time1 = '{0:02d}'.format(d1['appoint__set_hour'])
                    section = d1['appoint__set_section']
                    section1 = ""
                    if section == 1:
                      section1 = "00"
                    elif section == 2:
                      section1 = "20"
                    elif section == 3:
                      section1 = "40"
                    else:
                      section1 = "00"

                    set_date = f"{date1} {time1}:{section1}"
                    rs1['set_date'] = set_date
                    rs1['status'] = d1['appoint__status']
                    data.append(rs1)                

                success = True
                result["data"] = data

                if ret1.count() == 0:
                    error = f"查無資料!"

            except Exception as e:
                success = False
                error_class = e.__class__.__name__ #取得錯誤類型
                detail = e.args[0] #取得詳細內容
                cl, exc, tb = sys.exc_info() #取得Call Stack
                lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
                fileName = lastCallStack[0] #取得發生的檔案名稱
                lineNum = lastCallStack[1] #取得發生的行號
                funcName = lastCallStack[2] #取得發生的函數名稱
                error = f"[GetUserAppointListView(getUserAppointList)]File :{fileName}, line {lineNum}, in {funcName}: [{error_class}] {detail}"
                logger1.warning(error)
                
            result["success"] = success
            if len(error) > 0:
                result["error"] = error
        else:
            success = False
            result["success"] = False
            result["error"] = "需要用戶ID!"

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 獲得諮詢表清單
class GetUserAdviseDateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        member_id = request.GET.get("member_id",None)
        msg = f"[GetUserAdviseDateView(getUserAdviseDate)]1.start,member_id:{member_id}"
        logger1.warning(msg)
        success = False
        error = ""
        result = {}
        if member_id is not None:
            try:
                ret1 = advisory.objects.filter(member_id=member_id).order_by('-advisory_date')
                data = []
                
                for d1 in ret1:
                    rs1 = {}
                    rs1['advisory_id'] = d1.advisory_id
                    rs1['advisory_date'] = datetime.datetime.strftime(d1.advisory_date, "%Y/%m/%d")
                    data.append(rs1)      

                success = True
                result["data"] = data

                if ret1.count() == 0:
                    error = f"查無資料!"

            except Exception as e:
                success = False
                error_class = e.__class__.__name__ #取得錯誤類型
                detail = e.args[0] #取得詳細內容
                cl, exc, tb = sys.exc_info() #取得Call Stack
                lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
                fileName = lastCallStack[0] #取得發生的檔案名稱
                lineNum = lastCallStack[1] #取得發生的行號
                funcName = lastCallStack[2] #取得發生的函數名稱
                error = f"[GetUserAdviseDateView(getUserAdviseDate)]File :{fileName}, line {lineNum}, in {funcName}: [{error_class}] {detail}"
                logger1.warning(error)

            result["success"] = success
            if len(error) > 0:
                result["error"] = error
        else:
            success = False
            result["success"] = False
            result["error"] = "需要用戶ID!"

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)
    # @xframe_options_exempt
    # def get(self, request):
    #     # Get and validate the token from url
    #     token = request.GET.get("token", None)
    #     refresh = request.GET.get("refresh", None)

    #     validated_token = authentication.JWTAuthentication().get_validated_token(token)
    #     tokenUser = authentication.JWTAuthentication().get_user(validated_token)
        
    #     # Once we are here, tokenUser has been found
    #     # We refresh token again to make sure it won't expire
    #     refresh = RefreshToken.for_user(tokenUser)
        
    #     # Assign back the new token
    #     refresh = refresh
    #     token = refresh.access_token

'''
  首頁
'''
def index(request):
  d1=datetime.datetime.now()
  msg = f"[index]1-start ============================================"
  logger1.warning(msg)
  if not request.session.get('is_login',None):
    # 重新登入
    return redirect('/member/login/')

  return render(request, "member/index.html", )

'''
  登入
'''
def login(request):
  d1=datetime.datetime.now()
  msg = f"[login]1-start ============================================"
  logger1.warning(msg)
  if request.session.get('is_login',None): # 檢查 session 確定是否登入，不允許重複登入
    return redirect("/")

  if request.method == 'POST':  # 接收 POST 訊息，若無則讓返回空表單   
    login_form = LoginForm(request.POST)  # 導入表單類型 

    if login_form.is_valid(): # 驗證表單
        user_id  = login_form.cleaned_data['user_id']
        user_pwd = login_form.cleaned_data['user_pwd']
        msg = f"[login]2-user_id:{user_id} ; user_pwd : {user_pwd}"
        logger1.warning(msg)

        try:
            user = Account.objects.get(user_account=user_id)
            if user.is_delete:
                message = f"帳號 {user.user_account} 無登入權限！"
                obj1 = Helpers().addBKLoginData(user.user_id, False, message)
                return render(request,"member/login.html", locals())

            if user.user_password != user_pwd :
              message = f"帳號 {user.user_account} 密碼錯誤！"
              obj1 = Helpers().addBKLoginData(user.user_id, False, message)
              return render(request,"member/login.html", locals())

            # 使用 session 寫入登入資料
            request.session['is_login'] = True
            request.session['uid'] = user.user_id
            request.session['user_id'] = user.user_account
            request.session['user_name'] = user.user_name
            request.session['user_level'] = user.level

            # 新增登入記錄
            createdObj = Helpers().addBKLoginData(user.user_id, True, "登入成功")
            last_login_date = createdObj.login_date
            user.last_login_date = last_login_date
            user.save()
            d2=datetime.datetime.now()
            diff = (d2 - d1).total_seconds()
            msg = f"[login]done,spent : {diff} seconds======================"
            logger1.warning(msg)
            message = "登入成功～"
            return render(request, "member/index.html", )

        except Account.DoesNotExist:
            message = f"無此帳號( {user_id} )資料！"
            obj2 = Helpers().addBKLoginData(user.user_id, False, message)

  login_form = LoginForm(request.POST)  # 返回空表單
  d3=datetime.datetime.now()
  diff = (d3 - d1).total_seconds()
  msg = f"[login]返回空表單,spent : {diff} seconds"
  logger1.warning(msg)
  return render(request,"member/login.html", locals())

'''
  登出
'''
def logout(request):
  if not request.session.get('is_login',None): # 若尚未登入，就不需要登出
    return redirect('/member/login/')

  request.session.flush()   # 將 session 內容清除
  return redirect('/member/login/')

'''
  醫生-醫生申請審核
'''
def docApprovelist(request):
  if not request.session.get('is_login',None):
    # 重新登入
    return redirect('/member/login/')

  start_date = request.GET.get("startTime1",None)
  end_date = request.GET.get("endTime1",None)
  args = request.GET.get("args",None)

  d1=datetime.datetime.now()
  msg = f"[docApprovelist]1-start====================================================="
  logger1.warning(msg)
  msg = f"[docApprovelist]start_date:{start_date} end_date:{end_date} args:{args}"
  logger1.warning(msg)

  result = {}

  f1 = Q()
  f1.connector = "AND"
  if start_date is not None and len(start_date) > 0:
    chkdate = datetime.datetime.strptime(start_date,"%Y-%m-%d")
    chkdate = chkdate.replace(hour=0,minute=0,second=0,microsecond=0)
    f1.children.append(("created_date__gte",chkdate))

  if end_date is not None and len(end_date) > 0:
    chkdate = datetime.datetime.strptime(end_date,"%Y-%m-%d")
    chkdate = chkdate.replace(hour=23,minute=59,second=59,microsecond=999999)
    f1.children.append(("created_date__lte",chkdate))

  f2 = Q()
  f2.connector = "OR"
  if args is not None and len(args) > 0:
    if args.isdigit():
      f2.children.append(("member_id",args))

    f2.children.append(("doc_name",args))

  ret1 = doctor.objects.filter(f1).filter(f2).order_by('id')

  data = []
  for d in ret1:
    rs = {}
    rs['doc_id'] = d.id
    rs['member_id'] = d.member_id
    rs['doc_name'] = d.doc_name
    rs['clinic'] = d.clinic
    rs['title'] = d.title
    rs['skill'] = d.skill
    rs['created_date'] = datetime.datetime.strftime(d.created_date, "%Y/%m/%d %H:%M:%S")
    if d.is_approved:
      rs['is_approved'] = "1"
    else:
      rs['is_approved'] = "0"

    data.append(rs)
    msg = f"[docApprovelist]result:{data}"
    logger1.warning(msg)

  result = {
    "rs1": data
  }

  d2=datetime.datetime.now()
  diff = (d2 - d1).total_seconds()
  msg = f"[docApprovelist]done, spent : {diff} seconds ========================================="    
  logger1.warning(msg)
  
  if request.is_ajax():
    return JsonResponse(result, safe=False)

  return render(request, "member/docApprovelist.html", result,)

# 醫生-醫生申請審核-個人
def docDetail(request):
  if not request.session.get('is_login',None):
    # 重新登入
    return redirect('/member/login/')

  doc_id = request.GET.get("doc_id",None)
  d1=datetime.datetime.now()
  msg = f"[docDetail]1-start====================================================="
  logger1.warning(msg)
  msg = f"[docDetail]doc_id:{doc_id}"
  logger1.warning(msg)
  if doc_id is not None:

    result = {}

    # 個人資訊
    ret = doctor.objects.get(pk = doc_id)
    rs = {}
    uid = ret.member_id
    rs['doc_id'] = ret.id
    rs['member_id'] = ret.member_id
    rs['doc_name'] = ret.doc_name
    rs['clinic'] = ret.clinic
    rs['title'] = ret.title
    rs['skill'] = ret.skill
    rs['experience'] = ret.experience
    rs['area'] = ret.area
    rs['clinic_addr'] = ret.clinic_addr
    photo = ""
    if ret.doc_photo is not None and len(ret.doc_photo) > 0:
        image_path = f"{settings.IMAGE_URL}member/{uid}/"
        logger1.warning(image_path)
        photo = os.path.join(image_path,ret.doc_photo)
    rs['photo'] = photo

    rs['created_date'] = datetime.datetime.strftime(ret.created_date, "%Y/%m/%d %H:%M:%S")
    if ret.is_approved:
      rs['is_approved'] = "1"
    else:
      rs['is_approved'] = "0"

    ret1 = member.objects.get(pk = ret.member_id)
    rs['account'] = ret1.account
    rs['nick_name'] = ret1.nick_name
    rs['idNo'] = ret1.idNo
    rs['email'] = ret1.email
    rs['address'] = ret1.address
    rs['sex'] = ret1.get_sex_display()
    rs['myself'] = ret1.myself
    if ret1.fb_account is None or len(ret1.fb_account) == 0:
      rs['fb_account'] = "無"
    else:
      rs['fb_account'] = ret1.fb_account
    if ret1.google_account is None or len(ret1.google_account) == 0:  
      rs['google_account'] = "無"
    else:
      rs['google_account'] = ret1.google_account
    rs['status'] = ret1.get_status_display()
    if ret1.is_doctor:
      rs['is_doctor'] = "1"
    else:
      rs['is_doctor'] = "0"

    if ret1.is_clinic:
      rs['is_clinic'] = "1"
    else:
      rs['is_clinic'] = "0"

    if ret1.is_store:
      rs['is_store'] = "1"
    else:
      rs['is_store'] = "0"

    if ret1.last_login_date is not None:
      rs['last_login_date'] = datetime.datetime.strftime(ret1.last_login_date, "%Y/%m/%d %H:%M:%S")
    else:
      rs['last_login_date'] = ""

    if ret1.last_modify_date is not None:
      rs['last_modify_date'] = datetime.datetime.strftime(ret1.last_modify_date, "%Y/%m/%d %H:%M:%S")
    else:
      rs['last_modify_date'] = ""

    admin_account = request.session.get('user_id','')
    result = {
      "data": rs,
      "admin_account": admin_account
    }

  d2=datetime.datetime.now()
  diff = (d2 - d1).total_seconds()
  msg = f"[docDetail]done, spent : {diff} seconds ========================================="    
  logger1.warning(msg)

  if request.is_ajax():
    return JsonResponse(result, safe=False)

  return render(request, "member/docDetail.html", result,)

# 醫生申請核可
def approveDoctor(request):
  if not request.session.get('is_login',None):
    # 重新登入
    return redirect('/member/login/')

  if request.method == 'POST':

    admin_account = request.session.get('user_id',None)
    doc_id = request.POST['doc_id']
    result = {}
    msg = ""
    try:
      matched = doctor.objects.get(pk=doc_id)
      member_id = matched.member_id
      matched.is_approved = True
      matched.approve_account = admin_account
      matched.approve_date = datetime.datetime.now()
      matched.last_modify_date = datetime.datetime.now()
      matched.save()

      matched1 = member.objects.get(pk = member_id)
      matched1.is_doctor = True
      matched1.last_modify_date = datetime.datetime.now()
      matched1.save()

      msg = "確認完成。"

    except doctor.DoesNotExist:
      msg = f"此醫生ID{doc_id}不存在!!"

    result = {'msg':msg}

  if request.is_ajax():
    return JsonResponse(result, safe=False)

  return render(request, "member/docDetail.html", result,)

# 醫生-醫生視訊連結
def docVideoLink(request):
  if not request.session.get('is_login',None):
    # 重新登入
    return redirect('/member/login/')

  member_id = request.GET.get("member_id",None)
  d1=datetime.datetime.now()
  msg = f"[docVideoLink]1-start====================================================="
  logger1.warning(msg)
  result = {}

  if member_id is not None:
    msg = f"[docVideoLink]member_id:{member_id}"
    logger1.warning(msg)
    try:
      ret = doctor.objects.get(member_id = member_id)
      rs = {}
      rs['doc_id'] = ret.id
      rs['member_id'] = ret.member_id
      rs['doc_name'] = ret.doc_name
      rs['clinic'] = ret.clinic
      rs['title'] = ret.title
      rs['skill'] = ret.skill
      rs['experience'] = ret.experience
      rs['skill'] = ret.skill
      rs['area'] = ret.area
      rs['clinic_addr'] = ret.clinic_addr
      rs['room_url'] = ret.room_url

      # photo = ""
      # if len(ret.doc_photo) > 0:
      #     image_path = f"{settings.IMAGE_URL}member/{member_id}/"
      #     logger1.warning(image_path)
      #     photo = os.path.join(image_path,ret.doc_photo)
      # rs['photo'] = photo

      # rs['created_date'] = datetime.datetime.strftime(ret.created_date, "%Y/%m/%d %H:%M:%S")
      # if ret.is_approved:
      #   rs['is_approved'] = "1"
      # else:
      #   rs['is_approved'] = "0"

      ret1 = member.objects.get(pk = ret.member_id)
      rs['account'] = ret1.account
      rs['nick_name'] = ret1.nick_name
      # rs['idNo'] = ret1.idNo
      rs['email'] = ret1.email
      # rs['address'] = ret1.address
      rs['sex'] = ret1.get_sex_display()
      # rs['myself'] = ret1.myself
      # if ret1.fb_account is None or len(ret1.fb_account) == 0:
      #   rs['fb_account'] = "無"
      # else:
      #   rs['fb_account'] = ret1.fb_account
      # if ret1.google_account is None or len(ret1.google_account) == 0:  
      #   rs['google_account'] = "無"
      # else:
      #   rs['google_account'] = ret1.google_account
      # rs['status'] = ret1.get_status_display()
      # if ret1.is_doctor:
      #   rs['is_doctor'] = "1"
      # else:
      #   rs['is_doctor'] = "0"

      # if ret1.is_clinic:
      #   rs['is_clinic'] = "1"
      # else:
      #   rs['is_clinic'] = "0"

      # if ret1.is_store:
      #   rs['is_store'] = "1"
      # else:
      #   rs['is_store'] = "0"

      # if ret1.last_login_date is not None:
      #   rs['last_login_date'] = datetime.datetime.strftime(ret1.last_login_date, "%Y/%m/%d %H:%M:%S")
      # else:
      #   rs['last_login_date'] = ""

      # if ret1.last_modify_date is not None:
      #   rs['last_modify_date'] = datetime.datetime.strftime(ret1.last_modify_date, "%Y/%m/%d %H:%M:%S")
      # else:
      #   rs['last_modify_date'] = ""
      result = {
        'error':"",
        'data': rs
      }

    except doctor.DoesNotExist:
      error = f"無此醫生資料!!"
      result = {'error':error}

  d2=datetime.datetime.now()
  diff = (d2 - d1).total_seconds()
  msg = f"[docVideoLink]done, spent : {diff} seconds ========================================="    
  logger1.warning(msg)

  if request.is_ajax():
    return JsonResponse(result, safe=False)

  return render(request, "member/docVideoLink.html", result,)

# 更新醫生視訊連結
def updateDocVideoLink(request):
  if not request.session.get('is_login',None):
    # 重新登入
    return redirect('/member/login/')

  if request.method == 'POST':

    admin_account = request.session.get('user_id',None)
    doc_id = request.POST['doc_id']
    room = request.POST['room']
    result = {}
    msg = ""
    try:
      matched = doctor.objects.get(pk=doc_id)
      matched.room_url = room
      matched.last_modify_date = datetime.datetime.now()
      matched.save()
      msg = "更新完成。"

    except doctor.DoesNotExist:
      msg = f"更新失敗！！此醫生ID{doc_id}不存在!!"

    result = {'msg':msg}

  if request.is_ajax():
    return JsonResponse(result, safe=False)

  return render(request, "member/docVideoLink.html", locals(),)  

'''
  診所申請審核
'''
def clinicApprovelist(request):
  if not request.session.get('is_login',None):
    # 重新登入
    return redirect('/member/login/')

  start_date = request.GET.get("startTime1",None)
  end_date = request.GET.get("endTime1",None)
  args = request.GET.get("args",None)

  d1=datetime.datetime.now()
  msg = f"[clinicApprovelist]1-start====================================================="
  logger1.warning(msg)
  msg = f"[clinicApprovelist]start_date:{start_date} end_date:{end_date} args:{args}"
  logger1.warning(msg)

  result = {}

  f1 = Q()
  f1.connector = "AND"
  if start_date is not None and len(start_date) > 0:
    chkdate = datetime.datetime.strptime(start_date,"%Y-%m-%d")
    chkdate = chkdate.replace(hour=0,minute=0,second=0,microsecond=0)
    f1.children.append(("created_date__gte",chkdate))

  if end_date is not None and len(end_date) > 0:
    chkdate = datetime.datetime.strptime(end_date,"%Y-%m-%d")
    chkdate = chkdate.replace(hour=23,minute=59,second=59,microsecond=999999)
    f1.children.append(("created_date__lte",chkdate))

  f2 = Q()
  f2.connector = "OR"
  if args is not None and len(args) > 0:
    if args.isdigit():
      f2.children.append(("member_id",args))

    f2.children.append(("clinic_name",args))

  ret1 = clinic.objects.filter(f1).filter(f2).order_by('clinic_id')

  data = []
  for d in ret1:
    rs = {}
    rs['clinic_id'] = d.clinic_id
    rs['member_id'] = d.member_id
    rs['clinic_name'] = d.clinic_name
    rs['area'] = d.area
    rs['address'] = d.address
    rs['tel'] = d.tel
    rs['created_date'] = datetime.datetime.strftime(d.created_date, "%Y/%m/%d %H:%M:%S")
    if d.is_approved:
      rs['is_approved'] = "1"
    else:
      rs['is_approved'] = "0"

    data.append(rs)
    msg = f"[clinicApprovelist]result:{data}"
    logger1.warning(msg)

  result = {
    "rs1": data
  }

  d2=datetime.datetime.now()
  diff = (d2 - d1).total_seconds()
  msg = f"[clinicApprovelist]done, spent : {diff} seconds ========================================="    
  logger1.warning(msg)
  
  if request.is_ajax():
    return JsonResponse(result, safe=False)

  return render(request, "member/clinicApprovelist.html", result,)

# 診所申請審核
def clinicDetail(request):
  if not request.session.get('is_login',None):
    # 重新登入
    return redirect('/member/login/')

  clinic_id = request.GET.get("clinic_id",None)
  d1=datetime.datetime.now()
  msg = f"[clinicDetail]1-start====================================================="
  logger1.warning(msg)
  msg = f"[clinicDetail]clinic_id:{clinic_id}"
  logger1.warning(msg)

  if clinic_id is not None:

    result = {}

    # 個人資訊
    ret = clinic.objects.get(pk = clinic_id)
    rs = {}
    uid = ret.member_id
    rs['clinic_id'] = ret.clinic_id
    rs['member_id'] = ret.member_id
    rs['clinic_name'] = ret.clinic_name
    rs['area'] = ret.area
    rs['address'] = ret.address
    rs['tel'] = ret.tel
    rs['serv_content'] = ret.serv_content
    rs['desc'] = ret.desc
    rs['email'] = ret.email
    photo = ""
    if ret.photo is not None and len(ret.photo) > 0:
        image_path = f"{settings.IMAGE_URL}member/{uid}/"
        logger1.warning(image_path)
        photo = os.path.join(image_path,ret.photo)
    rs['photo'] = photo

    rs['created_date'] = datetime.datetime.strftime(ret.created_date, "%Y/%m/%d %H:%M:%S")
    if ret.is_approved:
      rs['is_approved'] = "1"
    else:
      rs['is_approved'] = "0"

    ret1 = member.objects.get(pk = ret.member_id)
    rs['account'] = ret1.account
    if ret1.is_doctor:
      rs['is_doctor'] = "1"
    else:
      rs['is_doctor'] = "0"

    if ret1.is_clinic:
      rs['is_clinic'] = "1"
    else:
      rs['is_clinic'] = "0"

    if ret1.is_store:
      rs['is_store'] = "1"
    else:
      rs['is_store'] = "0"

    if ret1.last_login_date is not None:
      rs['last_login_date'] = datetime.datetime.strftime(ret1.last_login_date, "%Y/%m/%d %H:%M:%S")
    else:
      rs['last_login_date'] = ""

    if ret1.last_modify_date is not None:
      rs['last_modify_date'] = datetime.datetime.strftime(ret1.last_modify_date, "%Y/%m/%d %H:%M:%S")
    else:
      rs['last_modify_date'] = ""

    admin_account = request.session.get('user_id','')
    result = {
      "data": rs,
      "admin_account": admin_account
    }

  d2=datetime.datetime.now()
  diff = (d2 - d1).total_seconds()
  msg = f"[clinicDetail]done, spent : {diff} seconds ========================================="    
  logger1.warning(msg)

  if request.is_ajax():
    return JsonResponse(result, safe=False)

  return render(request, "member/clinicDetail.html", result,)

# 診所申請核可
def approveClinic(request):
  if not request.session.get('is_login',None):
    # 重新登入
    return redirect('/member/login/')

  if request.method == 'POST':

    admin_account = request.session.get('user_id',None)
    clinic_id = request.POST['clinic_id']
    result = {}
    msg = ""
    try:
      matched = clinic.objects.get(pk=clinic_id)
      member_id = matched.member_id
      matched.is_approved = True
      matched.approve_account = admin_account
      matched.approve_date = datetime.datetime.now()
      matched.last_modify_date = datetime.datetime.now()
      matched.save()

      matched1 = member.objects.get(pk = member_id)
      matched1.is_clinic = True
      matched1.last_modify_date = datetime.datetime.now()
      matched1.save()

      msg = "確認完成。"

    except clinic.DoesNotExist:
      msg = f"此診所ID{clinic_id}不存在!!"

    result = {'msg':msg}

  if request.is_ajax():
    return JsonResponse(result, safe=False)

  return render(request, "member/clinicDetail.html", result,)

'''
  店家申請審核
'''
def storeApprovelist(request):
  if not request.session.get('is_login',None):
    # 重新登入
    return redirect('/member/login/')

  start_date = request.GET.get("startTime1",None)
  end_date = request.GET.get("endTime1",None)
  args = request.GET.get("args",None)

  d1=datetime.datetime.now()
  msg = f"[storeApprovelist]1-start====================================================="
  logger1.warning(msg)
  msg = f"[storeApprovelist]start_date:{start_date} end_date:{end_date} args:{args}"
  logger1.warning(msg)

  result = {}

  f1 = Q()
  f1.connector = "AND"
  if start_date is not None and len(start_date) > 0:
    chkdate = datetime.datetime.strptime(start_date,"%Y-%m-%d")
    chkdate = chkdate.replace(hour=0,minute=0,second=0,microsecond=0)
    f1.children.append(("created_date__gte",chkdate))

  if end_date is not None and len(end_date) > 0:
    chkdate = datetime.datetime.strptime(end_date,"%Y-%m-%d")
    chkdate = chkdate.replace(hour=23,minute=59,second=59,microsecond=999999)
    f1.children.append(("created_date__lte",chkdate))

  f2 = Q()
  f2.connector = "OR"
  if args is not None and len(args) > 0:
    if args.isdigit():
      f2.children.append(("member_id",args))

    f2.children.append(("store_name",args))

  ret1 = store.objects.filter(f1).filter(f2).order_by('store_id')

  data = []
  for d in ret1:
    rs = {}
    rs['store_id'] = d.store_id
    rs['member_id'] = d.member_id
    rs['store_name'] = d.store_name
    rs['area'] = d.area
    rs['address'] = d.address
    rs['tel'] = d.tel
    rs['created_date'] = datetime.datetime.strftime(d.created_date, "%Y/%m/%d %H:%M:%S")
    if d.is_approved:
      rs['is_approved'] = "1"
    else:
      rs['is_approved'] = "0"

    data.append(rs)
    msg = f"[storeApprovelist]result:{data}"
    logger1.warning(msg)

  result = {
    "rs1": data
  }

  d2=datetime.datetime.now()
  diff = (d2 - d1).total_seconds()
  msg = f"[storeApprovelist]done, spent : {diff} seconds ========================================="    
  logger1.warning(msg)
  
  if request.is_ajax():
    return JsonResponse(result, safe=False)

  return render(request, "member/storeApprovelist.html", result,)

# 店家申請審核明細頁面
def storeDetail(request):
  if not request.session.get('is_login',None):
    # 重新登入
    return redirect('/member/login/')

  store_id = request.GET.get("store_id",None)
  d1=datetime.datetime.now()
  msg = f"[storeDetail]1-start====================================================="
  logger1.warning(msg)
  msg = f"[storeDetail]store_id:{store_id}"
  logger1.warning(msg)
  if store_id is not None:

    result = {}

    # 個人資訊
    ret = store.objects.get(pk = store_id)
    rs = {}
    uid = ret.member_id
    rs['store_id'] = ret.store_id
    rs['member_id'] = ret.member_id
    rs['store_name'] = ret.store_name
    rs['area'] = ret.area
    rs['address'] = ret.address
    rs['tel'] = ret.tel
    rs['serv_content'] = ret.serv_content
    rs['desc'] = ret.desc
    rs['email'] = ret.email
    photo = ""
    if ret.photo is not None and len(ret.photo) > 0:
        image_path = f"{settings.IMAGE_URL}member/{uid}/"
        logger1.warning(image_path)
        photo = os.path.join(image_path,ret.photo)
    rs['photo'] = photo

    rs['created_date'] = datetime.datetime.strftime(ret.created_date, "%Y/%m/%d %H:%M:%S")
    if ret.is_approved:
      rs['is_approved'] = "1"
    else:
      rs['is_approved'] = "0"

    ret1 = member.objects.get(pk = ret.member_id)
    rs['account'] = ret1.account
    if ret1.is_doctor:
      rs['is_doctor'] = "1"
    else:
      rs['is_doctor'] = "0"

    if ret1.is_clinic:
      rs['is_clinic'] = "1"
    else:
      rs['is_clinic'] = "0"

    if ret1.is_store:
      rs['is_store'] = "1"
    else:
      rs['is_store'] = "0"

    if ret1.last_login_date is not None:
      rs['last_login_date'] = datetime.datetime.strftime(ret1.last_login_date, "%Y/%m/%d %H:%M:%S")
    else:
      rs['last_login_date'] = ""

    if ret1.last_modify_date is not None:
      rs['last_modify_date'] = datetime.datetime.strftime(ret1.last_modify_date, "%Y/%m/%d %H:%M:%S")
    else:
      rs['last_modify_date'] = ""

    admin_account = request.session.get('user_id','')
    result = {
      "data": rs,
      "admin_account": admin_account
    }

  d2=datetime.datetime.now()
  diff = (d2 - d1).total_seconds()
  msg = f"[storeDetail]done, spent : {diff} seconds ========================================="    
  logger1.warning(msg)

  if request.is_ajax():
    return JsonResponse(result, safe=False)

  return render(request, "member/storeDetail.html", result,)

# 店家申請核可
def approveStore(request):
  if not request.session.get('is_login',None):
    # 重新登入
    return redirect('/member/login/')

  if request.method == 'POST':

    admin_account = request.session.get('user_id',None)
    store_id = request.POST['store_id']
    result = {}
    msg = ""
    try:
      matched = store.objects.get(pk=store_id)
      member_id = matched.member_id
      matched.is_approved = True
      matched.approve_account = admin_account
      matched.approve_date = datetime.datetime.now()
      matched.last_modify_date = datetime.datetime.now()
      matched.save()

      matched1 = member.objects.get(pk = member_id)
      matched1.is_store = True
      matched1.last_modify_date = datetime.datetime.now()
      matched1.save()

      msg = "確認完成。"

    except store.DoesNotExist:
      msg = f"此店家ID{store_id}不存在!!"

    result = {'msg':msg}

  if request.is_ajax():
    return JsonResponse(result, safe=False)

  return render(request, "member/storeDetail.html", result,)

# 動態
def dynMsg(request):
  return render(request, "member/dynMsg.html")

# 取得所有動態消息清單
class getDynaPostListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        search_type = request.GET.get("search_type",None)
        d1=datetime.datetime.now()
        msg = f"[getDynaPostListView(getDynaPostList)]1.start====================="
        logger1.warning(msg)
        msg = f"[getDynaPostListView(getDynaPostList)]search_type:{search_type}"
        logger1.warning(msg)

        success = False
        error = ""
        result = {}
        ret1 = ""
        if search_type == '1':          # order by  post_created_at
            ret1 = dynaPost.objects.all().order_by('-post_created_at')
        elif search_type == '2':        # order by  post_like
            ret1 = dynaPost.objects.all().order_by('-post_like')
        else:
            ret1 = dynaPost.objects.all().order_by('-post_id')

        data = []

        for obj1 in ret1:
            rs1 = {}
            rs1['post_id'] = obj1.post_id
            if obj1.post_published is not None:
                rs1['post_published'] = datetime.datetime.strftime(obj1.post_published, "%Y/%m/%d %H:%M:%S")
            else:
                rs1['post_published'] = ""

            if obj1.post_created_at is not None:
                rs1['post_created_at'] = datetime.datetime.strftime(obj1.post_created_at, "%Y/%m/%d %H:%M:%S")
            else:
                rs1['post_created_at'] = ""

            if obj1.post_update_at is not None:
                rs1['post_update_at'] = datetime.datetime.strftime(obj1.post_update_at, "%Y/%m/%d %H:%M:%S")
            else:
                rs1['post_update_at'] = ""

            rs1['post_content'] = obj1.post_content
            rs1['post_decription'] = obj1.post_decription
            rs1['post_picture'] = obj1.post_picture
            rs1['post_url'] = obj1.post_url
            rs1['post_like'] = obj1.post_like
            rs1['post_views'] = obj1.post_views
            rs1['page_provider'] = obj1.page_provider
            rs1['page_name'] = obj1.page_name
            rs1['page_icon'] = obj1.page_icon

            data.append(rs1)

        success = True
        result["data"] = data

        if ret1.count() == 0:
            error = f"查無資料!"
        
        result["success"] = success
        if len(error) > 0:
            result["error"] = error

        d2=datetime.datetime.now()
        diff = (d2 - d1).total_seconds()
        msg = f"[getDynaPostListView(getDynaPostList)]2.done, spent : {diff} seconds"
        logger1.debug(msg)
        
        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 用戶動態資料按讚設定
def member_like_post(request):
    result = {}
    code = -1
    msg = ""
    uid = -1
    if request.method == 'POST':
        try:
            member_id = request.POST.get('member_id',None)
            post_id = request.POST.get('post_id',None)
            isLike = request.POST.get('isLike',None)

            if member_id is not None:
                isExist = member.objects.filter(pk=member_id).exists()
                if not isExist:
                    msg = f"會員ID:{member_id} 不存在."
            else:
                msg = "Need member id !"

            if post_id is not None:
                isExist = dynaPost.objects.filter(post_id=post_id).exists()    
                if not isExist:
                    msg = f"貼文ID:{post_id} 不存在."
            else:
                msg = "Need post id !"

            if isLike is None:
                msg = "Need isLike data !"

            like_count = 0
            isLike_num = 0
            if len(msg) == 0:
                isLike_num = int(isLike)
                f1 = Q()
                f1.connector = "AND"
                f1.children.append(("member_id",member_id))
                f1.children.append(("post_id_id",post_id))
                isExist = MemberLikePost.objects.filter(f1).exists()

                if not isExist:
                    createdObj = MemberLikePost.objects.create(
                        member_id = member_id,
                        post_id_id = post_id,
                        isLike = isLike,
                        last_modify_date = datetime.datetime.now()
                    )
                    if isLike_num == 1:
                        like_count = 1
                    elif isLike_num == 2:
                        like_count = -1
                else:
                    rslist = MemberLikePost.objects.filter(f1)
                    for d in rslist:
                        if d.isLike != isLike_num:
                            if d.isLike == 1:
                                if isLike_num == 0 or isLike_num == 2:
                                    like_count = -1 
                            elif d.isLike == 0 or d.isLike == 2:
                                if isLike_num == 1:
                                    like_count = 1
                            d.isLike = isLike
                            d.last_modify_date = datetime.datetime.now()
                            d.save()
                    #  更新按讚次數
                matched = dynaPost.objects.get(post_id=post_id)
                if like_count != 0:
                    matched.post_like = matched.post_like + like_count
                    matched.last_modify_date = datetime.datetime.now()
                    matched.save()

                code = 0
                likes_count = matched.post_like
                msg = "success"
        except Exception as e:
            code = -1
            msg = f"[member_like_post]error:{e}"

    if code == 0:
        result = {
            "code": code,
            "msg" : msg,
            "likes_count" : likes_count
        }
        return JsonResponse(result, safe=False)
    else:
        result = {
            "code": code,
            "msg": msg
        }
        return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

# 新動態清單(增加用戶按讚資料)
class getNewDynaPostListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        member_id = request.GET.get("member_id",None)
        search_type = request.GET.get("search_type",None)
        success = False
        error = ""
        result = {}
        d1=datetime.datetime.now()
        msg = f"[getNewDynaPostListView(getNewDynaPostList)]1.start====================="
        logger1.warning(msg)

        if member_id is None:
            error = f"Need member id!"
        else:
            msg = f"[getNewDynaPostListView(getNewDynaPostList)]member_id:{member_id},search_type:{search_type}"
            logger1.warning(msg)

            ret1 = ""
            if search_type == '1':          # order by  post_created_at
                ret1 = dynaPost.objects.all().order_by('-post_created_at')
            elif search_type == '2':        # order by  post_like
                ret1 = dynaPost.objects.all().order_by('-post_like')
            else:
                ret1 = dynaPost.objects.all().order_by('-post_id')

            data = []

            for obj1 in ret1:
                rs1 = {}
                rs1['post_id'] = obj1.post_id
                if obj1.post_published is not None:
                    rs1['post_published'] = datetime.datetime.strftime(obj1.post_published, "%Y/%m/%d %H:%M:%S")
                else:
                    rs1['post_published'] = ""

                if obj1.post_created_at is not None:
                    rs1['post_created_at'] = datetime.datetime.strftime(obj1.post_created_at, "%Y/%m/%d %H:%M:%S")
                else:
                    rs1['post_created_at'] = ""

                if obj1.post_update_at is not None:
                    rs1['post_update_at'] = datetime.datetime.strftime(obj1.post_update_at, "%Y/%m/%d %H:%M:%S")
                else:
                    rs1['post_update_at'] = ""

                rs1['post_content'] = obj1.post_content
                rs1['post_decription'] = obj1.post_decription
                rs1['post_picture'] = obj1.post_picture
                rs1['post_url'] = obj1.post_url
                rs1['post_like'] = obj1.post_like
                rs1['post_views'] = obj1.post_views
                rs1['page_provider'] = obj1.page_provider
                rs1['page_name'] = obj1.page_name
                rs1['page_icon'] = obj1.page_icon
                # 取得用戶是否有按讚的紀錄
                f1 = Q()
                f1.connector = "AND"
                f1.children.append(("member_id",member_id))
                f1.children.append(("post_id_id",obj1.post_id))
                isExist = MemberLikePost.objects.filter(f1).exists()
                isLike = 0
                if isExist:
                    rslist = MemberLikePost.objects.filter(f1)
                    for d in rslist:
                        isLike = d.isLike

                rs1['isLike'] = isLike
                data.append(rs1)

            success = True
            result["data"] = data

            if ret1.count() == 0:
                error = f"查無資料!"
            
            result["success"] = success
        if len(error) > 0:
            result["error"] = error

        d2=datetime.datetime.now()
        diff = (d2 - d1).total_seconds()
        msg = f"[getNewDynaPostListView(getNewDynaPostList)]2.done, spent : {diff} seconds"
        logger1.debug(msg)
        
        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# 第三方登入
class SocialLogin(TokenObtainPairView):
    permission_classes = (AllowAny, ) # AllowAny for login
    serializer_class = SocialLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            social_user = serializer.save()
            refresh = RefreshToken.for_user(social_user.user)
            result = {
                'code': 0,
                'msg' : 'success',
                'uid' : social_user.member_id,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(result)
        else:
            raise ValueError('Not serializable')

class SocialBindView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SocialBindSerializer
    
    def post(self, request, format=None):
        success = False
        error = ""
        result = {}
        serializer = self.serializer_class(data=request.data)
        msg = ""
        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                success = True
            else:
                success = False
                error = serializer.errors
                print(f"error1:{error}")

        except Exception as e:
            success = False
            error = str(e)
            print(f"error2:{error}")

        print(f"[SocialBindView]6")
        result["success"] = success
        if len(error) > 0:
            result["error"] = error

        if success == True:
            return JsonResponse(result, safe=False)
        elif success == False:
            return JsonResponse(result, safe=False,status=status.HTTP_400_BAD_REQUEST)