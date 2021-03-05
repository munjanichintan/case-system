from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from decimal import *

financetype_name_en_choice = (
		('partfinanced','Part-Financed'),
		('percentagefinanced','Percentage-Financed'),
		('fullyfinanced','Fully-Financed')
	)

financetype_name_de_choice = (
		('teilfinanzierung','Teilfinanzierung'),
		('prozentfinanzierung','Prozentfinanzierung'),
		('vollfinanzierung','Vollfinanzierung')
	)

state_name_choice = (
		('new','New'),
		('processing','Processing'),
		('waiting','Waiting'),
		('lawsuitfiled','Lawsuit Filed'),
		('won','Won'),
		('inactive','Inactive'),
		('lost','Lost'),

	)

category_name_en_choice = (
		('onlinecasino','Online-Casino'),
		('sportsbet','Sports-Bet'),
		('slotmachine','Slot-Machine')
	)
category_name_de_choice = (
		('onlinecasino','Online-Casino'),
		('sportwetten','Sportwetten'),
		('automaten','Automaten')
	)

country_name_en_choice = (
		('austria','Austria'),
		('germany','Germany'),
		('switzerland','Switzerland'),
	)

country_name_de_choice = (
		('osterreich','Österreich'),
		('deutschland','Deutschland'),
		('schweiz','Schweiz'),
	)

currency_name_choice = (
		('eur','EUR'),
		('usd','USD'),
		('chf','CHF'),
	)

user_type_name_choice = (
		('admin','ADMIN'),
		('user','USER'),
	)


def from_100():
    largest = Person.objects.all().order_by('person_id').last()
    if not largest:
        return 100
    return largest.person_id + 2


def from_200():
    largest = Lawyer.objects.all().order_by('lawyer_id').last()
    if not largest:
        return 200
    return largest.lawyer_id + 2    


def from_300():
    largest = Customer.objects.all().order_by('customer_id').last()
    if not largest:
        return 300
    return largest.customer_id + 2   


def from_400():
    largest = Case.objects.all().order_by('case_id').last()
    if not largest:
        return 400
    return largest.case_id + 2  


def from_10():
    largest = State.objects.all().order_by('state_id').last()
    if not largest:
        return 10
    return largest.state_id + 1 


def from_1000():
    largest = Currency.objects.all().order_by('currency_id').last()
    if not largest:
        return 1000
    return largest.currency_id + 1 


def from_user_100():
    largest = User.objects.all().order_by('user_id').last()
    if not largest:
        return 100
    return largest.user_id + 2   


def from_finance_10():
    largest = FinanceType.objects.all().order_by('financetype_id').last()
    if not largest:
        return 10
    return largest.financetype_id + 1     


def from_category_10():
    largest = Category.objects.all().order_by('category_id').last()
    if not largest:
        return 10
    return largest.category_id + 1   


def from_country_10():
    largest = Country.objects.all().order_by('country_id').last()
    if not largest:
        return 10
    return largest.country_id + 1   



class Earning_data(models.Model):
	TotalEarningOfAllCase = models.CharField(max_length=1500)
	TotalEarningsOfAllSportsBetsCases = models.CharField(max_length=1500)
	TotalEarningsOfAllSlotMachineCases = models.CharField(max_length=1500)
	TotalEarningsOfAllOnlineCasinoCases	= models.CharField(max_length=1500)
	TotalEarningsOfAllWonCases	= models.CharField(max_length=1500)
	TotalAmountWonOfAllWonCases	= models.CharField(max_length=1500)
	TotalEaringsOfAllLostCases	= models.CharField(max_length=1500)
	TotalClaimAmountOfAllFiledLawsuitsCases	= models.CharField(max_length=1500)
	TotalCustomerAmountLossOfAllProcessingCases	= models.CharField(max_length=1500)
	TotalClaimAmountOfAllProcessingCases	= models.CharField(max_length=1500)


class Person(models.Model):
	person_id = models.IntegerField(primary_key=True,default=from_100)
	first_name = models.CharField(max_length=100, null=False)
	last_name = models.CharField(max_length=100, null=False)
	telephone1 = PhoneNumberField(help_text='Contact phone number', null=False)
	telephone2 = PhoneNumberField(blank=True, help_text='Contact phone number2')
	email1 = models.EmailField(max_length = 254)
	email2 = models.EmailField(max_length = 254)
	street = models.CharField(max_length=255)
	town = models.CharField(max_length=255)
	postalcode = models.IntegerField(null=True)
	country = models.CharField(max_length=100, null=False)
	message = models.TextField(null=True)
	creation_date = models.DateTimeField(auto_now_add=True, null=False)
	changed_date = models.DateTimeField(auto_now_add=True, null=False)
	agree_condition = models.BooleanField(null=True)

	def __str__(self):
		return self.first_name


class Lawyer(models.Model):
	lawyer_id = models.IntegerField(primary_key=True,default=from_200)
	person_id = models.OneToOneField(Person,db_column="person_id",on_delete=models.CASCADE,null=True,blank=True)
	fees_per_hour = models.DecimalField(max_digits = 6, decimal_places = 2)
	fees_per_service = models.DecimalField(max_digits = 6, decimal_places = 2)
	creation_date = models.DateTimeField(auto_now_add=True, null=False)
	changed_date = models.DateTimeField(auto_now_add=True, null=False)
	comment = models.CharField(max_length=1000, null=True)

	def __str__(self):
		return str (self.lawyer_id) 


class Customer(models.Model):
	customer_id = models.IntegerField(primary_key=True,default=from_300)
	person_id = models.OneToOneField(Person,db_column="person_id",on_delete=models.CASCADE)
	creation_date = models.DateTimeField(auto_now_add=True, null=False)
	changed_date = models.DateTimeField(auto_now_add=True, null=False)
	comment = models.CharField(max_length=1000, null=True)

	def __str__(self):
		return str (self.customer_id)


