try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

import os

import collectmeterdigits

my_project_path = os.path.abspath(os.path.dirname(__file__))

install_reqs = parse_requirements('requirements.txt', session='hack')
print(install_reqs)
long_description = """
    The program readout digital meter images from edgeAI devices, collect the images 
    and removes duplicated.
    The images will be anonymized (name replaced with hash).
    At last step, the images will be pre labeled by a neuronal network
    """

setup(
    name='collectmeterdigits',
    version='0.1.0',
    url='https://github.com/haverland/collectmeterdigits',
    license='Apache 2.0',
    author='Frank Haverland',
    author_email='iotson@t-online.de',
    install_requires=[str(requirement.requirement) for requirement in install_reqs],
    tests_require=['nose'],
    packages=find_packages(exclude=['tests']),
    description='Reads images from digital meters.',
    long_description = long_description,
    platforms='any',
    keywords = "different tags here",
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Operating System :: Linux',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],

    )