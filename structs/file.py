import os
from io import BytesIO
import zlib
from .file_entry import XP3FileEntry

from encrypt.encrypt_interface import EncryptInterface

class XP3DecryptionError(Exception):
    pass


class XP3File(XP3FileEntry):
    """Wrapper around file entry with buffer access to be able to read the file"""
    buffer: BytesIO
    silent: bool
    use_numpy: bool

    def __init__(self, index_entry: XP3FileEntry, buffer, silent, use_numpy):
        super().__init__(
            special_format=index_entry.special_format,
            time=index_entry.time,
            adlr=index_entry.adlr,
            segm=index_entry.segm,
            info=index_entry.info
        )
        self.buffer = buffer
        self.silent = silent
        self.use_numpy = use_numpy

    def read(self, encryption_type='none', raw=False, encrypt_instance: EncryptInterface=None):
        """Reads the file from buffer and return its data"""
        for segment in self.segm:
            self.buffer.seek(segment.offset)
            data = self.buffer.read(segment.compressed_size)

            if segment.is_compressed:
                data = zlib.decompress(data)
            if len(data) != segment.uncompressed_size:
                raise AssertionError(len(data), segment.uncompressed_size)

            if self.is_encrypted:
                file_buffer = BytesIO(data)
                if encryption_type in ('none', None) and not raw:
                    raise XP3DecryptionError('File is encrypted and no encryption type was specified')

                encrypt_instance.decrypt(file_buffer, self.adler32, self.use_numpy)
                data = file_buffer.getvalue()
                file_buffer.close()
        return data

    def extract(self, to='', name=None, encryption_type='none', raw=False, encrypt_instance: EncryptInterface=None):
        """
        Reads the data and saves the file to specified folder,
        if no location is specified, unpacks into folder with archive name (data.xp3, unpacks into data folder)
        """
        file = self.read(encryption_type=encryption_type, raw=raw, encrypt_instance=encrypt_instance)
        if zlib.adler32(file) != self.adler32 and not self.silent:
            print('! Checksum error')

        if not to:
            # Use archive name as output folder if it's not explicitly specified
            basename = os.path.basename(self.buffer.name)
            to = os.path.splitext(basename)[0]
        if not name:
            name = self.file_path
        to = os.path.join(to, name)
        dirname = os.path.dirname(to)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(to, 'wb') as output:
            output.write(file)


