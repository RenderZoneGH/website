from app.util.env import env

config = {
    """
    |--------------------------------------------------------------------------
    | Application Version
    |--------------------------------------------------------------------------
    |
    | This value is set when creating a RenderZone release.
    |
    """
    'version': 'canary',

    """
    |--------------------------------------------------------------------------
    | Application Environment
    |--------------------------------------------------------------------------
    |
    | This value determines the "environment" your application.
    | dev/prod
    |
    """
    'env': env('ENVIORMENT', 'prod'),

    """
    |--------------------------------------------------------------------------
    | Application Debug Mode
    |--------------------------------------------------------------------------
    |
    | When your application is in debug mode, detailed error messages will be
    | shown on every error that occurs within your application. If disabled,
    | a simple generic error page is shown.
    |
    """
    # 'debug': True,
    'debug': True if env('ENVIORMENT', 'prod') == 'dev' else False,
    
    """
    |--------------------------------------------------------------------------
    | Application URL
    |--------------------------------------------------------------------------
    |
    | This URL is used by the application to link to assets.
    | You should set this to the root of your application so that it is used
    |
    """
    'url': env('APP_URL', 'http://localhost:5000'),

}