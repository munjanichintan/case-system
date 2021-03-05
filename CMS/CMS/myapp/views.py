from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from decimal import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import xlwt
import datetime
from django.http import HttpResponse
from forex_python.converter import CurrencyRates 
from sqlalchemy import Table, Column, Float, Integer, String, MetaData, ForeignKey
from datetime import datetime, timezone,date
from django.core.paginator import Paginator

# Create your views here.
def person(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        telephone1 = request.POST.get('telephone1')
        telephone2 = request.POST.get('telephone2')
        email1 = request.POST.get('email1')
        email2 = request.POST.get('email2')
        street = request.POST.get('street')
        town = request.POST.get('town')
        postalcode = request.POST.get('postalcode')
        country = request.POST.get('country')
        message = request.POST.get('message')
        creation_date = request.POST.get('creation_date')
        changed_date = request.POST.get('changed_date')
        agree_condition = request.POST.get('agree_condition')

        data = Person.objects.filter(first_name=first_name).exists()
        if data:
            messages.warning(request,"USERNAME ALREADY EXISTS")
            return render(request, 'myapp/person.html')
        person = Person(first_name=first_name, last_name=last_name, telephone1=telephone1, telephone2=telephone2,
                        email1=email1, email2=email2, street=street, town=town, postalcode=postalcode, country=country, message=message,
                        creation_date=creation_date, changed_date=changed_date, agree_condition=agree_condition)
        person.save()
        # subject = "Person Detail"  
        # msg     = f"First Name : {first_name} \n Last_Name : {last_name} \n Telephone Number : {telephone1,telephone2} \n Email Address : {email1,email2} \n Street : {street} \n Town : {town} \n PostalCode : {postalcode} \n Country : {country} \n Creation Date : {creation_date} \n Change Date : {changed_date} \n Agree Condition : {agree_condition}"
        # res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [email1])
        # return render(request, 'myapp/person.html')
        return redirect("casedetailpage")
    return render(request, 'myapp/person.html')


def persondetail(request):
    person = Person.objects.all()
    return render(request, 'myapp/persondetail.html', {'person':person})


def customer(request):
    if request.method == "POST":
        person_id = Person.objects.latest('person_id')
        comment = request.POST.get('comment')
        customer = Customer(person_id=person_id,comment=comment)
        customer.save()
        return redirect('case')
    return render(request, 'myapp/customer.html')


def case(request):
    if request.method == "POST":
        # customer_id = Customer.objects.latest('customer_id')
        lawyer_id = request.POST.get('lawyer_id')
        customer_name = request.POST.get('customer_name')
        creation_date = request.POST.get('creation_date')
        changed_date = request.POST.get('changed_date')
        financetype_id = request.POST.get('financetype_id')
        country_id = request.POST.get('country_id')
        category_id = request.POST.get('category_id')
        customer_amount_lost = request.POST.get('customer_amount_lost')
        customer_amount_lost=Decimal(customer_amount_lost)
        currency_id = request.POST.get('currency_id')
        case_amount_claim = request.POST.get('case_amount_claim')
        if case_amount_claim:
            pass
        else:
            case_amount_claim=Decimal('0.00')    

    
        case_amount_won = request.POST.get('case_amount_won')
        if case_amount_won:
            pass
        else:
            case_amount_won=Decimal('0.00')    

       
        case_amount_lost = request.POST.get('case_amount_lost')
        if case_amount_lost:
            pass
        else:
            case_amount_lost=Decimal('0.00')    
 
        lawyer_fees = request.POST.get('lawyer_fees')
        if lawyer_fees:
            pass
        else:
            lawyer_fees=Decimal('0.00')    
 
        court_fees = request.POST.get('court_fees')
        if court_fees:
            pass
        else:
            court_fees=Decimal('0.00')    
        
        other_fees = request.POST.get('other_fees')
        if other_fees:
            pass
        else:
            other_fees=Decimal('0.00')    
        
        earnings_from_claim = request.POST.get('earnings_from_claim')
        if earnings_from_claim:
            pass
        else:
            earnings_from_claim=Decimal('0.00')    
      
        money_earned_netto = request.POST.get('money_earned_netto')
        if money_earned_netto:
            pass
        else:
            money_earned_netto=Decimal('0.00')    
      
        customer_loss_evidence = request.POST.get('customer_loss_evidence')
        customer_signed_contract = request.POST.get('customer_signed_contract')
        lawyer_sent_letter_to_vendor = request.POST.get('lawyer_sent_letter_to_vendor')
        fee_paid_to_lawyer = request.POST.get('fee_paid_to_lawyer')
        state_id = request.POST.get('state_id')
        lawyer_assigned = request.POST.get('lawyer_assigned')
        lawsuit_has_been_filed = request.POST.get('lawsuit_has_been_filed')
        lawsuit_won = request.POST.get('lawsuit_won')
        comment = request.POST.get('comment')
        customer_wants_financing = request.POST.get('customer_wants_financing')
        is_customer_already = request.POST.get('is_customer_already')
        customer_played_where = request.POST.get('customer_played_where')
        customer_lost_amounttxt = request.POST.get('customer_lost_amounttxt')   
        customer_message = request.POST.get('customer_message')

        try:
            lawyer_data = Lawyer.objects.get(lawyer_id = lawyer_id)
            case_data = Case.objects.filter(lawyer_id=lawyer_data).exists()
            if case_data:
                messages.error(request,"Lawyer assigned! plz Choose Another")
                lawyer = Lawyer.objects.all()  
                customer = Customer.objects.all()
                return render(request, 'myapp/case.html',{'lawyer':lawyer,'customer':customer})
            else:
                lawyer_data = Lawyer.objects.get(lawyer_id = lawyer_id)
        except:
               lawyer_data = None;          
        
        try:
            person = Person.objects.get(first_name=customer_name)
        except:
            messages.error(request,"Plz Fill Up Person")
            lawyer = Lawyer.objects.all()  
            print("lawyer",lawyer) 
            customer = Customer.objects.all()
            return render(request, 'myapp/case.html',{'lawyer':lawyer,'customer':customer})


        customer_data = Customer.objects.get(person_id = person)
        fin_data = FinanceType.objects.get(financetype_name_en=financetype_id)
        country_data = Country.objects.get(country_name_en=country_id)
        category_data = Category.objects.get(category_name_en=category_id)
        currency_data = Currency.objects.get(currency_short=currency_id)
        state_name = State.objects.get(state_name=state_id)
        # state_data =State.objects.latest('state_id')

        
        case = Case(customer_id=customer_data,lawyer_id=lawyer_data,creation_date=creation_date,changed_date=changed_date,financetype_id=fin_data,country_id=country_data,category_id=category_data,customer_amount_lost=customer_amount_lost,currency_id=currency_data,case_amount_claim=case_amount_claim,case_amount_won=case_amount_won,case_amount_lost=case_amount_lost,lawyer_fees=lawyer_fees,court_fees=court_fees,other_fees=other_fees,earnings_from_claim=earnings_from_claim,money_earned_netto=money_earned_netto,customer_loss_evidence=customer_loss_evidence,customer_signed_contract=customer_signed_contract,lawyer_sent_letter_to_vendor=lawyer_sent_letter_to_vendor,fee_paid_to_lawyer=fee_paid_to_lawyer,state_id=state_name,lawyer_assigned=lawyer_assigned,lawsuit_has_been_filed=lawsuit_has_been_filed,lawsuit_won=lawsuit_won,comment=comment,customer_wants_financing=customer_wants_financing,is_customer_already=is_customer_already,customer_played_where=customer_played_where,customer_lost_amounttxt=customer_lost_amounttxt,customer_message=customer_message)
        case.save()
        if customer_loss_evidence == 'True' and customer_signed_contract == 'True' and lawyer_sent_letter_to_vendor == 'True' and fee_paid_to_lawyer == 'True' and  lawyer_assigned== 'True':

            data = Case.objects.get(customer_id=customer_data)
            state = State.objects.get(state_name="waiting")
            data.state_id = state
            data.save()

        elif lawsuit_has_been_filed == 'True':

            data = Case.objects.get(customer_id=customer_data)
            state = State.objects.get(state_name="lawsuitfiled")
            data.state_id = state
            data.save()

        elif lawsuit_won == 'True':

          data = Case.objects.get(customer_id=customer_data)
          state = State.objects.get(state_name="won")
          data.state_id = state
          data.save()

        return redirect("casedetailpage")

    lawyer = Lawyer.objects.all()  
    print("lawyer",lawyer) 
    customer = Customer.objects.all()
    
    return render(request, 'myapp/case.html',{'lawyer':lawyer,'customer':customer})


def case_detail_page(request):
    case = Case.objects.all().order_by('-case_id')
    paginator = Paginator(case,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'myapp/case_detail_page.html', {'page_obj':page_obj})   


def case_detail_page_edit(request, case_id):
    case = Case.objects.get(case_id=case_id)
    finance = FinanceType.objects.all()
    country = Country.objects.all()
    category = Category.objects.all()
    currency = Currency.objects.all()
    print(case.financetype_id.financetype_name_en)
    print(case.currency_id)
    lawyer = Lawyer.objects.all()
    state=State.objects.all()
    print(state)
    return render(request, 'myapp/case_detail_page_update.html', {'case':case,'finance':finance,'country':country,'category':category,'currency':currency,'lawyer':lawyer,'state':state})


def case_update(request, case_id):
    if request.method == "POST":
        customer_id = request.POST.get('customer_id')
        creation_date = request.POST.get('creation_date')
        changed_date = request.POST.get('changed_date')
        financetype_id = request.POST.get('financetype_id')
        country_id = request.POST.get('country_id')
        category_id = request.POST.get('category_id')
        customer_amount_lost = request.POST.get('customer_amount_lost')
        if customer_amount_lost:
            pass
        else:
            customer_amount_lost=Decimal('0.00')    
        currency_id = request.POST.get('currency_id')
        currency_name = request.POST.get('currency_name')
        currency_symbol = request.POST.get('currency_symbol')
        case_amount_claim = request.POST.get('case_amount_claim')
        state_name1 = request.POST.get('state_name1')
        print("abhishek is",state_name1)
        if case_amount_claim:
            pass
        else:
            case_amount_claim=Decimal('0.00')

        case_amount_won = request.POST.get('case_amount_won')
        if case_amount_won:
            pass
        else:
            case_amount_won=Decimal('0.00')
        case_amount_lost = request.POST.get('case_amount_lost')
        if case_amount_lost:
            pass
        else:
            case_amount_lost=Decimal('0.00')
        lawyer_fees = request.POST.get('lawyer_fees')
        if lawyer_fees:
            pass
        else:
            lawyer_fees=Decimal('0.00')
        court_fees = request.POST.get('court_fees')
        if court_fees:
            pass
        else:
            court_fees=Decimal('0.00')
        other_fees = request.POST.get('other_fees')
        if other_fees:
            pass
        else:
            other_fees=Decimal('0.00')
        earnings_from_claim = request.POST.get('earnings_from_claim')
        if earnings_from_claim:
            pass
        else:
            earnings_from_claim=Decimal('0.00')
        money_earned_netto = request.POST.get('money_earned_netto')
        if money_earned_netto:
            pass
        else:
            money_earned_netto=Decimal('0.00')
        customer_loss_evidence = request.POST.get('customer_loss_evidence')
        customer_signed_contract = request.POST.get('customer_signed_contract')
        lawyer_sent_letter_to_vendor = request.POST.get('lawyer_sent_letter_to_vendor')
        fee_paid_to_lawyer = request.POST.get('fee_paid_to_lawyer')
        lawyer_assigned = request.POST.get('lawyer_assigned')
        print("lawyer_assigned",lawyer_assigned)

        state_id = request.POST.get('state_id')
        lawyer_assigned = request.POST.get('lawyer_assigned')
        lawyer_id = request.POST.get('lawyer_id')
        if lawyer_id:
            pass
        else:
            lawyer_id = None;   

        print("dsfgdsgvfds",lawyer_id) 

        lawsuit_has_been_filed = request.POST.get('lawsuit_has_been_filed')
        lawsuit_won = request.POST.get('lawsuit_won')
        comment = request.POST.get('comment')
        customer_wants_financing = request.POST.get('customer_wants_financing')
        is_customer_already = request.POST.get('is_customer_already')
        customer_played_where = request.POST.get('customer_played_where')
        customer_lost_amounttxt = request.POST.get('customer_lost_amounttxt')   
        customer_message = request.POST.get('customer_message')
        try:
            lawyer_data = Lawyer.objects.get(lawyer_id = lawyer_id)
            case_data = Case.objects.filter(lawyer_id=lawyer_data).exists()
            if case_data:
                case_data1 = Case.objects.filter(case_id=case_id,lawyer_id=lawyer_data).exists()
                if case_data1:
                    pass
                else:
                    messages.error(request,"Lawyer assigned! plz Choose Another")
                    lawyer = Lawyer.objects.all()
                    customer = Customer.objects.all()
                    return redirect(case_detail_page_edit,case_id=case_id)
                # return render(request, 'myapp/case_detail_page_update.html',{'lawyer':lawyer,'customer':customer})
            else:
                lawyer_data = Lawyer.objects.get(lawyer_id = lawyer_id)
        except:
               lawyer_data = None;          


       

        try:
            data = Case.objects.get(case_id=case_id)
            state = State.objects.get(state_name=state_id)
            print("before",state.state_name)
            if state.state_name == "new":
                pass
            if state.state_name == "processing":
                pass
            if state.state_name == "inactive":
                pass
            if state.state_name == "lost":
                pass    

            data.state_id = state
            data.save()

        except:
            if state_name1 == 'won':
                state_name = State.objects.get(state_name="won")
                data = Case.objects.get(case_id=case_id)
                data.state_id = state_name
                data.save()
            if state_name1 == "lawsuitfiled":
                state_name = State.objects.get(state_name="lawsuitfiled")
                data = Case.objects.get(case_id=case_id)
                data.state_id = state_name
                data.save()
            if state_name1 == "waiting":
                state_name = State.objects.get(state_name="waiting")
                data = Case.objects.get(case_id=case_id)
                data.state_id = state_name
                data.save()
                

        Case.objects.filter(case_id=case_id).update(financetype_id=financetype_id,country_id=country_id,category_id=category_id,customer_amount_lost=customer_amount_lost,currency_id=currency_id,case_amount_claim=case_amount_claim,case_amount_won=case_amount_won,case_amount_lost=case_amount_lost,lawyer_fees=lawyer_fees,court_fees=court_fees,other_fees=other_fees,earnings_from_claim=earnings_from_claim,money_earned_netto=money_earned_netto,customer_loss_evidence=customer_loss_evidence,customer_signed_contract=customer_signed_contract,lawyer_sent_letter_to_vendor=lawyer_sent_letter_to_vendor,fee_paid_to_lawyer=fee_paid_to_lawyer,lawyer_assigned=lawyer_assigned,lawsuit_has_been_filed=lawsuit_has_been_filed,lawsuit_won=lawsuit_won,comment=comment,customer_wants_financing=customer_wants_financing,is_customer_already=is_customer_already,customer_played_where=customer_played_where,customer_lost_amounttxt=customer_lost_amounttxt,customer_message=customer_message,lawyer_id=lawyer_data)


        if customer_loss_evidence == 'True' and customer_signed_contract == 'True' and lawyer_sent_letter_to_vendor == 'True' and fee_paid_to_lawyer == 'True' and  lawyer_assigned == 'True':

                data = Case.objects.get(case_id=case_id)
                state = State.objects.get(state_name="waiting")
                data.state_id = state
                data.save()

        elif lawsuit_has_been_filed == 'True':
                data = Case.objects.get(case_id=case_id)
                state = State.objects.get(state_name="lawsuitfiled")
                data.state_id = state
                data.save()

        elif lawsuit_won == 'True':
              data = Case.objects.get(case_id=case_id)
              state = State.objects.get(state_name="won")
              data.state_id = state
              data.save()

        return redirect("casedetailpage")
    return render(request, 'myapp/case_detail_page_update.html')


def customer_list(request,data_object):
    data=Person.objects.filter(first_name=data_object)
    return render(request,'myapp/customer_detail.html',{'data':data})


def lawyerform(request):
    if request.method == "POST":
        person = request.POST.get('person')
        fees_per_hour = request.POST.get('fees_per_hour')
        fees_per_service = request.POST.get('fees_per_service')
        if len(fees_per_service) == 0  and len(fees_per_hour) == 0:
            messages.error(request,"Form FillUp Correctly")
            data=Person.objects.all()
            return render(request,'myapp/lawyerform.html',{'data':data})

        fees_per_hour=Decimal(fees_per_hour)
        fees_per_service = request.POST.get('fees_per_service')
        fees_per_service=Decimal(fees_per_service)
        comment = request.POST.get('comment')
        try:
            person_data = Person.objects.get(first_name=person)
        except Exception as e:
            messages.error(request,"Form FillUp Correctly")  
            data=Person.objects.all()
            return render(request,'myapp/lawyerform.html',{'data':data})  
        else:
            lawyerdata = Lawyer.objects.filter(person_id=person_data).exists()
            if lawyerdata:
                messages.error(request,"Lawyer Already Exist")
                data=Person.objects.all()
                return render(request,'myapp/lawyerform.html',{'data':data})
            else:
                data=Lawyer(person_id=person_data,fees_per_hour=fees_per_hour,fees_per_service=fees_per_service,comment=comment)
                data.save()
        messages.success(request,"SuccessFully created")    
        return redirect(case_detail_page)
    else:
        data=Person.objects.all()
        return render(request,'myapp/lawyerform.html',{'data':data})    


def customerform(request):
    if request.method == "POST":
        person = request.POST.get('person')
        comment = request.POST.get('comment')
        try:
            persondata=Person.objects.get(first_name=person)
        except:
            messages.error(request,"Form FillUp Correctly")  
            data=Person.objects.all()
            return render(request,'myapp/customerform.html',{'data':data})  

        else:   
            customerdata = Customer.objects.filter(person_id=persondata).exists()
            if customerdata:
                data=Person.objects.all()
                messages.error(request,"Customer Already Exist")
                return render(request,'myapp/customerform.html',{'data':data})    
            else:     
                data = Customer(person_id=persondata,comment=comment)
                data.save()
        return redirect(case_detail_page) 
    else:
        data=Person.objects.all()
        return render(request,'myapp/customerform.html',{'data':data})        


def state(request):
    if request.method == "POST":
        state_name = request.POST.get('state_name')
        state = State(state_name=state_name)
        state.save()
        return redirect('case')
    return render(request, 'myapp/state.html')


def case_full_detail(request,case_id):
    data = Case.objects.get(case_id=case_id)
    return render(request,'myapp/case_full_detail.html',{'data':data})


def customer_full_detail(request,case_id):
    data = Case.objects.get(case_id=case_id)
    return render(request,'myapp/customer_full_detail.html',{'data':data})


def lawyer_full_detail(request,case_id):
    data = Case.objects.get(case_id=case_id)
    return render(request,'myapp/lawyer_full_detail.html',{'data':data})   


def all_lawyer(request):
    data = Lawyer.objects.all()
    return render(request,'myapp/all_lawyer.html',{'data':data})  


def all_customer(request):
    data = Customer.objects.all()
    return render(request,'myapp/all_customer.html',{'data':data}) 


def same_color(request,state_name):
    state_data = State.objects.filter(state_name=state_name)
    case_data = Case.objects.filter(state_id__in=state_data)
    return render(request,'myapp/same_color_case.html',{'case_data':case_data})


def excel(request):
    today_date = date.today()
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename="Case System' + str(today_date) + '.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('CMS') # this will make a sheet named Users Data
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    ws.write(row_num, 0, 'Person-Table', font_style)
    row_num = 1 
    columns = ['person_id', 'first_name', 'last_name','telephone1','telephone2','email1','email2','street','town','postalcode','country','creation_date','changed_date','agree_condition']
    # naive = dt.replace(tzinfo=None)
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows =  Person.objects.all().values_list('person_id','first_name','last_name','telephone1','telephone2','email1','email2','street','town','postalcode','country','creation_date','changed_date','agree_condition',) 
    
    rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime) else x for x in row] for row in rows ]
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    row_num += 2
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    ws.write(row_num, 0, 'Lawyer-Table', font_style)
    row_num += 1 
    col = ['lawyer_id', 'person_id', 'fees_per_hour','fees_per_service','creation_date','changed_date','comment']
    # naive = dt.replace(tzinfo=None)
    for col_num in range(len(col)):
        ws.write(row_num, col_num, col[col_num], font_style) # at 0 row 0 column 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Lawyer.objects.all().values_list('lawyer_id', 'person_id', 'fees_per_hour','fees_per_service','creation_date','changed_date','comment')
    
    rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime) else x for x in row] for row in rows ]
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)


    row_num += 2
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    ws.write(row_num, 0, 'Customer-Table', font_style)
    row_num += 1 
    col = ['customer_id', 'person_id','creation_date' ,'changed_date','comment']
    # naive = dt.replace(tzinfo=None)
    for col_num in range(len(col)):
        ws.write(row_num, col_num, col[col_num], font_style) # at 0 row 0 column 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Customer.objects.all().values_list('customer_id', 'person_id','creation_date' ,'changed_date','comment')
    rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime) else x for x in row] for row in rows ]
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)        



    row_num += 2
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    ws.write(row_num, 0, 'FinanceType-Table', font_style)
    row_num += 1 
    col = ['financetype_id', 'financetype_name_en', 'financetype_name_de','creation_date','changed_date']
    # naive = dt.replace(tzinfo=None)
    for col_num in range(len(col)):
        ws.write(row_num, col_num, col[col_num], font_style) # at 0 row 0 column 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = FinanceType.objects.all().values_list('financetype_id', 'financetype_name_en', 'financetype_name_de','creation_date','changed_date')
    rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime) else x for x in row] for row in rows ]
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)     

    row_num += 2
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    ws.write(row_num, 0, 'State-Table', font_style)
    row_num += 1 
    col = ['state_id', 'state_name']
    # naive = dt.replace(tzinfo=None)
    for col_num in range(len(col)):
        ws.write(row_num, col_num, col[col_num], font_style) # at 0 row 0 column 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = State.objects.all().values_list('state_id', 'state_name')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)                      
   
    row_num += 2
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    ws.write(row_num, 0, 'User-Table', font_style)
    row_num += 1 
    col = ['user_type','username','password','creation_date','changed_date']
    # naive = dt.replace(tzinfo=None)
    for col_num in range(len(col)):
        ws.write(row_num, col_num, col[col_num], font_style) # at 0 row 0 column 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = User.objects.all().values_list('user_type','username','password','creation_date','changed_date')
    rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime) else x for x in row] for row in rows ]
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)        


    
    row_num += 2
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    ws.write(row_num, 0, 'Category-Table', font_style)
    row_num += 1 
    col = ['category_id', 'category_name_en','category_name_de','creation_date','changed_date']
    # naive = dt.replace(tzinfo=None)
    for col_num in range(len(col)):
        ws.write(row_num, col_num, col[col_num], font_style) # at 0 row 0 column 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Category.objects.all().values_list('category_id', 'category_name_en','category_name_de','creation_date','changed_date')
    rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime) else x for x in row] for row in rows ]
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)        
  


    row_num += 2
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    ws.write(row_num, 0, 'Country-Table', font_style)
    row_num += 1 
    col = ['country_id', 'country_name_en','country_name_de','creation_date','changed_date']
    # naive = dt.replace(tzinfo=None)
    for col_num in range(len(col)):
        ws.write(row_num, col_num, col[col_num], font_style) # at 0 row 0 column 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Country.objects.all().values_list('country_id', 'country_name_en','country_name_de','creation_date','changed_date')
    rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime) else x for x in row] for row in rows ]
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)        
    


    row_num += 2
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    ws.write(row_num, 0, 'Currency-Table', font_style)
    row_num += 1 
    col = ['currency_id', 'currency_name','currency_short','currency_symbol','country_id']
    # naive = dt.replace(tzinfo=None)
    for col_num in range(len(col)):
        ws.write(row_num, col_num, col[col_num], font_style) # at 0 row 0 column 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Currency.objects.all().values_list('currency_id', 'currency_name','currency_short','currency_symbol','country_id')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style) 
 
    

    row_num += 2
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    ws.write(row_num, 0, 'Case-Table', font_style)
    row_num += 1 
    col = ['case_id', 'customer_id','financetype_id','country_id','category_id','customer_amount_lost','currency_id','case_amount_claim','case_amount_won','case_amount_lost','lawyer_fees','court_fees','other_fees','earnings_from_claim','money_earned_netto','customer_loss_evidence','customer_signed_contract','lawyer_sent_letter_to_vendor','fee_paid_to_lawyer','state_id','lawyer_assigned','lawyer_id','lawsuit_has_been_filed','lawsuit_won','comment','customer_wants_financing','is_customer_already','customer_played_where','customer_lost_amounttxt','customer_message']
    # naive = dt.replace(tzinfo=None)
    for col_num in range(len(col)):
        ws.write(row_num, col_num, col[col_num], font_style) # at 0 row 0 column 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Case.objects.all().values_list('case_id', 'customer_id','financetype_id','country_id','category_id','customer_amount_lost','currency_id','case_amount_claim','case_amount_won','case_amount_lost','lawyer_fees','court_fees','other_fees','earnings_from_claim','money_earned_netto','customer_loss_evidence','customer_signed_contract','lawyer_sent_letter_to_vendor','fee_paid_to_lawyer','state_id','lawyer_assigned','lawyer_id','lawsuit_has_been_filed','lawsuit_won','comment','customer_wants_financing','is_customer_already','customer_played_where','customer_lost_amounttxt','customer_message')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style) 
    wb.save(response)           
              
    return response


