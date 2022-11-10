
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
| Claim Coupon
| -------------------------------------------------------------------
|
| Route: /coupon/checkout/<uuid>
"""
import app.routes.claim_coupon as coupon_checkout

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

"""
| -------------------------------------------------------------------
| Admin: Jobs
| -------------------------------------------------------------------
|
| Route: /admin/jobs
"""
import app.routes.admin.jobs as admin_jobs
admin_jobs.init("/admin/jobs")

"""
| -------------------------------------------------------------------
| Admin: All Jobs
| -------------------------------------------------------------------
|
| Route: /admin/jobs/all
"""
import app.routes.admin.all_jobs as admin_jobs_all
admin_jobs_all.init("/admin/jobs/all")

"""
| -------------------------------------------------------------------
| Admin: Products
| -------------------------------------------------------------------
|
| Route: /admin/products
"""
import app.routes.admin.products as admin_products
admin_products.init("/admin/products")

"""
| -------------------------------------------------------------------
| Admin: Edit Product
| -------------------------------------------------------------------
|
| Route: /admin/products/edit/<uuid>
"""
import app.routes.admin.edit_template as admin_edit_template
admin_edit_template.init("/admin/products/edit/<uuid>")

"""
| -------------------------------------------------------------------
| Admin: Coupons
| -------------------------------------------------------------------
|
| Route: /admin/products/coupons
"""
import app.routes.admin.coupons as admin_coupons
admin_coupons.init("/admin/products/coupons")

"""
| -------------------------------------------------------------------
| Admin: Edit Coupon
| -------------------------------------------------------------------
|
| Route: /admin/products/coupons/edit/<code>
"""
import app.routes.admin.edit_coupon as admin_edit_coupon
admin_edit_coupon.init("/admin/products/coupons/edit/<code>")

"""
| -------------------------------------------------------------------
| Admin: Delete Coupon
| -------------------------------------------------------------------
|
| Route: /admin/products/coupons/delete/<code>
"""
import app.routes.admin.delete_coupon as admin_delete_coupon
admin_delete_coupon.init("/admin/products/coupons/delete/<code>")

"""
| -------------------------------------------------------------------
| Admin: Create Coupon
| -------------------------------------------------------------------
|
| Route: /admin/products/coupons/new
"""
import app.routes.admin.new_coupon as admin_create_coupon
admin_create_coupon.init("/admin/products/coupons/new")

