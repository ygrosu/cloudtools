__author__ = 'yairgrosu'


from setuptools import setup


setup(
    name='cloudtools',
    version='0.2',
    packages=['ec2ools'],
    url='www.grosu.io',
    license='',
    author='yairgrosu',
    author_email='yair@grosu.io',
    description='cloudtools - your AWS swiss army knife',
    entry_points={
        'console_scripts': [
            'ec2ls = ec2ools.ec2ls:main',
        ]
    },
    requires=['boto', 'setuptools']
)



