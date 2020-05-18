from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from institute.models import Employees, Products, Rooms

# Create your views here.
def official_home(request):
    username = request.COOKIES['username']
    user = Employees.objects.get(emp_id=username)
    
    if user.designation == 'Lab Incharge' or user.designation == 'Room Incharge' or user.designation == 'Caretaker' :
        room = get_object_or_404(Rooms, room_id=user.room_id)
        return render(request, 'institute/incharge-home.html',{ 'user':user, 'room':room })
    
    elif user.designation == 'HOD' or user.designation == 'HOS' or user.designation == 'Head' or user.designation == 'Chief Warden' or user.designation == 'Deputy Chief Warden':
        room_count = Rooms.objects.filter(branch=user.branch).count()
        
        return render(request, 'institute/head-home.html',{ 'user':user,'room_count':room_count})

def unmet_require(request):
    username = request.COOKIES['username']
    user = Employees.objects.get(emp_id=username)
    if user.designation == 'HOD' or user.designation == 'HOS' or user.designation == 'Head' or user.designation == 'Chief Warden' or user.designation == 'Deputy Chief Warden':
        rooms = Rooms.objects.filter(branch=user.branch)
        unmet_requirements = []

        for room in rooms:
            room.requirements = room.requirements.replace('\r\n','')
            room_requirement = room.requirements.split(';')

            for product in room_requirement:
                if product != '':
                    item = product.split('-')
                    product_type = item[0]
                    product_spec = item[1]
                    product_count = item[2]

                    stock_count = Products.objects.filter(type=product_type, specs=product_spec, branch=user.branch, status='Usable').count()

                    unmet_requirements.append({
                        'room_id':room.room_id,
                        'room_name':room.name,
                        'product_type':product_type,
                        'product_spec':product_spec,
                        'product_count':product_count,
                        'stock_count':stock_count,

                    })

    return render(request, 'institute/unmet-require.html',{'user':user, 'unmet_requirements':unmet_requirements})
    

