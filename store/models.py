from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from store.errors import InsufficientBalance
from decimal import Decimal


CURRENCY_STORE_FIELD = getattr(settings,
        'WALLET_CURRENCY_STORE_FIELD', models.BigIntegerField)



class Wallet(models.Model):
    user           = models.ForeignKey(User,on_delete = models.CASCADE)
    current_balance= CURRENCY_STORE_FIELD(default=0)
    created_at     = models.DateTimeField(auto_now_add=True)

    def deposit(self,value,information,typeofmoney):
        self.transaction_set.create(
            value=value,
            running_balance=self.current_balance + value,
            information=information,
            typeofmoney=typeofmoney,
        )
        self.current_balance += value
        self.save()

    def carddeposit(self,value,information,card_info,typeofmoney):
        self.transaction_set.create(
            value=value,
            running_balance=self.current_balance + value,
            information=information,
            typeofmoney=typeofmoney,
            card_info=card_info,
        )
        self.current_balance += value
        self.save()
       

class Transaction(models.Model):
	wallet           =models.ForeignKey(Wallet,on_delete=models.CASCADE)
	value            =CURRENCY_STORE_FIELD(default=0)
	running_balance  =CURRENCY_STORE_FIELD(default=0)
	information      =models.CharField(max_length=1000,default='None')
	typeofmoney      =models.CharField(max_length=100,default='credit')
	card_info        =models.CharField(max_length=1000,default=None,blank=True,null=True)
	created_at       =models.DateTimeField(auto_now_add=True)

	def __str__(self): # i hate autoField 
		return '%s' % (self.id)


class Tshirtsize(models.Model):
	small      =models.CharField(max_length=120,blank=True,null=True)
	Medium     =models.CharField(max_length=120,blank=True,null=True)
	large      =models.CharField(max_length=120,blank=True,null=True)
	xl         =models.CharField(max_length=120,blank=True,null=True)
	xxl        =models.CharField(max_length=120,blank=True,null=True)

	def __str__(self): # i hate autoField 
		return '%s' % (self.id)

	class Meta:
		db_table="tshirtsize"


class Products(models.Model):
	sku			=models.CharField(max_length=500,default='None')
	category    =models.CharField(max_length=1000)
	model_No    =models.CharField(max_length=1000)
	images1     =models.FileField(upload_to='profile_image',blank=True,null=True)
	images2     =models.FileField(upload_to='profile_image',blank=True,null=True)
	images3     =models.FileField(upload_to='profile_image',blank=True,null=True)
	title       =models.CharField(max_length=1000)
	description =models.CharField(max_length=2000)
	price       =models.CharField(max_length=500)
	sub_category=models.CharField(max_length=1000)
	weight      =models.CharField(max_length=500,default='0',blank=True,null=True)
	size        =models.CharField(max_length=500,default='0',blank=True,null=True)
	add_date    =models.DateTimeField(auto_now_add=True)
	company     =models.CharField(default='Desi Cover',max_length=100,blank=True,null=True)
	add_recent  =models.BooleanField(default=False)
	tshirt      =models.ForeignKey(Tshirtsize,on_delete=models.CASCADE,blank=True, null=True)
	avg_rating  =models.FloatField(default='0',blank=True,null=True)

	def __str__(self): 
		return '%s %s %s %s' % (self.id,self.size,self.model_No,self.company)
	
	class Meta:
		db_table="products"

# 103.143.46.218

class recentarrival(models.Model):
	products=models.ForeignKey(Products,on_delete=models.CASCADE)

	class Meta:
		db_table = "recentarrival"


class imagesupload(models.Model):
	images    = models.FileField(upload_to='carouselimage',blank=True,null=True)
	model_name= models.CharField(max_length=100,default='0')
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return '%s' % (self.id)

	class Meta:
		db_table="imageupload"

