def navbar_visibility(request):
    match = request.resolver_match
    no_sidebar_pages = ["welcome", "login", "sign-up"]
    return {"show_sidebar": not match or match.url_name not in no_sidebar_pages}
