from setuptools import setup

package_name = 'my_first_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='chinmayagouda',
    maintainer_email='chinmayagouda@todo.todo',
    description='My first ROS2 package',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'simple_publisher = my_first_pkg.simple_publisher:main',
            'cmd_vel_publisher = my_first_pkg.cmd_vel_publisher:main',
            'turn_90_controller = my_first_pkg.turn_90_controller:main',
	    'wall_stop = my_first_pkg.wall_stop:main',
        ],
    },
)