class desiarmy(models.Model):
	titles     =models.CharField(max_length=100)
	description=models.CharField(max_length=1000)
	images     =models.FileField(upload_to='army_image',blank=True,null=True)

	class Meta:
		db_table="desiarmy"


class Carts(models.Model):
	product_id    =models.ForeignKey(Products,on_delete=models.CASCADE)
	price         =models.IntegerField()
	cust_username =models.ForeignKey(User,on_delete=models.CASCADE)
	quantitys      =models.IntegerField(default='1')
	title         =models.CharField(max_length=100)
	size          =models.CharField(max_length=100,blank=True, null=True)
	image         =models.ImageField(upload_to='profile_image',blank=True,null=True)
	added         =models.BooleanField(default=True)

	def __str__(self):
		return '%s %s' % (self.product_id, self.price)
	
	class Meta:
		db_table="cart"


class Coupon(models.Model):
	ccode       =models.CharField(max_length=100)
	description =models.CharField(max_length=100)
	Userlimit   =models.CharField(max_length=100,default='0')  
	percentage  =models.CharField(max_length=30,default="None")
	add_date    =models.DateTimeField()
	end_date    =models.DateTimeField()
	discount    =models.IntegerField(default='0')
	
	def __str__(self):
		return self.ccode
	class Meta:
		db_table="coupon"

class bankdetails(models.Model):
	paymentid    =models.CharField(max_length=500,null=False,blank=False,default=None)
	currency     =models.CharField(max_length=100,null=False,blank=False)
	error_code   =models.CharField(max_length=100,null=True,blank=True,default=None)
	card_id      =models.CharField(max_length=100,null=True,blank=True)
	paymentmode  =models.CharField(max_length=100,null=False,blank=False)
	totalamount  =models.FloatField()
	status       =models.CharField(max_length=100,null=False,blank=False)
	txndate      =models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return '%s' %(self.id)

	class Meta:
		db_table='bankdetails'

class cancelorders(models.Model):
	payment     = models.ForeignKey(bankdetails,on_delete=models.CASCADE,blank=True, null=True)
	cancelinfo  = models.CharField(max_length=1000,null=False,blank=False)
	order_id    = models.CharField(max_length=1000,null=True,blank=True)
	add_date    = models.DateTimeField(auto_now_add=True)
	initiatedpay= models.BooleanField(default=False)#false mean nahi Diya

	def __str__(self):
		return '%s %s' % (self.order_id,self.cancelinfo)

	class Meta:
		db_table="cancelorders"


class OrderGenManager(models.Manager):
	def generator(self):
		orderid=self.get_queryset().last()
		print(orderid)
		if orderid is None:
			return 2
		else:
			autoorder=int(str(orderid))+1
			return autoorder
			
		
class Orders(models.Model):
	cust_username=models.ForeignKey(User,on_delete=models.CASCADE)
	order        =models.CharField(max_length=100, blank=True)
	cart_id		 =models.ForeignKey(Carts,on_delete=models.CASCADE,blank=True, null=True)
	session_date =models.DateTimeField(auto_now_add=True)

	objects      = OrderGenManager()

	def __str__(self):
		return '%s' % (self.order)
	
	class Meta:
		db_table="orders"


class placeorders(models.Model):
	order_id     =models.CharField(null=False,blank=False,max_length=20)
	order_date   =models.DateTimeField(auto_now_add=True)
	cust_username=models.ForeignKey(User,on_delete=models.CASCADE)
	products     =models.ForeignKey(Carts,on_delete=models.CASCADE)
	coupon       =models.ForeignKey(Coupon,on_delete=models.CASCADE,blank=True, null=True)
	address1     =models.CharField(max_length=100,null=False,blank=False)#3
	address2     =models.CharField(max_length=100,null=False,blank=False)#4
	pincode      =models.CharField(max_length=6,null=False,blank=False)#5
	city         =models.CharField(max_length=100,null=False,blank=False)#6
	state        =models.CharField(max_length=100,null=False,blank=False)#7
	phone        =models.CharField(max_length=11,null=False,blank=False)#8
	email        =models.EmailField()#9
	totalamount  =models.IntegerField()
	last_name    =models.CharField(max_length=100,null=False,blank=False)#1
	first_name   =models.CharField(max_length=100,null=False,blank=False)#2
	paymentmode  =models.CharField(max_length=100,null=False,blank=False)
	bank         =models.ForeignKey(bankdetails,on_delete=models.CASCADE,null=True)
	cancelorders =models.ForeignKey(cancelorders,on_delete=models.CASCADE,null=True)
	delivered    =models.BooleanField(default=True)
	custdelieverd=models.BooleanField(default=False)#false mean nahi huwa
