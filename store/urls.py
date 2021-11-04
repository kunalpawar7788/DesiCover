from django.urls import path, include
from . import views
from user.views import register
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('ajax/load-model/', views.load_model, name='ajax_load_model'),
    path('ajax/load-company/', views.load_company, name='ajax_load_company'),

    path('ajax/verifypayment/',views.verifypayment,name='verifypayment'),



    path('export_search_csv/',views.export_search_csv,name='Expory Filter Value'),

    path('verifyadminotp/',views.verifyadminotp,name="Verify Admin OTP"),
    path('moneycancelorder/',views.moneycancelorder,name='Assign Money for Cancelorder'),
    path('calculation/',views.calculation,name='Cart Calculation'),
    path('addwallet/',views.addwallet,name="Money Add to Wallet"),
    path('trackpackage/<id>',views.trackpackage,name='Track Package'),
    path('pincode/',views.pincode,name='Pincode'),
    path('destroypincode/<id>',views.destroypincode,name='Destroy Pincode'),

    
    path('adminsize/',views.adminsize,name='Admin Size'),
    path('batch/',views.batch,name='Batch'),
    path('bulkadminsize/',views.bulkadminsize,name='Admin Bulk Size'),

    path('', views.home, name='home'),

    path('adminreview/',views.adminreview,name='Admin Review'),
    path('destoyreview/<id>',views.destoyreview,name='Destroy Review'),
        


    path('adminaddwallet/',views.adminaddwallet,name='Admin Add Wallet'),


    path('homepage/',views.homepage,name='homepage'),
    path('destroyhomeimg/<id>',views.destroyhomeimg,name='destroyhome'),
    path('submitcart/',views.submitcart,name='Submit Cart'),

    path('login/otpsend', views.otpsend,name='smsotpsend'),
    path('login/verifyotp',views.verifyotp,name='verifysms'),
    path('admincancelorder/',views.admincancelorder,name="Admin Cancel Order"),

    path('google/',views.google,name="Google login"),

    path('home/',views.home,name="home"),
    path('about/', views.about, name='store_about'),


    path('paymentmode',views.paymentmode,name="Payment Mode"),


    path('razorpay',views.razorpay,name="Razorpay"),

    path('addreview/<product_id>',views.addreview,name="add review"),
    path('review/<product_id>',views.review,name="add review"),

    path('bulkupdate/', views.bulkupdate, name='Bulk Update Price'),
    path('bulkdes/', views.bulkdes, name='Bulk Update Description'),


    path('contact/',views.contact,name="contact"),
    # path('emp/', views.emp, name='emp'),
    path('userprofile/',views.userprofile,name='userprofile'),
    path('updateimage/',views.updateimage,name='updateimage'),
    path('updateprofile/',views.updateprofile,name='updateprofile'),
    path('customerwallet/',views.customerwallet,name='customerwallet'),
    path('destroycarousel/<id>',views.destroycarousel,name="destroycarousel"),
    path('upload_csv/', views.upload_csv,name='upload_csv'),

    path('deletrecent/<id>',views.deletrecent,name='deletrecent'),
    path('adminfile/',views.adminfile,name='adminfile'),

    path('adminindex/',views.adminindex,name='adminindex'),
    path('fliparmy/',views.fliparmy,name='fliparmy'),
    # path('chart/',views.chart,name='chart'),


    path('addmoney/',views.addmoney,name='addmoney'),
    path('addcarousel/',views.addcarousel,name='addcarousel'),
    path('updatemobile/',views.updatemobile,name='updatemobile'),
    path('mobilename/',views.mobilename,name='mobilename'),
    path('mobiledestroy/<id>',views.mobiledestroy,name='mobiledestroy'),

    path('adminorder/',views.adminorder,name='adminorder'),


    path('flip/',views.flip,name="flip"),
    path('cancelorder/<id>/',views.cancelorder,name='cancelorder'),
    path('postcancel/',views.postcancel,name='postcancel'),
    path('userwallet/',views.userwallet,name='userwallet'),

    path('filter/',views.filter,name="filter"),
    # path('show/', views.show, name="show"),
    path('add_to_cart/', views.add_to_cart, name=" add to cart"),
    path('Cart/', views.Cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    



    
    path('placeorder/',views.placeorder,name="placeorder"),
    path('cover/',views.mobile,name="Mobile"),
    path('checkout/', views.product, name="product"),

    path('customer/', views.customer, name="customer"),
   
    path('ordersummary/', views.ordersummary, name="ordersummary"),
    path('deletecart/<id>',views.rem_from_cart,name="deletecart"),
    path('product/<product_id>',views.product,name="Product"),
    path('edit/<product_id>',views.edit,name="Edit Product"),
    # path('update/<product_id>',views.update,name="Update Product"),

    path('delete/<product_id>',views.destroy,name="Delete Product"),
    path('mugs/', views.mugs, name="mugs"),
    path('tshirt/<category>/<theme>', views.tshirts, name="tshirts"),
    path('mobilecover/<model_No>', views.mobileCovers, name="mcovers"),
    path('popsocket/', views.pshokets, name="pshockets"),
    path('couponcheck/',views.couponcheck,name="couponcheck"),
    path('searchbar/',views.searchbar,name="SearchBAr"),


    path('', include('user.urls'), name="show"),

    path('login/register',views.register,name="register"),
    # path('addcoupon/',views.addcoupon),
    path('coupon/',views.coupon),
    path('editcoupon/<id>', views.editcoupon,name="Edit Coupon"),  
    # path('updatecoupon/<id>', views.updatecoupon,name="Update Coupon"),  
    path('deletecoupon/<id>', views.destroycoupon,name="Delete Coupon"),
    path('showcoupon/',views.showcoupon,name="SHOW Coupon"),
    path('myaccount/',views.account,name="MY Account"),

    path('addrecent/<product_id>',views.addrecent,name="Recent Add"),
    path('showrecent/',views.showrecent,name="Recent Show"),

    # path('sms/',views.sms,name="sms"),

    path('adminheading/',views.adminheading,name="Admin Heading"),



    path('adminhomeimage/',views.adminhomeimage,name="Admin Home Image"),
    path('adminhomeimagedestroy/<id>',views.adminhomeimagedestroy,name="Admin home Image Destroy"), ##



    path('createorder/',views.createorder,name="createorder"), ##

    path('textdestroy/<id>',views.textdestroy,name="Text Destroy"),


    path('adminhomeword/',views.adminhomeword,name="adminhomeword"),

    path('adminlogin/',views.adminlogin,name="adminlogin"),
    path('adminhome/',views.adminhome,name="adminhome"),
    path('account/',views.account,name="cancelorder"),



    # CSV FILE FOR USER
    path('export_users_csv/',views.export_users_csv,name="User All Data"),
    path('export_users_csv_day/',views.export_users_csv_day,name="User one day Data"),
    path('export_users_csv_week/',views.export_users_csv_week,name="User Week Data"),
    path('export_users_csv_month/',views.export_users_csv_month,name="User Month Data"),

    path('export_product_csv/',views.export_product_csv,name="Product All Data"),
    path('export_product_csv_month/',views.export_product_csv_month,name="Product Week Data"),
    path('export_product_csv_week/',views.export_product_csv_week,name="Product Month Data"),
    path('export_product_csv_day/',views.export_product_csv_day,name="Product Day Data"),
  


] + static(settings.STATIC_URL,documnet_root=settings.STATIC_ROOT)