import ntpath
import os
import glob

from abc import abstractmethod


class ArchiveAbstract:
    """
    An abstract class used to represent an basic archive and related methods

    Attributes
    ----------
    path : str
        a path to archive file
    basename : str
        file name with extension
    basename_wo_ext : str
        file name without extension
    to_remove : bool
        if file required to be removed after processing
    is_multipart : bool
        if archive file happened to be multipart
    multipart_array_list : list
        if archive file happened to be multipart this field will contain all path'es to all parts

    Methods
    -------
    extensions : list
        :returns a list of recognized extensions of particular archive type
    decompress(target_dir, target_same=False)
        Unpacks archives to target directory provided by target_dir parameter
    """
    is_multipart = None
    multipart_array_list = []

    @classmethod
    @abstractmethod
    def extensions(cls):
        pass

    def __init__(self, path, to_remove):
        self.path = path
        self.to_remove = to_remove
        self.root_dir = os.path.dirname(path)

        # Determine if archive is multipart or no
        self.check_if_multipart_archive()

        self.basename = ntpath.basename(path)
        if not self.is_multipart:
            self.basename_wo_ext = os.path.splitext(self.basename)[0]
        else:
            self.basename_wo_ext = os.path.splitext(os.path.splitext(self.basename)[0])[0]

    @abstractmethod
    def decompress(self, target_dir):
        """
        Abstract method for decompressing any archive

        Parameters
        ----------
        target_dir : str
            Path to destination directory where we will unpack the archive
        """
        print('Unpacking ' + self.path)

    def check_if_multipart_archive(self):
        """
        Method to determine if archive is multipart or no

        Parameters
        ----------
        """
        if self.is_multipart is None:
            # Determination has not being done therefore checking if archive is multipart
            dir_path = os.path.dirname(self.path)
            base = os.path.basename(self.path)
            name, extension = os.path.splitext(base)

            similar = glob.glob(os.path.join(dir_path, name) + '*')

            # Setting the value
            if len(similar) > 1:
                self.is_multipart = True
                self.multipart_array_list = similar
            else:
                self.is_multipart = False

        # Determination already being done (either before or in above "if" block) and we can just return the value
        return self.is_multipart
