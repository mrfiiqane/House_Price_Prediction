# For Vercel serverless
def handler(request):
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    from flask import Response
    with app.test_request_context(
        path=request.path,
        method=request.method,
        headers=request.headers,
        data=request.get_data()
    ):
        resp = app.full_dispatch_request()
        return Response(resp.get_data(), status=resp.status_code, headers=dict(resp.headers))
