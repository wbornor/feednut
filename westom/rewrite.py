

class RewiteLocalForwardedRequest:

    def process_request(self, request):
        if request.META.has_key('HTTP_X_FORWARDED_HOST'):
            request.META['HTTP_HOST'] = request.META['HTTP_X_FORWARDED_HOST']
        #request.META['SERVER_NAME'] = request.META['HTTP_X_FORWARDED_HOST']
