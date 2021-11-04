from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from store.models import *
from user.models import *
from django.db.models import Sum 
from store.forms import *
from django.db.models import Q
from django.contrib.auth.models import User, auth 
from django.views.decorators.csrf import csrf_exempt 
# from paytm import Checksum
from django.core.mail import send_mail
from django.conf import settings
from django.conf.urls.static import static
import datetime,requests
from random import random
from django.utils.crypto import get_random_string
import requests
import json
import http.client
import mimetypes
from user.views import register
from django.contrib import messages
import logging
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import openpyxl
import os
import tempfile
import xlrd
from math import ceil
import csv
from datetime import date, timedelta
from django.db.models import *
import re
import itertools
import razorpay
import ast
from django.core import serializers
from urllib.parse import urlparse
from urllib.parse import parse_qs
from django.http import QueryDict
from .filters import *

razorpay_client = razorpay.Client(auth=("rzp_test_oQByQXLDQXLDDf", "aImCmxD2ZOTuNS6iqOldZE3n"))  #test mode
# razorpay_client = razorpay.Client(auth=("rzp_live_SyC9jYVOwKg5Jk", "tGI3wDNg9LClSDaE71Ku16VW"))

def calculation(request):
	if request.method=='POST':

		query=QueryDict(request.POST['form'].encode('ASCII'))
		x2=dict(query.lists())
		ids=x2.get('id')
		qty=x2.get('quantity')
		remove=qty.pop(len(qty)-1)
		m=remove.split('"')
		add=m.pop(0)
		qty.append(add)
		price=x2.get('price')
		sum_list = []
		for (item1, item2) in zip(qty, price):
			sum_list.append(int(item1)*int(item2))
		total=sum(sum_list)
		return HttpResponse(total)
		

@login_required(login_url="/user/login")
def userprofile(request):
	try:
		cust_username=auth.get_user(request)
		cart=Carts.objects.filter(cust_username=cust_username,added=True)
		user=Userprofile.objects.filter(user_id=cust_username.id)
		return render(request,'userprofile.html',{'cart':cart,'user':user})
	except Exception as e:
		print(e)
	return render(request,'Notfound.html')


@login_required(login_url="/user/login")
def updateimage(request):
	if request.method=='POST':
		try:
			id=request.POST['id']
			image=request.FILES.get('image',None)
			form=User.objects.get(id=id)
			f=Userprofile.objects.get(user_id=id)
			f.image=image
			f.save()
			return HttpResponseRedirect('/userprofile')
		except Exception as e:
			print(e)
	return redirect('userprofile')


@login_required(login_url="/user/login")
def updateprofile(request):
	if request.method=='POST':
		try:
			id=request.POST['id']
			fname=request.POST.get('fname',None)
			lname=request.POST.get('lname',None)
			citys=request.POST.get('city',None)
			Userprofile.objects.filter(user_id=id).update(city=citys)
			User.objects.filter(id=id).update(first_name=fname,last_name=lname)
			return HttpResponseRedirect('/userprofile')
		except Exception as e:
			print(e)
	return redirect('userprofile')


@login_required(login_url="/user/login")
def paymentmode(request):
	try:
		order_id=request.session['order_id']
		status=request.session['status']
		totalamount=request.session['amount']
		del request.session['amount']
		del request.session['order_id']
		del request.session['status']
		context={'order_id':order_id,'status':status,'totalamount':totalamount}
	except Exception as e:
		print(e)
		order_id='Wrong Id'
		status='Failure'
		totalamount=0
		context={'order_id':order_id,'status':status,'totalamount':totalamount}
	return render(request,'paymentstatus.html',context)	


@login_required(login_url="/user/login")
def razorpay(request):
	if 'POST' == request.method:
		try:
			cust_username=auth.get_user(request)
			amt        = request.POST['amount']
			payment_id = request.POST['razorpay_payment_id']
			order_id   = request.POST['shopping_order_id']
			z=razorpay_client.payment.capture(payment_id, amt)
			m=razorpay_client.payment.fetch(payment_id)
			totalamount=float(int(amt)/100)
			request.session['amount']=totalamount
			form=bankdetails(paymentid=m['id'],currency=m['currency'],error_code=m['error_code'],card_id=m['card_id'],paymentmode=m['method'],totalamount=totalamount,status=m['status'])
			form.save()
			bankinfo=bankdetails.objects.get(id=form.id)
			request.session['status']=m['status']

			products=Carts.objects.filter(cust_username_id=cust_username,added=True)

			# payload = {
			# 		"vendor_code":"V001",
			# 		"company_name":"DESICOVERS",
			# 		"user_email":"desicovers.1@gmail.com",
			# 		"pickup_location": "DESICOVERS",
			# 		"order_type": "Prepaid",
			# 		"orderno":request.session['order_id'],
			# 		"quantity":request.session['tot_qty'],
			# 		"customer_name":request.session['first_name'],
			# 		"customer_email":request.session['email'],
			# 		"customer_mobile":request.session['phone'],
			# 		"customer_phone": "",
			# 		"customer_city":request.session['city'],
			# 		"customer_state":request.session['state'],
			# 		"custom_address":request.session['address1'],
			# 		"customer_pincode":request.session['pincode'],
			# 		"delivery_mode": "surface",
			# 		"product_group": "",
			# 		"codamount":totalamount,
			# 		"packamount": "0",
			# 		"octroi_mrp": "0",
			# 		"product_items":request.session['cart_value'],
			# 		}

			# print(payload)
			
			# conn = http.client.HTTPSConnection("admin.milesawayy.com")
			# headers={
			# 		'Authorization': 'f82de5343eac3925cbb0c14378ca508f0fa18bafb236efed983b871c59cae033065eea91091f843552d1c7602e99fbc27fd3077c2bafc2f5f31db79831faef4e',
			# 		'Content-Type': 'application/json'
			# }
			# conn.request("POST", "/api/v1/order_create",json.dumps(payload), headers)
			# res  = conn.getresponse()
			# data = res.read()
			# print(data.decode("utf-8"))
			# dic = json.loads(data)


			for p in products:
				cart=Carts.objects.get(id=p.id)
				form1=Orders(cust_username=cust_username,order=request.session['order_id'],cart_id=cart)
				form1.save()
				orderinst=form1.id
				fororder=Orders.objects.get(id=orderinst)
				
				form=placeorders(first_name=request.session['first_name'],paymentmode='Prepaid',products=cart,last_name=request.session['last_name'],order_id=request.session['order_id'],
					address1=request.session['address1'],address2=request.session['address2'],city=request.session['city'],state=request.session['state'],pincode=request.session['pincode'],email=request.session['email'],
					totalamount=totalamount,cust_username=cust_username,phone=request.session['phone'],bank=bankinfo)
				form.save()
				instance=form.id

				forplace=placeorders.objects.get(id=instance)

				Carts.objects.filter(id=cart.id).update(added=False)

				# form=orderawb(awb=dic['data']['awb_no'],awb_order_id =dic['data']['orderId'],placeorder_id=forplace,order_id=fororder)
				# form.save()


				if request.session['coupon'] !='':
					coupon=Coupon.objects.get(id=cid)
					form=placeorders.objects.filter(id=instance).update(coupon=coupon)
					print(form)
					del request.session['coupon']
				
			del request.session['first_name']
			del request.session['last_name']
			del request.session['address1']
			del request.session['address2']
			del request.session['city']
			del request.session['state']
			del request.session['pincode']
			del request.session['phone']
			del request.session['email']
			del request.session['cart_value']
			# del request.session['order_id']
		except Exception as e:
			print(e)

	return HttpResponseRedirect('paymentmode')

import base64		
@login_required(login_url="/user/login")
def trackpackage(request,id):
	try:
		encoded = base64.b64decode(bytes(str(id), encoding='ascii'))
		print(encoded)

		id=encoded.decode("utf-8") 
		array=list(orderawb.objects.filter(placeorder_id=id).values('awb'))
		payload={"awb_no":list(array)}
		conn = http.client.HTTPSConnection("admin.milesawayy.com")
		headers={
			'Authorization': 'f82de5343eac3925cbb0c14378ca508f0fa18bafb236efed983b871c59cae033065eea91091f843552d1c7602e99fbc27fd3077c2bafc2f5f31db79831faef4e',
			'Content-Type': 'application/json'
		}
		conn.request("POST", "/api/v1/order_track_status",json.dumps(payload),headers)
		res = conn.getresponse()
		data = res.read()
		dic = json.loads(data)
		z=dic['data'][0]['track_status']
		track={}
		for i in range(0,len(z)):
			track[z[i]['status']] = z[i]['status'],z[i]['remark'],z[i]['track_date']
		status=[]
		for i in range(0,len(track)):
			status.append(list(track.keys())[i]) 
		stat = list(dict.fromkeys(status))
		print(stat)
	except Exception as e:
		print("Exception",e)
		return render(request,'Notfound.html')
	return render(request,'trackship.html',{'track':track,'status':stat})



