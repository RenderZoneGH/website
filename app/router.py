
"""
| -------------------------------------------------------------------
| Index
| -------------------------------------------------------------------
| 
| Route: /
"""
import app.routes.index as index
index.init("/")

"""
| -------------------------------------------------------------------
| Browse
| -------------------------------------------------------------------
|
| Route: /browse
"""
import app.routes.browse as browse
browse.init("/browse")

"""
| -------------------------------------------------------------------
| Generate
| -------------------------------------------------------------------
|
| Route: /generate/<uuid>
"""
import app.routes.generate as generate
generate.init("/generate/<uuid>")

"""
| -------------------------------------------------------------------
| Checkout
| -------------------------------------------------------------------
|
| Route: /checkout/<uuid>
| Route: /checkout/<uuid>/generate
"""
import app.routes.checkout as checkout
checkout.init("/checkout/<uuid>")
import app.routes.checkout_generate as checkout_generate
checkout_generate.init("/checkout/<uuid>/render")

"""
| -------------------------------------------------------------------
| Generating
| -------------------------------------------------------------------
|
| Route: /generating/<uuid>
"""
import app.routes.generating as generating
generating.init("/generating/<uuid>")



"""
| -------------------------------------------------------------------
                         API Routes

    All API routes are automatically prefixed with /api/v1/
| -------------------------------------------------------------------
"""

"""
| -------------------------------------------------------------------
| API: Get job
| -------------------------------------------------------------------
|
| Route: /api/v1/job/<uuid>
| Method: GET
| No authentication required
"""
import app.routes.api.job as api_job
api_job.init("/job/<uuid>")

"""
| -------------------------------------------------------------------
| API PayPal Middleware
| -------------------------------------------------------------------
|
| Route: /api/v1/paypal/payment/<jobuuid>
| Route: /api/v1/paypal/payment/execute/<jobuuid>
| Method: POST
| No authentication required
"""
import app.routes.api.paypal_payment as api_paypal
api_paypal.init("/paypal/payment/<jobuuid>")

"""
| -------------------------------------------------------------------
                    Admin Routes
| -------------------------------------------------------------------
"""

"""
| -------------------------------------------------------------------
| Admin: Index
| -------------------------------------------------------------------
|
| Route: /admin
"""
import app.routes.admin.index as admin_index
admin_index.init("/admin")

"""
| -------------------------------------------------------------------
| Admin: Login
| -------------------------------------------------------------------
|
| Route: /admin/login
"""
import app.routes.admin.login as admin_login
admin_login.init("/admin/login")

"""
| -------------------------------------------------------------------
| Admin: Logout
| -------------------------------------------------------------------
|
| Route: /admin/logout
"""
import app.routes.admin.logout as admin_logout
admin_logout.init("/admin/logout")

"""
| -------------------------------------------------------------------
| Admin: Dashboard
| -------------------------------------------------------------------
|
| Route: /admin/analytics
"""
import app.routes.admin.analytics as admin_analytics
admin_analytics.init("/admin/analytics")
