from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from institute.models import Cart, Employees, Products, Requests, Rooms
from datetime import date
from django.contrib import messages


# Create your views here.
def official_home(request):
    username = request.COOKIES['username']
    user = Employees.objects.get(emp_id=username)
    
    if user.designation == 'Lab Incharge' or user.designation == 'Room Incharge' or user.designation == 'Caretaker' :
        room = get_object_or_404(Rooms, room_id=user.room_id)
        products_use = Products.objects.filter(branch=user.branch, room=room, status='Usable').count()
        products_main = Products.objects.filter(branch=user.branch,room=room, status='Maintenance').count()
        products_unus = Products.objects.filter(branch=user.branch,room=room, status='Unusable').count()
        return render(request, 'institute/incharge-home.html',{ 'user':user, 'room':room,'products_use':products_use,'products_main':products_main, 'products_unus':products_unus })
    
    elif user.designation == 'HOD' or user.designation == 'HOS' or user.designation == 'Head' or user.designation == 'Chief Warden' or user.designation == 'Deputy Chief Warden':
        room_count = Rooms.objects.filter(branch=user.branch).count()
        products_use = Products.objects.filter(branch=user.branch, status='Usable').exclude(room=None).count()
        products_main = Products.objects.filter(branch=user.branch, status='Maintenance').exclude(room=None).count()
        products_unus = Products.objects.filter(branch=user.branch, status='Unusable').exclude(room=None).count()
        stock = Products.objects.filter(branch=user.branch, room=None).count()
        stock_use = Products.objects.filter(branch=user.branch, room=None, status='Usable').count()
        stock_main = Products.objects.filter(branch=user.branch, room=None, status='Maintenance').count()
        stock_unus = Products.objects.filter(branch=user.branch, room=None, status='Unusable').count()
        
        return render(request, 'institute/head-home.html',{
            'user':user,
            'room_count':room_count,
            'products_use':products_use,
            'products_main':products_main, 
            'products_unus':products_unus,
            'stock':stock,
            'stock_use':stock_use,
            'stock_main':stock_main,
            'stock_unus':stock_unus,
        })


def inven_home(request):
    username = request.COOKIES['username']
    user = Employees.objects.get(emp_id=username)
    room_count = Rooms.objects.filter().count()
    products_use = Products.objects.filter(status='Usable').exclude(branch=None).count()
    products_main = Products.objects.filter(status='Maintenance').exclude(branch=None).count()
    products_unus = Products.objects.filter(status='Unusable').exclude(branch=None,room=None).count()
    stock = Products.objects.filter(branch=None, room=None).count()
    stock_use = Products.objects.filter(branch=None, room=None, status='Usable').count()
    stock_main = Products.objects.filter(branch=None, room=None, status='Maintenance').count()
    stock_unus = Products.objects.filter(branch=None, room=None, status='Unusable').count()

    return render(request, 'institute/inven-home.html',{
            'user':user,
            'room_count':room_count,
            'products_use':products_use,
            'products_main':products_main, 
            'products_unus':products_unus,
            'stock':stock,
            'stock_use':stock_use,
            'stock_main':stock_main,
            'stock_unus':stock_unus,
        })

@csrf_exempt
def inven_requests(request):
    username = request.COOKIES['username']
    user = Employees.objects.get(emp_id=username)
    inven_req = Requests.objects.filter(status='Pending') | Requests.objects.filter(status='In Cart')
    item_list = []
    for item in inven_req:
        item_list.append({
            'req':item,
            'stock_count': Products.objects.filter(type=item.type, specs=item.specs, status='Usable', branch=None, room=None).count()
        })

    if request.method == 'POST':
        for item in inven_req:
            id = str(item.id)
            if request.POST.get('R'+id):
                if Cart.objects.filter(type=item.type, specs=item.specs, status='To Buy').exists():
                    newCart = Cart.objects.get(type=item.type, specs=item.specs, status='To Buy')
                    newCart.count += int(item.count)
                else:
                    newCart = Cart(type=item.type, specs=item.specs, count=item.count, kind=item.kind)
                newCart.save()
                item.status = 'In Cart'
                item.save()
            
            elif request.POST.get('A'+id):
                stock = Products.objects.filter(type=item.type, specs=item.specs, status='Usable', branch=None, room=None)
                for i in range(int(request.POST.get('A'+id))):
                    try:
                        update_product = stock[i]
                        update_product.branch = item.branch
                        update_product.room_id = item.room_id
                        update_product.save()
                    except IndexError:
                        break

                item.count -= i+1
                if item.count == 0:
                    item.status = 'Resolved'
                item.save()


        return redirect('institute:inven_requests')

    return render(request, 'institute/inven-requests.html',{
            'user':user,
            'item_list':item_list,
        })

