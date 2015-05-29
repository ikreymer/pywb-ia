from pywb.webapp.handlers import WBHandler
from pywb.cdx.zipnum import ZipNumCluster
from pywb.cdx.cdxserver import CDXServer
import os
import requests
import shutil


#=============================================================================
class ItemHandler(WBHandler):
    def __init__(self, query_handler, config=None):
        self.item_cdx_root = config.get('index_paths')
        self.download_prefix = config.get('archive_paths')
        if not os.path.isdir(self.item_cdx_root):
            os.makedirs(self.item_cdx_root)
        super(ItemHandler, self).__init__(query_handler, config)

    def handle_request(self, wbrequest):
        self.load_item_files(wbrequest)
        return super(ItemHandler, self).handle_request(wbrequest)

    def load_item_files(self, wbrequest):
        item = wbrequest.coll

        idx_file = os.path.join(self.item_cdx_root, item + '.cdx.idx')
        cdx_file = os.path.join(self.item_cdx_root, item + '.cdx.gz')

        # first, try to download idx and use remote cdx
        if not os.path.isfile(idx_file) and not os.path.isfile(cdx_file):
            idx_url = self.download_prefix + item + '/' + item + '.cdx.idx'
            try:
                self.download_file(idx_url, idx_file)
                self.number_idx(idx_file)
                idx_found = True
            except:
                idx_found = False

            if idx_found:
                return

            # try to download cdx file if no idx
            cdx_url = self.download_prefix + item + '/' + item + '.cdx.gz'
            try:
                self.download_file(cdx_url, cdx_file)
            except:
                raise

    def download_file(self, url, filename):
        """ Download cdx or idx file locally
        """
        r = requests.get(url, stream=True)
        r.raise_for_status()

        with open(filename, 'wb') as f:
            for chunk in r.iter_content():
                if chunk:
                    f.write(chunk)
                    f.flush()

    def number_idx(self, filename):
        """ If idx doesn't have the last line number column, add it
        to allow for much better search ops
        """
        with open(filename) as fh:
            firstline = fh.readline()
            parts = firstline.split('\t')
            # only add if there are 4 parts
            if len(parts) != 4:
                return

            count = 1
            def writeline(fho, line, count):
                fho.write(line.rstrip() + '\t' + str(count) + '\n')

            with open(filename + '.tmp', 'w+b') as fho:
                writeline(fho, firstline, count)
                count += 1
                for line in fh:
                    writeline(fho, line, count)
                    count += 1

            shutil.move(filename + '.tmp', filename)


#=============================================================================
class ItemCDXServer(CDXServer):
    def _create_cdx_sources(self, paths, config):
        src = ItemCDXIndex(paths, config)
        self.sources = [src]


#=============================================================================
class ItemCDXIndex(ZipNumCluster):
    def __init__(self, summary, config):
        self.root_path = summary
        super(ItemCDXIndex, self).__init__(summary, config)
        self.prefix = config.get('archive_paths')

        def resolve(part, query):
            coll = query.params.get('coll')
            local_cdx = os.path.join(self.root_path, coll + '.cdx.gz')
            remote_cdx = self.prefix + coll + '/' + part
            return [local_cdx, remote_cdx]

        self.loc_resolver = resolve

    def load_cdx(self, query):
        coll = query.params.get('coll')
        full = os.path.join(self.root_path, coll + '.cdx.idx')

        return self._do_load_cdx(full, query)
