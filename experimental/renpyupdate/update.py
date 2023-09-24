import argparse
import os

from . import filetypes


class Update(object):

    def __init__(self, rpudir, newlists, targetdir, oldlists):
        self.targetdir = targetdir
        self.oldlists = oldlists
        self.sourcedir = rpudir
        self.newlists = newlists

        self.new_files = [ i for j in self.newlists for i in j.files ]
        self.old_files = [ i for j in self.oldlists for i in j.files ]

        self.scan_old_files()
        self.remove_identical_files()

    def log(self, message, *args):
        print(message % args)

    def scan_old_files(self):
        """
        Scans the old files, generating a list of segments.
        """

        # TODO: Progress

        for i in self.old_files:
            i.add_data_filename(self.targetdir)
            i.scan()

    def remove_identical_files(self):
        """
        Removes from self.source_files any file that exists and is identical
        to the file in self.target_files.
        """

        old_by_name = { i.name : i for i in self.old_files }

        new_files = [ ]

        self.log("Removing identical files:")

        for f in self.new_files:
            if f.name not in old_by_name:
                new_files.append(f)
                self.log("  new     %s", f.name)
                continue

            if f.segments != old_by_name[f.name].segments:
                new_files.append(f)
                self.log("  changed %s", f.name)
                continue

            self.log("  same    %s", f.name)

        self.log("%d files are unchanged.", len(self.new_files) - len(new_files))
        self.log("%d files are new/changed.", len(new_files))

        self.new_files = new_files



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sourcedir")
    ap.add_argument("targetdir")

    args = ap.parse_args()

    targetlist = filetypes.FileList()
    targetlist.scan(args.targetdir, data_filename=False)

    with open(os.path.join(args.sourcedir, "game.index.rpu"), "rb") as f:
        sourcelist = filetypes.FileList.decode(f.read())

    # from .util import dump
    # dump(sourcelist.to_json())

    Update(args.sourcedir, [ sourcelist ], args.targetdir, [ targetlist ])

if __name__ == "__main__":
    main()