def profile(request):
    username = request.COOKIES['username']
    user = Employees.objects.get(emp_id=username)

    return render(request, 'institute/profile.html',{'item':user})


@csrf_exempt
def unmet_require(request):
    username = request.COOKIES['username']
    user = Employees.objects.get(emp_id=username)
    if user.designation == 'HOD' or user.designation == 'HOS' or user.designation == 'Head' or user.designation == 'Chief Warden' or user.designation == 'Deputy Chief Warden':
        rooms = Rooms.objects.filter(branch=user.branch)
        unmet_requirements = []
        require_id=1
        for room in rooms:
            room.requirements = room.requirements.replace('\r\n','')
            room_requirement = room.requirements.split(';')
            for product in room_requirement:
                if product != '':
                    item = product.split('-')
                    product_type = item[0]
                    product_spec = item[1]
                    required_count = int(item[2])

                    available_count = Products.objects.filter(type=product_type, specs=product_spec, branch=user.branch, room_id=room).count()
                    needed_count = required_count - available_count
                    try:
                        request_obj = Requests.objects.get(type=product_type, specs=product_spec, branch=user.branch, room_id=room, status='Pending')
                        request_count = request_obj.count
                        
                    except Requests.DoesNotExist:
                        request_count = 0
                    
                    stock_count = Products.objects.filter(type=product_type, specs=product_spec, branch=user.branch, room=None, status='Usable').count()
                    
                    if needed_count > request_count:
                        unmet_requirements.append({
                            'require_id':require_id,
                            'room_id':room.room_id,
                            'room_name':room.name,
                            'product_type':product_type,
                            'product_spec':product_spec,
                            'product_count':needed_count - request_count,
                            'stock_count':stock_count,
                        })
                        require_id += 1

        if request.method == 'POST':
            for item in unmet_requirements:
                id = str(item['require_id'])
                if request.POST.get('R'+id):
                    if Requests.objects.filter(branch=user.branch, type=item['product_type'], specs=item['product_spec']).exists():
                        newRequest = Requests.objects.get(branch=user.branch, type=item['product_type'], specs=item['product_spec'], room_id=item['room_id'])
                        newRequest.count += int(item['product_count'])
                        newRequest.status = 'Pending'
                    else:
                        tempProduct = Products.objects.filter(type=item['product_type'], specs=item['product_spec'])
                        newRequest = Requests(branch=user.branch, type=item['product_type'], specs=item['product_spec'], count=item['product_count'], room_id=item['room_id'], kind=tempProduct[0].kind)
                    newRequest.save()
                
                elif request.POST.get('A'+id):
                    stock = Products.objects.filter(type=item['product_type'], specs=item['product_spec'], branch=user.branch, room=None, status='Usable')
                    for i in range(item['product_count']):
                        try:
                            update_product = stock[i]
                            update_product.room_id = item['room_id']
                            update_product.save()
                        except IndexError:
                            break

            return redirect('institute:unmet_require')
        return render(request, 'institute/unmet-require.html',{'user':user, 'unmet_requirements':unmet_requirements})


    elif user.designation == 'Lab Incharge' or user.designation == 'Room Incharge' or user.designation == 'Caretaker' :
        room = get_object_or_404(Rooms, room_id=user.room_id)
        unmet_requirements = []
        require_id=1
        room.requirements = room.requirements.replace('\r\n','')
        room_requirement = room.requirements.split(';')
        for product in room_requirement:
            if product != '':
                item = product.split('-')
                product_type = item[0]
                product_spec = item[1]
                required_count = int(item[2])
                available_count = Products.objects.filter(type=product_type, specs=product_spec, branch=user.branch, room_id=room).count()
                needed_count = required_count - available_count
                if needed_count >0:
                    unmet_requirements.append({
                        'require_id':require_id,
                        'room_id':room.room_id,
                        'room_name':room.name,
                        'product_type':product_type,
                        'product_spec':product_spec,
                        'product_count':needed_count,
                    })
                    require_id += 1

               

        return render(request, 'institute/unmet-require-incharge.html',{'user':user, 'unmet_requirements':unmet_requirements, 'room':room})