@login_required(login_url="/user/login")
def postcancel(request):
	if 'POST' == request.method:
		id        =request.POST['id']
		cancelinfo=request.POST['cars']
		place12=placeorders.objects.filter(id=id)
		place1 =placeorders.objects.get(id=id)
		mode  =place1.paymentmode
		bankid=place1.order_id
		Bankid=place1.bank_id

		array=list(orderawb.objects.filter(placeorder_id=id).values('awb'))
		print(array)

		order=orderawb.objects.get(placeorder_id=id)
		print(order.order_id)
		orderlist=list(Orders.objects.filter(order=order.order_id).values_list('order',flat=True))
		print(orderlist)

		cancellen=len(array)
		print(cancellen)
		
		try:
			if mode=='COD':
				form=cancelorders(order_id=bankid,cancelinfo=cancelinfo)
				form.save()
				
				cancel=cancelorders.objects.get(id=form.id)
				for i in orderlist:
					placeorders.objects.filter(order_id=i).update(cancelorders=cancel)

			if mode=='Prepaid':
				detailbank=bankdetails.objects.get(id=Bankid)
				form =cancelorders(payment=detailbank,cancelinfo=cancelinfo)
				form.save()
				
				cancel=cancelorders.objects.get(id=form.id)
				for i in orderlist:
					placeorders.objects.filter(order_id=i).update(cancelorders=cancel)

			payload={"awb_no":list(array)}
			conn = http.client.HTTPSConnection("admin.milesawayy.com")
			headers={
				'Authorization': 'f82de5343eac3925cbb0c14378ca508f0fa18bafb236efed983b871c59cae033065eea91091f843552d1c7602e99fbc27fd3077c2bafc2f5f31db79831faef4e',
				'Content-Type': 'application/json'
			}
			conn.request("POST", "/api/v1/order_cancel",json.dumps(payload),headers)
			res = conn.getresponse()
			data= res.read()
			dic = json.loads(data)
			print(dic)

		except Exception as e:
			print(e)
			return render(request,'Notfound.html')
	return render(request,"successrefund.html",{'place':place12})


from django.db.models.functions import Concat



@login_required(login_url="/user/login")
def checkout(request):
	cust_username=auth.get_user(request)
	print(cust_username)
	products=Carts.objects.filter(cust_username_id=cust_username,added=True)

	if request.session['totalamount']:
		tol_price=request.session['totalamount']

	else:
		tol_price=request.session['totalamount']
		tol_price=Carts.objects.filter(cust_username=cust_username,added=True).aggregate(total=Sum(F('price')*F('quantitys')))['total']
	

	if 'GET' == request.method:
		pin = Pincode.objects.all()
		print(pin)
		pincodes= []
		for i in pin:
			pincodes.append(i.pincode)
		print(pincodes)
		return render(request,'checkout.html',{'tol_price':tol_price,'products':products, 'pincodes':pincodes})

	if 'POST' == request.method:
		print("1")
		order_date= datetime.datetime.now()
		cid       = request.session['coupon']

		# print("2")
		first_name=request.POST['first_name']
		last_name =request.POST['last_name']
		address1  =request.POST['address1']
		address2  =request.POST['address2']
		city      =request.POST['city']
		state     =request.POST['state']
		pincode   =request.POST['pincode']
		phone     =request.POST['phone']
		email     =request.POST['email']
		mode      =request.POST['internet']
		
		request.session['first_name']=first_name
		request.session['last_name'] =last_name
		request.session['address1']  =address1
		request.session['address2']  =address2
		request.session['city']      =city
		request.session['state']     =state
		request.session['pincode']   =pincode
		request.session['phone']     =phone
		request.session['email']     =email
		
		address3=address1+address2
		cust_name=first_name+last_name
		# orderid=Orders.objects.generator()
		orderid="12121212"
		request.session['order_id']=orderid
		cart_value=list(Carts.objects.filter(cust_username=cust_username,added=True).values(product_desc=F('title'),quantity=F('quantitys'),product_mrp=F('price')))
		print(cart_value)

		request.session['cart_value']=cart_value

		tot_qty=Carts.objects.filter(cust_username=cust_username,added=True).aggregate(total=Sum(F('quantitys')))['total']
		request.session['tot_qty']     =tot_qty

		request.session['cart_value']=cart_value
		print("3")
		print("---------------------------------------------COD")
		
		if mode=='COD':
			
			for p in products:
				cart=Carts.objects.get(id=p.id)
				
				form1=Orders(cust_username=cust_username,order=orderid,cart_id=cart)
				form1.save()

				orderinst=form1.id
				fororder =Orders.objects.get(id=orderinst)

				form=placeorders(first_name=first_name,paymentmode='COD',products=cart,last_name=last_name,order_id=orderid,address1=address1,
					address2=address2,city=city,state=state,pincode=pincode,email=email,totalamount=tol_price,cust_username=cust_username,phone=phone)
				form.save()
				instance=form.id

				forplace=placeorders.objects.get(id=instance)

				Carts.objects.filter(id=cart.id).update(added=False)
				
				# form=orderawb(awb=awbNumber,awb_order_id =orderNumber,placeorder_id=forplace,order_id=fororder)
				# form.save()

				if cid != '':
					cop=Coupon.objects.get(id=cid)
					form=placeorders.objects.filter(id=instance).update(coupon=cop)
					# print(form)
					del request.session['coupon']
				return render(request, 'codorderplaced.html' )
				# messages.error(request,"Order is Successfully Placed")


		if mode=='Prepaid':
			amount=tol_price*100
			context={
				'order_id':orderid,'tol_price':amount,'first_name':first_name,
				'email':email,'phone':phone
			}
			return render(request,'razor.html',context)

		return HttpResponseRedirect(reverse("checkout"))
	

@login_required(login_url="/user/login")
def submitcart(request):
	if 'POST'==request.method:
		z=dict(request.POST.lists())
		prodid=z.get('id')
		price =z.get('price')
		qty   =z.get('quantity')
		try:
			l=len(prodid)
			for i in range(0,l):
				Carts.objects.filter(id=prodid[i]).update(price=price[i],quantitys=qty[i])
		except Exception as e:
			print(e)
			messages.info(request, ''+e)

		return HttpResponseRedirect("/checkout")


@login_required(login_url="/user/login")
def filter(request):
	# if 'GET'==request.method:
	first_name='Shavej Shaikh'
	email='shavejshaikh@gmail.com'
	phone=9967984238
	context={
	'order_id':154,'tol_price':120,'first_name':first_name,
	'email':email,'phone':phone}
	return render(request,'payment.html',context)

def verifypayment(request):
	if 'POST'==request.method:
		print(request.POST)
		print("Ek no")
		card_no=request.POST['card_no']
		card_name=request.POST['card_name']
		expiry_month=request.POST['expiry_month']
		expiry_year=request.POST['expiry_year']
		card_cvv=request.POST['card_cvv']
		return HttpResponse("Ekno")

@login_required(login_url="/user/login")
def addmoney(request):
	cust_id=auth.get_user(request).id
	try:
		if 'POST' == request.method:
			money=request.POST['amount']
			phone=request.POST['phone']
			print(money)
			user=User.objects.get(id=cust_id)

			order=Transaction.objects.last()
			usermobile=Userprofile.objects.get(user=cust_id)
			amount=int(money)*100
			context={
				'order_id':int(str(order))+1,'tol_price':amount,'first_name':user.first_name,
				'email':user.email,'phone':phone
			}	
	except Exception as e:
		print(e)
		return render(request,'Notfound.html')
	return render(request,'paywallet.html',context)

@login_required(login_url="/user/login")
def addwallet(request):
	if 'POST' == request.method:
		try:
			cust_id    = auth.get_user(request).id
			amt        = request.POST['amount']
			payment_id = request.POST['razorpay_payment_id']
			order_id   = request.POST['shopping_order_id']
			z=razorpay_client.payment.capture(payment_id, amt)
			m=razorpay_client.payment.fetch(payment_id)
			totalamount=float(int(amt)/100)
			wallets=Wallet.objects.get(user_id=cust_id)
			info=str(m)
			wallets.carddeposit(value=totalamount,information="Added by Me",card_info=info,typeofmoney='credit')
			context={'order_id':order_id,'status':"captured",'totalamount':totalamount}
		except Exception as e:
			print(e)
			return render(request,'Notfound.html')
	return render(request,'paymentstatus.html',context)	


@login_required(login_url="/user/login")
def userwallet(request):
	try:
		cust_username=auth.get_user(request).id
		findid=Wallet.objects.get(user_id=cust_username).id
		wallet=Wallet.objects.filter(user_id=cust_username)
		history=Transaction.objects.filter(wallet=findid)
	except Exception as e:
		print(e)
		return render(request,'Notfound.html')
	return render(request,'wallet.html',{'wallet':wallet,'history':history})


def flip(request):
	products=desiarmy.objects.all()
	if request.user.is_authenticated == True:
		cust_username=auth.get_user(request)
		cart =Carts.objects.filter(cust_username=cust_username,added=True)
		return render(request,'Flip.html',{'products':products,'cart':cart})
	return render(request,'Flip.html',{'products':products})




# ------------------------------------------------------Admin------------------------------------------------#




@login_required(login_url="/adminlogin")
def edit(request,product_id): 
	if 'GET' == request.method: 
		product = Products.objects.get(id=product_id)  
		return render(request,'edit.html', {'product':product})
	if 'POST' == request.method:
		product = Products.objects.get(id=product_id) 
		print(product)
		form =ProductForm(request.POST,request.FILES, instance = product)  
		if form.is_valid():
			try:  
				form.save()
			except Exception as e:
				print(e)
		return render(request,'edit.html', {'product':product})



@login_required(login_url="/adminlogin")
def coupon(request):
	if 'GET' == request.method:
		return render(request,'addcoupon.html')
	if 'POST' == request.method:
		form=CouponForm(request.POST)
		if form.is_valid():
			try:
				form.save()
				product=Coupon.objects.all()
				return render(request, "coupon.html", {'product': product})
			except Exception as e:
				print(e)
				pass
	return render(request,'addcoupon.html')


