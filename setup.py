import setuptools  
  
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name="trello_client_Vit_An", version="0.0.1", author="Roshchupkin Vitali", author_email="elpistolero1999@gmail.com", description="Консольный клиент для Trello", long_description=long_description, long_description_content_type="text/markdown", url="https://github.com/VitAn1999/-SkillFactory-D1-", packages=setuptools.find_packages(), classifiers=[ "Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License", "Operating System :: OS Independent", ], python_requires='>=3.6')