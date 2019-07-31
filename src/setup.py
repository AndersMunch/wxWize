from setuptools import setup

with open('../README.rst','rb') as f:
    long_description = f.read().decode('utf-8')

setup(
    name='wxWize',
    version='1.1.0',
    description='wxPython object builder',
    long_description=long_description,
    url='https://github.com/AndersMunch/wxWize',
    author='Anders Munch',
    author_email='ajm@jmunch.dk',
    license='WTFPL',
    py_modules=['wize'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Environment :: MacOS X :: Carbon',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: GTK',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Topic :: Software Development :: User Interfaces ',
        ],
    keywords='wxPython wxWidgets sizers',
)
