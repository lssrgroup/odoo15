{
    "name": """Project Website""",
    "summary": """Project Customization and webiste Integration """,
    "category": "Hidden/Tools",
    "version": "15.0.0.6",
    "application": False,
    "sequence": 10,
    "author": "Prime Minds Consulting Services",
    "website": "http://primeminds.co",
    "license": "LGPL-3",  # MIT
    "depends": ["project", "website"],
    "data": [
        "data/project_webpage_form.xml",
        "data/uk_incorporations_website_form_view.xml",
        "data/website_page_data.xml",
        "views/project_task_inherit.xml",
        "views/project_project_field_view_inherit.xml"
    ],
    "qweb": [
    ],
    "auto_install": False,
    "installable": True,
}