class FinanceType(models.Model):
	financetype_id = models.IntegerField(primary_key=True,default=from_finance_10)
	financetype_name_en = models.CharField(max_length=255, choices=financetype_name_en_choice)
	financetype_name_de = models.CharField(max_length=255, choices=financetype_name_de_choice)
	creation_date = models.DateTimeField(auto_now_add=True)
	changed_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.financetype_name_en


class State(models.Model):
	state_id = models.IntegerField(primary_key=True,default=from_10,validators=[MinValueValidator(10),
                                       MaxValueValidator(17)])
	state_name = models.CharField(max_length=100, choices=state_name_choice)

	def __str__(self):
		return self.state_name


class User(AbstractUser):
	# user_id = models.IntegerField(primary_key=True,default=from_user_100, null=True)
	# person_id = models.OneToOneField(Person,db_column="person_id",on_delete=models.CASCADE, null=True)
	user_type = models.CharField(max_length=100,choices=user_type_name_choice,default="admin")
	username = models.CharField(max_length=100, null=False, unique=True)
	password = models.CharField(max_length=100, null=False)
	creation_date = models.DateTimeField(auto_now_add=True, null=False)
	changed_date = models.DateTimeField(auto_now_add=True, null=False)


class Category(models.Model):
	category_id = models.IntegerField(primary_key=True,default=from_category_10)
	category_name_en = models.CharField(max_length=255, choices=category_name_en_choice)
	category_name_de = models.CharField(max_length=255,choices=category_name_de_choice)
	creation_date = models.DateTimeField(auto_now_add=True, null=False)
	changed_date = models.DateTimeField(auto_now_add=True, null=False)

	def __str__(self):
		return self.category_name_en



class Country(models.Model):
	country_id = models.IntegerField(primary_key=True,default=from_country_10)
	country_name_en = models.CharField(max_length=255, choices=country_name_en_choice)
	country_name_de = models.CharField(max_length=255, choices=country_name_de_choice)
	creation_date = models.DateTimeField(auto_now_add=True, null=True)
	changed_date = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.country_name_en



class Currency(models.Model):
	currency_id = models.IntegerField(primary_key=True,default=from_1000)
	currency_name = models.CharField(max_length=100, null=False)
	currency_short = models.CharField(max_length=100,choices=currency_name_choice,null=False)
	currency_symbol = models.CharField(max_length=100)
	country_id = models.ForeignKey(Country,db_column="country_id",on_delete=models.CASCADE)

	def __str__(self):
		return self.currency_short


class Case(models.Model):
	case_id = models.IntegerField(primary_key=True,default=from_400)
	customer_id = models.ForeignKey(Customer,db_column="customer_id",on_delete=models.CASCADE, null=False)
	creation_date = models.DateTimeField(auto_now_add=True, null=False)
	changed_date = models.DateTimeField(auto_now_add=True, null=False)
	financetype_id = models.ForeignKey(FinanceType,db_column="financetype_id",on_delete=models.CASCADE,blank=True, null=True)
	country_id = models.ForeignKey(Country,db_column="country_id",on_delete=models.CASCADE,blank=True, null=True)
	category_id = models.ForeignKey(Category,db_column="category_id",on_delete=models.CASCADE,blank=True, null=True)
	customer_amount_lost = models.DecimalField(max_digits = 10, decimal_places = 2,default=Decimal('0.00'))
	currency_id = models.ForeignKey(Currency,db_column="currency_id",on_delete=models.CASCADE, null=True)
	case_amount_claim = models.DecimalField(max_digits = 10, decimal_places = 2,null=True,blank=True,default=Decimal('0.00'))
	case_amount_won = models.DecimalField(max_digits = 10, decimal_places = 2,null=True,blank=True,default=Decimal('0.00'))
	case_amount_lost = models.DecimalField(max_digits = 10, decimal_places = 2,null=True,blank=True,default=Decimal('0.00'))
	lawyer_fees = models.DecimalField(max_digits = 10, decimal_places = 2,null=True,blank=True,default=Decimal('0.00'))
	court_fees = models.DecimalField(max_digits = 10, decimal_places = 2,null=True,blank=True,default=Decimal('0.00'))
	other_fees = models.DecimalField(max_digits = 10, decimal_places = 2,null=True,blank=True,default=Decimal('0.00'))
	earnings_from_claim = models.DecimalField(max_digits = 10, decimal_places = 2,null=True,blank=True,default=Decimal('0.00'))
	money_earned_netto = models.DecimalField(max_digits = 10, decimal_places = 2,null=True,blank=True,default=Decimal('0.00'))
	customer_loss_evidence = models.BooleanField()
	customer_signed_contract = models.BooleanField()
	lawyer_sent_letter_to_vendor = models.BooleanField()
	fee_paid_to_lawyer = models.BooleanField()
	state_id = models.ForeignKey(State,db_column="state_id",on_delete=models.CASCADE, default="new", null=True)
	lawyer_assigned = models.BooleanField()
	lawyer_id = models.ForeignKey(Lawyer,db_column="lawyer_id",on_delete=models.CASCADE,null=True)
	lawsuit_has_been_filed = models.BooleanField()
	lawsuit_won = models.BooleanField()
	comment = models.CharField(max_length=1000, null=True)
	customer_wants_financing = models.BooleanField()
	is_customer_already 	 = models.BooleanField()
	customer_played_where	 = models.CharField (max_length=300, null=True)
	customer_lost_amounttxt	 = models.CharField (max_length=200, null=True)
	customer_message	 = models.CharField (max_length=1000, null=True)

	def __str__(self):
		return str (self.case_id)