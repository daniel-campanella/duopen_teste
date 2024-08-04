from django.db import models


class Account(models.Model):
	id = models.CharField(max_length=40, primary_key=True)
	tipo = models.CharField(max_length=50)
	subtype = models.CharField(max_length=20)
	number = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	balance = models.FloatField()
	currencyCode = models.CharField(max_length=6)
	marketingName = models.CharField(max_length=100, blank=True, null=True)
	owner = models.CharField(max_length=100, blank=True, null=True)
	taxNumber = models.CharField(max_length=50, blank=True, null=True)
	age = models.BigIntegerField(blank=True, null=True)

	def __str__(self):
		return(f"{self.id}")


class Transaction(models.Model):
	id = models.CharField(max_length=40, primary_key=True)
	accountId = models.CharField(max_length=40)
	date = models.DateTimeField()
	tipo = models.CharField(max_length=20)
	description = models.TextField()
	descriptionRaw = models.TextField(blank=True, null=True)
	currencyCode = models.CharField(max_length=6)
	amount = models.FloatField()
	balance = models.FloatField(blank=True, null=True)
	amountInAccountCurrency = models.FloatField(blank=True, null=True)
	category = models.TextField(blank=True, null=True)
	categoryId = models.BigIntegerField(blank=True, null=True)
	providerCode = models.CharField(max_length=50, blank=True, null=True)
	status = models.CharField(max_length=50)

	def __str__(self):
		return(f"{self.id}")


class Merchant(models.Model):
	transactionId = models.CharField(max_length=40, primary_key=True)
	name = models.CharField(max_length=200,blank=True, null=True)
	businessName = models.CharField(max_length=200,blank=True, null=True)
	cnpj = models.CharField(max_length=20,blank=True, null=True)
	cnae = models.CharField(max_length=20,blank=True, null=True)
	category = models.CharField(max_length=200,blank=True, null=True)

	def __str__(self):
		return(f"{self.transactionId}")


class CreditCardMetaData(models.Model):
	transactionId = models.CharField(max_length=40, primary_key=True)
	installmentNumber = models.BigIntegerField(blank=True, null=True)
	totalInstallments = models.BigIntegerField(blank=True, null=True)
	totalAmount = models.FloatField(blank=True, null=True)
	payeeMCC = models.BigIntegerField(blank=True, null=True)
	cardNumber = models.CharField(max_length=60,blank=True, null=True)
	billId = models.CharField(max_length=40,blank=True, null=True)
	
	def __str__(self):
		return(f"{self.transactionId}")

