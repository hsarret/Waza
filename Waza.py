import sublime, sublime_plugin
import os

debug = True

def log(text):
    debug = True
    if debug:
        print(text)

p4exe = 'p4'

kEditTag = 'p4edit'
kAddTag = 'p4add'
kStatsTag = 'p4stats'

import threading

timer = None

class P4Checkout(sublime_plugin.WindowCommand):
    def __init__(self, *args, **kwargs):
        super(P4Checkout, self).__init__(*args, **kwargs)
        self.timer = None

    def run(self):
        # print("awa")
        log("{}".format(self))
        log("{}".format(self.window))
        log("{}".format(self.window.active_view()))
        filename = self.window.active_view().file_name()
        print("{}".format(filename))
        if filename is not None:
            p = os.popen("{} edit \"{}\"".format(p4exe, filename))
            p.close()
            if self.timer is not None:
                # print("{}").format(timer)
                self.timer.cancel()
            self.timer = threading.Timer(3, self.clearStatus)
            self.timer.start()
            self.window.active_view().set_status(kEditTag, 'p4 edit')
        else:
            print("ERROR > Active view's filename is None")

    def clearStatus(self):
        print('clearStatus')
        self.window.active_view().erase_status(kEditTag)


class P4Add(sublime_plugin.WindowCommand):
    def __init__(self, *args, **kwargs):
        super(P4Add, self).__init__(*args, **kwargs)
        self.timer = None

    def run(self):
        # print edit
        filename = self.window.active_view().file_name()
        print("{}".format(filename))
        p = os.popen("{} add \"{}\"".format(p4exe, filename))
        p.close()
        if self.timer is not None:
            # print("{}").format(timer)
            self.timer.cancel()
        self.timer = threading.Timer(3, self.clearStatus)
        self.timer.start()
        self.window.active_view().set_status(kAddTag, 'p4 add')

    def clearStatus(self):
        print('clearStatus')
        self.window.active_view().erase_status(kAddTag)

class P4DefaultChangelistStats(sublime_plugin.WindowCommand):
    def __init__(self, *args, **kwargs):
        super(P4DefaultChangelistStats, self).__init__(*args, **kwargs)
        self.timer = None

    def run(self):
        import os

        changelist = "default"

        stream = os.popen("{} opened -c {}".format(p4exe, changelist))

        addLines = deletedLines = changedLines = 0

        filesCount = 0
        for line in stream:
            filesCount = filesCount + 1
            parts = line.split("#")
            if debug:
                print(parts[0])

            p = os.popen("{} diff -ds {}".format(p4exe, parts[0]))
            for diffLine in p:
                if debug:
                    print('"{}"'.format(diffLine))

                import re
                m = re.search("^(add|deleted|changed)\s(\d*)\schunks\s(\d*)(\s/\s)?(:?\d*)\slines$", diffLine)
                if m is not None:
                    if debug:
                        print("{} {} {}".format(m.group(1), m.group(2), m.group(3)))
                    if m.group(1) == 'add':
                        addLines = addLines + int(m.group(3))
                    elif m.group(1) == 'deleted':
                        deletedLines = deletedLines + int(m.group(3))
                    elif m.group(1) == 'changed':
                        changedLines = changedLines + int(m.group(3))

            p.close()

        print("Changelist {} summary".format(changelist))
        files = "\t{} modified files".format(filesCount)
        print(files)
        added = "\t{} added lines".format(addLines)
        print(added)
        deleted = "\t{} deleted lines".format(deletedLines)
        print(deleted)
        changed = "\t{} changed lines".format(changedLines)
        print(changed)

        if self.timer is not None:
            # print("self {}").format(self)
            # print("self.timer {}").format(self.timer)
            self.timer.cancel()
        self.timer = threading.Timer(10, self.clearStatus)
        self.timer.start()
        self.window.active_view().set_status(kStatsTag, '{} - {} - {}'.format(added, deleted, changed))

    def clearStatus(self):
        print('clearStatus')
        self.window.active_view().erase_status(kStatsTag)
