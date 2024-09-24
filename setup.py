from setuptools import setup, find_packages

setup(
    name='matching_algorithms',
    version='0.1.0',
    author='Irfan Tekdir',
    author_email='irfan.tekdir@gmail.com',
    description='A collection of matching algorithms for applications like school choice, job assignments and marriage markets.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Tekdirfan/Matching-Algorithms.git',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=['numpy', 'random', 'pulp'
        
    ],
    
)