# models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=10)
	def __str__(self):
		return '%s %s %s %s %s %s %s %s %s %s %s' % (self.bank,self.order_id,self.order_date,self.address1,self.address2,self.city,self.state,self.phone,self.email,self.last_name,self.first_name)

	class Meta:
		db_table="placeorder"


class Review(models.Model):
	cust_username=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
	product_id   =models.ForeignKey(Products,on_delete=models.CASCADE,null=True,blank=True,related_name='reviewprod')
	review       =models.CharField(max_length=500,)
	picture      =models.ImageField(upload_to='profile_image',blank=True,null=True)
	rating       =models.FloatField()
	def __str__(self):
		return '%s %s' % (self.product_id,self.rating)

	class Meta:
		db_table="review"

class Contact(models.Model):
	name   =models.CharField(max_length=50)
	phone  =models.CharField(max_length=11)
	subject=models.CharField(max_length=100)
	message=models.CharField(max_length=500)
	email  =models.EmailField(max_length=50)
	date   =models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return '%s %s %s %s %s' % (self.name,self.phone,self.subject,self.message,self.email)

	class Meta:
		db_table="contact"


class Mobilecover(models.Model):
	company	   =models.CharField(max_length=500)
	mobilename =models.CharField(max_length=500)
	def __str__(self):
		return '%s' % (self.mobilename)

	class Meta:
		db_table="arrangementofcover"

#Static Homeback
class homepageimg(models.Model):
	name =models.CharField(max_length=100)
	img  =models.ImageField(upload_to='homepage_image',blank=False,null=False)

	def __str__(self):
		return '%s' % (self.name)
	class Meta:
		db_table="homepageimg"


#Homepage Cachy words
class homepageword(models.Model):
	name =models.CharField(max_length=100)
	info =models.CharField(max_length=100)

	def __str__(self):
		return '%s' % (self.name)
	class Meta:
		db_table="homepageword"

# Homepage Image
class homedesimage(models.Model):
	name =models.CharField(max_length=100)
	prod =models.ForeignKey(Products,on_delete=models.CASCADE)
	
	def __str__(self):
		return '%s' % (self.name)
	class Meta:
		db_table="homedesimage"



class orderawb(models.Model):
	awb          =models.CharField(max_length=100,blank=False,null=False)
	awb_order_id =models.CharField(max_length=10000,blank=False,null=False)
	placeorder_id=models.ForeignKey(placeorders,on_delete=models.CASCADE,blank=False,null=False)
	order_id	 =models.ForeignKey(Orders,on_delete=models.CASCADE,blank=False,null=False)
	def __str__(self):
		return '%s' % (self.awb)
	
	class Meta:
		db_table="orderawb"

class Pincode(models.Model):
	pincode=models.IntegerField(default=False,null=False)

	def __str__(self):
		return '%s' % (self.pincode)

	class Meta:
		db_table="pincode"


class headingtitle(models.Model):
	title    =models.CharField(max_length=100,blank=False,null=False)
	sub_title=models.CharField(max_length=100,blank=True,null=True)
	link     =models.CharField(max_length=100,blank=True,null=True)
	
	def __str__(self):
		return '%s' % (self.awb)
	
	class Meta:
		db_table="title"





