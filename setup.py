from setuptools import setup, find_packages

import metadata as m

install_requires = [
    'fabric >= 1.9'
]

setup(
    name=m.name,
    version=m.version,
    description=m.description,
    url=m.project_url,
    author=m.author,
    author_email=m.author_email,
    license=m.license,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
)
