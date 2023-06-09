
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from .models import Users, Courses
from . import models
from .data_files.images_data import images_data
from django.db import connection, connections



def add_admin_role():
    with connections['admin'].cursor() as cursor:
        query = '''
            EXEC sp_addrolemember 'admin', 'account1';
        '''
        cursor.execute(query)

def add_role_after_login():
    with connections['admin'].cursor() as cursor:
        query = '''
            EXEC sp_addrolemember 'role_after_login', 'account1';
        '''
        cursor.execute(query)
def log_out_role():
    with connections['admin'].cursor() as cursor:
        query = '''
            EXEC sp_droprolemember 'role_after_login', 'account1';
            EXEC sp_droprolemember 'admin', 'account1';
        '''
        cursor.execute(query)
# Convert data from request.data :
def convertDataReqToDict(data):
    data = dict(data)
    for key, value in data.items():
        data[f'{key}'] = value[0]
    return data

# Convert data from query sel server:
def dict_fetch_all(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
# Convert SQl sp,func to python def :
def getNumUserRegisterCourses(user_id):
    with connection.cursor() as cursor:
        query = '''
            select dbo.func_num_reg_courses(%s) as num_cart
        '''
        cursor.execute(query, [user_id])
        data = dict_fetch_all(cursor)
    return data
def getTotalMoneyRegCourses(user_id):
    with connection.cursor() as cursor:
        query = '''
            select dbo.func_total_money_reg_courses(%s) as total_cost
        '''
        cursor.execute(query,[user_id])
        total_cost = dict_fetch_all(cursor)[0]['total_cost']
    return total_cost

def check_wallet(user_id):
    with connection.cursor() as cursor:
        query = """
            SELECT dbo.func_check_wallet_exist(%s) AS has_wallet;
        """
        cursor.execute(query,[user_id])
        data = dict_fetch_all(cursor)
    print(data)
    if (data[0]['has_wallet'] == 1):
        return 1
    return 0
def getCurrentMoney(user_id):
    with connection.cursor() as cursor:
        query = """
            SELECT dbo.func_get_current_money(%s) As current_money 
        """
        cursor.execute(query,[user_id])
        data = dict_fetch_all(cursor)
    return data[0]['current_money']

# Create your views here.
# Global Variable For home_page:
mess_error = False
log_decision = True
object_data = None
images_data = images_data
num_cart = None
role = None
# Set up for maintaining Get request:
def home_page(request): #
    global mess_error, log_decision, object_data, num_cart, role
    if request.method == 'POST':
        data = request.POST
        # See all data from request POST.
        data = convertDataReqToDict(data)
        print(data)
        data_POST = [val.strip() for key, val in data.items() if key in ['username', 'email',  'password','passwordAgain']]
        # Code to Sign up with role admin page:
        try:
            code = [val.strip() for key, val in data.items() if key == 'code'][0]
        except:
            code = None
        print(code)
        # see data when posting request:
        print(data_POST)
        # Analysis data to decide data out/in.
        len_data_before_register = Users.objects.count()
        print(len(data))
        if len(data) == 6 or len(data) == 7 :       
            if data['role'] == 'user':
                with connection.cursor() as cursor:
                    query_proc_regiser_user = """
                        exec sp_reg_user_account %s,%s,%s,%s
                    """
                    cursor.execute(query_proc_regiser_user,data_POST)
                    len_data_after_update = Users.objects.count()
                    if len_data_after_update == len_data_before_register:
                        mess_error = True
                    else: 
                        mess_error = False
                return redirect('/')
            elif data['role'] == 'admin' and code == '123':
                with connection.cursor() as cursor:
                    query_proc_regiser_admin = """
                        exec sp_reg_admin_account %s,%s,%s,%s
                    """
                    cursor.execute(query_proc_regiser_admin,data_POST)
                    cursor.execute(query_proc_regiser_admin,data_POST)
                    len_data_after_update = Users.objects.count()
                    if len_data_after_update == len_data_before_register:
                        mess_error = True
                    else: 
                        mess_error = False
                return redirect('/')
           
        elif len(data) == 3:
            with connection.cursor() as cursor:
                query_func_login_user = """
                    exec sp_check_login %s,%s 
                """
                cursor.execute(query_func_login_user,data_POST)
                check_log_in = dict_fetch_all(cursor)[0] # convert data query to dict (like Objects).
            print(check_log_in)

            if check_log_in['result'] == 2: # Functions Check Login Return 0 Or 1:
                role = 'user'
                add_role_after_login()
                print('User Account')
                log_decision = False
                mess_error = False
                print(data_POST) # Check data, we see ['email]
                user = get_object_or_404(Users, email=data_POST[0])
                object_data = user
                num_cart = getNumUserRegisterCourses(user.user_id)[0]['num_cart']
                print('Num of cart:',num_cart)
                return redirect(f'/user/{user.user_id}')
            
            elif check_log_in['result'] == 1:
                role = 'admin'
                add_role_after_login()
                add_admin_role()
                print('Admin Account')
                log_decision = False
                mess_error = False
                print(data_POST) # Check data, we see ['email]
                user = get_object_or_404(Users, email=data_POST[0])
                object_data = user
                num_cart = getNumUserRegisterCourses(user.user_id)[0]['num_cart']
                print('Num of cart:',num_cart)
                return redirect(f'/admin-dashboard/{user.user_id}/action-index/all-user')
            else:
                log_decision = True
                mess_error = True
                object_data = None
                return redirect('/')
    if request.method == 'GET': # GET http:
        with connections['admin'].cursor() as cursor:
            query = '''
                EXEC sp_addrolemember 'user', 'account1';
            '''
            cursor.execute(query)
        log_out_role()
        log_decision = True
        object_data = None
        if mess_error == True:
            mess_error = True
        else:
            mess_error = False
    print('Data:',object_data,log_decision, mess_error)
    print(reverse_lazy('index'))
    return render(request, 'index.html', {
        'log_decision': log_decision,
        'mess_error': mess_error,
        'object_data': object_data,
        'role': role,
    })
# User After Login:
def page_user_login(request, pk):
    # page for each each user
    global mess_error, log_decision, object_data, num_cart, role # update object when log in user.
    object_data = get_object_or_404(Users, pk=pk)
    return render(request, 'index.html',{
                    'log_decision': log_decision,
                    'object_data': object_data,
                    'mess_error': mess_error,
                    'num_cart':num_cart,
                    'role': role,
                })

def profile(request):
    global mess_error, log_decision, object_data, num_cart, role
    print(object_data)
    return render(request, 'templates/user/profile/profile.html',{
        'log_decision': log_decision,
        'object_data': object_data,
        'mess_error': mess_error,
        'num_cart': num_cart,
        'role': role,
    })

# End Set up For User:

# Views For User:

# Views About Courses:
def list_all_courses(request, slug):
    global mess_error, log_decision, object_data, num_cart, role # remain data for user when using website.
    global images_data
    print(images_data)
    if request.method == 'GET':
        with connection.cursor() as cursor:
            if slug == 'all':
                # Data Origin:
                query = """
                    select * from all_courses_info
                """
                cursor.execute(query)
                data_origin = dict_fetch_all(cursor)
                data = data_origin
            elif slug == 'prices_asc':
                # Prices_Asc
                query = """
                    SELECT * FROM v_courses_price_asc
                    ORDER BY price ASC
                """
                cursor.execute(query)
                data_prices_asc = dict_fetch_all(cursor)
                data = data_prices_asc
            elif slug == 'prices_desc':
                # Price_Desc:
                query = """
                    SELECT * FROM v_course_price_descending
                    ORDER BY price DESC
                """
                cursor.execute(query)
                data_prices_desc = dict_fetch_all(cursor)
                data = data_prices_desc

            elif slug == 'beginner':
                query = """
                    SELECT * FROM v_beginner_courses_info
                """
                cursor.execute(query)
                data_beginner = dict_fetch_all(cursor)
                data = data_beginner
            elif slug == 'intermediate':
                query = """
                    SELECT * FROM v_intermediate_courses_info
                """
                cursor.execute(query)
                data_intermediate = dict_fetch_all(cursor)
                data = data_intermediate

            elif slug == 'expert':
                query = """
                    SELECT * FROM v_expert_courses_info
                """
                cursor.execute(query)
                data_expert = dict_fetch_all(cursor)
                data = data_expert

            elif slug == 'master':
                query = """
                    SELECT * FROM v_master_courses_info
                """
                cursor.execute(query)
                data_master = dict_fetch_all(cursor)
                data = data_master

            elif slug == 'advanced':
                query = """
                    SELECT * FROM v_advanced_courses_info
                """
                cursor.execute(query)
                data_advanced = dict_fetch_all(cursor)
                data = data_advanced
    key = [key for key, val in images_data.items()]
    for item in data:
        idx = item.get('title')
        if idx in key:
            print(images_data.get(f'{idx}'))
    print(object_data)
    return render(request, 'templates/courses/listAllCourses.html',{
        'data': data,
        'log_decision': log_decision,
        'mess_error': mess_error,
        'object_data': object_data,
        'images_data': images_data,
        'num_cart':num_cart,
        'role': role,
    })




# View for mentors:
def list_all_mentors(request):
    global mess_error, log_decision, object_data, num_cart, role
    with connection.cursor() as cursor:
        query = """
            SELECT * FROM v_instructor
        """
        cursor.execute(query)
        mentors = dict_fetch_all(cursor)
    print(object_data)
    return render(request, 'templates/mentors/listAllMentors.html',{
        'mentors':mentors,
        'log_decision': log_decision,
        'mess_error': mess_error,
        'object_data': object_data,
        'images_data': images_data,
        'num_cart':num_cart,
        'role': role,
    })

def register_courses(request, pk):
    global mess_error, log_decision, object_data, num_cart, role
    try:
        user_id = object_data.user_id
        with connection.cursor() as cursor:
            query = """
                exec sp_reg_courses %s,%s
            """
            cursor.execute(query,[user_id, pk])
        num_cart = getNumUserRegisterCourses(user_id)[0]['num_cart']
        print('Success')
        return redirect('/all-courses/all')
    except:
        return redirect('/')

def cart_bill(request, slug, reg_id):
    global mess_error, log_decision, object_data, num_cart, role
    if slug == 'get-registered-course' and reg_id == '0':
        try:
            id = object_data.user_id
            print(id)
            with connection.cursor() as cursor:
                query = """
                    select * from dbo.func_list_all_reg_courses(%s)
                """
                cursor.execute(query,[id])
                data = dict_fetch_all(cursor)
                total_cost = getTotalMoneyRegCourses(id)
                print(total_cost)
            print(data)
            print('Success')
            return render(request, 'templates/user/cart/cart.html',{
                'log_decision': log_decision,
                'mess_error': mess_error,
                'object_data': object_data,
                'cart': data,
                'num_cart':num_cart,
                'total_cost':total_cost,
                'role': role,
            })
        except mess_error as err:
            print(err)
    elif slug == 'delete-course':
        try:
            id = object_data.user_id
            with connection.cursor() as cursor:
                query = '''
                    exec sp_delete_reg_courses %s,%s
                '''
                cursor.execute(query,[id, reg_id])
            num_cart = getNumUserRegisterCourses(id)[0]['num_cart'] 
            print(id, reg_id)

        except mess_error as err:
            print(err)
        return redirect('/cart-and-bill/get-registered-course/0')

    elif slug == 'paid':
        try:
            id = object_data.user_id
            with connection.cursor() as cursor:
                query = """
                    exec sp_processTransactionForAllOrders %s
                """
                cursor.execute(query,[id])
            num_cart = getNumUserRegisterCourses(id)[0]['num_cart'] 
            print(id, reg_id)

        except mess_error as err:
            print(err)
        return redirect('/cart-and-bill/get-registered-course/0')

    return redirect('/')
    # return render(request, 'templates/user/cart/cart.html',{
    #     'log_decision': log_decision,
    #     'mess_error': mess_error,
    #     'object_data': object_data,
    # })

# Wallet:
def wallet(request, params):
    global mess_error, log_decision, object_data, num_cart, role
    check_budget = None
    data = request.POST
    data_req = convertDataReqToDict(data)
    print(data_req)
    data_POST = [val.strip() for key, val in data_req.items() if key == 'money']
    print(data_POST)
    # Check wallet exist:
    id = object_data.user_id
    check_budget = check_wallet(id)
    # Get current money:
    current_money = getCurrentMoney(id)
    if params == 'action-index':
        return render(request,'templates/user/budget/budget.html',{
            'log_decision': log_decision,
            'mess_error': mess_error,
            'object_data': object_data,
            'num_cart':num_cart,
            'check_budget':check_budget,
            'current_money':current_money,
            'role':role,
        })
    elif params == 'create-budget':
        with connection.cursor() as cursor:
            query="""
                exec sp_create_budget %s;
            """
            cursor.execute(query, [id])
        return redirect(reverse_lazy('wallet', kwargs={'params':'action-index'}))
    elif params == 'deposit-budget':
        with connection.cursor() as cursor:
            query="""
                exec sp_deposit_budget %s,%s;
            """
            cursor.execute(query, [id, data_POST[0]])
        return redirect(reverse_lazy('wallet', kwargs={'params':'action-index'}))
    return redirect('/')

# Paid Courses:
def paid_courses(request):
    global mess_error, log_decision, object_data, num_cart, images_data, role
    try:
        id = object_data.user_id
        with connection.cursor() as cursor:
            query = '''
                select * from func_list_all_paid_courses(%s)
            '''
            cursor.execute(query, [id])
            data = dict_fetch_all(cursor)

        return render(request,'templates/user/paid_courses/paid_courses.html',{
            'log_decision': log_decision,
            'mess_error': mess_error,
            'object_data': object_data,
            'num_cart':num_cart,
            'images_data': images_data,
            'data': data,
            'role': role,
        })
    except:
        raise ValueError('paid-courses ERROR')
# Admin:
def admin_site(request, pk, params, options):
    global mess_error, log_decision, object_data, role
    try:
        id = object_data.user_id
        if id is not None and role == 'admin':
            if params in ['action-index','action-index-role-to-admin','action-index-delete','action-index-role-to-user']:
                with connection.cursor() as cursor:
                    query = '''
                        select * from v_user_info
                        order by user_id
                    '''
                    cursor.execute(query)
                    data = dict_fetch_all(cursor)
                    lst = []
                    data_lst = [[ lst.append(str(val)) for key, val in item.items() if key=='user_id'] for item in data]
                    print(lst)
                    if options in lst and params == 'action-index-role-to-admin':
                        query = '''
                            exec sp_update_user_authorization %s;
                        '''
                        cursor.execute(query, [options])
                        return redirect(f'/admin-dashboard/{id}/action-index/all-user')
                    elif options in lst and params == 'action-index-role-to-user' and str(id)!= options:
                        query = '''
                            exec sp_role_to_user %s;
                        '''
                        cursor.execute(query, [options])
                        return redirect(f'/admin-dashboard/{id}/action-index/all-user')
                    elif options in lst and params == 'action-index-delete' and str(id) != options:
                        query = '''
                            exec sp_delete_user %s;
                        '''
                        cursor.execute(query, [options])
                        return redirect(f'/admin-dashboard/{id}/action-index/all-user')
                    if str(id) == options:
                        return redirect(f'/admin-dashboard/{id}/action-index/all-user')
                print(data)
                return render(request,'templates/admin/admin_site/admin_site.html',{
                    'log_decision': log_decision,
                    'mess_error': mess_error,
                    'object_data': object_data,
                    'role': role,
                    'data': data,
                    'action':params,
                    })
            elif params == 'action-add':
                try:
                    data = request.POST
                    # See all data from request POST.
                    data = convertDataReqToDict(data)
                    print(data)
                    data_POST = [val.strip() for key, val in data.items() if key in ['title','description','price','instructor','level_id','category_id']]
                    print(data_POST)
                    # Insert data to table courses.
                    with connection.cursor() as cursor:
                        query = ''' 
                            select * from all_courses_info
                        '''
                        cursor.execute(query)
                        v_all_courses = dict_fetch_all(cursor)
                        lst = []
                        data_lst = [[ lst.append(str(val)) for key, val in item.items() if key=='course_id'] for item in v_all_courses]
                        if options in lst:
                            query = ''' 
                                exec sp_delete_course %s;
                            '''
                            cursor.execute(query,[options])
                            return redirect(f'/admin-dashboard/{id}/action-add/all-courses')
                    #
                    if request.method == 'POST' and options == 'create':
                        print(len(request.POST))
                        if len(data) == 7:
                            with connection.cursor() as cursor:
                                query = ''' 
                                    exec sp_post_course %s,%s,%s,%s,%s,%s;
                                '''
                                cursor.execute(query,data_POST)
                                data = dict_fetch_all(cursor)
                                return redirect(f'/admin-dashboard/{id}/action-add/all-courses')
                        elif len(data) == 8:
                            data_POST = [val.strip() for key, val in data.items() if key in ['title','description','price','instructor','level_id','category_id','id']]
                            print(data_POST)
                            with connection.cursor() as cursor:
                                query = '''
                                    exec sp_update_course %s,%s,%s,%s,%s,%s,%s;
                                '''
                                cursor.execute(query,data_POST)
                            return redirect(f'/admin-dashboard/{id}/action-add/all-courses')
                        
                    print(data)
                    return render(request,'templates/admin/admin_site/admin_site.html',{
                        'log_decision': log_decision,
                        'mess_error': mess_error,
                        'object_data': object_data,
                        'role': role,
                        'action':params,
                        'data': v_all_courses,
                        })
                except mess_error:
                    raise ValueError(mess_error)
        
    except mess_error:
        raise ValueError(mess_error)






def test(request):
    obj = Users.objects.all()
    return render(request, 'test.html', {
        'objs' : obj,
        'len' : obj.__len__
    })


