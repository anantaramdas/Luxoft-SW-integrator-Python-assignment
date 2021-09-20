import os
import os.path

from classes.ArchiveZip import ArchiveZip
from classes.Archive7Zip import Archive7Zip


class Unpacker:
    """
    A class used to represent an Unpacker

    Attributes
    ----------
    files : list
        a list of archives we need to process

    # exclude_similar_names : list
    #     a list of filenames which where processed on similarity screening

    Methods
    -------
    unpack(dir_path, target_same=False)
        Unpacks list of archives and
    """

    files = list()

    def __init__(self, args):
        """
        Constructor of the class.
        During construction we are transforming list of arguments to list of archive files for further processing

        Parameters
        ----------
        args : list
            The list of passed arguments from command line
        """

        for path in args:
            # Making path os absolute
            path = os.path.abspath(path)
            if not os.path.isfile(path) and not os.path.isdir(path):
                # Provided target directory is not a directory - aborting
                print("One of provided arguments is not valid file or folder: " + path)
                print("Please check syntax by running --help argument and try again")
                exit(-1)

            # If current passed argument is a directory
            if os.path.isdir(path):
                for root, directories, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # self.add_archive_to_list_with_split_archive_check_and_combine(file_path)
                        self.add_archive_to_list(file_path, False, False)

            # If current passed argument is a file
            if os.path.isfile(path):
                self.add_archive_to_list(path, True, False)

    def unpack(self, dir_path):
        """
        Method to unpack archives from list.

        Parameters
        ----------
        dir_path : str
            destination directory to unpack the archive
        """

        # Making path os absolute
        dir_path = os.path.abspath(dir_path)

        if not os.path.isdir(dir_path):
            # Provided target directory is not a directory - aborting
            print("Target is not a directory. Please check syntax by running --help argument and try again")
            exit(-1)

        for x in self.files:
            print(x.path)

        if len(self.files):
            print("Unpacking to " + dir_path)

            for el in self.files:
                try:
                    el.decompress(dir_path)
                except OSError:
                    print("Error: Looks like file is corrupted - aborting")
                    exit(-1)

            # Making list of files empty and checking if any nested archives being compressed
            # If so - add them to file list and rerun unpack() method with unpacked archives
            self.files = list()
            for root, directories, files in os.walk(dir_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    self.add_archive_to_list(file_path, False, True)

            if len(self.files) > 0:
                self.unpack(dir_path)
        else:
            print("Warning: provided arguments are not archives or does not contain archives - aborting")
            exit(-1)

    def add_archive_to_list(self, file_path, output_warning=False, to_remove=False):
        """
        Method which adding archive to the file list for further processing

        Parameters
        ----------
        file_path : str
            path to archive file to be added to the list the archive
        output_warning : bool
            do we need to output warning in case file is not archive
        to_remove : bool
            do we need to remove this file after procession or no
        """

        root, extension = os.path.splitext(file_path)

        if extension in ['.001']:
            # If multipart archive we taking first part in account and will process other according to archive type
            extension = os.path.splitext(root)[1] + extension

        # Determining which class instance need to be created and added to list based on extracted extension
        if extension in ArchiveZip.extensions():
            self.files.append(ArchiveZip(file_path, to_remove))
        elif extension in Archive7Zip.extensions():
            self.files.append(Archive7Zip(file_path, to_remove))

        else:
            if output_warning:
                print("Warning: provided file is not archive - " + file_path
                      + " - extension detected is '" + extension + "'")
