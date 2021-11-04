from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from import_export.admin import ImportExportModelAdmin


@admin.register(Products,Review,Contact,recentarrival)
class ViewAdmin(ImportExportModelAdmin):
	pass


# class ImageAdmin(admin.ModelAdmin):
#     list_display = ('product_id','title','price', 'category', 'sub_category',
#                     'add_date', 'company')
#     # search_fields = ('fname','lname','mobile','email',)
#     # readonly_fields=('date_of_purchase')

#     # filter_horizontal = ()
#     # list_filter = ('date_of_purchase', 'fname', 'lname', 'email', 'mobile', 'city',
#     #                'state', 'pin', 'country',)
#     # fieldsets = ()

# admin.site.register(imagesupload,ImageAdmin)



















# @admin.register(Products,Review,Contact,Coupon)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('product_id','title','price', 'category', 'sub_category',
#                     'add_date', 'company')
#     # search_fields = ('fname','lname','mobile','email',)
#     # readonly_fields=('date_of_purchase')

#     # filter_horizontal = ()
#     # list_filter = ('date_of_purchase', 'fname', 'lname', 'email', 'mobile', 'city',
#     #                'state', 'pin', 'country',)
#     # fieldsets = ()

# admin.site.register(Products,ProductAdmin)

# admin.site.register(Products,ViewAdmin)


# class OrdersAdmin(admin.ModelAdmin):
#     list_display = ('order_id','cust_username','total_amount', 'address1', 'mobile_no')
#     search_fields = ('order_id','cust_username','address1','mobile_no',)
#     readonly_fields=('order_id',)

#     filter_horizontal = ()
#     list_filter = ('cust_username', 'total_amount', 'address1', 'address2', 'address3',)
#     fieldsets = ()
# admin.site.register(Orders,OrdersAdmin)


# class CartsAdmin(admin.ModelAdmin):
#     list_display = ('product_id','price','cust_username', 'quantity', 'title')
#     search_fields = ('product_id','cust_username','title',)
#     readonly_fields=('product_id',)

#     filter_horizontal = ()
#     list_filter = ('cust_username', 'title',)
#     fieldsets = ()
# admin.site.register(Carts,CartsAdmin)



# class CouponAdmin(admin.ModelAdmin):
#     list_display = ('cname','ccode', 'cdescription', 'discount')
#     search_fields = ('cname','ccode','cdescription', 'discount')
#     # readonly_fields=('cid',)

#     filter_horizontal = ()
#     list_filter = ('cname', 'ccode',)
#     fieldsets = ()
# admin.site.register(Coupon,CouponAdmin)


# class placeordersAdmin(admin.ModelAdmin):
#     list_display = ('placeid','order_id','order_date', 'cust_username', 'address1', 'address2','pincode',
#                     'city','state','phone','email','totalamount','first_name','last_name','item',)

#     search_fields = ('placeid','order_id','order_date','cust_username', 'address1', 'address2','pincode',
#                     'city','state','phone','email','totalamount','first_name','last_name','item',)

#     readonly_fields=('placeid','order_id', 'order_date',)
#     filter_horizontal = ()
#     list_filter = ('order_id', 'order_date',)
#     fieldsets = ()
# admin.site.register(placeorders,placeordersAdmin)


# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ('cust_username','product_id','review', 'rating',)

#     search_fields = ('cust_username','product_id','review','rating')
#     readonly_fields=('product_id',)

#     filter_horizontal = ()
#     list_filter = ('product_id', 'cust_username', 'review','rating',)
#     fieldsets = ()
# admin.site.register(Review,ReviewAdmin)



# class ContactAdmin(admin.ModelAdmin):
#     list_display = ('name','phone','subject', 'message', 'email',)

#     search_fields = ('name','phone','subject','message','email')
#     # readonly_fields=('product_id',)

#     filter_horizontal = ()
#     list_filter = ('name','phone','subject','message','email',)
#     fieldsets = ()
# admin.site.register(Contact,ContactAdmin)


# data.bcatalyst@gmail.com
# branding@123