def incharge_status(id,status,emp_id):
    currProduct = Products.objects.get(prod_id=id)
    currProduct.status = status
    if currProduct.update == '': currProduct.update = str(date.today())+'='+str(emp_id)+'='+status+';'
    else: currProduct.update += '\r\n'+str(date.today())+'='+str(emp_id)+'='+status+';'
    currProduct.save()

def maintainence(request):
    username=request.COOKIES['username']
    user = Employees.objects.get(emp_id=username)
    
    if user.branch == 'Inventory Section' and (user.designation=='Head' or user.designation=='HOS' or user.designation=='Admin') :
        product_det=Products.objects.filter(status='Maintenance')
        return render(request,'institute/maintainence-inven.html',{'user':user,'product_det':product_det})

    else:
        if user.designation == 'HOD' or user.designation == 'HOS' or user.designation == 'Head' or user.designation == 'Chief Warden' or user.designation == 'Deputy Chief Warden':
            product_det=Products.objects.filter( branch=user.branch, status='Maintenance')
            return render(request,'institute/maintainence-product.html',{'user':user,'product_det':product_det})

        elif user.designation == 'Lab Incharge' or user.designation == 'Room Incharge' or user.designation == 'Caretaker' :
            room = get_object_or_404(Rooms, room_id=user.room_id)
            product_det=Products.objects.filter( branch=user.branch, status='Maintenance',room=room)
            return render(request,'institute/maintainence-product.html',{'user':user,'product_det':product_det,'room':room})
                         
def unusable(request):
    username=request.COOKIES['username']
    user = Employees.objects.get(emp_id=username)

    if user.branch == 'Inventory Section' and (user.designation=='Head' or user.designation=='HOS' or user.designation=='Admin') :
        product_det=Products.objects.filter(status='Unusable')
        return render(request,'institute/unusable-inven.html',{'user':user,'product_det':product_det})

    else:
        if user.designation == 'HOD' or user.designation == 'HOS' or user.designation == 'Head' or user.designation == 'Chief Warden' or user.designation == 'Deputy Chief Warden':
             product_det=Products.objects.filter( branch=user.branch, status='Unusable')
             return render(request,'institute/unusable-products.html',{'user':user,'product_det':product_det})
        elif user.designation == 'Lab Incharge' or user.designation == 'Room Incharge' or user.designation == 'Caretaker' :
            room = get_object_or_404(Rooms, room_id=user.room_id)
            product_det=Products.objects.filter( branch=user.branch, status='Unusable',room=room)
        return render(request,'institute/unusable-products.html',{'user':user,'product_det':product_det, 'room':room})

def stock(request):
    username=request.COOKIES['username']
    user = Employees.objects.get(emp_id=username)
    if user.branch != 'Inventory Section':
        if user.designation == 'HOD' or user.designation == 'HOS' or user.designation == 'Head' or user.designation == 'Chief Warden' or user.designation == 'Deputy Chief Warden':
            product_det=Products.objects.filter( branch=user.branch,room=None)
            return render(request,'institute/stock-product.html',{'user':user,'product_det':product_det})
    else:
        product_det=Products.objects.filter(branch=None, room=None)
        return render(request,'institute/stock-product.html',{'user':user,'product_det':product_det})
    
                         
