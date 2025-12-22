def navbar_visibility(request):
    match = request.resolver_match
    return {
        "show_navbar": not match or match.url_name != "welcome"
    }
