from setuptools import setup

requirements = {
    "package": [
        'six',
        'requests',
        'yamlsettings>=1.0.1',
    ],
    "setup": [
        "pytest-runner",
    ],
    "test": [
        "responses",
        "pytest",
        "pytest-pudb",
    ],
}

requirements.update(all=sorted(set().union(*requirements.values())))

setup(
    name='yamlsettings-requests',
    version='1.0.0',
    author='Kyle Walker',
    author_email='KyleJamesWalker@gmail.com',
    description='Quick Example',
    py_modules=['yamlsettings_requests'],
    extras_require=requirements,
    install_requires=requirements['package'],
    setup_requires=requirements['setup'],
    tests_require=requirements['test'],
    entry_points={
        'yamlsettings10': [
            'ext = yamlsettings_requests:RequestsExtension',
        ],
    },
)
