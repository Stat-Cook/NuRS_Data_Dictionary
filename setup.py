from distutils.core import setup


setup(
    name='nurs_data_reference',
    version='0.1.0',
    packages=['nurs_data_reference',
              "nurs_data_reference.word2reference",
              "nurs_data_reference.cli"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "nurs_spider = nurs_data_reference.cli.nurs_reference_spider:main"
        ]
    }
)
