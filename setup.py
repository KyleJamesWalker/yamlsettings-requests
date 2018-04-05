from setuptools import setup

setup(
    name='yamlsettings-requests',
    version='1.0.0',
    author='Kyle Walker',
    author_email='KyleJamesWalker@gmail.com',
    description='Quick Example',
    py_modules=['yamlsettings_requests'],
    install_requires=[
        'requests',
        'yamlsettings>=1.0.1',

    ],
    entry_points={
        'yamlsettings10': [
            'ext = yamlsettings_requests:RequestsExtension',
        ],
    },
)
