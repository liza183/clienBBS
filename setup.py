from setuptools import setup


setup(
    name='clienBBS',
    version='1.0.0',
    description='Retro-feeling BBS interface for Clien',
    long_description='',  # RestructuredText 문자열 넣으면 pypi.org 프로젝트 페이지에 표시
    url='https://github.com/liza183/clienBBS',
    author='Matt Sangkeun Lee',
    author_email='Matt Sangkeun Lee',
    license='Private',  # 알맞게 고쳐주세요!
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=[],
    py_modules=['clien'],
    python_requires='>=3.5',
    install_requires=[
        'urllib3',
        'bs4',
        'certifi',
        'requests',
        'pyreadline',
        'lxml',
        'image',
    ],
    entry_points={
        'console_scripts': [
            'clien = clien:main',
        ]
    },
)
