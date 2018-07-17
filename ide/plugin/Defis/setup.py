from setuptools import setup

__author__ = 'Kolchanov Alexander'
__doc__ = 'Defis plugin'
__version__ = '0.0.1.2'

setup(name='Defis',          # Plugin Name
      version=__version__,   # Plugin Version
      description=__doc__,   # Short plugin description
      author=__author__,     # Your Name
      author_email='xhermitone@gmail.com',  # Your contact
      license='GPL',        # Plugins licensing info
      packages=['Defis'],   # Package directory name(s)
      entry_points='''
    [Editra.plugins]
    Defis = Defis:DefisProjectPlugin
    ''')
