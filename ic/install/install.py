#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Инсталяционный скрипт DEFIS и прикладных систем под Linux.
"""

# --- Подключение библиотек ---
import sys
import os
import os.path

__version__ = (0, 0, 1, 2)


# --- Секция основных настроек ---
# Полное имя устанавливаемого пакета
__package_name__ = '%s'

# Требуемые пакеты
required_packages = [('python', '2.7.1'), ('wxPython', '3.0.2.1'), ('sqlalchemy', '0.8.1')]


# --- Запуск инсталяции ---
# Сначала необходимо проверить под каким пользователем запущена инсталяция
cur_user = os.popen('whoami').read().strip()
if cur_user != 'root':
	print(u'ВНИМАНИЕ: Инсталяция возможна только под польхователем root.')
	exit(0)


# Проверка установленных пакетов
for pkg in required_packages:
	print(u'Проверка требуемого пакета: %s версии: %s ' % pkg)
	installed_pkgs = os.popen('rpm -qa | grep %s' % pkg[0]).readlines()
	find_requered_pkg = False
	for installed_pkg in installed_pkgs:
		print(installed_pkg.strip())
		if installed_pkg.find(pkg[0]) > 0:
			if pkg[1]:
				# Необходимо проверить версию
				if installed_pkg.find(pkg[1]) > 0:
					find_requered_pkg = True
					break
			else:
				find_requered_pkg = True
				break
	if 	not find_requered_pkg:
		# Требуемый пакет не найден
		print(u'ВНИМАНИЕ: Требуемый для работы пакет %s версии %s не найден.' % pkg)
		exit(0)
	else:
		print(u'Ok')


# Запрос инсталяционной папки
install_dir = input(u'Введите полный путь к инсталяционной папке: ')

if not os.path.exist(install_dir):
	os.makedirs(install_dir)

# Расппаковка основного пакета в инсталяционную папку
if os.path.splitext(__package_name__)[1].lower() == '.zip':
	# Зазипованный пакет
	cmd = 'unzip %s -d %s' % (__package_name__, install_dir)
	print(u'Распаковка  пакета: <%s>' % cmd)
	os.system(cmd)

# Создание PTH файлов
site_packages_dir = os.path.join(sys.prefix, sys.lib, 'python',
								 str(sys.version_info[0])+'.'+str(sys.version_info[1]),
								 'site-packages')

defis_pth_file_name = os.path.join(site_packages_dir, 'defis.pth')
f_pth = None
try:
	f_pth = open(defis_pth_file_name, 'w')
	f_pth.write(os.path.dirname(install_dir))
	f_pth.close()
except:
	if f_pth:
		f_pth.close()
	raise

ic_pth_file_name = site_packages_dir+'ic.pth'
f_pth = None
try:
	f_pth = open(ic_pth_file_name, 'w')
	f_pth.write(install_dir)
	f_pth.close()
except:
	if f_pth:
		f_pth.close()
	raise

print(u'Инсталяция пакета прошла успешно')
