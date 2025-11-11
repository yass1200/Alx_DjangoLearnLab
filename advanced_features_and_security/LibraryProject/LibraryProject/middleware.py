# LibraryProject/middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    """
    Minimal CSP middleware without extra packages.
    Reads simple string directives from settings:
      CSP_DEFAULT_SRC, CSP_SCRIPT_SRC, CSP_STYLE_SRC, etc.
    """

    def process_response(self, request, response):
        # Build a simple CSP from settings values if present
        directives = []
        for key, name in [
            ("CSP_DEFAULT_SRC", "default-src"),
            ("CSP_SCRIPT_SRC", "script-src"),
            ("CSP_STYLE_SRC", "style-src"),
            ("CSP_IMG_SRC", "img-src"),
            ("CSP_FONT_SRC", "font-src"),
            ("CSP_CONNECT_SRC", "connect-src"),
            ("CSP_FRAME_SRC", "frame-src"),
        ]:
            val = getattr(settings, key, None)
            if val:
                directives.append(f"{name} {val}")

        if directives:
            response["Content-Security-Policy"] = "; ".join(directives)
        return response
