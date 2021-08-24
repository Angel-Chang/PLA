from django.contrib.auth.models import User, Group
from django.conf import settings
from rest_framework import serializers
from member.models import *
from google.oauth2 import id_token
from google.auth.transport import requests

from petslife.settings import SOCIAL_GOOGLE_CLIENT_ID,SOCIAL_AUTH_FACEBOOK_KEY,SOCIAL_AUTH_FACEBOOK_SECRET
from member.models import SocialAccount
import json
import requests

# 會員註冊資料
class RegisterSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = member
        fields = [
            'uid', 'account', 'user_password'
        ]

class UpdatePasswordSerializer(serializers.HyperlinkedModelSerializer):
    uid = serializers.IntegerField(label='UID')
    new_password = serializers.CharField(label='新密碼', max_length=20)
    class Meta:
        model = member
        fields = [
            'uid', 'new_password'
        ]

# for login
class LoginSerializer(serializers.HyperlinkedModelSerializer):
    LOGIN_TYPE = (
        (0, '一般登入'),
        (1, 'google 登入'),
        (2, 'facebook 登入')
    )
    login_method = serializers.ChoiceField(choices=LOGIN_TYPE, label='登入方式')
    class Meta:
        model = member
        fields = [
            'uid', 'account', 'user_password', 'login_type'
        ]

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    uid = serializers.IntegerField(label='uid')
    class Meta:
        model = member
        fields = [
            'uid', 'account', 'real_name','nick_name','idNo','email',
            'address','sex','myself','status','photo',
            'is_doctor','is_clinic','is_store'
        ]

# 寵物資料 for 新增
class NewPetSerializer(serializers.HyperlinkedModelSerializer):
    member_id = serializers.IntegerField(label='會員ID')
    class Meta:
        model = pet
        fields = [
            'member_id','pet_name', 'chip','category','breed','sex','age',
            'weight','description','photo'
        ]

# 寵物資料
class PetSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(label='寵物ID')
    member_id = serializers.IntegerField(label='會員ID')
    class Meta:
        model = pet
        fields = [
            'id', 'member_id','pet_name', 'chip','category','breed','sex','age',
            'weight','description','photo'
        ]

# 醫生資料 for 新增
class NewDoctorSerializer(serializers.HyperlinkedModelSerializer):
    member_id = serializers.IntegerField(label='會員ID')
    class Meta:
        model = doctor
        fields = [
            'member_id','clinic', 'title','skill','experience',
            'area','clinic_addr','doc_photo'
        ]

# 醫生資料
class DoctorSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(label='醫師ID')
    member_id = serializers.IntegerField(label='會員ID')
    class Meta:
        model = doctor
        fields = [
            'id','member_id','clinic', 'title','skill','experience',
            'area','clinic_addr','doc_photo','doc_name','room_url'
        ]

# 醫生看診資料 for 新增
class NewDocAppointSerializer(serializers.HyperlinkedModelSerializer):
    doc_id = serializers.IntegerField(label='醫生ID')
    set_date = serializers.DateField(format=settings.DATE_FORMAT)
    class Meta:
        model = docAppoint
        fields = [
            'doc_id','set_date', 'set_hour','set_section','status'
        ]

# 醫生看診資料
class DocAppointSerializer(serializers.HyperlinkedModelSerializer):
    appoint_id = serializers.IntegerField(label='看診表ID')
    set_date = serializers.DateField(format=settings.DATE_FORMAT)
    class Meta:
        model = docAppoint
        fields = [
            'appoint_id','doc_id', 'set_date','set_hour','set_section',
            'status'
        ]

# 醫生看診資料 for 更新狀態
class UpdDocAppointSerializer(serializers.HyperlinkedModelSerializer):
    appoint_id = serializers.IntegerField(label='看診表ID')
    class Meta:
        model = docAppoint
        fields = [
            'appoint_id','status'
        ]

# 會員預約看診資料 for 新增
class NewUserAppointSerializer(serializers.HyperlinkedModelSerializer):
    appoint_id = serializers.IntegerField(label='看診表ID')
    member_id = serializers.IntegerField(label='會員ID')
    pet_id = serializers.IntegerField(label='寵物ID')
    class Meta:
        model = userAppoint
        fields = [
            'appoint_id','member_id', 'pet_id','mark'
        ]