@login_required(login_url="/adminlogin")
def showcoupon(request):
	try:
		product=Coupon.objects.all()
	except Exception as e:
		print(e)
	return render(request,"coupon.html",{'product':product})


@login_required(login_url="/adminlogin")
def editcoupon(request,id):
	if 'GET' == request.method:
		product = Coupon.objects.get(id=id)
		return render(request,'editcoupon.html', {'product':product})
	if 'POST' == request.method:
		prod = Coupon.objects.get(id=id) 
		form =CouponForm(request.POST, instance = prod) 
		print(form.errors)
		if form.is_valid(): 
			form.save()

		product=Coupon.objects.all()
		return render(request, "coupon.html", {'product': product})


@login_required(login_url="/adminlogin")
def destroycoupon(request,id):
	try:
		Coupon.objects.get(id=id).delete()  
	except Exception as e:
		print(e)
	return HttpResponseRedirect('/showcoupon')

@login_required(login_url="/adminlogin")
def adminreview(request):
	photos_list = Review.objects.all()
	return render(request,'adminreview.html',{'photos':photos_list})


@login_required(login_url="/adminlogin")
def destoyreview(request,id):
	try:
		product = Review.objects.get(id=id)
		product.delete()  
	except Exception as e:
		print(e)
	return HttpResponseRedirect('/adminreview')


@login_required(login_url="/adminlogin")
def showrecent(request):
	order=recentarrival.objects.all()
	return render(request,'showrecent.html',{'orders':order})


@login_required(login_url="/adminlogin")
def addrecent(request,product_id):
	try:
		product=Products.objects.get(id=product_id)
		form=recentarrival(products=product)
		form.save()
		Products.objects.filter(id=product_id).update(add_recent=True)
	except Exception as e:
		print(e)   
	return redirect('adminindex')

@login_required(login_url="/adminlogin")
def deletrecent(request,id):
	try:
		instance=recentarrival.objects.get(id=id)
		Products.objects.filter(id=instance.products.id).update(add_recent=False)
		recentarrival.objects.get(id=id).delete()
	except Exception as e:
		print(e)   
	return HttpResponseRedirect('/showrecent')


def adminlogin(request):
	if request.method == "POST":
		username=request.POST['username']
		passw=request.POST['passw']
		user =auth.authenticate(username=username,password=passw,is_superuser=1)
		staff=auth.authenticate(username=username,password=passw,is_staff=1)
		print(staff)
		if user is not None and user.is_superuser==1:
			auth.login(request,user)
			request.session['username'] = username
			phone=9967984238

			url = "https://2factor.in/API/R1/?module=SMS_OTP&apikey=4e32200c-3173-11ea-9fa5-0200cd936042&to=%s&otpvalue=AUTOGEN3&templatename=StreetMart" % (phone)
		
			response = requests.request("POST", url)

			if "Success" in response.text:
				messages.success(request,"OTP is Send Successfully to your Mobile")
				return render(request,'Verifyadmin.html')

		if staff is not None and user.is_staff==1:
			auth.login(request,user)
			request.session['username'] = username
			print('staff')
			return redirect('/adminhome')
	return render(request,'adminlogin.html')

@csrf_exempt
def verifyadminotp(request):
	if request.method=='POST':
		phone=9967984238
		otp_value=request.POST['otp']
		print(otp_value)
		print(phone)
		url = "https://2factor.in/API/V1/4e32200c-3173-11ea-9fa5-0200cd936042/SMS/VERIFY3/%s/%s" % (phone, otp_value)
		response = requests.request("POST", url)
		print(response.text)
		if "Success" in response.text:
			return redirect('/adminhome')
		else:
			messages.success(request,"Incorrect OTP")
	return render(request,'Verifyadmin.html')


@login_required(login_url="/adminlogin")
def adminhome(request):
	product=Products.objects.all().count()

	current_date= date.today().isoformat()
	days_before = (date.today()-timedelta(days=30)).isoformat()
	days_after  = (date.today()+timedelta(days=30)).isoformat()
	week=(date.today()-timedelta(days=7)).isoformat()
	
	
	monthly = placeorders.objects.filter(order_date__range=(days_before,current_date),cancelorders_id__isnull=True).aggregate(total=Sum(F('totalamount')))
	annual = placeorders.objects.filter(cancelorders_id__isnull=True).aggregate(total=Sum(F('totalamount')))
	cancel = placeorders.objects.filter(cancelorders_id__isnull=False).count()
	result = (placeorders.objects.filter(cancelorders_id__isnull=True).values_list('order_date__year', 'order_date__month').annotate(Sum('totalamount')).order_by('order_date__year', 'order_date__month'))
	result1 = placeorders.objects.all().values_list('products')
	c=[]
	for i in result1:
		cart=Carts.objects.get(id=i[0])
		c.append(cart.product_id)


	m=t=m1=p=0;

	for j in c:
		if j.category=='MOBILE':
			m=m+1
		if j.category=='TSHIRT':
			t=t+1

		if j.category=='mug':
			m1=m1+1

		if j.category=='popsocket':
			p=p+1

	#Total no of placeorder
	place= placeorders.objects.all().count()
	paytm=placeorders.objects.filter(paymentmode='paytm').count()
	cod  =placeorders.objects.filter(paymentmode='cod').count()
	contact=Contact.objects.all().count()
	coupon=Coupon.objects.all().count()
	cust=Userprofile.objects.all().count()
	review=Review.objects.all().count()

	try:
		mode=float((paytm)*100)/(paytm+cod)
	except Exception as e:
		mode=0
	mode1=round(mode,2)

	context={'product':product,'monthly':monthly,'annual':annual,'cancel':cancel,
			'result':result,'mobile':m,'tshirt':t,'mug':m1,'popsocket':p,'cust':cust,
			'place':place,'paytm':paytm,'cod':cod,'contact':contact,'coupon':coupon,
			'mode':mode1}

	return render(request,'adminhome.html',context)



@login_required(login_url="/adminlogin")
def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="usersall.csv"'
    writer = csv.writer(response)

    writer.writerow(['Username', 'First name', 'Last name', 'Email Address'])

    users = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    for user in users:
        writer.writerow(user)

    return response

