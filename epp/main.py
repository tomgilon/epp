from __future__ import print_function
import argparse
import os
import string
import subprocess
import re


def package_file(name):
	return os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

SETUP_PY_TMPL = package_file('setup.py.tmpl')
GITIGNORE_TMPL = package_file('gitignore.tmpl')


class Project(object):
	version = '1.0.0'
	@property
	def name(self):
		return os.path.basename(os.getcwd())

	def get_requirements(self):
		return subprocess.check_output(". venv/bin/activate; pip freeze", shell=True).decode().split()


def create_setup_script(project):
	if os.path.exists('setup.py'):
		print('Setup file \'setup.py\' exists, skipping creation.')
		return

	with open(SETUP_PY_TMPL, "r") as f:
		tmpl = string.Template(f.read())

	with open("setup.py", "w") as f:
		f.write(tmpl.substitute({
				'name': project.name,
				'ver': project.version,
				'requirements': project.get_requirements(),
				'console_scripts': ['{0}={0}/main:main'.format(project.name)]
				}))


def create_gitignore(project):
	with open(GITIGNORE_TMPL, 'r') as tmpl:
		with open('.gitignore', 'w') as res:
			res.write(tmpl.read())


def create_virtualenv(project):
	if os.path.exists('venv'):
		print('Directory \'venv\' exists, not creating a virtual environment.')
		return

	os.system("virtualenv venv --no-site-packages")


def create_git_repo(project):
	if os.path.exists(".git"):
		print('git repository seems to already exist, skipping.')
		return

	os.system("git init")
	

def git_add(filename):
	os.system("git add {}".format(filename))


def move_code_to_subdir(project):
	if os.path.exists(project.name):
		print('Subdirectory \'{}\' already exists, skipping.'.format(project.name))
		return

	os.system("mkdir {0} && mv `ls | grep -v venv | grep -v setup.py` {0}/ 2>/dev/null".format(project.name))


def new_project(args):
	project = Project()

	if args.create_venv:
		create_virtualenv(project)

	create_git_repo(project)
	create_setup_script(project)
	git_add('setup.py')	
	create_gitignore(project)
	git_add('.gitignore')
	move_code_to_subdir(project)
	git_add('{}/'.format(project.name))
	

	print(
		  'Great !\n'
		  'You can now use \'epp go\' to start using your new virtual environment\n'
		  'You can now use \'epp requ\' to update your project\'s requirements\n'
		  'See \'epp --help\''
		)


def activate_env(args):
	os.system("bash -c \"exec bash --rcfile <(echo '. ~/.bashrc; . ./venv/bin/activate')\"")


def add_requirements(args):
	project = Project()
	with open('setup.py', 'r') as f:
		data = f.read()

	r = re.search(r"install_requires=(\[[,'\"=\.\w\d\s]*\])", data)
	if not r:
		print("Can't add requirements")
		return

	data = data.replace(r.groups()[0], str(project.get_requirements()))
	with open('setup.py', 'w') as f:
		f.write(data)

	os.system("git diff setup.py")


def main():
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers(dest='command')
	subparsers.required = True

	new = subparsers.add_parser('new', help='Initialize a new project in the current directory')
	new.set_defaults(func=new_project)
	new.add_argument('--no-venv', dest='create_venv', default=True, action='store_false', help='Do not create a virtual environemnt for the project')

	go = subparsers.add_parser('go', help='Open a shell in the project\'s virtual environment(the project within the current directory)')
	go.set_defaults(func=activate_env)

	requ = subparsers.add_parser('requ', help='Update the package\'s requirements in the setup.py script(based on the packages which are currently installed)')
	requ.set_defaults(func=add_requirements)

	args = parser.parse_args()
	args.func(args)


if __name__ == '__main__':
	main()
