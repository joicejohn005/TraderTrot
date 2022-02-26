
def user_reqmanage(request):
    if request.session.is_empty():
        return HttpResponseRedirect('/login')
    id=request.session['id']    
    requestdata = doubt_tbl.objects.filter(login_id=id)
    return render(request,'user_reqmanage.html',{"ureq":requestdata})

def user_reqdetails(request,id):
    if request.session.is_empty():
        return HttpResponseRedirect('/login')
    reqdetail = doubt_tbl.objects.get(id=id)
    return render(request,'user_reqdetails.html',{"reqdet":reqdetail})