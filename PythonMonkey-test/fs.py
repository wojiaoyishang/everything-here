def readFileSync(path):
    with open(path, 'rb') as f:
        return bytearray(f.read())

exports = {
    'path': None
}