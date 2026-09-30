from setuptools import setup, find_packages

setup(
    name='antigravity-sync',
    version='1.0.0',
    description='Recover, merge, and inject Antigravity AI chat histories across IDE and Desktop App.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='marioalbu08',
    url='https://github.com/marioalbu08/antigravity-sync',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'blackboxprotobuf>=1.0.1',
    ],
    entry_points={
        'console_scripts': [
            'antigravity-sync=antigravity_sync.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Utilities',
    ],
)
