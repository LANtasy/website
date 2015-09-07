from mezzanine.conf import register_setting

# Admin editable
register_setting(
    name='SITE_TITLE',
    label='Site Title',
    description='Title that will display at the top of the site, and be appended to the content of the HTML title tags '
                'on every page.',
    editable=True,
    default='LANtasy'
)

register_setting(
    name='SITE_TAGLINE',
    label='Tagline',
    description='A tag line that will appear at the top of all pages.',
    editable=True,
    default='LANtasy is Western Canada\'s largest hobby game convention in Victoria, BC. There\'s something for '
            'everybody from tabletop, to miniatures, to video games.'
)


# Not admin editable
register_setting(
    name='SSL_ENABLED',
    label='Enable SSL',
    description='If True, users will be automatically redirected to HTTPS for the URLs specified by the '
                'SSL_FORCE_URL_PREFIXES setting.',
    editable=False,
    default=False
)

register_setting(
    name='SSL_FORCE_HOST',
    label='Force Host',
    description='Host name that the site should always be accessed via that matches the SSL certificate.',
    editable=False,
    default=''
)

register_setting(
    name='GOOGLE_ANALYTICS_ID',
    label='Google Analytics ID',
    description='Google Analytics ID (http://www.google.com/analytics/)',
    editable=False,
    default='UA-66487938-1'
)

#
register_setting(
    name='RICHTEXT_FILTER_LEVEL',
    label='Rich Text filter level',
    description='Protects rich text fields against unsafe HTML tags.',
    editable=False,
    default=1
)
