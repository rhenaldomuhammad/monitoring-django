from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import LogTable
from django.db.models import Count
from collections import defaultdict
from django.utils import timezone
import calendar
from datetime import datetime


class IndexView(APIView):
	def get(self, request, *args, **kwargs):
		return render(request, "theme/index.html", {})

	def post(self, request, *args, **kwargs):

		return Response({'status': 200})

@api_view(['GET'])

def get_stats(request):
	logs = LogTable.objects.values('attack_type').annotate(count=Count('attack_type'))

	attack_types = [log['attack_type'] for log in logs]
	attack_counts = [log['count'] for log in logs]

	return Response({"attack_types": attack_types, "attack_counts": attack_counts})

@api_view(['GET'])
def get_bars(request):
	chart_data = get_attack_data()
	return Response({'chart_data': chart_data})


def get_attack_data():
    # Mendapatkan tanggal saat ini dan tanggal 3 bulan yang lalu
    current_date = timezone.now()
    
	# Membuat daftar bulan untuk November, Oktober, dan September
    months = [(current_date - timezone.timedelta(days=30 * i)).strftime("%B %Y") for i in range(3)][::-1]

	# Menentukan warna untuk setiap attack_type
    colors = {"XSS Attack": "#4e73df", "Unix Command Injection": "#1cc88a", "SQL Injection": "#36b9cc"}

	# Mengorganisir data ke dalam struktur yang diinginkan
    data_format = {
        "time": months,
        "data": {attack_type: {"label": attack_type, "backgroundColor": color, "data": [0] * 3} for attack_type, color in colors.items()}
    }
	
    # Membuat query untuk mengambil data
    start_date = current_date.replace(day=1) - timezone.timedelta(days=90)  # Mulai dari awal bulan 3 bulan yang lalu
    end_date = current_date.replace(day=1) + timezone.timedelta(days=32)  # Berakhir di akhir bulan saat ini
    end_date = end_date.replace(day=1)  # Memastikan tidak melebihi bulan saat ini

    attacks = LogTable.objects.filter(
        timestamp__range=[start_date, end_date]
    ).values('attack_type', 'timestamp__month', 'timestamp__year').annotate(count=Count('id'))

    for attack in attacks:
        year = attack['timestamp__year']
        month = attack['timestamp__month']
        attack_type = attack['attack_type']
        count = attack['count']

        month_year = f"{calendar.month_name[month]} {year}"

        # Cari indeks bulan dalam daftar months
        if month_year in months:
            month_index = months.index(month_year)
            data_format["data"][attack_type]["data"][month_index] = count

	

    

    

    # monthly_data = defaultdict(lambda: defaultdict(int))

    # for attack in attacks:
    #     year = attack['timestamp__year']
    #     month = attack['timestamp__month']
    #     attack_type = attack['attack_type']
    #     count = attack['count']

    #     month_year = f"{calendar.month_name[month]} {year}"
    #     if month_year not in data_format["time"]:
    #         data_format["time"].append(month_year)

    #     monthly_data[month_year][attack_type] += count

    # for month_year in data_format["time"]:
    #     for attack_type, color in colors.items():
    #         data_format["data"][attack_type]["label"] = attack_type
    #         data_format["data"][attack_type]["backgroundColor"] = color
    #         data_format["data"][attack_type]["data"].append(monthly_data[month_year][attack_type])

    # Mengkonversi defaultdict menjadi list
    data_format["data"] = list(data_format["data"].values())

    return data_format
