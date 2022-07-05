import sysconfig
import sys
import os
import subprocess
import re
from setuptools import setup, find_packages

setup(
    # package information
    name='ocms_rnaseq',
    version="0.0.1",
    description='OCMS_RNAseq : Oxford Centre for Microbiome Studies pipelines for RNAseq processing'
    author='Nicholas Ilott',
    license="MIT",
    platforms=["any"],
    keywords="RNAseq, genomics",
    url="https://github.com/OxfordCMS/OCMS_RNAseq",
    packages=find_packages("./") + find_packages("./ocmsrnaseq/"),
    entry_points={
        'console_scripts': ['ocms_rnaseq = ocmsrnaseq.ocms_rnaseqs:main']
    },
    include_package_data=True,
    python_requires='>=3.6.0'                                            
)

