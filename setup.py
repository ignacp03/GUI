from setuptools import setup, find_packages

setup(
    name='KLabGUI',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'PyQt5 = 5.15.11',
        'watchdog =6.0.0',
        'matplotlib = 3.8.3',
        'numpy= 1.26.4 ',
        'imageio = 2.36.0',
        'scipy =  1.12.0',
        'pandas = 2.2.2',
        # ...
    ],
    #entry_points={
        #'console_scripts': [
        #    'klabgui=KLabGUI:main',  # Replace `main` with your main entry function if needed.
        #],
    #},
    author="Ignacio Perez Ramos",
    author_email="ignacio.perez@icfo.eu",
    description="Simple GUI for monitoring and processing absorpton images",
    url="https://github.com/ignacp03/GUI"
)
