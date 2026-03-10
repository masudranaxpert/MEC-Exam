from django.http import request
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Product, ExcelFile
from django.core.paginator import Paginator
import openpyxl
from django.db.models import Q


def display(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        id = data.get('product_id')
        choice = data.get('choice')
        product = get_object_or_404(Product, product_id=id)
        product.status = choice
        product.save()
        return redirect('display')

    products = Product.objects.all().order_by('status')
    paginator = Paginator(products, 10) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    
    return render(request, 'display.html', context)



def excel_file(request):
    if request.method == 'POST':
        data = request.FILES
        excel_file = data.get('excel_file')
        if excel_file.name.endswith('.xlsx'):
            wb = openpyxl.load_workbook(excel_file)
            ws = wb.active

            for row in ws.iter_rows(min_row=2, values_only=True):
                exist_product = Product.objects.filter(product_id=row[0]).first()
                if exist_product:
                    exist_product.name=row[1],
                    exist_product.category=row[2],
                    exist_product.price=row[3],
                    exist_product.quantity=row[4],
                    exist_product.status=row[5],
                    exist_product.updated_at = row[6]
                else:
                    Product.objects.create(
                        product_id=row[0],
                        name=row[1],
                        category=row[2],
                        price=row[3],
                        quantity=row[4],
                        status=row[5],
                        updated_at = row[6],
                        created_at = row[7]
                    )
            return redirect('display')
        else:
            return HttpResponse("Invalid file format")




def approved(request):
    per_page = request.GET.get('per_page', 10)
    search = request.GET.get('search', '')

    from_date = request.GET.get('from')
    to_date = request.GET.get('to')

    products = Product.objects.filter(status='approved', )
    
    if from_date and to_date:
        products = products.filter(created_at__range=[from_date, to_date])

    if search:
        products = products.filter(
            Q(name__icontains=search) | Q(category__icontains=search)
        )   

    paginator = Paginator(products, per_page) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'approved.html', context)