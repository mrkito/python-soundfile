#!/usr/bin/env python
import os
from platform import architecture
from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

# environment variables for cross-platform package creation
platform = os.environ.get('PYSOUNDFILE_PLATFORM', sys.platform)
architecture0 = os.environ.get('PYSOUNDFILE_ARCHITECTURE', architecture()[0])

if platform == 'darwin':
    libname = 'libsndfile_' + architecture0 + '.dylib'
elif platform == 'win32':
    libname = 'libsndfile_' + architecture0 + '.dll'
else:
    libname = None

if libname and os.path.isdir('_soundfile_data'):
    packages = ['_soundfile_data']
    package_data = {'_soundfile_data': [libname, 'COPYING']}
    zip_safe = False
else:
    packages = None
    package_data = None
    zip_safe = True


class PyTest(TestCommand):

    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

cmdclass = {'test': PyTest}

try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    pass
else:

    class bdist_wheel_half_pure(bdist_wheel):
        """Create OS-dependent, but Python-independent wheels."""

        def get_tag(self):
            pythons = 'py2.py3'
            if platform == 'darwin':
                if architecture0 == 'x86_64':
                    oses = 'macosx_10_9_x86_64.macosx_11_0_x86_64'
                else:
                    oses = 'macosx_10_9_arm64.macosx_11_0_arm64'
            elif platform == 'win32':
                if architecture0 == '32bit':
                    oses = 'win32'
                else:
                    oses = 'win_amd64'
            else:
                pythons = 'py2.py3'
                oses = 'any'
            return pythons, 'none', oses

    cmdclass['bdist_wheel'] = bdist_wheel_half_pure

setup(
    name='soundfile',
    version='0.11.0',
    description='An audio library based on libsndfile, CFFI and NumPy',
    author='Bastian Bechtold',
    author_email='basti@bastibe.de',
    url='https://github.com/bastibe/python-soundfile',
    keywords=['audio', 'libsndfile'],
    py_modules=['soundfile'],
    packages=packages,
    package_data=package_data,
    zip_safe=zip_safe,
    license='BSD 3-Clause License',
    setup_requires=["cffi>=1.0"],
    install_requires=['cffi>=1.0'],
    cffi_modules=["soundfile_build.py:ffibuilder"],
    extras_require={'numpy': ['numpy']},
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Multimedia :: Sound/Audio',
    ],
    long_description=open('README.rst').read(),
    long_description_content_type="text/x-rst",
    tests_require=['pytest'],
    cmdclass=cmdclass,
)
