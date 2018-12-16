from setuptools import setup,find_packages

setup(name='examc',
      version='0.1',
      description='an exam document generator (exam and solution)',
      url='',
      author='Pierre Bayerl',
      author_email='pierre.bayerl@googlemail.com',
      license='MIT',
      packages=find_packages(),
      package_data={'': ['*.tx', '*.template', 'support_*_code/**/*']},
      install_requires=["textx","arpeggio","jinja2"],
      tests_require=[
          'pytest',
      ],
      keywords="exam DSL",
      entry_points={
          'console_scripts': [
              'examc=examc.console:examc',
          ]
      },
      )


# to play around without installing: do "export PYTHONPATH=."