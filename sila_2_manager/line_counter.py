import os

def countlines(start, lines=0, header=True, begin_start=None):
    exclude_dirs = ['sila_python-feature-silacodegenerator-0.3', 'test_cases', 'unused_tests', 'data', 'gRPC', '.idea', 'inspectionProfiles.xml', 'coverage.xml']
    if header:
        print('{:>10} |{:>10} | {:<20}'.format('ADDED', 'TOTAL', 'FILE'))
        print('{:->11}|{:->11}|{:->20}'.format('', '', ''))

    for thing in os.listdir(start):
        if thing in exclude_dirs:
            pass
        else:
            thing = os.path.join(start, thing)
            if os.path.isfile(thing):
                if thing.endswith('.py') or thing.endswith('.xml'):
                    with open(thing, 'r') as f:
                        newlines = f.readlines()
                        newlines = len(newlines)
                        lines += newlines

                        if begin_start is not None:
                            reldir_of_thing = '.' + thing.replace(begin_start, '')
                        else:
                            reldir_of_thing = '.' + thing.replace(start, '')

                        print('{:>10} |{:>10} | {:<20}'.format(
                            newlines, lines, reldir_of_thing))


    for thing in os.listdir(start):
        if thing in exclude_dirs:
            pass
        else:
            thing = os.path.join(start, thing)
            if os.path.isdir(thing):
                lines = countlines(thing, lines, header=False, begin_start=start)

    return lines


if __name__ == '__main__':
    lines = countlines(r'.')
    print('Total lines: ', lines)
