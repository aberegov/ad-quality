from distutils.core import setup

setup(
    name='ad-quality',
    version='1.0.0',
    packages=['com', 'com.conversant', 'com.conversant.common', 'com.conversant.simulators',
              'com.conversant.viewability', 'unit', 'unit.conversant', 'unit.conversant.common',
              'unit.conversant.viewability'],
    package_dir={'com': 'src/com', 'unit': 'test/unit'},
    url='',
    license='',
    author='beregov',
    author_email='alekseyberegov@gmail.com',
    description=''
)
