from django.shortcuts import redirect
from django.urls import reverse

class StaffRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect(reverse('login_required'))
        return super().dispatch(request, *args, **kwargs)
