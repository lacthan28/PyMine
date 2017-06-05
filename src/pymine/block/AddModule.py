# coding=utf-8
import os


class AddModule:
    def loadImports(path):
        files = os.listdir(path)
        imps = []

        for i in range(len(files)):
            name = files[i].split('.')
            if len(name) > 1:
                if name[1] == 'py' and name[0] != '__init__' and name[0] != 'AddModule':
                    name = name[0]
                    imps.append(name)

        file = open(path + '__init__.py', 'w')

        toWrite = '__all__ = ' + str(imps)

        file.write(toWrite)
        file.close()

AddModule.loadImports('E:/PycharmProjects/PyMine/src/pymine/block/')