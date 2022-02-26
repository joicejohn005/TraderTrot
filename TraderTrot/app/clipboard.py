def tradebook(request):
    if request.session.is_empty():
        return HttpResponseRedirect('/login')
    tradedata = tradebook_tbl.objects.all()
    return render(request,'tradebook.html',{"td":tradedata})

def user_reqmanage(request):
    if request.session.is_empty():
        return HttpResponseRedirect('/login')
    id=request.session['id']    
    requestdata = doubt_tbl.objects.filter(login_id=id)
    return render(request,'user_reqmanage.html',{"ureq":requestdata})
