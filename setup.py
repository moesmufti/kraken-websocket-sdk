from setuptools import setup, find_packages
import os

# Read the contents of README.md
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kraken-websocket-sdk', 
    version='0.1.1',
    author='Mustafa "Moes" Mufti',
    author_email='moes.mufti@icloud.com',
    description='A Python package for interacting with Kraken WebSocket API',
    long_description='A Python package for interacting with Kraken WebSocket API',
    long_description_content_type='text/markdown',
    url='https://github.com/moesmufti/kraken-websocket-sdk', 
    packages=find_packages(),
    install_requires=[
        'pydantic>=2.9.2',
        'websockets>=13.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.12',
    entry_points={
        'console_scripts': [
            'kraken-ws=kraken_ws.kraken_ws_example:main',
        ],
    },
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
)
