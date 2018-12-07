import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name='DopedCat',
        version="0.0.0",
        description='Python code for dopant enumeration on catalyst surfaces',
        author='Hieu Doan',
        author_email='hieu.a.doan@gmail.com',

        packages=[
                'dopedcat'
                ],
        package_dir={'dopedcat': 'dopedcat'}
    )
