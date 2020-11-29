import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uzemszunet",
    version="0.0.1",
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
            "pandas",
            "xlrd"
    ],
    entry_points={
        'console_scripts': [
            'uzemszunet = uzemszunet.__main__:main'
        ]
    },
    package_data={'uzemszunet': ['uzemszunet.cfg']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: Public Domain',
        'Intended Audience :: System Administrators',
        'Natural Language :: Hungarian',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Communications :: Email',
        'Topic :: Utilities',
    ]
)
