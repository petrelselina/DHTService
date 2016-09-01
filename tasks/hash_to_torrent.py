#!/usr/bin/env python
import shutil
import tempfile
import sys
import libtorrent as lt
from time import sleep

def hash_to_torrent(hash, timeout=60):
    hash = 'magnet:?xt=urn:btih:' + hash
    tempdir = tempfile.mkdtemp()
    ses = lt.session()
    params = {
        'save_path': tempdir,
        'storage_mode': lt.storage_mode_t(2),
        'paused': False,
        'auto_managed': True,
        'duplicate_is_error': True
    }
    handle = lt.add_magnet_uri(ses, hash, params)
    print("Downloading Metadata (this may take a while)")
    time = 0
    while (not handle.has_metadata()):
        if time < timeout:
            try:
                sleep(1)
                time = time + 1
            except KeyboardInterrupt:
                print("Aborting...")
                ses.pause()
                print("Cleanup dir " + tempdir)
                shutil.rmtree(tempdir)
                sys.exit(0)
        else:
            print("Timeout...")
            ses.pause()
            print("Cleanup dir " + tempdir)
            ses.remove_torrent(handle)
            shutil.rmtree(tempdir)
            return None
    ses.pause()
    print("Done")
    torinfo = handle.get_torrent_info()
    torfile = lt.create_torrent(torinfo)
    torcontent = lt.bencode(torfile.generate())
    ses.remove_torrent(handle)
    shutil.rmtree(tempdir)
    return torcontent
hash_to_torrent('13d63f9feacd7480e9e06a70bacf6326f21488ba'.lower())
