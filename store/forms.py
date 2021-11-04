from django import forms
from store.models import *
# from bootstrap_datepicker_plus import DatePickerInput
from datetime import datetime
class CartForm(forms.ModelForm):
	class Meta:
		model=Carts
		fields="__all__"

class ProductForm(forms.ModelForm):
	class Meta:
		model=Products
		fields="__all__"
		exclude=('tshirt',)

class ImageForm(forms.ModelForm):
	class Meta:
		model=imagesupload
		fields="__all__"

class DesiArmyForm(forms.ModelForm):
	class Meta:
		model=desiarmy
		fields="__all__"
		exclude=()


class CouponForm(forms.ModelForm):
	class Meta:
		model=Coupon
		fields="__all__"

class ContactForm(forms.ModelForm):
	class Meta:
		model=Contact
		fields="__all__"


class placeorderForm(forms.ModelForm):
	class Meta:
		model=placeorders
		fields="__all__"

class ReviewForm(forms.ModelForm):
	class Meta:
		model=Review
		fields="__all__"

class HomeForm(forms.ModelForm):
	class Meta:
		model=homepageimg
		fields="__all__"

class MobileForm(forms.ModelForm):
	company   =forms.ModelChoiceField(queryset=Products.objects.values_list('company',flat=True).filter(category='MOBILE').distinct(), empty_label=None)
	mobilename=forms.ModelChoiceField(queryset=Products.objects.values_list('model_No',flat=True).filter(category='MOBILE').distinct(), empty_label=None)

	class Meta:
		model=Mobilecover
		fields="__all__"

	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	self.fields['mobilename'].queryset = Products.objects.none()


class TshirtForm(forms.ModelForm):
	class Meta:
		model=Tshirtsize
		fields="__all__"

class PincodeForm(forms.ModelForm):
	class Meta:
		model=Pincode
		fields="__all__"


class TitleForm(forms.ModelForm):
	mobilename=forms.ModelChoiceField(queryset=Products.objects.values_list('model_No',flat=True).distinct(),empty_label=None)
	company   =forms.ModelChoiceField(queryset=Products.objects.values_list('company',flat=True).distinct(),empty_label=None)

	class Meta:
		model =headingtitle
		fields="__all__"
		
class HomepagewordForm(forms.ModelForm):
	class Meta:
		model=homepageword
		fields='__all__'
		