@csrf_exempt
def products(request):
    username=request.COOKIES['username']
    user = Employees.objects.get(emp_id=username)
    if user.branch != 'Inventory Section':
        if user.designation == 'Lab Incharge' or user.designation == 'Room Incharge' or user.designation == 'Caretaker' :
            room = get_object_or_404(Rooms, room_id=user.room_id)
            product_det=Products.objects.filter(room=room)

            if request.method == 'POST':
                for item in product_det:
                    if request.POST.get(item.prod_id) != item.status:
                        incharge_status(item.prod_id,request.POST.get(item.prod_id), user.emp_id)
                return redirect('institute:products')
            return render(request,'institute/product-incharge.html',{'user':user,'product_det':product_det,'room':room})

        elif user.designation == 'HOD' or user.designation == 'HOS' or user.designation == 'Head' or user.designation == 'Chief Warden' or user.designation == 'Deputy Chief Warden':
            product_det=Products.objects.filter(branch=user.branch)
            if request.method == 'POST':
                for item in product_det:
                    if request.POST.get('S'+str(item.prod_id)) != item.status:
                        currProduct = Products.objects.get(prod_id=item.prod_id)
                        currProduct.status = request.POST.get('S'+str(item.prod_id))
                        if currProduct.update == '': currProduct.update = str(date.today())+'='+str(user.emp_id)+'='+request.POST.get('S'+str(item.prod_id))+';'
                        else: currProduct.update += '\r\n'+str(date.today())+'='+str(user.emp_id)+'='+request.POST.get('S'+str(item.prod_id))+';'
                        currProduct.save()
                        
                    if request.POST.get('A'+str(item.prod_id)) == 'Remove Room':
                        currProduct = Products.objects.get(prod_id=item.prod_id)
                        currProduct.room = None
                        currProduct.save()

                    elif request.POST.get('A'+str(item.prod_id)) == 'Permanent Remove':
                        currProduct = Products.objects.get(prod_id=item.prod_id)
                        currProduct.room = None
                        currProduct.branch = None
                        currProduct.save()
                return redirect('institute:products')

            return render(request,'institute/product-head.html',{'user':user,'product_det':product_det,})

    else:
        if user.designation=='Head' or user.designation=='HOS' or user.designation=='Admin':
            product_det=Products.objects.all()
            room_list = Rooms.objects.all()
            branch = Employees.BRANCH
            branch_list = []
            for item in branch:
                branch_list.append(item[0])

            if request.method == 'POST':
                for item in product_det:
                    if request.POST.get('S'+str(item.prod_id))!= 'Delete' and request.POST.get('S'+str(item.prod_id)) != item.status :
                        currProduct = Products.objects.get(prod_id=item.prod_id)
                        currProduct.status = request.POST.get('S'+str(item.prod_id))
                        if currProduct.update == '': currProduct.update = str(date.today())+'='+str(user.emp_id)+'='+request.POST.get('S'+str(item.prod_id))+';'
                        else: currProduct.update += '\r\n'+str(date.today())+'='+str(user.emp_id)+'='+request.POST.get('S'+str(item.prod_id))+';'
                        currProduct.save()

                    elif request.POST.get('S'+str(item.prod_id)) == 'Delete':
                        currProduct = Products.objects.get(prod_id=item.prod_id)
                        currProduct.delete()
                        continue


                    if request.POST.get('B'+str(item.prod_id)) != item.branch:
                        currProduct = Products.objects.get(prod_id=item.prod_id)
                        currProduct.branch = request.POST.get('B'+str(item.prod_id))
                        currProduct.save()
                        

                    if request.POST.get('R'+str(item.prod_id)) != 'None' and request.POST.get('R'+str(item.prod_id)) != item.room:
                        currProduct = Products.objects.get(prod_id=item.prod_id)
                        currProduct.room_id = request.POST.get('R'+str(item.prod_id))
                        currProduct.save()
                    elif request.POST.get('R'+str(item.prod_id)) == 'None':
                        currProduct = Products.objects.get(prod_id=item.prod_id)
                        currProduct.room = None
                        currProduct.save()
                    
                return redirect('institute:products')

            return render(request,'institute/product-inven.html',{'user':user,'product_det':product_det, 'branch_list':branch_list, 'room_list':room_list})




def register (request):
    username=request.COOKIES['username']
    user = Employees.objects.get(emp_id=username)

    if user.branch != 'Inventory Section' and (user.designation == 'HOD' or user.designation == 'HOS' or user.designation == 'Head' or user.designation == 'Chief Warden' or user.designation == 'Deputy Chief Warden'):
        if request.method=='POST'  :
            if request.POST["submit"]:
                emp_id=request.POST['empid']
                name=request.POST['name']
                desig=request.POST['desig']
                roomid=request.POST['roomid']
                if roomid ==None or roomid=='':
                        room=None
                else:
                        room=get_object_or_404(Rooms, room_id=roomid)
                ph=request.POST['ph']
                emailid=request.POST['emailid']
                if Employees.objects.filter(emp_id=emp_id).exists():
                        messages.error(request, 'Employee already exists. Please Login!')
                        return redirect('institute:register')
                else  :
                        emp=Employees(emp_id=emp_id,name=name,branch=user.branch,designation=desig,room_id=room,phone=ph,email_id=emailid)
                        emp.save()
                        messages.success(request, 'Employee created successfully!')
                        return redirect('institute:register')

  
        return render(request,'institute/register.html',{'user':user})


        

        
    
    

