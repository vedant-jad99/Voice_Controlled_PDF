import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

print(setuptools.find_packages())

setuptools.setup(name='iris_pdfviewer',
                 version='0.1',
                 description='VoicePDF',
                 url='https://github.com/Daishinkan002/Voice_Controlled_PDF',
                 packages=setuptools.find_packages(),
                 install_requires=[
                     'Pillow',
                     'pdfplumber',
                     'PyPDF2',
                 ],
                 zip_safe=False)
