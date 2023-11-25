from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import LogTable
from django.db.models import Count


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
