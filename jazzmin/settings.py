import copy

from django.conf import settings
from django.contrib.admin import AdminSite

from .utils import get_admin_url, get_custom_url, get_model_meta, get_app_admin_urls

DEFAULT_SETTINGS = {
    # title of the window
    'site_title': AdminSite.site_title,

    # Title on the login screen
    'site_header': AdminSite.site_header,

    # Relative path to logo for your site, used for favicon and brand on top left (must be present in static files)
    'site_logo': 'adminlte/img/AdminLTELogo.png',

    # Welcome text on the login screen
    'welcome_sign': 'Welcome',

    # Copyright on the footer
    'copyright': '',

    # The model admin to search from the search bar, search bar omitted if excluded
    'search_model': None,

    # Field name on user model that contains avatar image
    'user_avatar': 'avatar',

    ############
    # Top Menu #
    ############

    # Links to put along the nav bar
    'topmenu_links': [],

    #############
    # UI Tweaks #
    #############

    # Relative paths to custom CSS/JS scripts (must be present in static files)
    'custom_css': None,
    'custom_js': None,

    # Whether to show the UI customizer on the sidebar
    'show_ui_builder': False,

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    'show_sidebar': True,

    # Whether to aut expand the menu
    'navigation_expanded': True,

    # Hide these apps when generating side menu e.g (auth)
    'hide_apps': [],

    # Hide these models when generating side menu (e.g auth.user)
    'hide_models': [],

    # List of apps to base side menu ordering off of
    'order_with_respect_to': [],

    # Custom links to append to side menu app groups, keyed on app name
    'custom_links': {},

    # Custom icons per model in the side menu See https://www.fontawesomecheatsheet.com/font-awesome-cheatsheet-5x/
    # for a list of icon classes
    'icons': {
        'auth.user': 'fa-user',
    }
}

#######################################
# Currently available UI tweaks       #
# Use the UI builder to generate this #
#######################################

DEFAULT_UI_TWEAKS = {

    # Small text on the top navbar
    "navbar_small_text": False,

    # Small text on the footer
    "footer_small_text": False,

    # Small text everywhere
    "body_small_text": False,

    # Small text on the brand/logo
    "brand_small_text": False,

    # brand/logo background colour
    "brand_colour": False,

    # Link colour
    "accent": "accent-primary",

    # topmenu colour
    "navbar": "navbar-white navbar-light",

    # topmenu border
    "no_navbar_border": False,

    # sidemenu colour
    "sidebar": "sidebar-dark-primary",

    # sidemenu small text
    "sidebar_nav_small_text": False,

    # Disable expanding on hover of collapsed sidebar
    "sidebar_disable_expand": False,

    # Indent child menu items on sidebar
    "sidebar_nav_child_indent": False,

    # Use a compact sidebar
    "sidebar_nav_compact_style": False,

    # Use the AdminLTE2 style sidebar
    "sidebar_nav_legacy_style": False,

    # Use a flat style sidebar
    "sidebar_nav_flat_style": False,
}


def get_settings():
    jazzmin_settings = copy.deepcopy(DEFAULT_SETTINGS)
    user_settings = {x: y for x, y in getattr(settings, 'JAZZMIN_SETTINGS', {}).items() if y is not None}
    jazzmin_settings.update(user_settings)

    if jazzmin_settings['search_model']:
        jazzmin_settings['search_url'] = get_admin_url(jazzmin_settings['search_model'].lower())
        jazzmin_settings['search_name'] = jazzmin_settings['search_model'].split('.')[-1] + 's'

    for link in jazzmin_settings.get('topmenu_links', []):
        if 'url' in link:
            link['url'] = get_custom_url(link['url'])
        elif 'model' in link:
            link['name'] = get_model_meta(link['model']).verbose_name_plural.title()
            link['url'] = get_admin_url(link['model'])
        elif 'app' in link:
            link['name'] = link['app'].title()
            link['app_children'] = get_app_admin_urls(link['app'])

    jazzmin_settings['hide_apps'] = [x.lower() for x in jazzmin_settings['hide_apps']]
    jazzmin_settings['hide_models'] = [x.lower() for x in jazzmin_settings['hide_models']]

    return jazzmin_settings


def get_ui_tweaks():
    ui_tweaks = copy.deepcopy(DEFAULT_UI_TWEAKS)
    ui_tweaks.update(getattr(settings, 'JAZZMIN_UI_TWEAKS', {}))
    ui_tweaks = {x: y for x, y in ui_tweaks.items() if y not in (None, "", False)}

    bool_map = {
        "navbar_small_text": 'text-sm',
        "footer_small_text": 'text-sm',
        "body_small_text": 'text-sm',
        "brand_small_text": 'text-sm',
        "sidebar_nav_small_text": 'text-sm',
        "no_navbar_border": 'border-bottom-0',
        "sidebar_disable_expand": 'sidebar-no-expand',
        "sidebar_nav_child_indent": 'nav-child-indent',
        "sidebar_nav_compact_style": 'nav-compact',
        "sidebar_nav_legacy_style": 'nav-legacy',
        "sidebar_nav_flat_style": 'nav-flat',
    }

    for key, value in bool_map.items():
        if key in ui_tweaks:
            ui_tweaks[key] = value

    def classes(*args):
        return ' '.join([ui_tweaks.get(arg, '') for arg in args if arg]).strip()

    return {
        'body_classes': classes('accent', 'body_small_text'),
        'sidebar_classes': classes('sidebar', 'sidebar_disable_expand'),
        'navbar_classes': classes('navbar', 'no_nav_border', 'navbar_small_text'),
        'sidebar_list_classes': classes(
            'sidebar_nav_small_text', 'sidebar_nav_flat_style', 'sidebar_nav_legacy_style',
            'sidebar_nav_child_indent', 'sidebar_nav_compact_style'
        ),
        'brand_classes': classes('brand_small_text', 'brand_colour'),
        'footer_classes': classes('footer_small_text')
    }