@login_required(login_url="/adminlogin")
def export_users_csv_day(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="usersday.csv"'

	writer = csv.writer(response)
	writer.writerow(['Username', 'First name', 'Last name', 'Email Address'])

	current_date= date.today().isoformat()
	days_before = (date.today()-timedelta(days=30)).isoformat()
	days_after  = (date.today()+timedelta(days=30)).isoformat()
	week=(date.today()-timedelta(days=7)).isoformat()
	
	users = User.objects.filter(date_joined=current_date).values_list('username', 'first_name', 'last_name', 'email')
	for user in users:
		writer.writerow(user)

	return response

@login_required(login_url="/adminlogin")
def export_users_csv_week(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="userweek.csv"'

	writer = csv.writer(response)
	writer.writerow(['Username', 'First name', 'Last name', 'Email Address'])

	current_date= date.today().isoformat()
	days_before = (date.today()-timedelta(days=30)).isoformat()
	days_after  = (date.today()+timedelta(days=30)).isoformat()
	week=(date.today()-timedelta(days=7)).isoformat()
	
	users = User.objects.filter(date_joined__range=(week,current_date)).values_list('username', 'first_name', 'last_name', 'email')
	for user in users:
		writer.writerow(user)

	return response


@login_required(login_url="/adminlogin")
def export_users_csv_month(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="usermonth.csv"'

	writer = csv.writer(response)
	writer.writerow(['Username', 'First name', 'Last name', 'Email Address'])

	current_date= date.today().isoformat()
	days_before = (date.today()-timedelta(days=30)).isoformat()
	days_after  = (date.today()+timedelta(days=30)).isoformat()
	week=(date.today()-timedelta(days=7)).isoformat()
	
	users = User.objects.filter(date_joined__range=(days_before,current_date)).values_list('username', 'first_name', 'last_name', 'email')
	for user in users:
		writer.writerow(user)

	return response


@login_required(login_url="/adminlogin")
def export_product_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="productall.csv"'

    writer = csv.writer(response)
    writer.writerow(['Sku Id', 'Category','Model No', 'Images1', 'Images2','Images3','Title','Description','Price',
    	'Sub Category','Weight','Size','Added Date','Company'])

    users = Products.objects.all().values_list('sku', 'category','model_No', 'images1', 'images2','images3','title',
    	'description','price',
    	'sub_category','weight','size','add_date','company')
    for user in users:
        writer.writerow(user)

    return response



@login_required(login_url="/adminlogin")
def export_product_csv_week(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="vendorproduct1week.csv"'
	writer = csv.writer(response)
	writer.writerow(['Sku Id', 'Category','Model No', 'Images1', 'Images2','Images3','Title','Description','Price',
    	'Sub Category','Weight','Size','Added Date','Company'])

	current_date= date.today().isoformat()
	days_before = (date.today()-timedelta(days=30)).isoformat()
	days_after  = (date.today()+timedelta(days=30)).isoformat()
	week=(date.today()-timedelta(days=7)).isoformat()
	
	users = Products.objects.filter(add_date__range=(week,current_date)).values_list('sku', 'category','model_No',
	 'images1', 'images2','images3','title','description','price','sub_category','weight','size','add_date','company')

	print(users)
	for user in users:
		writer.writerow(user)
	return response


@login_required(login_url="/adminlogin")
def export_product_csv_month(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="vendorproductmonth.csv"'
	writer = csv.writer(response)
	writer.writerow(['Sku Id', 'Category','Model No', 'Images1', 'Images2','Images3','Title','Description','Price',
    	'Sub Category','Weight','Size','Added Date','Company'])

	current_date= date.today().isoformat()
	days_before = (date.today()-timedelta(days=30)).isoformat()
	days_after  = (date.today()+timedelta(days=30)).isoformat()
	week=(date.today()-timedelta(days=7)).isoformat()
	
	users = Products.objects.filter(add_date__range=(week,current_date)).values_list('sku', 'category','model_No',
	 'images1', 'images2','images3','title','description','price','sub_category','weight','size','add_date','company')
	print(users)
	for user in users:
		writer.writerow(user)
	return response


@login_required(login_url="/adminlogin")
def export_product_csv_day(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="vendorproductmonth.csv"'
	writer = csv.writer(response)
	writer.writerow(['Sku Id', 'Category','Model No', 'Images1', 'Images2','Images3','Title','Description','Price',
    	'Sub Category','Weight','Size','Added Date','Company'])

	current_date= date.today().isoformat()
	days_before = (date.today()-timedelta(days=30)).isoformat()
	days_after  = (date.today()+timedelta(days=30)).isoformat()
	week=(date.today()-timedelta(days=7)).isoformat()

	users = Products.objects.filter(add_date=current_date).values_list('sku', 'category','model_No','images1',
	 'images2','images3','title','description','price','sub_category','weight','size','add_date','company')
	print(users)
	for user in users:
		writer.writerow(user)
	return response



@login_required(login_url="/adminlogin")
def moneycancelorder(request):
	wallet=placeorders.objects.filter(cancelorders_id__isnull=False,cancelorders_id__initiatedpay=False)

	if 'GET' == request.method:
		return render(request,'adcancelorder.html',{'wallet':wallet})

	if 'POST' == request.method:
		money   =request.POST['refundmoney']
		order_id=request.POST['order_id']
		Id      =request.POST['Id']

		cust_username=auth.get_user(request).id
		user=User.objects.get(id=cust_username)
		placeinfo=placeorders.objects.get(id=Id,order_id=order_id)
		cancel=placeinfo.cancelorders_id
		infocancel=cancelorders.objects.get(id=cancel)
		info=infocancel.cancelinfo

		moneys=int(money)
		try:
			wallets=Wallet.objects.get(user_id=user)
			wallets.deposit(value=moneys,information=info,typeofmoney='credit')
			cancelorders.objects.filter(id=cancel).update(initiatedpay=True,order_id=order_id)

		except Exception as e:
			print(e)
		return render(request,'adcancelorder.html',{'wallet':wallet})

@login_required(login_url="/adminlogin")
def admincancelorder(request):
	cancel=cancelorders.objects.all()
	return render(request,'admincancelorder.html',{'cancel':cancel})


@login_required(login_url="/adminlogin")
def customerwallet(request):
	if request.user.is_superuser:
		wallet=Wallet.objects.all()
		return render(request,'seewallet.html',{'wallet':wallet})
	messages.error(request,"Permission is Not allowed")
	return redirect('adminhome')



@login_required(login_url="/adminlogin")
def adminaddwallet(request):
	if 'POST' == request.method:
		money =request.POST['addmoney']
		uid   =request.POST['Id']
		info  ="Admin Added"
		try:
			wallets=Wallet.objects.get(user_id=uid)
			wallets.deposit(value=int(money),information=info,typeofmoney='credit')
		except Exception as e:
			print(e)
		return HttpResponseRedirect('/customerwallet')
		
@login_required(login_url="/adminlogin")
def adminsize(request):
	if 'GET' == request.method:
		size = Products.objects.filter(category='TSHIRT')
		return render(request,'admintshirtsize.html',{'size':size})

	if 'POST' == request.method:
		ID=request.POST['Id']
		small=request.POST.get('small',None)
		medium=request.POST.get('medium',None)
		large=request.POST.get('large',None)
		xl=request.POST.get('XL',None)
		xxl=request.POST.get('XXL',None)

		prod=Products.objects.get(id=ID)
		if prod.tshirt != None:
			fetchid=str(prod.tshirt)
			forms=Tshirtsize.objects.filter(id=fetchid).update(small=small,Medium=medium,large=large,xl=xl,xxl=xxl)
		else:
			form=Tshirtsize(small=small,Medium=medium,large=large,xl=xl,xxl=xxl)
			form.save()
			ins=Tshirtsize.objects.get(id=form.id)
			Products.objects.filter(id=ID).update(tshirt=ins)
		size = Products.objects.filter(category='tshirt')

		return render(request,'admintshirtsize.html',{'size':size})



@login_required(login_url="/adminlogin")
def bulkadminsize(request):
	if 'GET' == request.method:
		return render(request,'bulktshirtsize.html')

	if 'POST' == request.method:
		small =request.POST.get('small',None)
		medium=request.POST.get('medium',None)
		large =request.POST.get('large',None)
		xl    =request.POST.get('XL',None)
		xxl   =request.POST.get('XXL',None)
		form=Products.objects.filter(category='tshirt')
		for i in form:
			if i.tshirt != None:
				print(i.tshirt)
				fetchid=str(i.tshirt)
				forms=Tshirtsize.objects.filter(id=fetchid).update(small=small,Medium=medium,large=large,xl=xl,xxl=xxl)
			
			else:
				form=Tshirtsize(small=small,Medium=medium,large=large,xl=xl,xxl=xxl)
				form.save()
				ins=Tshirtsize.objects.get(id=form.id)
				Products.objects.filter(id=i.id).update(tshirt=ins)
		return render(request,'bulktshirtsize.html')


@login_required(login_url="/adminlogin")
def homepage(request):
	if 'GET' == request.method:
		photos_list = homepageimg.objects.all()
		return render(request,'homepage.html',{'photos':photos_list})

	if 'POST' == request.method:
		form = HomeForm(request.POST,request.FILES)
		photos_list = homepageimg.objects.all()
		if form.is_valid():
			form.save()
		return render(request,'homepage.html',{'photos':photos_list})

@login_required(login_url="/adminlogin")
def destroyhomeimg(request,id):
	try:
		product = homepageimg.objects.get(id=id)  
		product.delete()
	except Exception as e:
		print(e)
	return redirect('homepage')

@login_required(login_url="/adminlogin")
def pincode(request):
	if "GET" == request.method:
		pincode=Pincode.objects.all()
		return render(request,"pincode.html",{'pincode':pincode})
	try:
		csv_file = request.FILES["csv_file"]
		if not csv_file.name.endswith('.csv'):
			messages.error(request,'File is not CSV type')
			return HttpResponseRedirect(reverse("pincode"))

		if csv_file.multiple_chunks():
			messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
			return HttpResponseRedirect(reverse("pincode"))

		file_data = csv_file.read().decode("utf-8")		
		lines = file_data.split("\n")
		data_dict  = []# Track how many line is enter
		cnt=0
		k=0
		for line in lines:						
			fields = line.split(",")
			param_dict = {}# Store the data
		
			if(len(fields)==1):
				param_dict["pincode"]= fields[0]
				k=k+1
				if fields[0] != '':
					if Pincode.objects.filter(pincode=fields[0]).exists()==False:
						form = PincodeForm(param_dict)
						if form.is_valid():
							form.save()
							cnt=cnt+1
					else:
						data_dict.append(k)
	except Exception as e:
		logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
		messages.error(request,"Unable to upload file. "+repr(e)+"No of row Upload is ."+str(cnt)+" and error in line "+str(data_dict)+" already exists")	
	messages.error(request,"No of row upload is: "+str(cnt)+" Error in line :"+str(data_dict)+" already exists")

	return HttpResponseRedirect("/pincode/")

@login_required(login_url="/adminlogin")
def destroypincode(request,id):
	try:
		product = Pincode.objects.get(id=id)  
		product.delete()
	except Exception as e:
		print(e)  
	return redirect('/pincode/')

@login_required(login_url="/adminlogin")
def upload_csv(request):
	if "GET" == request.method:
		print("Add product")
		return render(request, "addproduct.html")

	if "POST" == request.method:
		print("Upload product")
		try:
			csv_file = request.FILES["csv_file"]
			print(csv_file)
			if not csv_file.name.endswith('.csv'):
				messages.error(request,'File is not CSV type')
				return HttpResponseRedirect(reverse("upload_csv"))

			if csv_file.multiple_chunks():
				messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
				return HttpResponseRedirect(reverse("upload_csv"))

			file_data = csv_file.read().decode("utf-8")		
			lines = file_data.split("\n")
			cnt=0
			k=0
			print("1")
			for line in lines:
				print("2")					
				fields = line.split(",")
				data_dict = []
				param_dict= {}
				k=k+1
				ls=[]
				print("fields length is :", len(fields))
				if(len(fields)==11):
					param_dict["sku"]         = fields[0] #A
					param_dict["category"]    = fields[1] #B
					param_dict["model_No"]    = fields[2] #C

					data_dict.append(fields[3]) #D
					data_dict.append(fields[4]) #E
					data_dict.append(fields[5]) #F

					param_dict["title"]       = fields[6] #G
					param_dict["description"] = fields[7] #H
					param_dict["price"]       = fields[8] #I
					param_dict["sub_category"]= fields[9] #J
					param_dict["company"]     = fields[10]#K

					print("Param Dict :",param_dict)
					name2=[]
					for i in data_dict:
						if i!='0':
							url=i;
							print(url)
							r=requests.get(i)
							file_name=r.url.split('/')
							name=file_name[-1]
							file_name=open('store/media/profile_image/'+str(name), 'wb').write(r.content)
							name1='profile_image/'+str(name)
							name2.append(name1)
						else:
							name2.append('None')

					data_dict.clear()
					form = ProductForm(param_dict)
					
					if form.is_valid():
						instance = form.save()
						model_instance = Products.objects.filter(id=instance.id).update(images1 = name2[0],images2= name2[1],images3=name2[2])
						cnt=cnt+1
				else:
					ls.append(k)

		except Exception as e:
			print(e)
			logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
			messages.error(request,"Unable to upload file. "+repr(e)+"No of row Upload is ."+str(cnt))	
		messages.error(request,"No of row upload is. "+str(cnt))	
		return HttpResponseRedirect(reverse("upload_csv"))

@login_required(login_url="/adminlogin")
def fliparmy(request):
	if "GET" == request.method:
		return render(request, "addfliparmy.html")
	try:
		csv_file = request.FILES["csv_file"]
		if not csv_file.name.endswith('.csv'):
			messages.error(request,'File is not CSV type')
			return HttpResponseRedirect(reverse("fliparmy"))

		if csv_file.multiple_chunks():
			messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
			return HttpResponseRedirect(reverse("fliparmy"))

		file_data = csv_file.read().decode("utf-8")
		lines = file_data.split("\n")
		data_dict  = []# Track how many line is enter
		cnt=0
		k=0
		for line in lines:						
			fields = line.split(",")
			param_dict= {}
			k=k+1
			if(len(fields)==3):
				param_dict["titles"]      = fields[0]
				param_dict["description"] = fields[1]
				url=fields[2]
				z=url.split('\r')[0]
				r=requests.get(z)
				file_name=r.url.split('FLIPKARTONEPLUS')
				names=file_name[1].split('/')
				name=names[2]
				file_name=open('store/media/army_image/'+str(name), 'wb').write(r.content)
				name1='army_image/'+str(name)
				form = DesiArmyForm(param_dict)
				if form.is_valid():
					instance = form.save()
					model_instance = desiarmy.objects.filter(id=instance.id).update(images = name1)
					cnt=cnt+1
				else:
					data_dict.append(k)
				
	except Exception as e:
		logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
		messages.error(request,"Unable to upload file. "+repr(e)+"No of row Upload is ."+str(cnt)+" and error in line "+str(data_dict))	
	messages.error(request,"No of row upload is: "+str(cnt)+" Error in line :"+str(data_dict))
	return HttpResponseRedirect(reverse("fliparmy"))


@login_required(login_url="/adminlogin")
def adminorder(request):
	orders=placeorders.objects.all()
	myFilter =PaymentFilter(request.GET, queryset=orders)
	orders = myFilter.qs

	context = {
	'orders':orders,
	'myFilter':myFilter,
	}
	return render(request,'order.html',context)


@login_required(login_url="/adminlogin")
def customer(request):
	cust = Userprofile.objects.all()
	myFilter = UserFilter(request.GET, queryset=cust)
	cust = myFilter.qs

	context = {
	'cust':cust,
	'myFilter':myFilter,
	}
	return render(request,'customer.html',context)



@login_required(login_url="/adminlogin")
def placeorder(request):
	# place=orderawb.objects.all()
	# print(place)
	obj = placeorders.objects.all()
	print(obj)
	# myFilter = placeorderFilter(request.GET, queryset=place)
	# place = myFilter.qs
	return render(request,'placeorder.html',{'place':obj})



from django.core.paginator import Paginator



@login_required(login_url="/adminlogin")
def adminindex(request):
	products=Products.objects.all().order_by('-add_date')
	print(request.GET)

	myFilter = ProductFilter(request.GET, queryset=products)
	products = myFilter.qs
	print(products.count())

	paginator=Paginator(products,10)
	page     =request.GET.get('page')
	products =paginator.get_page(page)

	context = {
	'products':products,
	'myFilter':myFilter,

	}
	return render(request,'adminproduct.html',context)



def export_search_csv(request):
	products=Products.objects.all().order_by('-add_date')
	myFilter = ProductFilter(request.GET, queryset=products)
	products = myFilter.qs
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment;filename=productresult.csv'
	writer = csv.writer(response)
	writer.writerow(['Sku Id', 'Category','Model No', 'Images1', 'Images2','Images3','Title','Description','Price','Sub Category','Weight','Added Date','Company'])
	
	for users in products:
		writer.writerow([users.sku,users.category,users.model_No,users.images1,users.images2,users.images3,users.title,users.description,users.price,users.sub_category,
			users.weight,users.add_date,users.company])
	return response



@login_required(login_url="/adminlogin")
def destroy(request,product_id):
	try:
		product = Products.objects.get(id=product_id)  
		product.delete()
	except Exception as e:
		print(e)  
	return redirect('adminindex')


@login_required(login_url="/adminlogin")
def destroycarousel(request,id):  
	try:
		product = imagesupload.objects.get(id=id)
		product.delete()
	except Exception as e:
		print(e)
	return redirect('addcarousel')


@login_required(login_url="/adminlogin")
def addcarousel(request):
	if 'GET' == request.method:
		photos_list = imagesupload.objects.all()
		form1=Products.objects.values_list('model_No',flat=True).distinct()
		return render(request,'addbanner.html',{'photos':photos_list,'form':form1})

	if 'POST' == request.method:
		form = ImageForm(request.POST,request.FILES)
		photos_list = imagesupload.objects.all()
		form1=Products.objects.values_list('model_No',flat=True).distinct()
		if form.is_valid():
			form.save()
		return render(request,'addbanner.html',{'photos':photos_list,'form':form1})

@login_required(login_url="/adminlogin")
def mobilename(request):
	if 'GET' == request.method:
		photos_list = Mobilecover.objects.all()
		form=MobileForm()
		return render(request,'mobilename.html',{'photos':photos_list,'form':form})

	if 'POST' == request.method:
		form = MobileForm(request.POST)
		com  = request.POST['company']
		state= request.POST['mobilename']

		Mobilecover(company=com,mobilename=state).save()
		photos_list = Mobilecover.objects.all()
		form=MobileForm()
		return render(request,'mobilename.html',{'photos':photos_list,'form':form})


def load_cities(request):
	company = request.GET.get('country')
	cities = Products.objects.values_list('model_No',flat=True).filter(company=company).distinct()
	return render(request, 'city_dropdown_list_options.html', {'cities': cities})

def load_model(request):
	company = request.GET.get('country')
	print(company)
	cities = Products.objects.values_list('model_No',flat=True).filter(company=company).distinct()
	return render(request, 'product_dropdown_list_model.html', {'cities': cities})

def load_company(request):
	company = request.GET.get('country')
	print(company)
	cities = Products.objects.values_list('company',flat=True).filter(category=company).distinct()
	print(cities)
	return render(request, 'product_dropdown_list_company.html', {'cities': cities})


@login_required(login_url="/adminlogin")
def mobiledestroy(request,id):
	try:
		Mobilecover.objects.get(id=id).delete()
	except Exception as e:
		print(e)   
	return redirect('mobilename') 


@login_required(login_url="/adminlogin")
def updatemobile(request):
	if 'POST' == request.method:
		id=request.POST['id']
		company=request.POST['company']
		name=request.POST['name']
		form=Mobilecover.objects.filter(id=id).update(company=company,mobilename=name)
		return redirect('mobilename')

@login_required(login_url="/adminlogin")
def adminfile(request):
	Products=desiarmy.objects.all()
	return render(request,'adminfile.html',{'products':Products})


@login_required(login_url="/adminlogin")
def bulkupdate(request):
	if 'GET' == request.method:
		form=Products.objects.values_list('model_No',flat=True).distinct()
		return render(request,'bulkupdate.html',{'form':form})

	if 'POST' == request.method:
		model   = request.POST['company_id']
		price = request.POST['price']
		forms=Products.objects.filter(model_No=model).update(price=price)
		form=Products.objects.values_list('model_No',flat=True).distinct()
		return render(request,'bulkupdate.html',{'form':form})


@login_required(login_url="/adminlogin")
def bulkdes(request):
	if 'GET' == request.method:
		form=Products.objects.values_list('model_No',flat=True).distinct()
		return render(request,'bulkdes.html',{'form':form})

	if 'POST' == request.method:
		model = request.POST['company_id']
		desc  = request.POST['desc']
		forms=Products.objects.filter(model_No=model).update(description=desc)
		form=Products.objects.values_list('model_No',flat=True).distinct()
		return render(request,'bulkdes.html',{'form':form})


@login_required(login_url="/adminlogin")
def adminheading(request):
	if 'GET' == request.method:
		form=Products.objects.values_list('sub_category',flat=True).distinct()
		return render(request,'adminheading.html',{'form':form})

	if 'POST' == request.method:
		model = request.POST['company_id']
		desc  = request.POST['desc']
		forms=Products.objects.filter(model_No=model).update(description=desc)
		form =Products.objects.values_list('model_No',flat=True).distinct()
		return render(request,'bulkdes.html',{'form':form})

@login_required(login_url="/adminlogin")
def adminhomeword(request):
	if 'GET' == request.method:
		photos_list = homepageword.objects.all()
		return render(request,'adminhomeword.html',{'photos':photos_list})

	if 'POST' == request.method:
		form = HomepagewordForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('/adminhomeword')

@login_required(login_url="/adminlogin")
def textdestroy(request,id):
	try:
		homepageword.objects.get(id=id).delete()
	except Exception as e:
		print(e)   
	return redirect('/adminhomeword')	

# OnePlus7t-YOUCANGIRL_1470

@login_required(login_url="/adminlogin")
def adminhomeimage(request):
	if 'GET' == request.method:
		photos_list = homedesimage.objects.all()
		return render(request,'adminhomeimage.html',{'photos':photos_list})

	if 'POST' == request.method:
		sku  = request.POST['sku']
		name = request.POST['name']
		try:
			product_id=Products.objects.get(sku=sku)
			homedesimage(name=name,prod=product_id).save()
		except Exception as e:
			messages.error(request,""+str(e))
		return redirect('/adminhomeimage')

@login_required(login_url="/adminlogin")
def adminhomeimagedestroy(request,id):
	try:
		homedesimage.objects.get(id=id).delete()
	except Exception as e:
		print(e)   
	return redirect('/adminhomeimage')
# ---------------------------------------------------End Admin-------------------------------------------------#



def home(request):
	request.session['totalamount']=''
	request.session['coupon']=''
	

	product=recentarrival.objects.all().order_by('-id')
	n=len(product)

	nSlides = n // 4 + ceil((n / 4) - (n // 4))
	allProds = [[product, range(1, nSlides), nSlides]]
	

	home=homepageimg.objects.all()
	word=homepageword.objects.all()
	pro=homedesimage.objects.all()
	# print(pro)

# Men Navbar 
	men=Products.objects.filter(category='TSHIRT',sub_category='MALE').values_list('model_No',flat=True).distinct()
	print(men)
# Women Navbar 
	women=Products.objects.filter(category='TSHIRT',sub_category='FEMALE').values_list('model_No',flat=True).distinct()
	print(women)


	if imagesupload.objects.all().count()==0:
		img1=0
		img2=0
		img3=0
		if request.user.is_authenticated == True:
			cust_username=auth.get_user(request)
			cart =Carts.objects.filter(cust_username=cust_username,added=True)
			context={

			'img1':img1,'img2':img2,'img3':img3,'allProds':allProds,'home':home,'cart':cart,'word':word,'pro':pro,'men':men,'women':women
			}
		else:
			context={
			'img1':img1,'img2':img2,'img3':img3,'allProds':allProds,'home':home,'word':word,'pro':pro,'men':men,'women':women
			}
			return render(request,'index-16.html',context)


	if imagesupload.objects.all().count()==1:
		img=imagesupload.objects.all().order_by('-id')[:1]
		img1=img[0]
		print(img1)
		img2=0
		img3=0
		if request.user.is_authenticated == True:
			cust_username=auth.get_user(request)
			cart =Carts.objects.filter(cust_username=cust_username,added=True)
			context={
			'img1':img1,'img2':img2,'img3':img3,'allProds':allProds,'home':home,'cart':cart,'word':word,'pro':pro,'men':men,'women':women
			}
		else:
			context={
			'img1':img1,'img2':img2,'img3':img3,'allProds':allProds,'home':home,'word':word,'pro':pro,'men':men,'women':women
			}
			return render(request,'index-16.html',context)


	if imagesupload.objects.all().count()==2:
		img=imagesupload.objects.all().order_by('-id')[:2]
		img1=img[0]
		img2=img[1]
		img3=0
		if request.user.is_authenticated == True:
			cust_username=auth.get_user(request)
			cart =Carts.objects.filter(cust_username=cust_username,added=True)
			context={
			'img1':img1,'img2':img2,'img3':img3,'allProds':allProds,'home':home,'cart':cart,'word':word,'pro':pro,'men':men,'women':women
			}
		else:
			context={
			'img1':img1,'img2':img2,'img3':img3,'allProds':allProds,'home':home,'word':word,'pro':pro,'men':men,'women':women
			}
		return render(request,'index-16.html',context)
	else:
		img=imagesupload.objects.all().order_by('-id')[:3]
		# img1=img[0]
		# img2=img[1]
		# img3=img[2]
		if request.user.is_authenticated == True:
			cust_username=auth.get_user(request)
			cart =Carts.objects.filter(cust_username=cust_username,added=True)
			print(cart)
			print("---------")
			context={
			# 'img1':img1,'img2':img2,'img3':img3,
			'allProds':allProds,'home':home,'cart':cart,'word':word,'pro':pro,'men':men,'women':women
			}
		else:
			context={
			# 'img1':img1,'img2':img2,'img3':img3,
			'allProds':allProds,'home':home,'word':word,'pro':pro,'men':men,'women':women
			}
		return render(request,'index-16.html',context)

def google(request):
	cust_id=auth.get_user(request)
	print(cust_id)

	if Userprofile.objects.filter(user_id=cust_id).exists()==False:
		mobile=Userprofile(user_id=cust_id.id)
		mobile.save()

		userwa=User.objects.get(id=cust_id.id)
		wallet=Wallet.objects.create(user=userwa)
		wallet.save()
		print("Userprofile Exist")
	return redirect('home')

def mobile(request):
	product=Mobilecover.objects.all()
	print(product)
	# coverdict = {}
	# for i in product:
	# 	print(i.mobilename)
	# 	print(i.company)
	# 	mobilename = i.mobilename.replace('Apple',"")
	# 	coverdict[i.company] = mobilename
	if request.user.is_authenticated == True:
		cust_username=auth.get_user(request)
		cart =Carts.objects.filter(cust_username=cust_username,added=True)
		return render(request,'a.html',{'product':product,'cart':cart})
	return render(request,'a.html',{'product':product})


def about(request):
	if request.user.is_authenticated == True:
		cust_username=auth.get_user(request)
		cart =Carts.objects.filter(cust_username=cust_username,added=True)
		return render(request,'about.html',{'cart':cart})
	return render(request,'about.html')


def contact(request):
	if request.method=='GET':
		if request.user.is_authenticated == True:
			cust_username=auth.get_user(request)
			cart =Carts.objects.filter(cust_username=cust_username,added=True)
			return render(request,'contact.html',{'cart':cart})
		return render(request,'contact.html')

	if request.method == "POST":
		try:
			form = ContactForm(request.POST,request.FILES)
			if form.is_valid():
				form.save()
		except Exception as e:
			print(e)
		return redirect('/contact')
	


def product(request,product_id):
	product=Products.objects.get(id=product_id)
	des=product.description
	keys=re.split(':|#',des)
	print(keys)
	d = dict(itertools.zip_longest(*[iter(keys)] * 2, fillvalue=""))
	review=Review.objects.filter(product_id_id=product_id)

	if request.user.is_authenticated == True:
		cust_username=auth.get_user(request)
		cart =Carts.objects.filter(cust_username=cust_username,added=True)
		return render(request,'productpage.html',{'product':product,'review':review,'cart':cart,'d':d})
	return render(request,'productpage.html',{'product':product,'review':review,'d':d})


@login_required(login_url="/user/login")
def review(request,product_id):
	try:
		product=Products.objects.get(id=product_id)
		cust_username=auth.get_user(request)
		cart =Carts.objects.filter(cust_username=cust_username,added=True)
	except Exception as e:
		print(e)
	return render(request,'addreview.html',{'product':product,'cart':cart})


@login_required(login_url="/user/login")
def addreview(request,product_id):
	if request.method=='POST':
		try:
			product=Products.objects.get(id=product_id)
			product_id=product.id
			cust_username=auth.get_user(request)
			review= request.POST['review']
			picture=request.FILES.get('picture',None)
			rating=request.POST['rating']
			Review(cust_username=cust_username,product_id_id=product_id,review=review,picture=picture,rating=rating).save()

			review=Review.objects.filter(product_id=product_id)
			for j in review:
				rev=Review.objects.filter(product_id=j.product_id).aggregate(rating=Avg('rating'))

			rev=round(rev['rating'],2)
			print(rev)	

			Products.objects.filter(id=product_id).update(avg_rating=rev)
		except Exception as e:
			print(e)
	return redirect('Product',product_id=product_id)

def mugs(request):
	products=Products.objects.all()
	if request.user.is_authenticated == True:
		cust_username=auth.get_user(request)
		cart =Carts.objects.filter(cust_username=cust_username,added=True)
		return render(request,'mug.html',{'title':'Mugs','products':products,'cart':cart})
	return render(request,'mug.html',{'title':'Mugs','products':products})	


def tshirts(request,category,theme):
	products=Products.objects.filter(sub_category=category,model_No=theme)
	myFilter=TshirtFilter(request.GET,queryset=products)
	products=myFilter.qs
	print(products)

	if request.user.is_authenticated == True:
		cust_username=auth.get_user(request)
		cart =Carts.objects.filter(cust_username=cust_username,added=True)
		return render(request,'tshirt.html',{'products':products,'cart':cart,'myFilter':myFilter})
	return render(request,'tshirt.html',{'products':products,'myFilter':myFilter})

def pshokets(request):
	products=Products.objects.all()
	if request.user.is_authenticated == True:
		cust_username=auth.get_user(request)
		cart =Carts.objects.filter(cust_username=cust_username,added=True)
		return render(request,'popsocket.html',{'title':'Pop Shokets','products':products,'cart':cart})
	return render(request,'popsocket.html',{'title':'Pop Shokets','products':products})

def batch(request):
	products=Products.objects.all()
	if request.user.is_authenticated == True:
		cust_username=auth.get_user(request)
		cart =Carts.objects.filter(cust_username=cust_username,added=True)
		return render(request,'batch.html',{'products':products,'cart':cart})
	return render(request,'batch.html',{'products':products})


def mobileCovers(request,model_No):
	products=Products.objects.filter(model_No=model_No)
	ducts   =Products.objects.filter(model_No=model_No).count()

	try:
		if request.method=='GET':
			sort=request.GET['sortby']
			print(sort)		
			if sort=='high':
				product=Products.objects.filter(model_No=model_No).order_by('-price')

			if sort=='low':
				product=Products.objects.filter(model_No=model_No).order_by('price')

			if sort=='new':
				product=Products.objects.filter(model_No=model_No).order_by('add_date')
			
			if sort=='rating':
				product=Products.objects.filter(model_No=model_No).order_by('-avg_rating')

			if sort=='Featured':
				product=Products.objects.filter(model_No=model_No)
			
			products = product
	except Exception as e:
		print(e)
		
	if request.user.is_authenticated == True:
		cust_username=auth.get_user(request)
		cart =Carts.objects.filter(cust_username=cust_username,added=True)
		context={'model':model_No,'products':products,'cart':cart}
		return render(request,'modelcover.html',context)
	return render(request,'modelcover.html',{'model':model_No,'products':products})


@login_required(login_url="/user/login")
def add_to_cart(request):
	if request.method=='POST':
		try:
			product_id=request.POST['product_ids']
			quantity=request.POST['qty']
			size=request.POST.get('shirt_size',None)
			p=Products.objects.get(id=product_id) 
			cust_username=auth.get_user(request)
			Carts(product_id=p,price=p.price,cust_username=cust_username,quantitys=quantity,size=size,title=p.category,image=p.images1).save()
		except Exception as e:
			print(e)	
	return redirect('/Cart')

@login_required(login_url="/user/login")
def rem_from_cart(request,id):
	try:
		product=Carts.objects.get(id=id)
		product.delete()
	except Exception as e:
		print(e)
	return redirect('/Cart')
	

def Cart(request):
	if request.user.is_authenticated:
		try:
			cust_username=auth.get_user(request)
			productsPick=Carts.objects.filter(cust_username=cust_username,added=True)
			total_price=Carts.objects.filter(cust_username=cust_username,added=True).aggregate(total=Sum(F('price')*F('quantitys')))['total']
			return render(request,"cart.html",{'productsPick':productsPick,'total_price':total_price,'cart':productsPick})
		except Exception as e:
			print(e)
	return render(request,"login.html")


@login_required(login_url="/user/login")
def ordersummary(request):
	try:
		cust_username=auth.get_user(request)
		order=placeorders.objects.filter(cust_username_id=cust_username,cancelorders_id__isnull=True,delivered=True)
		cart =Carts.objects.filter(cust_username=cust_username,added=True)
	except Exception as e:
		print(e)
		return render(request,'Notfound.html')
	return render(request,'ordersummary.html',{'orders':order,'cart':cart})  
	
@login_required(login_url="/user/login")
def couponcheck(request):
	query=request.GET.get('q')
	z=request.POST.get('price')
	print(z)
	print(query)
	cust_username=auth.get_user(request)

	if Coupon.objects.filter(Q(ccode=query)).exists():
		dis=Coupon.objects.get(ccode=query)
		dis11=dis.discount
		cid=dis.id
		productsPick=Carts.objects.filter(cust_username=cust_username,added=True)
		amount1=Carts.objects.filter(cust_username=cust_username,added=True).aggregate(Sum('price'))['price__sum']
		disamt=int((amount1*dis11)/100)
		tol_price=(amount1-disamt)
		request.session['totalamount'] = tol_price
		request.session['coupon'] = cid
		return render(request,'cart.html',{'productsPick':productsPick,'total_price':tol_price})
	else:
		try:
			if request.session['totalamount'] !='' and request.session['coupon'] != '':
				del request.session['totalamount']
				del request.session['coupon']
		except Exception as e:
			print(e)

		messages.error(request,"Invalid Coupon Code")
		return redirect('cart')



@login_required(login_url="/user/login")
def account(request):
	try:
		cust_username=auth.get_user(request)
		order=placeorders.objects.filter(cust_username=cust_username)
		cart=Carts.objects.filter(cust_username=cust_username,added=True)
		user=Userprofile.objects.filter(user_id=cust_username.id)
		adds=placeorders.objects.filter(cust_username=cust_username).last()
		findid=Wallet.objects.get(user_id=cust_username.id).id
		wallet=Wallet.objects.filter(user_id=cust_username.id)
		history=Transaction.objects.filter(wallet=findid)
		context={'order':order,'user':user,'cart':cart,'orders':adds,'wallet':wallet,'history':history}
	except Exception as e:
		print(e)
		return render(request,'Notfound.html')
	return render(request,'dashboard.html',context)
	


@login_required(login_url="/user/login")
def cancelorder(request,id):
	try:
		orders=placeorders.objects.filter(id=id)
		order=placeorders.objects.get(id=id)
		add_time=order.order_date
		current_time=datetime.datetime.now()
		current_time=current_time.time()
		time=datetime.timedelta(hours=current_time.hour,minutes=current_time.minute) - datetime.timedelta(hours=add_time.hour,minutes=add_time.minute)
		if (time.seconds < 14400 ):
			messages.error(request,"ITS WILL DELETE ALL PRODUCT WHICH IS ORDER IN BULK")
		else:
			messages.error(request,"ITS BEEN MORE THAN 4 HOUR CANNOT BE DELETED")
			return redirect('/myaccount')
		context={'orders':orders}
	except Exception as e:
		print(e)
	return render(request, "cancelorder.html",context)

def searchbar(request):
	query=request.GET.get('q')
	print(query)
	if Products.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)| Q(sub_category__icontains=query) | Q(company__icontains=query)).exists():
		products=Products.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(sub_category__icontains=query) | Q(company__icontains=query))
	else:
		products=Products.objects.all()
	return render(request,'show.html',{'products':products})



@csrf_exempt
def otpsend(request):
	if request.method=='POST':
		phone=request.POST['phonenumber']
		print("Phone no is :",phone);
		if Userprofile.objects.filter(mobile=phone).exists():
			return HttpResponse("Mobile")

		url = "https://2factor.in/API/R1/?module=SMS_OTP&apikey=4e32200c-3173-11ea-9fa5-0200cd936042&to=%s&otpvalue=AUTOGEN3&templatename=StreetMart" % (phone)
		response = requests.request("POST", url)
		if "Success" in response.text:
			return HttpResponse("Success")
		else:
			return HttpResponse("Failure")
	return render(request,'sendotp.html')


@csrf_exempt
def verifyotp(request):
	if request.method=='POST':
		phone=request.POST['phonenumber']
		otp_value=request.POST['otp']
		url = "https://2factor.in/API/V1/4e32200c-3173-11ea-9fa5-0200cd936042/SMS/VERIFY3/%s/%s" % (phone, otp_value)
		response = requests.request("POST", url)
		if "Success" in response.text:
			return HttpResponse("Success")
		else:
			return HttpResponse("Failure")
	return render(request,'verifyotp.html',{'m':m})

import http.client
import mimetypes


def createorder(request):
	conn = http.client.HTTPSConnection("admin.milesawayy.com")
	payload = "{\n    \"vendor_code\": \"V001\",\n    \"company_name\": \"DESICOVERS\",\n    \"user_email\": \"desicovers.1@gmail.com\",\n    \"pickup_location\": \"DESICOVERS\",\n    \"order_type\": \"%s\",\n    \"orderno\": \"%s\",\n    \"quantity\": \"%s\",\n    \"product_desc\": \"%s\",\n    \"customer_name\": \"%s\",\n    \"customer_email\": \"%s\",\n    \"customer_mobile\": \"%s\",\n    \"customer_phone\": \"\",\n    \"customer_city\": \"%s\",\n    \"customer_state\": \"%s\",\n    \"custom_address\": \"%s\",\n    \"customer_pincode\": \"%s\",\n    \"delivery_mode\": \"surface\",\n    \"product_mrp\": \"%s\",\n    \"product_group\": \"\",\n    \"codamount\": \"%s\",\n    \"packamount\": \"0\",\n    \"octroi_mrp\": \"0\",\n    \"physical_weight\": \"1\",\n    \"shipping_length\": \"1\",\n    \"shipping_width\": \"1\",\n    \"shipping_height\": \"1\"\n}\n" % ('COD',134570,1,'tshirt','kalim','shavej@gmail.com',7958412589,'Mumbai','Maharashtra','Room no 51 Kandivali',400059,100,125)
	print(payload)
	headers = {
	  'Authorization': 'f82de5343eac3925cbb0c14378ca508f0fa18bafb236efed983b871c59cae033065eea91091f843552d1c7602e99fbc27fd3077c2bafc2f5f31db79831faef4e',
	  'Content-Type': 'application/json'
	}
	conn.request("POST", "/api/v1/order_create", payload, headers)
	res = conn.getresponse()
	data = res.read()

	print(data.decode("utf-8"))

	dic = json.loads(data)
	print(dic)

	myawb=dic['data']
	print(myawb)

	orderid=dic['data']['orderId']
	print(orderid)

	awb=dic['data']['awb_no']
	print(awb)
	return HttpResponse(data)


# @login_required(login_url="/adminlogin")
# def multipleimage(request):
# 	if 'GET' == request.method:

# 		photos_list = imagesupload.objects.all()
# 		return render(request,'multipleimage.html',{'photos':photos_list})

# 	if 'POST' == request.method:
# 		form = ImageForm(request.POST,request.FILES)
# 		photos_list = imagesupload.objects.all()
# 		if form.is_valid():
# 			for f in request.FILES.getlist("images"):
# 				z=imagesupload.objects.create(images=f)
	
# 		return render(request,'multipleimage.html',{'photos':photos_list})

# def shiprocket(request):
# 	url = "https://apiv2.shiprocket.in/v1/external/auth/login"
# 	payload = "{\n    \"email\": \"desicovers.1@gmail.com\",\n    \"password\": \"Dhairya@123\"\n}"
# 	print(payload)
# 	headers = {
# 		'Content-Type': 'application/json',

# 	}
# 	print(headers)
# 	response = requests.request("POST", url, headers=headers, data = payload)
# 	print(response)
# 	print(response.text.encode('utf8'))
# 	j=response.json()
# 	print(j)
# 	print(j['token'])
# 	request.session['token'] = j['token']
# 	return HttpResponse('Ho ')




# def shiprocket1(request):
# 	conn = http.client.HTTPSConnection("apiv2.shiprocket.in")
# 	payload = "{\n    \"email\": \"rah.ranchal@gmail.com\",\n    \"password\": \"Rasanara@3\"\n}"
# 	headers = {'Content-Type': 'application/json'
# 			  }
# 	conn.request("POST", "/v1/external/auth/login", payload, headers)
# 	res = conn.getresponse()

# 	data = res.read()
# 	print(data.decode("utf-8"))
# 	return HttpResponse("THIS WORKS CONN WALA")

# def createorder1(request):
# 	conn = http.client.HTTPSConnection("apiv2.shiprocket.in")
# 	payload = "{\n  \"order_id\": \"224-477\",\n  \"order_date\": \"2019-07-24 11:11\",\n  \"pickup_location\": \"Jammu\",\n  \"channel_id\": \"12345\",\n  \"comment\": \"Reseller: M/s Goku\",\n  \"billing_customer_name\": \"Naruto\",\n  \"billing_last_name\": \"Uzumaki\",\n  \"billing_address\": \"House 221B, Leaf Village\",\n  \"billing_address_2\": \"Near Hokage House\",\n  \"billing_city\": \"New Delhi\",\n  \"billing_pincode\": \"110002\",\n  \"billing_state\": \"Delhi\",\n  \"billing_country\": \"India\",\n  \"billing_email\": \"naruto@uzumaki.com\",\n  \"billing_phone\": \"9876543210\",\n  \"shipping_is_billing\": true,\n  \"shipping_customer_name\": \"\",\n  \"shipping_last_name\": \"\",\n  \"shipping_address\": \"\",\n  \"shipping_address_2\": \"\",\n  \"shipping_city\": \"\",\n  \"shipping_pincode\": \"\",\n  \"shipping_country\": \"\",\n  \"shipping_state\": \"\",\n  \"shipping_email\": \"\",\n  \"shipping_phone\": \"\",\n  \"order_items\": [\n    {\n      \"name\": \"Kunai\",\n      \"sku\": \"chakra123\",\n      \"units\": 10,\n      \"selling_price\": \"900\",\n      \"discount\": \"\",\n      \"tax\": \"\",\n      \"hsn\": 441122\n    }\n  ],\n  \"payment_method\": \"Prepaid\",\n  \"shipping_charges\": 0,\n  \"giftwrap_charges\": 0,\n  \"transaction_charges\": 0,\n  \"total_discount\": 0,\n  \"sub_total\": 9000,\n  \"length\": 10,\n  \"breadth\": 15,\n  \"height\": 20,\n  \"weight\": 2.5\n}"
# 	token=request.session['token']
# 	# del request.session['token']
# 	headers = {'Content-Type': 'application/json',
#   			   "Authorization": 'Bearer {}'.format(token)			}
# 	conn.request("POST", "/v1/external/orders/create/adhoc", payload, headers)
# 	res = conn.getresponse()
# 	data = res.read()
# 	print(data.decode("utf-8"))
# 	return HttpResponse(data.decode('utf-8'))



# @csrf_exempt
# def handlerequest(request):#paytm will send you post request
# 	form=request.POST
# 	response_dict={}
# 	checksum = ""
# 	print('1')
# 	for i in form.keys():
# 		response_dict[i]=form[i]
# 		if i=='CHECKSUMHASH':
# 			checksum=form[i]
# 			print("-------------------")
# 			print(checksum)
	
# 	try:
# 		print('2')
# 		verify=Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
# 		print(verify)
# 		if verify:
# 			print(verify)
# 			if response_dict['RESPCODE']=='01':
# 				detail=placeorders.objects.filter(order_id=orderdata).update(bank=d)
# 			else:
# 				print("Order was not Successful because"+response_dict['RESPMSG'])
# 				detail=placeorders.objects.filter(order_id=orderdata).update(bank=d,delivered=False)
# 	except Exception as e:
# 		print(e)

# 	return render(request,'paymentstatus.html',{'response':response_dict})








# # def paytm(request):
# # 	print("In orderdetails 1")
# # 	cust_username=auth.get_user(request)
# # 	print(cust_username)
# # 	email=cust_username.email
# # 	print(email)  
# # 	req=placeorders.objects.all().last()
# # 	order_id=number=get_random_string(length=10,allowed_chars=u'0123456789')
# # 	print(order_id)
# # 	amount=req.totalamount
# # 	print(amount)
# # 	param_dict = {
# # 				'MID':'HampNc93618229896078',#Test api mid 
# # 				# 'MID':'fUrUX46436172672941',#PRoduction
# # 				# 'MID':'WorldP64425807474247',
# # 	            'ORDER_ID':str(order_id),
# # 	            'TXN_AMOUNT':str(amount),
# # 	            'CUST_ID':email,
# # 	            'INDUSTRY_TYPE_ID':'Retail',
# # 	            'WEBSITE':'WEBSTAGING',
# # 	            'CHANNEL_ID':'WEB',
# # 		    	'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',
# # 			}
# # 	param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
# # 	print(param_dict['CHECKSUMHASH'])
# # 	return render(request,'paytm.html',{'param_dict':param_dict})

# # def sendemail(request):
# #     subject = 'Thank you for registering to our site'
# #     message = ' it  means a world to us '
# #     email_from = settings.EMAIL_HOST_USER
# #     recipient_list = ['rsoni8672@gmail.com',]
# #     send_mail( subject, message, email_from, recipient_list, fail_silently=False )

# #     return render(request,'store/email.html')

# # def sms(request):
# # 	# +12052738515
# # 	to='+919594640375'
# # 	client=Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)

# # 	message=client.messages.create(body='qwerty',to=to,from_=settings.TWILIO_PHONE_NUMBER)
# # 	print(message.sid)

# # 	return HttpResponse("Sms send ")

# # def date(request):
# # 	orders=placeorders.objects.all()
# # 	return render(request,'date.html',{'orders':orders})

# # def delete_order(request,order_id):
# # 	order=placeorders.objects.get(order_id=order_id)
# # 	add_time=order.order_date

# # 	print(add_time)
# # 	print(add_time.hour)
# # 	print(add_time.minute)
# # 	current_time=datetime.datetime.now()
# # 	current_time=current_time.time()
# # 	print(current_time)
# # 	time=datetime.timedelta(hours=current_time.hour,minutes=current_time.minute) - datetime.timedelta(hours=add_time.hour,minutes=add_time.minute)
# # 	print(time)
# # 	print(time.seconds)
# # 	if (time.seconds < 14400 ):
# # 		order.delete()
# # 		print('product deleted')
# # 		return redirect('/cancelorder')
# # 	else:
# # 		print("ITS BEEN MORE THAN 4 hour cannot be deleted")
# # 		return redirect('/cancelorder') 

# @login_required(login_url="/adminlogin")
# def multipleimage(request):
# 	if 'GET' == request.method:

# 		photos_list = imagesupload.objects.all()
# 		return render(request,'multipleimage.html',{'photos':photos_list})

# 	if 'POST' == request.method:
# 		form = ImageForm(request.POST,request.FILES)
# 		photos_list = imagesupload.objects.all()
# 		if form.is_valid():
# 			for f in request.FILES.getlist("images"):
# 				z=imagesupload.objects.create(images=f)
	
# 		return render(request,'multipleimage.html',{'photos':photos_list})

# @login_required(login_url="/adminlogin")
# def chart(request):
# 	return render(request,'charts.html')


# @login_required(login_url="/adminlogin")
# def apicheck(request):
# 	return render(request,'api.html')

# @login_required(login_url="/adminlogin")
# def refundwallet(request):
# 	if 'GET' == request.method:
# 		photos_list = homepageimg.objects.all()
# 		return render(request,'homepage.html',{'photos':photos_list})

# 	if 'POST' == request.method:
# 		form = HomeForm(request.POST,request.FILES)
# 		print(form)
# 		photos_list = homepageimg.objects.all()
# 		if form.is_valid():
# 			form.save()
	
# 		return render(request,'homepage.html',{'photos':photos_list})

# @login_required(login_url="/adminlogin")
# def update(request, product_id):
  
#     product = Products.objects.get(id=product_id) 
#     print(product)
#     print(request.POST)
#     form =ProductForm(request.POST,request.FILES, instance = product) 
#     print(form.errors)  
#     if form.is_valid():  
#         form.save()
#         return redirect('adminindex')
#     return render(request, 'edit.html', {'product':product})


# @login_required(login_url="/user/login")
# def cancelorder(request,id):
# 	order=placeorders.objects.filter(id=id)
# 	print(order)
# 	context={'orders':order}
# 	return render(request, "cancelorder.html",context)