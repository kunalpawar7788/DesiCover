import django_filters
from django_filters import DateFilter
from .models import *
from django.contrib.auth.models import User
from user.models import Userprofile
from django import forms



class TshirtFilter(django_filters.FilterSet):
    pro    =Products.objects.filter(sub_category='MALE').values_list('company',flat=True).distinct()
    company=django_filters.ModelChoiceFilter(to_field_name='company',field_name='company',queryset=pro)
    # model_No=django_filters.AllValuesMultipleFilter(choices=pro,lookup_expr='contains',widget=forms.CheckboxSelectMultiple)
    price = django_filters.NumberFilter(field_name="price",lookup_expr='lte',widget=forms.NumberInput(attrs={'type':'range', 'step': '1', 'min': '1', 'max': '1000','class':"slider"}),)
    class Meta:
        model = Products
        fields= ['company','price']
        # ['order','awb','mobile','date','city','placeorder_id__cancelorders','placeorder_id__custdelieverd']


class placeorderFilter(django_filters.FilterSet):
    order =django_filters.CharFilter(label='Order id',field_name='order_id__order',lookup_expr='icontains')
    awb   =django_filters.CharFilter(label='AWB',field_name='awb',lookup_expr='icontains')
    mobile=django_filters.CharFilter(label='Mobile No',field_name='placeorder_id__phone',lookup_expr='icontains')
    date  =django_filters.DateFilter(label='Date of Order',field_name='placeorder_id__order_date',lookup_expr='icontains',widget=forms.DateInput(attrs={'type':'date'}))
    city  =django_filters.CharFilter(label='Address',field_name='placeorder_id__city',lookup_expr='icontains')

    class Meta:
        model = orderawb
        fields = ['order','awb','mobile','date','city','placeorder_id__cancelorders','placeorder_id__custdelieverd']

class UserFilter(django_filters.FilterSet):
    city   = django_filters.CharFilter(label='City',field_name='city',lookup_expr='icontains')
    mobile = django_filters.CharFilter(label='Mobile', field_name='mobile', lookup_expr='icontains')
    date   = django_filters.DateFilter(label='Date of Joining',lookup_expr='icontains',widget=forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model  =  Userprofile
        fields =  ['user','city','mobile','date']

class ProductFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='add_date',lookup_expr='icontains',widget=forms.DateInput(attrs={'type':'date'}))
 
    product_name = django_filters.CharFilter(label='Product Name', field_name='title', lookup_expr='icontains')

    SUB_CATEGORY_CHOICES =Products.objects.values_list('sub_category',flat=True).distinct()
    CATEGORY_CHOICES     =Products.objects.values_list('category',flat=True).distinct()
    MODEL_NO_CHOICES     =Products.objects.values_list('model_No',flat=True).distinct()
    COMPANY_CHOICES      =Products.objects.values_list('company',flat=True).distinct()

    category=django_filters.ModelChoiceFilter(label='categorys',field_name='category',to_field_name='category',queryset= CATEGORY_CHOICES)
    company =django_filters.ModelChoiceFilter(label='Companys',field_name='company',to_field_name='company',queryset=COMPANY_CHOICES)

    model_No    =django_filters.ModelChoiceFilter(label='Model',field_name='model_No',to_field_name='model_No',queryset=MODEL_NO_CHOICES)
    sub_category=django_filters.ModelChoiceFilter(label='Sub Category',field_name='sub_category',to_field_name='sub_category',queryset=SUB_CATEGORY_CHOICES)
    sku         =django_filters.CharFilter(label='SKU ID',field_name='sku',lookup_expr='icontains')

    class Meta:
        model = Products
        fields = ['sku','category', 'sub_category','company','model_No','product_name',]


class cancelordersFilter(django_filters.FilterSet):
    cancelinfo = django_filters.CharFilter(lookup_expr='icontains')
    order_id   = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = cancelorders
        fields = ['payment','cancelinfo', 'order_id',]