def Earning(request):
    data = Case.objects.all().order_by('case_id')
    sum = 0
    sum = Decimal(sum)
    for i in data:
        sum = sum + i.earnings_from_claim
        print(i.earnings_from_claim)
    
    c = CurrencyRates()
    Currency = c.get_rate('INR', 'EUR') 
    print(Currency)
    sum = Currency * int(sum)
    sum = round(sum,2)    
    print("Total Earning Of All Case",sum)   


    data1 = Case.objects.all().filter(category_id = 10)
    sum1 = 0
    sum1 = Decimal(sum1)
    for i in data1:
        sum1 = sum1 + i.earnings_from_claim
        print(i.earnings_from_claim)

    sum1 = Currency * int(sum1)
    sum1 = round(sum1,2)  

    print("Total Earnings of all Sports-Bets cases",sum1) 

    data2 = Case.objects.all().filter(category_id = 11)
    sum2 = 0
    sum2 = Decimal(sum2)
    for i in data2:
        sum2 = sum2 + i.earnings_from_claim
        print(i.earnings_from_claim)

    sum2 = Currency * int(sum2)
    sum2 = round(sum2,2)      
    print("Total Earnings of all Slot-Machine cases",sum2) 


    data3 = Case.objects.all().filter(category_id = 12)
    sum3 = 0
    sum3 = Decimal(sum3)
    for i in data3:
        sum3 = sum3 + i.earnings_from_claim
        print(i.earnings_from_claim)

    sum3 = Currency * int(sum3)
    sum3 = round(sum3,2)     
    print("Total Earnings of all Online-Casino cases",sum3) 

    data4 = Case.objects.all().filter(state_id = 14)
    sum4 = 0
    sum4 = Decimal(sum4)
    for i in data4:
        sum4 = sum4 + i.earnings_from_claim
        print(i.earnings_from_claim)

    sum4 = Currency * int(sum4)
    sum4 = round(sum4,2)    
    print("Total Earnings of all Won Cases ",sum4)

    data5 = Case.objects.all().filter(state_id = 14)
    sum5 = 0
    sum5 = Decimal(sum5)
    for i in data5:
        sum5 = sum5 + i.case_amount_won
        print(i.case_amount_won)

    sum5 = Currency * int(sum5)
    sum5 = round(sum5,2)      
    print("Total Amount Won of all Won Cases",sum5)  


    data6 = Case.objects.all().filter(state_id = 16)
    sum6 = 0
    sum6 = Decimal(sum6)
    for i in data6:
        sum6 = sum6 + i.case_amount_won
        print(i.case_amount_won)

    sum6 = Currency * int(sum6)
    sum6 = round(sum6,2)       
    print("Total Earings of all Lost" ,sum6)



    data7 = Case.objects.all().filter(state_id = 13)
    sum7 = 0
    sum7 = Decimal(sum7)
    for i in data6:
        sum7 = sum7 + i.case_amount_claim
        print(i.case_amount_claim)


    sum7 = Currency * int(sum7)
    sum7 = round(sum7,2)

    print("Total Claim Amount of all Filed Lawsuits Cases" ,sum7)

    data8 = Case.objects.all().filter(state_id = 11)
    sum8 = 0
    sum8 = Decimal(sum8)
    for i in data8:
        sum8 = sum8 + i.customer_amount_lost
        print(i.customer_amount_lost)

    sum8 = Currency * int(sum8)
    sum8 = round(sum8,2)
        
    print("Total Customer Amount Loss of all Processing  Cases" ,sum8)

    data9 = Case.objects.all().filter(state_id = 11)
    sum9 = 0
    sum9 = Decimal(sum9)
    for i in data9:
        sum9 = sum9 + i.case_amount_claim
        print(i.case_amount_claim)

    sum9 = Currency * int(sum9)
    sum9 = round(sum9,2)
    print("Total Claim Amount of all Processing Cases" ,sum9)


    return render(request,'myapp/earning.html',{'all_earnings':sum,'sports_bets':sum1,'Slot_Machine':sum2,'Online_Casino':sum3 ,'Won':sum4,'Won_case_amount_won':sum5,'Lost':sum6,'Claim_Amount':sum7,'customer_amount_lost':sum8,'case_amount_claim':sum9})


