## Usage

**Get information:** python path/to/pdf info
**Rotate:** python path/to/pdf rotate int/all angle
**Merge:** python path/to/pdf merge path/to/pdf path/to/pdf ... path/to/pdf
**Split:** python path/to/pdf split int out_dir
**Protect:** python path/to/pdf protect password

Output will, in the case of rotate, merge and protect be filename of first pdf file + _method.pdf and split with create two files, split_1.pdf for the first part of the split and split_2.pdf for the last part.