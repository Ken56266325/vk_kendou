from setuptools import setup, find_packages

setup(
    name="vk_kendou",
    version="1.0.0",
    author="Kenny",
    author_email="mampifaly56266325@gmail.com",
    description="VK automation library",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0",
        "urllib3>=1.26.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    zip_safe=False,
)
