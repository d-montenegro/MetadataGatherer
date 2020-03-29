file_extractors = {}


def file_extractor(extension):
    """
    This decorator registers functions to be used as extractors.

    Only functions decorated with this are considered metadata extractors, and will
    be called when the file extension matches the configured one.

    :param extension: the extension to match
    """
    def deco(f):
        assert extension not in file_extractors, f"extension {extension} already registered"
        file_extractors[extension] = f
        return f
    return deco
