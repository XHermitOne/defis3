from distutils.core import setup
from distutils.filelist import findall
import py2exe
import os
from .pyreditor import __version__ as ver
from .pyreditor import __author__ as author
from .pyreditor import __authormail__ as author_email

OS = 'w7'
#OS = 'xp'

if OS.lower() == 'xp':
        manifest_template = '''
        <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
        <assemblyIdentity
            version="5.0.0.0"
            processorArchitecture="x86"
            name="%(prog)s"
            type="win32"
        />
        <description>%(prog)s Program</description>
        <dependency>
            <dependentAssembly>
                <assemblyIdentity
                    type="win32"
                    name="Microsoft.Windows.Common-Controls"
                    version="6.0.0.0"
                    processorArchitecture="X86"
                    publicKeyToken="6595b64144ccf1df"
                    language="*"
                />
            </dependentAssembly>
        </dependency>
        </assembly>
        '''
        RT_MANIFEST = 24
elif OS.lower() == 'w7':
        manifest_template = '''
        <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
          <assemblyIdentity type="win32"
                            name="%(prog)s"
                            version="6.0.0.0"
                            processorArchitecture="x86"
                            publicKeyToken="0000000000000000"
          />
          <description>%(prog)s Program</description>
          <dependency>
            <dependentAssembly>
              <assemblyIdentity type="win32"
                                name="Microsoft.Windows.Common-Controls"
                                version="6.0.0.0"
                                processorArchitecture="X86"
                                publicKeyToken="0000000000000000"
                                language="*"
              />
            </dependentAssembly>
          </dependency>
        </assembly>
        '''

        RT_MANIFEST = 32

options = {"py2exe": {"compressed": 0,
                      "optimize": 2,
                      "bundle_files": 3}}

data = ['pyreditor.ico',\
        'pyreditor.bmp',\
        'readme.txt',\
        'rehelp.txt',\
        'bugs.txt',\
        'pyreditor.cfg',\
        'templates.cfg',\
        'history.txt',\
        'plugin-install.txt',\
        'todo.txt',\
        'license.txt'
        ]

# Extend data with all the files from the named subdirs
add_dirs = [r'images', r'demos']
for add_dir in add_dirs:
    add_data = findall(add_dir)
    files = []
    for f in add_data:
        dirname = os.path.join(add_dir, f[len(add_dir)+1:])
        files.append((os.path.split(dirname)[0], [f]))
    data.extend(files)
        
setup(
    version = ver,
    description = "PyReditor - Python Regular Expression Editor",
    author = author,
    author_email = author_email,
    url='http://www./',
    name = "pyreditor",
    options = options,
    zipfile='library.dat',

    # targets to build
    windows = [{"script":"pyreditor.pyw",
                "icon_resources": [(1, "pyreditor.ico")],
                'other_resources':
                    [(RT_MANIFEST, 1, manifest_template % dict(prog="pyreditor"))]
                }],
    data_files = data
    )