import os
import zipfile

from abc import ABC

from classes.ArchiveAbstract import ArchiveAbstract


class ArchiveZip(ArchiveAbstract, ABC):
    @classmethod
    def extensions(cls): return['.zip', '.zip.001']

    def decompress(self, target_dir):
        """
        Method for decompressing Zip archive

        Parameters
        ----------
        target_dir : str
            Path to destination directory where we will unpack the archive
        """

        # Calling parent method
        super().decompress(target_dir)

        if not self.is_multipart:
            # If not multipart just unpacking archive
            with zipfile.ZipFile(self.path, 'r') as zip_ref:
                zip_ref.extractall(target_dir)
        else:
            # If is multipart combining archive to single file
            combined_file_name = os.path.join(self.root_dir, self.basename_wo_ext + "_combined" + ".zip")
            for archive in self.multipart_array_list:
                # Combining archives to single archive file
                with open(os.path.join(self.root_dir, combined_file_name), "ab") as combined:
                    with open(os.path.join(self.root_dir, archive), "rb") as part:
                        combined.write(part.read())

            # Unpacking and removing combiner archive to target directory
            with zipfile.ZipFile(combined_file_name, 'r') as zip_ref:
                zip_ref.extractall(target_dir)
            os.remove(combined_file_name)

        # Remove file if required
        if self.to_remove:
            if not self.is_multipart:
                os.remove(self.path)
            else:
                for path in self.multipart_array_list:
                    os.remove(path)
