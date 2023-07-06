from rest_framework import viewsets
from rest_framework.response import Response
from .models import Printer, Check
from .serializers import PrinterSerializer, CheckSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import html_to_pdf, print_check

    
@csrf_exempt
def create_check(request):
    if request.method == 'POST':
        printer_api_key = request.POST.get('printer_api_key')
        check_type = request.POST.get('check_type')
        order_data = request.POST.get('order_data')
        try:
            printer = Printer.objects.get(api_key=printer_api_key, check_type=check_type)
        except Printer.DoesNotExist:
            return JsonResponse({'error': 'Printer not found'}, status=400)
        
        check = None
        try:
            existing_check = Check.objects.get(printer_id=printer, order=order_data)
            return JsonResponse({'error': 'Check already created for this order', 'order_id': order_data}, status=400)
            
        except Check.DoesNotExist:
            check = Check(printer_id=printer, type=check_type, order=order_data, status=Check.NEW_STATUS)
            check.save()
            context = {
                'check_id': check.id,
                'check_type': check_type,
                'printer_id': printer.id,
                'status': Check.NEW_STATUS,
                'check_obj': check,
                'order': order_data
            }
            html_to_pdf(context)
            return JsonResponse({'success': 'Check created successfully', 'check_id': check.id}, status=200)
    
    return JsonResponse({'success': 'printing completed'}, status=200)
    

@csrf_exempt
def print_checks(request):
    checks = Check.objects.filter(status=Check.NEW_STATUS)
    if request.method == "POST":
        print_check(checks)
        return JsonResponse({'success': 'Check printed'})
    else:
        return JsonResponse({'error': 'ERROR'})
