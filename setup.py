from setuptools import setup, find_packages

setup(
    name='matching_algorithms',
    version='0.1.0',
    author='Irfan Tekdir',
    author_email='irfan.tekdir@gmail.com',
    description='This project implements a variety of matching algorithms, including the Deferred Acceptance algorithm, the Boston Mechanism, the Top Trading Cycles (TTC) mechanism, and several linear programming approaches. These algorithms are widely applicable in various domains such as school admissions, job assignments, and resource allocation problems. Their effectiveness in creating stable and efficient matchings makes them valuable tools in economics, computer science and operations research.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Tekdirfan/Matching-Algorithms.git',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=['numpy', 'pulp'],
    
)