# 諮詢表資料 for 新增
class NewAdvisorySerializer(serializers.HyperlinkedModelSerializer):
    user_appoint_id = serializers.IntegerField(label='預約看診ID')
    member_id = serializers.IntegerField(label='會員ID')
    pet_id = serializers.IntegerField(label='寵物ID')
    doc_id = serializers.IntegerField(label='醫生ID')
    class Meta:
        model = advisory
        fields = [
            'user_appoint_id','member_id','pet_id', 'doc_id','advisory_date',
            'advisory_time','fee','description','case_history','sympton',
            'suggest','medcine'
        ]

# 諮詢表資料 for 更新
class AdvisorySerializer(serializers.HyperlinkedModelSerializer):
    advisory_id = serializers.IntegerField(label='諮詢表ID')
    class Meta:
        model = advisory
        fields = [
            'advisory_id','description','case_history','sympton',
            'suggest','medcine'
        ]

# 諮詢表資料 for 明細
class AdvisoryDetailSerializer(serializers.HyperlinkedModelSerializer):
    # user_appoint_id = serializers.IntegerField(label='預約看診ID')
    # member_id = serializers.IntegerField(label='會員ID')
    pet_id = serializers.IntegerField(label='寵物ID')
    doc_id = serializers.IntegerField(label='醫生ID')
    advisory_date = serializers.DateField(format=settings.DATE_FORMAT)
    class Meta:
        model = advisory
        # fields = [
        #     'user_appoint_id','member_id','pet_id', 'doc_id','advisory_date',
        #     'advisory_time','fee','description','case_history','sympton',
        #     'suggest','medcine'
        # ]
        fields = [
            'pet_id', 'doc_id','advisory_date',
            'advisory_time','fee','description','case_history','sympton',
            'suggest','medcine'
        ]

# 醫生評價資料 for 新增
class NewDocCommentSerializer(serializers.HyperlinkedModelSerializer):
    member_id = serializers.IntegerField(label='會員ID')
    doc_id = serializers.IntegerField(label='醫生ID')
    advisory_id = serializers.IntegerField(label='諮詢表ID')
    class Meta:
        model = docComment
        fields = [
            'member_id','doc_id','advisory_id','stars','memo','user_photo'
        ]

# 醫生營業時段 for 新增
class NewDocBHSerializer(serializers.HyperlinkedModelSerializer):
    doc_id = serializers.IntegerField(label='醫生ID')
    class Meta:
        model = docBH
        fields = [
            'doc_id','bh1_name', 'bh2_name','bh3_name',
            'bh1_setting','bh2_setting','bh3_setting'
        ]

# 醫生營業時段
class DocBHSerializer(serializers.HyperlinkedModelSerializer):
    bh_id = serializers.IntegerField(label='醫生營業時段ID')
    class Meta:
        model = docBH
        fields = [
            'bh_id','bh1_name', 'bh2_name','bh3_name',
            'bh1_setting','bh2_setting','bh3_setting'
        ]

# 診所資料 for 新增
class NewClinicSerializer(serializers.HyperlinkedModelSerializer):
    member_id = serializers.IntegerField(label='會員ID')
    class Meta:
        model = clinic
        fields = [
            'member_id','clinic_name', 'area','address','tel',
            'serv_content','desc','email','photo'
        ]

# 診所資料
class ClinicSerializer(serializers.HyperlinkedModelSerializer):
    clinic_id = serializers.IntegerField(label='診所ID')
    member_id = serializers.IntegerField(label='會員ID')

    class Meta:
        model = clinic
        fields = [
            'clinic_id','member_id','clinic_name', 'area','address','tel',
            'serv_content','desc','email','photo'
        ]

# 診所營業時段 for 新增
class NewClinicBHSerializer(serializers.HyperlinkedModelSerializer):
    clinic_id = serializers.IntegerField(label='診所ID')
    class Meta:
        model = clinicBH
        fields = [
            'clinic_id','bh1_name', 'bh2_name','bh3_name',
            'bh1_setting','bh2_setting','bh3_setting'
        ]

# 診所營業時段
class ClinicBHSerializer(serializers.HyperlinkedModelSerializer):
    bh_id = serializers.IntegerField(label='診所營業時段ID')
    class Meta:
        model = clinicBH
        fields = [
            'bh_id','bh1_name', 'bh2_name','bh3_name',
            'bh1_setting','bh2_setting','bh3_setting'
        ]

# 店家資料 for 新增
class NewStoreSerializer(serializers.HyperlinkedModelSerializer):
    member_id = serializers.IntegerField(label='會員ID')
    class Meta:
        model = store
        fields = [
            'member_id','store_name', 'area','address','tel',
            'serv_content','desc','email','photo'
        ]

