from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.serializers import serialize, deserialize
from .models import Account, Transaction, Merchant, CreditCardMetaData
from . import pluggyUtil


def home(request):
	return render(request, 'home.html', {})


def search(request):
	# Check to see if it's searching
	if request.method == 'POST':
		cpf = request.POST['cpf']
		age = request.POST['age']

		accounts = Account.objects.filter(taxNumber=cpf)
		if not accounts:
			messages.success(request, f"No transactions with the CPF [{cpf}] were found!")
			return redirect('search')
		else:
			transactions = []
			merchants = []
			creditcards = []
			accountsIDs = []
			count = 0
			for acct in accounts:
				acct.age = age
				acct.save()
				txn = Transaction.objects.filter(accountId=acct.id).values_list('id', flat=True)
				if txn:
					count = count + txn.count()
					transactions.extend(txn)
					for transaction in txn:
						mcc = Merchant.objects.filter(transactionId=transaction).values_list('transactionId', flat=True)
						if mcc:
							merchants.extend(mcc)
						cc = CreditCardMetaData.objects.filter(transactionId=transaction).values_list('transactionId', flat=True)
						if cc:
							creditcards.extend(cc)
			
			request.session['txn'] = list(transactions)
			request.session['mcc'] = list(merchants)
			request.session['cc'] = list(creditcards)
			request.session['search_trigger'] = True
			messages.success(request, f"{count} transactions were found for the CPF [{cpf}]!")
			return redirect('transactions')
	else:
		return render(request, 'search.html', {})


def show_accounts(request):
	accounts = Account.objects.all()
	# Check to see if it's refreshing
	if request.method == 'POST':
		api_key = pluggyUtil.createAPIKey()
		if api_key != None:
			accountList = pluggyUtil.listAccounts(api_key)
			if accountList != None:
				for acct in accountList:
					account, created = Account.objects.update_or_create(
						id=acct['id'],
						defaults={
							'tipo': acct.get('type', None),
							'subtype': acct.get('subtype', None),
							'owner': acct.get('owner', None),
							'taxNumber': acct.get('taxNumber', None),
							'number': acct.get('number', None),
							'name': acct.get('name', None),
							'marketingName': acct.get('marketingName', None),
							'balance': acct.get('balance', None),
							'currencyCode': acct.get('currencyCode', None)
						}
					)
			else:
				messages.success(request, "ERROR: Could not retrieve list of accounts from Pluggy API!")
				return redirect('accounts')
		else:
			messages.success(request, "ERROR: Could not create an API Key from Pluggy API!")
			return redirect('accounts')
		# SUCCESSFULLY RETRIEVED ACCOUNTS
		messages.success(request, "SUCCESS: All accounts were retrived from Pluggy API!")
		return redirect('accounts')
	else:
		return render(request, 'accounts.html', {'accounts':accounts})


def show_transactions(request):
	if 'search_trigger' in request.session:
		del request.session['search_trigger']
		transactions = Transaction.objects.filter(id__in=request.session.get('txn', None))
		merchants = Merchant.objects.filter(transactionId__in=request.session.get('mcc', None))
		creditcards = CreditCardMetaData.objects.filter(transactionId__in=request.session.get('cc', None))

		del request.session['txn']
		del request.session['mcc']
		del request.session['cc']
	else:
		transactions = Transaction.objects.all()
		merchants = Merchant.objects.all()
		creditcards = CreditCardMetaData.objects.all()

	#messages.success(request, f"txn[{type(transactions)}] | mcc[{type(merchants)}] | cc[{type(creditcards)}]")
	if request.method == 'POST':
		api_key = pluggyUtil.createAPIKey()
		if api_key != None:
			accountList = pluggyUtil.listAccounts(api_key)
			if accountList != None:
				for acct in accountList:
					transactionList = pluggyUtil.listTransactions(api_key,acct.get('id', None))
					if transactionList != None:
						for txn in transactionList:
							transaction, created_txn = Transaction.objects.update_or_create(
								id=txn.get('id', None),
								defaults={
									'date': txn.get('date', None),
									'tipo': txn.get('type', None),
									'description': txn.get('description', None),
									'descriptionRaw': txn.get('descriptionRaw', None),
									'currencyCode': txn.get('currencyCode', None),
									'amount': txn.get('amount', None),
									'balance': txn.get('balance', None),
									'amountInAccountCurrency': txn.get('amountInAccountCurrency', None),
									'category': txn.get('category', None),
									'categoryId': txn.get('categoryId', None),
									'providerCode': txn.get('providerCode', None),
									'status': txn.get('status', None),
									'accountId': txn.get('accountId', None)
								}
							)

							if txn['merchant'] != None:
								mcc = txn['merchant']
								merchant, created_mcc = Merchant.objects.update_or_create(
									transactionId=txn.get('id', None),
									defaults={
										'name': mcc.get('name', None),
										'businessName': mcc.get('businessName', None),
										'cnpj': mcc.get('cnpj', None),
										'cnae': mcc.get('cnae', None),
										'category': mcc.get('category', None)
									}
								)

							if txn['creditCardMetadata'] != None:
								cc = txn['creditCardMetadata']
								creditcard, created_cc = CreditCardMetaData.objects.update_or_create(
									transactionId=txn.get('id', None),
									defaults={
										'installmentNumber': cc.get('installmentNumber', None),
										'totalInstallments': cc.get('totalInstallments', None),
										'totalAmount': cc.get('totalAmount', None),
										'payeeMCC': cc.get('payeeMCC', None),
										'cardNumber': cc.get('cardNumber', None),
										'billId': cc.get('billId', None)
									}
								)
					else:
						messages.success(request, f"ERROR: Could not retrieve list of transactions from Pluggy API! ID:{acct.get('id', None)}")
						return redirect('transactions')
			else:
				messages.success(request, "ERROR: Could not retrieve list of accounts from Pluggy API!")
				return redirect('transactions')
		else:
			messages.success(request, "ERROR: Could not create an API Key from Pluggy API!")
			return redirect('transactions')
		# SUCCESSFULLY RETRIEVED ACCOUNTS
		messages.success(request, "SUCCESS: All transactions were retrived from Pluggy API!")
		return redirect('transactions')
	else:
		return render(request, 'transactions.html', {'transactions':transactions,'merchants':merchants,'creditcards':creditcards})


def terms_and_conditions(request):
	return render(request, 'terms_and_conditions.html', {})