def people(request):
    person_detail = Person.objects.all()
    return render(request,'myapp/person_detail.html',{'person_detail':person_detail})


#lawyer update
def lawyer_update(request,lawyer_id):
    lawyer_obj = Lawyer.objects.get(lawyer_id=lawyer_id)
    print(lawyer_obj.person_id)
    data=Person.objects.filter(first_name=lawyer_obj.person_id.first_name)
    if request.method == 'POST':
        person = request.POST.get('person')
        fees_per_hour = request.POST.get('fees_per_hour')
        fees_per_service = request.POST.get('fees_per_service')
        comment = request.POST.get('comment')
        if len(fees_per_service) == 0  and len(fees_per_hour) == 0:
            messages.error(request,"Form FillUp Correctly")
            data=Person.objects.all()
            return render(request,'myapp/lawyerform.html',{'data':data})
        fees_per_hour=Decimal(fees_per_hour)
        fees_per_service=Decimal(fees_per_service)
        lawyer_obj.fees_per_hour = fees_per_hour
        lawyer_obj.fees_per_service = fees_per_service
        lawyer_obj.comment = comment
        lawyer_obj.save()
        return redirect(all_lawyer)
    else:
        return render(request,'myapp/lawyer_update.html',{'lawyer_obj':lawyer_obj,'data':data})


#customer update
def customer_update(request,customer_id):
    customer_obj = Customer.objects.get(customer_id=customer_id)
    # print(lawyer_obj.person_id)
    data=Person.objects.filter(first_name=customer_obj.person_id.first_name)
    if request.method == 'POST':
        comment = request.POST.get('comment')
        customer_obj.comment = comment
        customer_obj.save()
        return redirect(all_customer)
    else:
        return render(request,'myapp/customer_update.html',{'customer_obj':customer_obj,'data':data})


def alluser(request):
    user1 = User.objects.all()
    return render(request,'myapp/user.html',{'user1':user1})        

def lawyer_full_detail_all(request,lawyer_id):
    lawyer=Lawyer.objects.filter(lawyer_id=lawyer_id)
    return render(request,'myapp/lawyer_full_detail_all.html',{'lawyer':lawyer})

def customer_full_detail_all(request,customer_id):
    customer=Customer.objects.filter(customer_id=customer_id)
    return render(request,'myapp/customer_full_detail_all.html',{'customer':customer})
