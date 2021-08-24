from django.conf.urls import url, include
from django.urls import path
#from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static

from member.views import *
from member.cron import *

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# app_name = 'member'
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('api/token/obtain/', GoogleLogin.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('', index, name='index'),
    # 註冊
    path('register/', AddMemberView.as_view()),
    # 重置密碼
    path('reset_password/', ResetPasswordView.as_view()),

    # 透過帳號取得UID(更改密碼)
    path('get_member_uid/', get_member_uid, name='get_member_uid'),

    # 登入
    path('member_login/', LoginView.as_view()),

    # 取得會員資料
    path('getMemberInfo/', GetMemberInfoView.as_view(), name='getMemberInfo'),
    # 更新會員資料
    path('updateMemberInfo/', UpdateMemberView.as_view()),

    # 新增寵物資料
    path('addPetInfo/', AddPetInfoView.as_view()),
    # 取得寵物資料
    path('getPetInfo/', GetPetInfoView.as_view(), name='getPetInfo'),
    # 更新寵物資料
    path('updatePetInfo/', UpdatePetInfoView.as_view()),
    # 獲得寵物清單資料
    path('getPetList/', GetPetListView.as_view(), name='getPetList'),

    # 新增醫生資料
    path('addDoctorInfo/', AddDoctorInfoView.as_view()),
    # 取得醫生資料
    path('getDoctorInfo/', GetDoctorInfoView.as_view(), name='getDoctorInfo'),
    # 更新醫生資料
    path('updateDoctorInfo/', UpdateDoctorInfoView.as_view()),
    # 取得醫生清單資料
    path('getDocList/', getDocListView.as_view(), name='getDocList'),

    # 建立醫生看診時間表
    path('addDocAppoint/', AddDocAppointView.as_view()),
    # 更新醫生看診時間表
    path('updateDocAppoint/', UpdateDocAppointView.as_view(), name='updateDocAppoint'),
    # 用戶獲得看診時間表
    path('getDocAppoint/', GetDocAppointView.as_view()),
    # 建立用戶預約看診表
    path('addUserAppoint/', AddUserAppointView.as_view()),

    # 建立諮詢表
    path('addAdvisory/', AddAdvisoryView.as_view()),
    # 更新諮詢表
    path('updateAdvisory/', UpdateAdvisoryView.as_view(), name='updateAdvisory'),
    # 獲得諮詢表明細
    path('getAdvisoryDetail/', GetAdvisoryDetailView.as_view()),
    # 獲得諮詢表清單(for用戶)
    path('getUserAdvisoryList/', GetUserAdvisoryListView.as_view()),
    # 獲得諮詢表清單(for醫生)
    path('getDocAdvisoryList/', GetDocAdvisoryListView.as_view()),    

    # 建立評價資料
    path('addDocComment/', AddDocCommentView.as_view()),
    # 取得評價資料清單
    path('getDocCommentList/', GetDocCommentListView.as_view()),

    # 建立醫生營業時段
    path('addDocBH/', AddDocBussinssHourView.as_view()),
    # 更新醫生營業時段
    path('updateDocBH/', UpdateDocBussinssHourView.as_view(), name='updateDocBH'),
    # 取得醫生營業時段
    path('getDocBH/', GetDocBussinssHourView.as_view()),

    # 新增診所資料
    path('addClinicInfo/', AddClinicInfoView.as_view()),
    # 取得診所資料
    path('getClinicInfo/', GetClinicInfoView.as_view(), name='getClinicInfo'),
    # 更新診所資料
    path('updateClinicInfo/', UpdateClinicInfoView.as_view()),
    # 取得診所清單資料
    path('getClinicList/', getClinicListView.as_view(), name='getClinicList'),
    # 建立診所營業時段
    path('addClinicBH/', AddClinicBussinssHourView.as_view()),
    # 更新診所營業時段
    path('updateClinicBH/', UpdateClinicBussinssHourView.as_view(), name='updateClinicBH'),
    # 取得診所營業時段
    path('getClinicBH/', GetClinicBussinssHourView.as_view()),

    # 新增店家資料
    path('addStoreInfo/', AddStoreInfoView.as_view()),
    # 取得店家資料
    path('getStoreInfo/', GetStoreInfoView.as_view(), name='getStoreInfo'),
    # 更新店家資料
    path('updateStoreInfo/', UpdateStoreInfoView.as_view()),
    # 取得店家清單資料
    path('getStoreList/', getStoreListView.as_view(), name='getStoreList'),
    # 建立店家營業時段
    path('addStoreBH/', AddStoreBussinssHourView.as_view()),
    # 更新店家營業時段
    path('updateStoreBH/', UpdateStoreBussinssHourView.as_view(), name='updateStoreBH'),
    # 取得店家營業時段
    path('getStoreBH/', GetStoreBussinssHourView.as_view()),

    # 獲得用戶諮詢清單
    path('getUserAdviseList/', GetUserAdviseListView.as_view()),
    # 獲得用戶預約清單
    path('getUserAppointList/', GetUserAppointListView.as_view()),
    # 獲得寵物病例清單資料
    path('getUserAdviseDate/', GetUserAdviseDateView.as_view()), 

    # 登入
    path('login/', login, name='login'),
    # 登出
    path('logout/', logout, name='logout'), 

    # 醫生申請核可
    path('docApprovelist/', docApprovelist, name='docApprovelist'),
    path('docDetail/', docDetail, name='docDetail'),
    path('approveDoctor/', approveDoctor, name='approveDoctor'),
    # 醫生視訊連結
    path('docVideoLink/', docVideoLink, name='docVideoLink'),
    path('updateDocVideoLink/', updateDocVideoLink, name='updateDocVideoLink'),

    # 診所申請核可
    path('clinicApprovelist/', clinicApprovelist, name='clinicApprovelist'),
    path('clinicDetail/', clinicDetail, name='clinicDetail'),
    path('approveClinic/', approveClinic, name='approveClinic'),
    # 店家申請核可
    path('storeApprovelist/', storeApprovelist, name='storeApprovelist'),
    path('storeDetail/', storeDetail, name='storeDetail'),
    path('approveStore/', approveStore, name='approveStore'),

    # 動態
    path('dynMsg/', dynMsg, name='dynMsg'),
    #path('getDynaMsg_job/', getDynaMsg_job, name='getDynaMsg_job'),
    # 動態清單
    path('getDynaPostList/', getDynaPostListView.as_view()),
    # 用戶動態資料按讚紀錄
    path('member_like_post/', member_like_post, name='member_like_post'),
    # 新動態清單(增加用戶按讚資料)
    path('getNewDynaPostList/', getNewDynaPostListView.as_view()),

    # 第三方登入
    path('socialLogin/', SocialLogin.as_view()),
    # 第三方帳號綁定
    path('socialBind/', SocialBindView.as_view()),
]