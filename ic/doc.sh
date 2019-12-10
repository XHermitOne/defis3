# sudo apt install python3-sphinx
# pip3 install sphinx-epytext
rm --recursive /mnt/defis/defis3/ic/doc/*.*

# epydoc --debug --fail-on-error --html --graph umlclasstree --output /mnt/defis/defis3/ic/doc ic
# epydoc --debug --html --output /mnt/defis/defis3/ic/doc ic

#sphinx-apidoc --separate --full --output-dir /mnt/defis/defis3/ic/doc ./

# I was running Sphinx under Python 3, thus needed:
#sed -i.bak "s/ python / python3 /g" /mnt/defis/defis3/ic/doc/Makefile
# Note Bio.Restriction breaks Sphinx, so skip it entirely!
#
# Exception occurred:
#   File ".../site-packages/Bio/Restriction/Restriction.py", line 341, in __len__
#     return cls.size
# AttributeError: type object 'RestrictionType' has no attribute 'size'
#
#rm -rf /mnt/defis/defis3/ic/doc/ic.Restriction.*
#make -C /mnt/defis/defis3/ic/doc/ html

#cd /mnt/defis/defis3/ic/doc/
#python3 ~/.local/lib/python3.6/site-packages/sphinx/cmd/quickstart.py
# python3 ~/.local/lib/python3.6/site-packages/sphinx/cmd/build.py -a ./ /mnt/defis/defis3/ic/doc
