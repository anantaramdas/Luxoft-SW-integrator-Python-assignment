# Luxoft (SW integrator interview)  Python assignment

## Task overview
Will be checked coding style and possibility of script extension

## Task description

Write class which will handle 7zip and zip files. It should be able to accept single archive, list and folder of archives and should be able to unpack inner archives.
Class should be able to handle properly archives separated into parts - i.e. multipart archives.

If any exception occur we should stop any further execution.

Script should contain `main()` function which can provide information and execution example i.e help info with examples.

## Setup and execution

### Prerequisites

You should have `python` installed on your machine in order to run this. I have used and tested this only on `3.9.7`

You should install all dependencies using `pipenv` by running 

```bash
pipenv install
``` 

or manually running:

```bash
pip install patool pyunpack
```

### Execution
Run this program as ordinary python application providing as a first argument destination path followed my archive(-s) to extract 

Please run `python main.py --help` for more execution information

### Example test runs

`$ python main.py ./example/dest/ ./example/test_0/test.txt` gives error that provided file is not archive

`$ python main.py ./example/dest/ ./example/test_1` will unpack everything from archive to `./example/dest folder even inner archive`

`$ python main.py ./example/dest/ ./example/test_2` will be interrupted because of corrupted archive

`$ python main.py ./example/dest/ ./example/test_3` will unpack multipart archive to target directory

`$ python main.py ./example/dest/ ./example/test_4` will unpack with inner multipart archive to `./example/dest folder

## Extending

You could easily add new type of archive by extending `ArchiveAbstract` class and implementing `extensions`
`decompress` methods. You could use two existing implementations (`Archive7Zip` and `ArchiveZip`) as an example.

## Limitations

Only 7Zip utility created multipart archive currently supported. 