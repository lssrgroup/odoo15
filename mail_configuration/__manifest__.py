{
    "name": """Mail Configuration""",
    "summary": """Company wise outgoing mail configuration""",
    "category": "Hidden/Tools",
    "version": "15.0.0.0",
    "application": False,
    "author": "Prime Minds Consulting Services",
    "website": "http://primeminds.co",
    "license": "LGPL-3",  # MIT
    "depends": ["base",'mail'],
    "data": [
        "views/ir_mail_server_inherit.xml",
    ],
    "qweb": [
    ],
    "auto_install": False,
    "installable": True,
}
