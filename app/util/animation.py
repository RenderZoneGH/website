def a(request):
    return True if request.args.get('ani') == 'true' else False