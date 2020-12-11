import setuptools
import os

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('uzemszunet/templates')

setuptools.setup(
    name="uzemszunet",
    version="0.0.5",
    author="Ferenc Nánási",
    author_email="husudosu94@gmail.com",
    description="Üzemszünetek lekérdezése",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/husudosu/uzemszunet",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
            "requests",
            "pandas==1.1.5",
            "xlrd==1.2.0",
            "jinja2"
    ],
    entry_points={
        'console_scripts': [
            'uzemszunet = uzemszunet.__main__:main'
        ]
    },
    package_data={
        'uzemszunet': ['uzemszunet.cfg', *extra_files],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: System Administrators',
        'Natural Language :: Hungarian',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Communications :: Email',
        'Topic :: Utilities',
    ]
)
