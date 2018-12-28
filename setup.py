from setuptools import find_packages, setup

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
        name='csvcal',
        version='0.0.1',
        author='Florian Limberger',
        author_email='flo@snakeoilproductions.net',
        license='BSD',
        description='An iCalendar to CSV converter',
        long_description=long_description,
        long_description_content_type='text/x-rst',
        url='https://github.com/flimberger/csvcal',
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Console',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Topic :: Office/Business :: Scheduling',
            'Topic :: Utilities'
        ],
        install_requires=['icalendar'],
        py_modules=['csvcal'],
        scripts=['csvcal.py']
)
