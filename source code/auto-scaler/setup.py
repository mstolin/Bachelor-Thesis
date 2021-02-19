from setuptools import setup

requires = ['aiohttp', 'apscheduler', 'docker', 'pytest', 'pyyaml']

setup(name='auto-scaler',
      install_requires=requires,
      author='Marcel Stolin',
      author_email='marcel.pascal.stolin@ipa.fraunhofer.de')