# 店家資料
class StoreSerializer(serializers.HyperlinkedModelSerializer):
    member_id = serializers.IntegerField(label='會員ID')
    store_id = serializers.IntegerField(label='店家ID')
    class Meta:
        model = store
        fields = [
            'store_id','member_id','store_name', 'area','address','tel',
            'serv_content','desc','email','photo'
        ]

# 店家營業時段 for 新增
class NewStoreBHSerializer(serializers.HyperlinkedModelSerializer):
    store_id = serializers.IntegerField(label='店家ID')
    class Meta:
        model = storeBH
        fields = [
            'store_id','bh1_name', 'bh2_name','bh3_name',
            'bh1_setting','bh2_setting','bh3_setting'
        ]

# 店家營業時段
class StoreBHSerializer(serializers.HyperlinkedModelSerializer):
    bh_id = serializers.IntegerField(label='店家營業時段ID')
    class Meta:
        model = storeBH
        fields = [
            'bh_id','bh1_name', 'bh2_name','bh3_name',
            'bh1_setting','bh2_setting','bh3_setting'
        ]

class SocialLoginSerializer(serializers.Serializer):
    login_type = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def check_google_token(self, token):
        """
        驗證 id_token 是否正確

        token: JWT
        """
        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), SOCIAL_GOOGLE_CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            if idinfo['aud'] not in [SOCIAL_GOOGLE_CLIENT_ID]:
                raise ValueError('Could not verify audience.')
            # Success
            return idinfo
        except ValueError:
            pass

    def check_facebook_token(self, access_token):
        """
        驗證 access_token 是否有效
        https://graph.facebook.com/debug_token?
        input_token=INPUT_TOKEN
        &access_token=ACCESS_TOKEN

        其中 input_token 是登錄後 Facebook 返回的 token
        access_token 是你的 AppId 和 AppSecret  格式 ：AppId|AppSecret  ，豎線分開
        """
        try:
            # 驗證token是否有效的url
            url = 'https://graph.facebook.com/debug_token'
            my_params = {
                'input_token': access_token, 
                'access_token': SOCIAL_AUTH_FACEBOOK_KEY+'|'+SOCIAL_AUTH_FACEBOOK_SECRET
            }
            # call api (get)
            res = requests.get(url, params = my_params)
            res1 = json.loads(res.text)
            return res1
        except ValueError:
            pass

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

    def create(self, validated_data):
        login_type = validated_data.get('login_type')
        token = validated_data.get('token')
        if login_type == "1":      # google login
            idinfo = self.check_google_token(token)
            if idinfo:
                # User not exists
                if not SocialAccount.objects.filter(unique_id=idinfo['sub']).exists():
                    user = User.objects.create_user(
                        username=f"{idinfo['name']} {idinfo['email']}", # Username has to be unique
                        first_name=idinfo['given_name'],
                        last_name=idinfo['family_name'],
                        email=idinfo['email']
                    )
                    new_social = SocialAccount.objects.create(
                        user=user,
                        unique_id=idinfo['sub']
                    )
                    self.addLoginData(0,1,True,'success')
                    return new_social
                else:
                    social = SocialAccount.objects.get(unique_id=idinfo['sub'])
                    self.addLoginData(social.member_id,1,True,'success')
                    return social
                    # return social.user
            else:
                raise ValueError("Incorrect Credentials")
        elif login_type == "2":     # facebook login
            res = self.check_facebook_token(token)
            is_valid = res['data']['is_valid']
            if is_valid:
                user_id = res['data']['user_id']
                # 再去取user profile
                url = 'https://graph.facebook.com/me'
                my_params = {
                    'access_token': token, 
                    'fields': 'id,name,last_name,email,first_name'
                }
                # call api (get)
                mydata = requests.get(url, params = my_params)
                data = json.loads(mydata.text)
                
                unique_id = data['id']
                name = data['name']
                first_name = data['first_name']
                last_name = data['last_name']
                email = data['email']
                username=f"{name} {email}"
                if not SocialAccount.objects.filter(unique_id=unique_id).exists():
                    user = User.objects.create_user(
                        username=username, # Username has to be unique
                        first_name=first_name,
                        last_name=last_name,
                        email=email
                    )
                    new_social = SocialAccount.objects.create(
                        user=user,
                        unique_id=unique_id
                    )
                    self.addLoginData(0,2,True,'success')
                    return new_social
                else:
                    social = SocialAccount.objects.get(unique_id=unique_id)
                    self.addLoginData(social.member_id,2,True,'success')
                    return social
            else:
                raise ValueError("The facebook token is not valid!!")
        else:
            raise ValueError("Not support login type (1:google 2:facebook)!!")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class SocialBindSerializer(serializers.Serializer):
    """
    member_id:會員ID
    social_type:第三方登入的種類
      '1' : google
      '2' : facebook
    token : 取得第三方登入的token
    """
    member_id = serializers.IntegerField(required=True,label='會員ID')
    social_type = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def check_google_token(self, token):
        """
        驗證 id_token 是否正確

        token: JWT
        """
        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), SOCIAL_GOOGLE_CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            if idinfo['aud'] not in [SOCIAL_GOOGLE_CLIENT_ID]:
                raise ValueError('Could not verify audience.')
            # Success
            return idinfo
        except ValueError:
            pass

    def check_facebook_token(self, access_token):
        """
        驗證 access_token 是否有效
        https://graph.facebook.com/debug_token?
        input_token=INPUT_TOKEN
        &access_token=ACCESS_TOKEN

        其中 input_token 是登錄後 Facebook 返回的 token
        access_token 是你的 AppId 和 AppSecret  格式 ：AppId|AppSecret  ，豎線分開
        """
        try:
            # 驗證token是否有效的url
            url = 'https://graph.facebook.com/debug_token'
            my_params = {
                'input_token': access_token, 
                'access_token': SOCIAL_AUTH_FACEBOOK_KEY+'|'+SOCIAL_AUTH_FACEBOOK_SECRET
            }
            # call api (get)
            res = requests.get(url, params = my_params)
            res1 = json.loads(res.text)
            return res1
        except ValueError:
            pass

    def create(self, validated_data):
        member_id = validated_data.get('member_id')
        social_type = validated_data.get('social_type')
        token = validated_data.get('token')
        err = ""
        isExist = member.objects.filter(uid=member_id).exists()
        if not isExist:
            err = f"會員ID:{member_id} 不存在."
            raise Exception(err)

        if social_type not in ('1','2'):
            err = "Not support social type (1:google 2:facebook)!!"
            raise Exception(err)

        matched = member.objects.get(uid=member_id)
        account = matched.account
        matchedUser = User.objects.get(username=account)
        if social_type == "1":      # google
            if matched.google_account is not None and len(matched.google_account) > 0:
                err = f"會員ID:{member_id} google 帳號已綁定過，無法重新綁定！"
                raise Exception(err)
            else:
                idinfo = self.check_google_token(token)
                if idinfo:
                    matched.google_account = idinfo['email']
                    matched.last_modify_date = datetime.datetime.now()
                    matched.save()
                    # User not exists
                    if not SocialAccount.objects.filter(unique_id=idinfo['sub']).exists():
                        # matchedUser.first_name = idinfo['given_name']
                        # matchedUser.last_name = idinfo['family_name']
                        # matchedUser.save()

                        user = SocialAccount.objects.create(
                            user=matchedUser,
                            unique_id=idinfo['sub'],
                            member_id = member_id
                        )
                        return user
                    else:
                        social = SocialAccount.objects.get(unique_id=idinfo['sub'])
                        return social.user
                else:
                    raise Exception("Incorrect Credentials")
        elif social_type == "2":     # facebook login
            if matched.fb_account is not None and len(matched.fb_account) > 0:
                err = f"會員ID:{member_id} facebook 帳號已綁定過，無法重新綁定！"
                raise Exception(err)
            else:
                res = self.check_facebook_token(token)
                is_valid = res['data']['is_valid']
                if is_valid:
                    user_id = res['data']['user_id']
                    # 再去取user profile
                    url = 'https://graph.facebook.com/me'
                    my_params = {
                        'access_token': token, 
                        'fields': 'id,name,last_name,email,first_name'
                    }
                    # call api (get)
                    mydata = requests.get(url, params = my_params)
                    data = json.loads(mydata.text)

                    unique_id = data['id']
                    name = data['name']
                    first_name = data['first_name']
                    last_name = data['last_name']
                    email = data['email']
                    username=f"{name} {email}"

                    matched.fb_account = email
                    matched.last_modify_date = datetime.datetime.now()
                    matched.save()

                    if not SocialAccount.objects.filter(unique_id=unique_id).exists():
                        # matchedUser = User.objects.get(username=account)
                        # matchedUser.first_name = first_name
                        # matchedUser.last_name = last_name
                        # matchedUser.save()

                        user = SocialAccount.objects.create(
                            user=matchedUser,
                            unique_id=unique_id,
                            member_id = member_id,
                            provider = 'facebook'
                        )
                        return user
                    else:
                        social = SocialAccount.objects.get(unique_id=unique_id)
                        return social.user
                else:
                    raise Exception("Incorrect Credentials")
        else:
            raise Exception("Not support social type (1:google 2:facebook)!!")