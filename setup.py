from setuptools import setup

setup(
    setup_requires=["setuptools >= 40", "wheel >= 0.32", "pytest-runner >= 5.0, <6.0"],
    # Entry point can't be specified in setup.cfg
    entry_points={
        "console_scripts": [
            "covid19-btwa = btwa.__main__:main"
        ]
    },
)
